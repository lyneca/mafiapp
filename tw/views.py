import re
from random import shuffle
from twython import Twython
from django.shortcuts import render
trump_name = 'realDonaldTrump'
west_name = 'kanyewest'
replacements = [
    (r'&amp;', '&'),
    # (r'\n', ' '),
    # (r'  ', ' '),
    (r'https?://.+/.+', ''),
    # (r'#.+', ''),
]
exclude_words = [
    'kanye', 'west',
    'album', 'song', 'grammy', 'music',

    'donald', 'trump',
    'democrat', 'republican',
    'virginia', 'texas', 'illinois',
    'hillary', 'bernie',
]
client_args = {
    "headers": {
        "accept-charset": "ascii",
        # "content-type": "utf-8",
    }
}

APP_KEY = 'lFcxIHXpGXT0ayTxcXJmNlAh0'
APP_SECRET = 'sg5hdS85bXfC4Wz2l5vBD7yvFXaCpO1L6X3WtXA9qYSRHEa6o9'
ACCESS_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAMh7twAAAAAAi7Ik4A7vdzag7Fshm94k9x' \
               'llgCM%3DJ8aTEwzNT9IPFRbbjdcvsOF5YeSaxMkHoHOQSGnmMdPkELvtFw'


# Create your views here.
def replace_stuff(s):
    for match, sub in replacements:
        s = re.sub(match, sub, s)
    return s


def ambiguify(s):
    r = replace_stuff(s['text']).encode('ascii', 'ignore').decode("utf-8")
    for word in exclude_words:
        if word in r.lower():
            return None
    if len(r) < 3:
        return None
    if r[0] == '"':
        return None
    return r


def get_tweets():
    twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
    trump = twitter.search(q='from:realDonaldTrump -' + ' -'.join(exclude_words), result_type='mixed', count='100')['statuses']
    west = twitter.search(q='from:kanyewest -' + ' -'.join(exclude_words), result_type='mixed', count='100')['statuses']
    trump_tweets = [ambiguify(tweet) for tweet in trump]
    trump_tweets_ = []
    west_tweets = [ambiguify(tweet) for tweet in west]
    west_tweets_ = []
    for tweet in trump_tweets:
        if tweet is not None:
            trump_tweets_.append(tweet)
    for tweet in west_tweets:
        if tweet is not None:
            west_tweets_.append(tweet)

    trump_tweets = trump_tweets_
    west_tweets = west_tweets_
    print(len(trump_tweets) + len(west_tweets))
    del trump_tweets_
    del west_tweets_
    return trump_tweets, west_tweets


def index(request):
    trump, west = get_tweets()
    trump = [[0, t] for t in trump]
    west = [[1, t] for t in west]
    combined = trump + west
    shuffle(combined)
    context = {
        'tweets': combined
    }
    return render(request, 'tw/index.html', context=context)
