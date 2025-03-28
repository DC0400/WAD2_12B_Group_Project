import os
import random
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rankedify.settings')

django.setup()

from rankedifyapp.models import Profile

# Sample data for randomization
first_names = ["dan", "james", "Alice", "Bob", "Charlie", "David", "Emily", "Frank", "Grace", "Henry"]
last_names = ["Doe", "Smith", "Johnson", "Williams", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]
songs = ["Bohemian Rhapsody", "Shape of You", "Blinding Lights", "Smells Like Teen Spirit", "Imagine",
         "Billie Jean", "Someone Like You", "Rolling in the Deep", "Hotel California", "Stairway to Heaven"]

def generate_users(n=10):
    users = []
    for i in range(1, n + 1):
        forename = random.choice(first_names)
        surname = random.choice(last_names)
        username = f"user{i}"
        email = f"{username}@example.com"
        password = f"password{i}"
        spotify_username = f"{forename.lower()}{surname.lower()}{i}"
        rank = i
        top_song = random.choice(songs)
        listening_minutes = random.randint(1000, 5000)

        users.append({
            "username": username,
            "email": email,
            "password": password,
            "forename": forename,
            "surname": surname,
            "spotify_username": spotify_username,
            "rank": rank,
            "top_song": top_song,
            "listening_minutes": listening_minutes
        })
    
    return users

def populate():
    users = generate_users(10)  

    for user_data in users:
        add_user(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
            forename=user_data["forename"],
            surname=user_data["surname"],
            spotify_username=user_data["spotify_username"],
            rank=user_data["rank"],
            top_song=user_data["top_song"],
            listening_minutes=user_data["listening_minutes"],
        )

    # Print out the users we have added
    for user in Profile.objects.all():
        print(f"- {user.username}: {user.forename} {user.surname}, Rank {user.rank}")

def add_user(username, email, password, forename, surname, spotify_username, rank, top_song, listening_minutes):
    user, created = Profile.objects.get_or_create(
        username=username,
        defaults={
            "email": email,
            "forename": forename,
            "surname": surname,
            "spotify_username": spotify_username,
            "rank": rank,
            "top_song": top_song,
            "listening_minutes": listening_minutes
        }
    )

    if created:
        user.set_password(password)  
        user.save()
        print("Created user: {username}")
    else:
        print(" User {username} already exists!")

# Start execution here!
if __name__ == '__main__':
    print('🚀 Starting ')
    populate()