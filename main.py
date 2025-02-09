import requests
from datetime import datetime, timedelta
import time
import json
import os

PAGE_LIMIT = 10
DAYS_AGO = 30

def print_help():
    print('Usage: GITHUB_TOKEN=your_token python main.py [OPTIONS]')

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    print_help()
    exit(1)

HEADERS = {'Authorization': f'token {GITHUB_TOKEN}'}

def get_following_users():
    following = []
    url = 'https://api.github.com/user/following'
    while url:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        following.extend([user['login'] for user in response.json()])
        url = response.links.get('next', {}).get('url')
    return following

def filter_date(event):
    time_limit = datetime.now() - timedelta(days=DAYS_AGO)
    return datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ') >= time_limit

def get_user_events(username):
    events = []
    url = f'https://api.github.com/users/{username}/events?per_page=100'
    page = 0
    while url:
        page += 1
        response = requests.get(url, headers=HEADERS)
        remaining_requests = int(response.headers.get('X-RateLimit-Remaining', 0))
        if remaining_requests <= 1:
            reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 60))
            sleep_duration = max(reset_time - time.time(), 0) + 10
            time.sleep(sleep_duration)
        response.raise_for_status()
        new_events = [event for event in response.json() if filter_date(event)]
        if page >= PAGE_LIMIT or len(new_events) == 0:
            break
        events.extend(new_events)
        url = response.links.get('next', {}).get('url')
    return events

def deduplicate_list(lst):
    return [x for i, x in enumerate(lst) if x not in lst[:i]]

def get_all_events():
    following = get_following_users()
    print(f"Found {len(following)} followed users")

    # event: (repo, type)
    # events: list[event]
    # user_events: dict[user, events]
    # all_events: list[user_events]
    all_events: list[dict[str, list[tuple[str, str]]]] = []
    for i, user in enumerate(following):
        print(f"({i+1}/{len(following)}) Processing events for user: {user}")
        events = get_user_events(user)
        events = [(event['repo']['name'], event['type']) for event in events]
        events = deduplicate_list(events)
        user_events = {user: events}
        all_events.append(user_events)

    return all_events


if __name__ == '__main__':
    events = get_all_events()
    with open('events.json', 'w') as f:
        json.dump(events, f)