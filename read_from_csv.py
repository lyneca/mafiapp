import random

from django.contrib.auth.models import User

with open('appform.csv') as file:
    for line in file:
        time, fname, lname, email, act = line.strip().split(',')
        if not time == 'Timestamp':
            print('adding user', fname.strip('"').lower() + '_' + lname.strip('"').lower()[0])
            u = User(first_name=fname.strip('"').capitalize(),
                     last_name=lname.strip('"').capitalize(),
                     username=fname.strip('"').lower() + '_' + lname.strip('"').lower()[0], email=email.strip('"')
                     )
            u.set_password('abcde')
            u.save()

i = 0
for user in User.objects.filter(is_superuser=False):
    pwd = hex(random.randint(16 ** 5, 16 ** 6 - 1))[2:]
    user.set_password(pwd)
    user.save()
    print(user.first_name, pwd)
    i += 1