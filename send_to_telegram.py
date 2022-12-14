import time
import requests
import json

import config
import utils


def send_error(message):
    url = f'https://api.telegram.org/bot{config.TG_TOKEN}/sendMessage'
    params = {
        'chat_id': config.TG_CHANNEL_ERROR,
        'text': message
    }
    r = requests.post(url, data=params)
    if r.status_code != 200:
        data = r.json()
        time_to_sleep = data['parameters']['retry_after']
        time.sleep(time_to_sleep)
        send_error(message)
    return r.status_code


def send_as_media_group(image_caption, product):
    url = f'https://api.telegram.org/bot{config.TG_TOKEN}/sendMediaGroup'
    params = {
        'chat_id': utils.get_tg_channel(product.market),
        'media': [],
    }
    if type(product.image) == str:
        product.image = product.image.split(', ')
    for path in product.image[:2]:
        params['media'].append({'type': 'photo',
                                'media': path,
                                'parse_mode': 'HTML', })
    params['media'][0]['caption'] = image_caption
    params['media'] = json.dumps(params['media'])
    r = requests.post(url, data=params)
    if r.status_code != 200:
        data = r.json()
        time_to_sleep = data['parameters']['retry_after']
        time.sleep(time_to_sleep)
        send_as_media_group(image_caption, product)
    return r.status_code
