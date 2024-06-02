import json
from slack import WebClient
from datetime import datetime
from collections import defaultdict
import pytz

# Slack Access Token setting 액세스 토큰 설정
# Add slack app token in config.json
with open('config.json') as config_file:
    config = json.load(config_file)
    token = config.get('slack_api_token')
    client = WebClient(token=token)

# Your channel ID wanted to counting messages
channel_id = "Your channel ID"


# Setting timezone anything you want
current_time = datetime.now(pytz.utc)
kr_tz = pytz.timezone('Asia/Seoul')
current_time_kr = current_time.astimezone(kr_tz)

start_time = current_time_kr.replace(hour=8, minute=0)

# Set the time for reading the message
start_timestamp = int(start_time.timestamp())
end_timestamp = int(current_time_kr.timestamp())


response = client.conversations_history(channel=channel_id, oldest=start_timestamp, latest=end_timestamp)
messages = response['messages']

user_counts = defaultdict(int)

for message in messages:
    if 'user' in message:
        user_id = message['user']
        user_counts[user_id] += 1

user_info = client.users_list()
user_dict = {user['id']: user['profile']['display_name'] for user in user_info['members'] if '개발사업부' in user['profile']['display_name']}

result = []

# 예외 for kidding
result.append(("박정훈 Developer_개발사업부", 10000))

for user_id, count in user_counts.items():
    username = user_dict.get(user_id)
    if username is not None:
        result.append((username, count))

result = sorted(result, key=lambda x: x[1], reverse=True)
for username, count in result:
    print(f"{username}: {count} 번 슬랙")
