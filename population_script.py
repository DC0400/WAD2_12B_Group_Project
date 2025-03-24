import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rankedify.settings')

import django
django.setup()

from rankedify.models import Profile

def populate():
    users = [
        {'forename': 'Daniel', 'surname': 'Corbett', 'email': 'titianfilly00@gmail.com'},
        {'forename': 'Test', 'surname': 'Test', 'email': 'WAD2spotifytest@gmail.com'},
    ]

    for user, user_data in users:
        u = add_user(user_data['forename'], user_data['surname'], user_data['email'])
        print(u)

def add_user(fore, sur, email):
    new_user = Profile.objects.get_or_create(forename = fore, surname = sur, email = email)
    new_user.save()
    return new_user