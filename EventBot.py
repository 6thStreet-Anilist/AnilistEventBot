
import requests
import json
import random
import time

# Set up Anilist API variables
url = 'https://graphql.anilist.co'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
query = '''
query ($id: Int, $page: Int, $perPage: Int) {
    Page (page: $page, perPage: $perPage) {
        media (id: $id) {
            id
            title {
                romaji
            }
            description
            coverImage {
                large
            }
        }
    }
}
'''

# Set up bot variables
post_id = 69144 # Replace with the ID of the post you want to monitor
bot_username = '6thstreet' # Replace with your bot's username
challenges = ['Name an anime with a cat in it', 'Name an anime with a beach episode', 'Name an anime with a time travel plot', 'Name an anime with a tournament arc', 'Name an anime with a school setting', 'Name an anime with a mecha', 'Name an anime with a yandere character', 'Name an anime with a food theme', 'Name an anime with a supernatural theme', 'Name an anime with a detective plot'] # Replace with your list of challenges
participated_users = [] # Keep track of users who have already participated

# Function to send a message to a user
def send_message(user_id, message):
    query = '''
    mutation ($userId: Int, $message: String) {
        sendMessage(userId: $userId, message: $message) {
            id
        }
    }
    '''
    variables = {
        'userId': user_id,
        'message': message
    }
    response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})
    return response.json()

# Function to get comments on a post
def get_comments(post_id):
    query = '''
    query ($postId: Int) {
        Page {
            thread (id: $postId) {
                comments {
                    id
                    userId
                    text
                }
            }
        }
    }
    '''
    variables = {
        'postId': post_id
    }
    response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})
    return response.json()

# Function to check if a user has already participated
def has_participated(user_id):
    if user_id in participated_users:
        return True
    else:
        return False

# Function to pick a random challenge
def pick_challenge():
    return random.choice(challenges)

# Main loop
while True:
    # Get comments on the post
    comments = get_comments(post_id)

    # Loop through comments
    for comment in comments['data']['Page']['thread']['comments']:
        # Check if user has already participated
        if has_participated(comment['userId']):
            continue

        # Pick a random challenge
        challenge = pick_challenge()

        # Send challenge message to user
        message = f'Hello @{comment["user"]["name"]}, your challenge is: {challenge}'
        send_message(comment['userId'], message)

        # Add user to participated users list
        participated_users.append(comment['userId'])

    # Wait an hour before checking again
    time.sleep(3600)
