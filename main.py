import json
import logging
import requests

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
        self.items_count = 0

    def start(self):
        logging.info(f"Zara Parser Start: {self.market}")
        for url in self.make_urls():
            try:
                self.get_data_from_json_loads(url)
            except Exception as e:
                logging.exception(e)
                send_to_telegram.send_as_message(e)

    def make_urls(self):
        urls = []
        for category_id, url_category in self.urls_category_id.items():
            urls.append(f'https://www.zara.com/kz/ru/category/{category_id}/products')
        logging.info(f"{len(urls)} urls created")
        return urls

    def get_data_from_json_loads(self, url):
        logging.info(f"Start URL: {url}")
        session = requests.Session()
        response = session.get(url, params=config.PARAMS, headers=config.HEADERS)
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
            if str(category_id) in url:
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
            if int(price_obj.discount) <= -15:
                image_caption = utils.make_image_caption(product_obj, self.prices_crud.get_last_n_prices(product.id))
                send_tg = send_to_telegram.send_as_media_group(image_caption, product_obj.image)
                logging.info(f"Send to telegram status code: {send_tg}")
        if not last_price or price_obj.discount != '0':
            self.prices_crud.insert(price_obj)
            logging.info(f"New Price: {price_obj.price} for product: {product.id}")

    def __del__(self):
        logging.info(f"Total Parsed: {self.market}, {self.items_count}")


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
        handlers=[logging.FileHandler('zara_parser.log', 'a+', 'utf-8')],
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.INFO,
    )
    ZaraWomanParser().start()
    ZaraManParser().start()
    ZaraKidParser().start()
    ZaraBeautyParser().start()
    ZaraOriginsParser().start()
