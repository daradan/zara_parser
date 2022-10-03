import requests
import json
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
tg_token = os.getenv('TG_TOKEN')
url_part = f"https://api.telegram.org/bot{tg_token}/"


def main(msg: str, method: str, media: str, error: bool):
    if method == 'sendMessage':
        send_as_message(msg, error)
    elif method == 'sendPhoto':
        send_as_photo(msg, media)
    elif method == 'sendMediaGroup':
        send_as_media_group(msg, media)


def send_as_message(msg: str, error: bool):
    channel = os.getenv('TG_CHANNEL')
    if error:
        channel = os.getenv('TG_CHANNEL_ERROR')
    url = f"{url_part}sendMessage"
    params = {
        'chat_id': channel,
        'text': msg,
    }
    r = requests.post(url, data=params)


def send_as_photo(msg: str, media: str):
    url = f'{url_part}sendPhoto'
    params = {
        'chat_id': os.getenv('TG_CHANNEL'),
        'caption': msg,
        'parse_mode': 'HTML',
        'photo': media,
    }
    r = requests.post(url, data=params)


def send_as_media_group(msg: str, media: str):
    url = f'{url_part}sendMediaGroup'
    params = {
        'chat_id': os.getenv('TG_CHANNEL'),
        'media': [],
    }
    media = list(media.split(', '))
    for path in media:
        params['media'].append({'type': 'photo',
                                'media': path,
                                'parse_mode': 'HTML', })
    params['media'][0]['caption'] = msg
    params['media'] = json.dumps(params['media'])
    r = requests.post(url, data=params)
