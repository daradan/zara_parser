import requests
import json
import logging

import config
import categories
from crud import WomanProductsCrud, WomanPricesCrud, ManProductsCrud, ManPricesCrud
from database import SessionLocal
from schemas import ProductSchema, PriceSchema
import utils


class ZaraParser:
    def __init__(self):
        self.data = config.data  # TODO разделить
        self.db_session = SessionLocal()
        self.urls_category_id = None
        self.market = None
        self.products_crud = None
        self.prices_crud = None
        self.items_count = 0

    def start(self):
        logging.info(f"Zara Parser Start: {self.market}")
        for url in self.make_urls():
            try:
                self.get_data_from_json_loads(url)
            except Exception as e:
                logging.exception(e)
                ...  # send error to telegram

    def make_urls(self):
        urls = []
        for category_id, url_category in self.urls_category_id.items():
            urls.append(f'https://www.zara.com/kz/ru/category/{category_id}/products')
        logging.info(f"{len(urls)} urls created")
        return urls

    def get_data_from_json_loads(self, url):
        logging.info(f"Start URL: {url}")
        session = requests.Session()
        response = session.get(url, params=config.params, headers=config.headers)
        json_loads = json.loads(response.text)
        if len(json_loads['productGroups']) <= 0:
            return

        elements = json_loads['productGroups'][0]['elements']
        for element in elements:
            com_components = element.get('commercialComponents')
            if not com_components:
                continue
            for com_component in com_components:
                colors = com_component['detail']['colors']
                if not com_component.get('name'):
                    continue
                for color in colors:
                    if not color.get('name') or not color.get('price'):
                        continue
                    category_id, category = self.get_category(url)
                    product_url = utils.make_url(com_component['seo'], category_id)
                    if not product_url:
                        continue
                    product_obj = {
                        'market': self.market,
                        'url': product_url,
                        'category': category,
                        'name': com_component['name'],
                        'color': color['name'],
                        'description': com_component.get('description', ''),
                        'image': utils.make_photo_urls(color['xmedia'])
                    }
                    product_obj = ProductSchema(**product_obj)
                    price_obj = PriceSchema(price=color['price'] // 100)
                    self.check_data_from_db(product_obj, price_obj)

    def get_category(self, url):
        for category_id, category in self.urls_category_id.items():
            if category_id in url:
                return category_id, category

    def check_data_from_db(self, product_obj: ProductSchema, price_obj: PriceSchema):
        self.items_count += 1
        logging.info(f"Check From DB: {self.items_count}")
        product = self.products_crud.get_or_create(product_obj)
        price_obj.product_id = product.id
        last_price = self.prices_crud.get_last_price(product.id)
        if last_price:
            discount = utils.get_percentage(price_obj.price, last_price.price)
            price_obj.discount = discount
            ...  # send to telegram
        if price_obj.discount != '0':
            self.prices_crud.insert(price_obj)
            logging.info(f"New Price: {price_obj.price} for product: {product.id}")

    def make_image_caption(self):
        self.make_hashtag_to_category()
        image_caption = f"<b>{self.data['name']}</b>\n" \
                        f"<b>{self.data['color']}</b>\n" \
                        f"#{self.data['market']} {self.data['category']}\n\n" \
                        f"{self.data['description']}\n\n" \
                        f"{self.data['last_prices']}\n" \
                        f"<a href='{self.data['url_non_utf8']}'>Купить на оф.сайте</a>\n\n" \
                        f"{self.data['tg_channel']}"
        return image_caption

    def make_hashtag_to_category(self):
        temp_list = []
        temp_list2 = self.data['category'].split()
        for k in temp_list2:
            temp_list.append(f'#{k}')
        self.data['category'] = ' '.join(temp_list)

    def __del__(self):
        logging.info(f"Total Parsed: {self.market}, {self.items_count}")


class ZaraWomenParser(ZaraParser):
    def __init__(self):
        super().__init__()
        self.market = 'zara_w'
        self.urls_category_id = categories.categories_by_market[self.market]
        self.products_crud: WomanProductsCrud = WomanProductsCrud(session=self.db_session)
        self.prices_crud: WomanPricesCrud = WomanPricesCrud(session=self.db_session)


class ZaraMenParser(ZaraParser):
    def __init__(self):
        super().__init__()
        self.market = 'zara_m'
        self.urls_category_id = categories.categories_by_market[self.market]
        self.products_crud: ManProductsCrud = ManProductsCrud(session=self.db_session)
        self.prices_crud: ManPricesCrud = ManPricesCrud(session=self.db_session)


if __name__ == '__main__':
    print("HELLO")
    logging.basicConfig(
        handlers=[logging.FileHandler('zara_parser.log', 'a+', 'utf-8')],
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.INFO,
    )
    ZaraWomenParser().start()
    ZaraMenParser().start()
