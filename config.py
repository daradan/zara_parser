import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

data = {
    'tg_token': os.getenv('TG_TOKEN'),
    'tg_channel': os.getenv('TG_CHANNEL'),
    'tg_send_method': 'sendMediaGroup',
    'market': 'zara_w',
    'availability': '',
    'discount': '',
    'last_rows': 10,
}
urls_category_id = {
    '2111785': 'новинки',
    '2113870': 'базовый_гардероб',
    '2113343': 'пальто пуховики',
    '2113388': 'пиджаки',
    '2113411': 'куртки',
    '2113500': 'платья комбинезоны',
    '2113575': 'рубашки',
    '2113611': 'футболки',
    '2113643': 'топы корсеты',
    '2113659': 'боди',
    '2113699': 'трикотаж',
    '2113758': 'джинсы',
    '2113807': 'брюки',
    '2113840': 'юбки',
    '2113861': 'шорты',
    '2113707': 'толстовки',
    '2113873': 'костюмы',
    '2113871': 'total_look',
    '2113973': 'обувь',
    '2114083': 'сумки',
    '2114411': 'специальные_предложения',
    '2114175': 'аксессуары',
}

params = {'ajax': 'true'}
headers = {
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
