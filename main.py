import requests
import json
import working_with_db
import send_to_telegram
import config


class ZaraWomanParser:
    def __init__(self):
        self.data = config.data
        self.urls_category_id = config.urls_category_id
        self.json_loads = dict()
        self.v2 = ''

    def main(self):
        try:
            for url in self.make_urls():
                self.get_data_from_json_loads(url)
        except Exception as e:
            self.data = dict(
                tg_channel='125975839',
                tg_send_method='sendMessage',
                msg_text=f'ERROR: ZARA_W - {e}'
            )
            send_to_telegram.main(**self.data)
            print(e)

    def make_urls(self):
        urls = []
        for category_id, url_category in self.urls_category_id.items():
            urls.append(f'https://www.zara.com/kz/ru/category/{category_id}/products')
            return urls

    def get_data_from_json_loads(self, url):
        session = requests.Session()
        response = session.get(url, params=config.params, headers=config.headers)
        self.json_loads = json.loads(response.text)

        if len(self.json_loads['productGroups']) <= 0:
            return

        elements = self.json_loads['productGroups'][0]['elements']
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
                    self.get_category(url)
                    # self.data['url'] = self.make_url(com_component['seo'])
                    self.make_url(com_component['seo'])
                    if not self.data['url']:
                        continue
                    self.data['name'] = com_component['name']
                    self.data['color'] = color['name']
                    self.data['description'] = com_component.get('description', '')
                    self.data['price'] = color['price'] // 100
                    self.data['image'] = ', '.join(self.make_photo_urls(color['xmedia']))
                    print(self.data)
                    self.check_data_from_db()

    def get_category(self, url):
        for category_id, category in self.urls_category_id.items():
            if category_id in url:
                self.v2 = category_id
                self.data['category'] = category
                break

    def make_url(self, seo):
        if seo['keyword'] == '':
            return False
        keyword = f"{seo['keyword']}"
        seo_product_id = f"{seo['seoProductId']}"
        discern_product_id = f"{seo['discernProductId']}"
        url = f"https://www.zara.com/kz/ru/{keyword}-p{seo_product_id}.html?v1={discern_product_id}&v2={self.v2}"
        self.data['url_non_utf8'] = url
        self.data['url'] = requests.utils.unquote(url)
        # return url
        # return requests.utils.unquote(url)

    def make_photo_urls(self, photos):
        photos_list = []
        for photo in photos:
            path = photo['path']
            name = photo['name']
            timestamp = photo['timestamp']
            photo_str = f"https://static.zara.net/photos//{path}/w/750/{name}.jpg?ts={timestamp}"
            photos_list.append(photo_str)
        return photos_list

    def check_data_from_db(self):
        if working_with_db.check_product('one', **self.data) is None:
            working_with_db.insert_data_to_products(**self.data)
            last_inserted_row = working_with_db.last_row(**self.data)
            self.data['product_id'] = last_inserted_row[0]
            working_with_db.insert_data_to_db_prices(**self.data)
        else:
            # finded_product = [item for item in working_with_db.check_product('all', **self.data) if self.data['url'] == item]
            finded_product = [item for item in working_with_db.check_product('all', **self.data) if
                              self.data['url'] in item]
            if not finded_product:
                working_with_db.insert_data_to_products(**self.data)
                last_inserted_row = working_with_db.last_row(**self.data)
                self.data['product_id'] = last_inserted_row[0]
                working_with_db.insert_data_to_db_prices(**self.data)
            else:
                finded_product_price = list(working_with_db.find_product_price(finded_product[0][0], **self.data))
                self.data['product_id'] = finded_product[0][0]
                finded_price = finded_product_price[3]
                if finded_price != self.data['price']:
                    self.data['discount'] = self.get_percentage(self.data['price'], finded_price)
                    working_with_db.insert_data_to_db_prices(**self.data)
                    # if int(self.data['discount']) <= -15 and self.data['price'] >= 3000:
                    if int(self.data['discount']) <= -15:
                        self.data['last_prices'] = working_with_db.last_n_prices_rows(**self.data)
                        self.data['image_caption'] = self.make_image_caption()
                        # self.send_to_telegram_as_image_caption()
                        send_to_telegram.main(**self.data)
                        print(self.data['image_caption'])
                        # print('YES')

    def get_percentage(self, price, price_old):
        percent = round(-1 * (100 - (price * 100 / price_old)))
        if percent > 0:
            percent = f'+{percent}'
        return str(percent)

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


if __name__ == '__main__':
    ZaraWomanParser().main()
