import config


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


def make_image_caption(product_obj, last_n_prices):
    image_caption = f"<b>{product_obj.name}</b>\n" \
                    f"<b>{product_obj.color}</b>\n" \
                    f"#{product_obj.market} {fix_category(product_obj.category)}\n\n" \
                    f"{fix_last_n_prices(last_n_prices)}\n" \
                    f"<a href='{product_obj.url}'>Купить на оф.сайте</a>\n\n" \
                    f"{config.TG_CHANNEL}"
    if product_obj.description != '':
        image_caption = image_caption.replace('\n\n', f'\n\n{product_obj.description}\n\n', 1)
    return image_caption


def fix_category(category):
    category = category.replace(' ', ' #')
    return f"#{category}"


def fix_last_n_prices(last_n_prices):
    last_n_prices_text = ''
    for data_price in last_n_prices:
        if data_price.discount:
            dscnt = f' ({data_price.discount}%)'
        else:
            dscnt = ''
        last_n_prices_text += f'{data_price.created.year}/{data_price.created.month}/{data_price.created.day}' \
                              f' - {data_price.price} ₸{dscnt}\n'
    return last_n_prices_text
