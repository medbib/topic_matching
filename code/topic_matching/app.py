# app.py
import json

def load_json(file_path):
    with open(file_path) as f:
        return json.load(f)

def load_users():
    return load_json('code/data/users.json')

def load_content():
    return load_json('code/data/content.json')

def is_relevant(user_interest, content_tag):
    print('type of user_interest', type(user_interest))
    print(user_interest['type'])
    print('content_tag', content_tag)
    if type(content_tag) is list:
        content_tag = content_tag[0]
    return (
        user_interest['type'] == content_tag['type'] and
        user_interest['value'] == content_tag['value'] and
        user_interest['threshold'] <= content_tag['threshold']
    )

def is_relevant_without_threshold(user_interest, content_tag):
    print('in is_relevant_without_threshold')
    if type(content_tag) is list:
        content_tag = content_tag[0]
    return (
        user_interest['type'] == content_tag['type'] and
        user_interest['value'] == content_tag['value']
    )

def match_content(users, content):
    matched_results = []
    print('length users', len(users))
    for user in users:
        relevant_content = []
        print('user', user)
        print('user_type', type(user))
        print(len(content))
        #for el in content:
        for el in user['interests']:
            print('type of el in content', type(el))
            #print(el)
            #print(user['interests'])
            #if any(is_relevant(interest, tag['tags']) for interest in user['interests'] for tag in content):
            #print('content', content)
            #if any(is_relevant(el, tag['tags']) for tag in content):
            for tag in content:
                if is_relevant(el, tag['tags']):
                    relevant_content.append(tag)
        # Sort matches by decreasing thresholds
        relevant_content.sort(key=lambda x: max(tag['threshold'] for tag in x['tags']), reverse=True)
        matched_results.append({
                'user': user['name'],
                'content': relevant_content
                })
        print(matched_results)
        print('matched_results in matching function', matched_results)
    return matched_results

def match_without_threshold(users, content):
    matched_results = []
    for user in users:
        relevant_content = []
        for el in user['interests']:
            for tag in content:
                if is_relevant_without_threshold(el, tag['tags']):
                    relevant_content.append(tag)
        relevant_content.sort(key=lambda x: max(tag['threshold'] for tag in x['tags']), reverse=True)
        matched_results.append({
            'user': user['name'],
            'content': relevant_content
        })
    return matched_results

def get_alternative_suggestions(users, content):
    suggestions = []
    for user in users:
        user_suggestions = []
        for interest in user['interests']:
            suggestion_values = set()
            for tag in content:
                if interest['type'] == tag['tags'][0]['type']:
                    suggestion_values.add(tag['tags'][0]['value'])
            if suggestion_values:
                user_suggestions.append({
                    'type': interest['type'],
                    'values': list(suggestion_values)
                })
        suggestions.append({
            'user': user['name'],
            'suggestions': user_suggestions
        })

