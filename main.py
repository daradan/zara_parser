import json
import logging
from logging.handlers import RotatingFileHandler
import requests
from random import randrange, shuffle

import categories
import config
import utils
import send_to_telegram
from crud import WomanProductsCrud, WomanPricesCrud, ManProductsCrud, ManPricesCrud, KidProductsCrud, KidPricesCrud, \
    BeautyProductsCrud, BeautyPricesCrud, OriginsProductsCrud, OriginsPricesCrud
from database import SessionLocal
from schemas import ProductSchema, PriceSchema


class ZaraParser:
    def __init__(self):
        self.db_session = SessionLocal()
        self.urls_category_id = None
        self.market = None
        self.products_crud = None
        self.prices_crud = None
        self.count = 0

    def start(self):
        logging.info(f"START: {self.market}")
        all_categories = utils.make_urls(self.urls_category_id)
        shuffle(all_categories)
        for url in all_categories:
            try:
                self.get_data_from_json_loads(url)
            except Exception as e:
                logging.info(f"{self.market} - {e}")
                send_to_telegram.send_error(e)

    def get_data_from_json_loads(self, url):
        session = requests.Session()
        response = session.get(url, params=config.PARAMS, headers=config.HEADERS)
        if response.status_code != 200:
            self.count += 1
            logging.info(f"{self.market}: status {response.status_code}, count {self.count}")
            self.get_data_from_json_loads(url)
        json_loads = json.loads(response.text)
        if not json_loads.get('productGroups'):
            logging.info(f"{self.market}: 'productGroups' is missing\n{json_loads}")
            return

        elements = json_loads['productGroups'][0]['elements']
        for element in elements:
            com_components = element.get('commercialComponents')
            if not com_components:
                logging.info(f"{self.market}: 'commercialComponents' is missing\n{com_components}")
                continue
            for com_component in com_components:
                if not com_component.get('detail') \
                        or not com_component['detail'].get('colors') \
                        or not com_component.get('name') \
                        or not com_component.get('seo'):
                    logging.info(f"{self.market}: 'detail' or 'colors' or 'name' or 'seo' are missing\n{com_component}")
                    continue
                colors = com_component['detail']['colors']
                for color in colors:
                    if not color.get('name') \
                            or not color.get('price') \
                            or not color.get('xmedia') \
                            or not color.get('productId'):
                        logging.info(f"{self.market}: 'name' or 'price' or 'xmedia' or 'productId' are missing\n{color}")
                        continue
                    category_id, category = utils.get_category(self.urls_category_id, url)
                    product_url = utils.make_url(com_component['seo'], category_id)
                    if not product_url:
                        logging.info(f"{self.market}: 'product_url' is missing")
                        continue
                    product_obj = {
                        'market': self.market,
                        'url': product_url,
                        'store_id': color['productId'],
                        'category': category,
                        'name': com_component['name'],
                        'color': color['name'],
                        'description': com_component.get('description', ''),
                        'image': utils.make_photo_urls(color['xmedia'])
                    }
                    product_obj = ProductSchema(**product_obj)
                    price_obj = PriceSchema(price=color['price'] // 100)
                    self.check_data_from_db(product_obj, price_obj)

    def check_data_from_db(self, product_obj: ProductSchema, price_obj: PriceSchema):
        product = self.products_crud.get_or_create(product_obj)
        price_obj.product_id = product.id
        last_price = self.prices_crud.get_last_price(product.id)
        if last_price:
            discount = utils.get_percentage(price_obj.price, last_price.price)
            price_obj.discount = discount
        if not last_price or price_obj.discount != '0':
            self.prices_crud.insert(price_obj)
            if int(price_obj.discount) <= -15:
                image_caption = utils.make_image_caption(product_obj, self.prices_crud.get_last_n_prices(product.id))
                send_tg = send_to_telegram.send_as_media_group(image_caption, product_obj)
                logging.info(f"Send to telegram status code: {send_tg}")


    def __del__(self):
        logging.info(f"END: {self.market}")


class ZaraWomanParser(ZaraParser):
    def __init__(self):
        super().__init__()
        self.market = 'zara_w'
        self.urls_category_id = categories.categories_by_market(self.market)
        self.products_crud: WomanProductsCrud = WomanProductsCrud(session=self.db_session)
        self.prices_crud: WomanPricesCrud = WomanPricesCrud(session=self.db_session)


class ZaraManParser(ZaraParser):
    def __init__(self):
        super().__init__()
        self.market = 'zara_m'
        self.urls_category_id = categories.categories_by_market(self.market)
        self.products_crud: ManProductsCrud = ManProductsCrud(session=self.db_session)
        self.prices_crud: ManPricesCrud = ManPricesCrud(session=self.db_session)


class ZaraKidParser(ZaraParser):
    def __init__(self):
        super().__init__()
        self.market = 'zara_k'
        self.urls_category_id = categories.categories_by_market(self.market)
        self.products_crud: KidProductsCrud = KidProductsCrud(session=self.db_session)
        self.prices_crud: KidPricesCrud = KidPricesCrud(session=self.db_session)


class ZaraBeautyParser(ZaraParser):
    def __init__(self):
        super().__init__()
        self.market = 'zara_b'
        self.urls_category_id = categories.categories_by_market(self.market)
        self.products_crud: BeautyProductsCrud = BeautyProductsCrud(session=self.db_session)
        self.prices_crud: BeautyPricesCrud = BeautyPricesCrud(session=self.db_session)


class ZaraOriginsParser(ZaraParser):
    def __init__(self):
        super().__init__()
        self.market = 'zara_o'
        self.urls_category_id = categories.categories_by_market(self.market)
        self.products_crud: OriginsProductsCrud = OriginsProductsCrud(session=self.db_session)
        self.prices_crud: OriginsPricesCrud = OriginsPricesCrud(session=self.db_session)


if __name__ == '__main__':
    logging.basicConfig(
        handlers=[RotatingFileHandler('zara_parser.log', mode='a+', maxBytes=10485760, backupCount=2, encoding='utf-8')],
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.INFO,
    )
    ZaraWomanParser().start()
    ZaraManParser().start()
    ZaraKidParser().start()
    ZaraBeautyParser().start()
    ZaraOriginsParser().start()
