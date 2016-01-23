from django.contrib.auth.models import User

with open('appform.csv') as file:
    for line in file:
        time, fname, lname, email, slack, apt, orig = line.strip().split(',')
        if not time == 'Timestamp':
            print('adding user', fname.lower())
            u = User(first_name=fname.capitalize(),
                     last_name=lname.capitalize(),
                     username=fname.lower(), email=email
                     )
            u.set_password('abcde')
            u.save()
