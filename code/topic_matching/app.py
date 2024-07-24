# app.py
import json

def load_json(file_path):
    with open(file_path) as f:
        return json.load(f)

def load_user_input_json(user_input):
    return json.load(user_input)

def load_users():
    return load_json('code/data/users.json')

def load_content():
    return load_json('code/data/content.json')

def is_relevant(user_interest, content_tag):
    #print('type of user_interest', type(user_interest))
    #print(user_interest['type'])
    #print(content_tag)
    return (
        user_interest['type'] == content_tag['type'] and
        user_interest['value'] == content_tag['value'] and
        user_interest['threshold'] <= content_tag['threshold']
    )

def match_content(users, content):
    matched_results = []
    for user in users:
        relevant_content = []
        print('user', user)
        print(len(content))
        for el in content:
            print('type of el in content', type(el))
            print(el['tags'][0]['type'])
            print(user['interests'])
            if any(is_relevant(interest, tag) for interest in user['interests'] for tag in el['tags']):
                relevant_content.append(el)
                matched_results.append({
                    'user': user['name'],
                    'content': relevant_content
                })
    return matched_results
