import requests
import json


def main(**kwargs):
    if kwargs['tg_send_method'] == 'sendPhoto':
        send_as_photo(**kwargs)
    elif kwargs['tg_send_method'] == 'sendMediaGroup':
        send_as_media_group(**kwargs)


def send_as_message(**kwargs):
    url = f'https://api.telegram.org/bot{kwargs["tg_token"]}/sendMessage'
    params = {
        'chat_id': kwargs['tg_channel'],
        'text': kwargs['msg_text']
    }
    r = requests.post(url, data=params)


def send_as_photo(**kwargs):
    url = f'https://api.telegram.org/bot{kwargs["tg_token"]}/sendPhoto'
    params = {
        'chat_id': kwargs['tg_channel'],
        'caption': kwargs['image_caption'],
        'parse_mode': 'HTML',
        'photo': kwargs['image'],
    }
    r = requests.post(url, data=params)


def send_as_media_group(**kwargs):
    url = f'https://api.telegram.org/bot{kwargs["tg_token"]}/sendMediaGroup'
    params = {
        'chat_id': kwargs['tg_channel'],
        'media': [],
    }
    temp_images = kwargs['image']
    if type(kwargs['image']) == str:
        temp_images = list(kwargs['image'].split(', '))
        print('temp_images = STRING')
    for path in temp_images:
        params['media'].append({'type': 'photo',
                                'media': path,
                                'parse_mode': 'HTML', })
    params['media'][0]['caption'] = kwargs['image_caption']
    params['media'] = json.dumps(params['media'])
    r = requests.post(url, data=params)
