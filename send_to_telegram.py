import time

import requests
import json


def main(data: dict):
    if data['tg_send_method'] == 'sendPhoto':
        send_as_photo(data)
    elif data['tg_send_method'] == 'sendMediaGroup':
        send_as_media_group(data)


def send_as_message(**kwargs):
    url = f'https://api.telegram.org/bot{kwargs["tg_token"]}/sendMessage'
    params = {
        'chat_id': kwargs['tg_channel'],
        'text': kwargs['msg_text']
    }
    r = requests.post(url, data=params)


def send_as_photo(data: dict):
    url = f'https://api.telegram.org/bot{data["tg_token"]}/sendPhoto'
    params = {
        'chat_id': data['tg_channel'],
        'caption': data['image_caption'],
        'parse_mode': 'HTML',
        'photo': data['image'],
    }
    r = requests.post(url, data=params)


def send_as_media_group(data: dict):
    url = f'https://api.telegram.org/bot{data["tg_token"]}/sendMediaGroup'
    params = {
        'chat_id': data['tg_channel'],
        'media': [],
    }
    temp_images = data['image']
    if type(data['image']) == str:
        temp_images = list(data['image'].split(', '))
        print('temp_images = STRING')
    for path in temp_images:
        params['media'].append({'type': 'photo',
                                'media': path,
                                'parse_mode': 'HTML', })
    params['media'][0]['caption'] = data['image_caption']
    params['media'] = json.dumps(params['media'])
    r = requests.post(url, data=params)


def send(message):
    from config import data
    url = f'https://api.telegram.org/bot{data["tg_token"]}/sendMessage'
    params = {
        'chat_id': data['tg_channel'],
        'text': message
    }
    r = requests.post(url, data=params)
    if r.status_code != 200:
        data = r.json()
        time_to_sleep = data['parameters']['retry_after']
        print(f'limit exceeded, time_to_sleep: {time_to_sleep}')
        time.sleep(time_to_sleep)
        send(message)


def test_telegram():
    for i in range(100):
        send(f'test_{i}')


