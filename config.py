import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

URL = 'https://www.zara.com/kz/ru/'
URL_CATEGORY = f'{URL}categories?ajax=true'
URL_PRODUCT = f'{URL}category/'
URL_PHOTO = 'https://static.zara.net/photos/'

LAST_N_PRICES = 10
TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHANNEL_W = os.getenv('TG_CHANNEL_W')
TG_CHANNEL_M = os.getenv('TG_CHANNEL_M')
TG_CHANNEL_K = os.getenv('TG_CHANNEL_K')
TG_CHANNEL_ERROR = os.getenv('TG_CHANNEL_ERROR')

PARAMS = {'ajax': 'true'}
HEADERS = {
    'authority': 'www.zara.com',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'referer': 'https://www.zara.com/',
    'user-agent': os.getenv('USER_AGENT'),
}
