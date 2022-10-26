def make_url(seo, category_id):
    if seo['keyword'] == '':
        return
    keyword = seo['keyword']
    seo_product_id = seo['seoProductId']
    discern_product_id = seo['discernProductId']
    url = f"https://www.zara.com/kz/ru/{keyword}-p{seo_product_id}.html?v1={discern_product_id}&v2={category_id}"
    return url


def make_photo_urls(photos):
    photos_list = []
    for photo in photos:
        path = photo['path']
        name = photo['name']
        timestamp = photo['timestamp']
        photo_str = f"https://static.zara.net/photos//{path}/w/750/{name}.jpg?ts={timestamp}"
        photos_list.append(photo_str)
    return ', '.join(photos_list)


def get_percentage(price, price_old):
    percent = round(-1 * (100 - (price * 100 / price_old)))
    if percent > 0:
        percent = f'+{percent}'
    return str(percent)
