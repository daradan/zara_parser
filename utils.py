import config


def make_urls(urls_category_id: dict) -> list:
    urls = []
    for category_id, url_category in urls_category_id.items():
        urls.append(f'https://www.zara.com/kz/ru/category/{category_id}/products')
    return urls


def get_category(urls_category_id: dict, url: str) -> tuple:
    for category_id, category in urls_category_id.items():
        if str(category_id) in url:
            return category_id, category


def make_url(seo: dict, category_id: str) -> str | None:
    if not seo.get('keyword'):
        return
    keyword = seo['keyword']
    seo_product_id = seo['seoProductId']
    discern_product_id = seo['discernProductId']
    url = f"https://www.zara.com/kz/ru/{keyword}-p{seo_product_id}.html?v1={discern_product_id}&v2={category_id}"
    return url


def make_photo_urls(photos: list) -> str:
    photos_list = []
    for photo in photos:
        path = photo['path']
        name = photo['name']
        timestamp = photo['timestamp']
        photo_str = f"https://static.zara.net/photos//{path}/w/750/{name}.jpg?ts={timestamp}"
        photos_list.append(photo_str)
    return ', '.join(photos_list)


def get_percentage(price: int, price_old: int) -> str:
    percent = round(-1 * (100 - (price * 100 / price_old)))
    if percent > 0:
        percent = f'+{percent}'
    return str(percent)


def make_image_caption(product_obj, last_n_prices) -> str:
    image_caption = f"<b>{product_obj.name}</b>\n" \
                    f"<b>{product_obj.color}</b>\n" \
                    f"{fix_category(product_obj.category)}\n\n" \
                    f"{fix_last_n_prices(last_n_prices)}\n" \
                    f"<a href='{product_obj.url}{make_utm_tags(product_obj.market)}'>Купить на оф.сайте</a>\n\n" \
                    f"{get_tg_channel(product_obj.market)}"
    if product_obj.description:
        image_caption = image_caption.replace('\n\n', f'\n\n{product_obj.description}\n\n', 1)
    if product_obj.market == 'zara_b':
        image_caption = image_caption.replace('#', f'#beauty #', 1)
    return image_caption


def fix_category(category: str) -> str:
    category = category.replace(' ', ' #')
    return f"#{category}"


def fix_last_n_prices(last_n_prices) -> str:
    last_n_prices_text = ''
    for data_price in last_n_prices:
        month = data_price.created.month
        day = data_price.created.day
        if data_price.discount:
            dscnt = f' ({data_price.discount}%)'
        else:
            dscnt = ''
        if month < 10:
            month = f"0{month}"
        if day < 10:
            day = f"0{day}"
        last_n_prices_text += f'{data_price.created.year}/{month}/{day} - {data_price.price} ₸{dscnt}\n'
    return last_n_prices_text


def get_tg_channel(market: str) -> str:
    if market in ['zara_w', 'zara_b', 'zara_o']:
        return config.TG_CHANNEL_W
    if market == 'zara_m':
        return config.TG_CHANNEL_M
    if market == 'zara_k':
        return config.TG_CHANNEL_K


def make_utm_tags(market) -> str:
    utm_campaign = get_tg_channel(market)[1:]
    return f"&utm_source=telegram&utm_medium=messenger&utm_campaign={utm_campaign}&utm_term=zara_skidki_kazakhstan"
