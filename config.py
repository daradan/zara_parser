import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

URL = 'https://www.zara.com/kz/ru/'
URL_CATEGORY = f'{URL}categories?ajax=true'
URL_PRODUCT = f'{URL}category/'
URL_PHOTO = 'https://static.zara.net/photos/'

LAST_N_PRICES = 10
TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHANNEL = os.getenv('TG_CHANNEL')
TG_CHANNEL_ERROR = os.getenv('TG_CHANNEL_ERROR')

PARAMS = {'ajax': 'true'}
HEADERS = {
    'authority': 'www.zara.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'if-none-match': 'W/"90e4b-fICHcllNvYuI0ZWA0xJhJSeZbnE"',
    'referer': 'https://www.zara.com/',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="104", "Opera";v="90"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/104.0.5112.102 Safari/537.36',
}
