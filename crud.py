from typing import Union

from sqlalchemy.orm import Session

from models import ZaraWomanProducts, ZaraWomanPrices
from database import SessionLocal


class WomanProductsCrud:
    def __init__(self, session: Session):
        self.session = session

    def get(self, pk: int) -> ZaraWomanProducts:
        return self.session.get(ZaraWomanProducts, pk)

    def update(self, data):
        ...  # update

    def delete(self, pk):
        ...  # delete

    def insert(self, data: dict):
        obj = ZaraWomanProducts(**data)
        self.session.add(obj)
        self.session.commit()
        return obj

    def get_by_url(self, url: str):
        return self.session.query(ZaraWomanProducts).filter_by(url=url).first()

    def get_or_create(self, data: dict):
        obj = self.get_by_url(data['url'])
        if obj:
            return obj
        return self.insert(data)


class WomanPricesCrud:
    def __init__(self, session: Session):
        self.session = session

    def get(self, pk: int) -> ZaraWomanPrices:
        return self.session.get(ZaraWomanPrices, pk)

    def update(self, data):
        ...  # update

    def delete(self, pk):
        ...  # delete

    def insert(self, data: dict):
        obj = ZaraWomanPrices(**data)
        self.session.add(obj)
        self.session.commit()
        return obj

    def get_by_product(self, product_id: int):
        return self.session.query(ZaraWomanPrices).filter_by(product_id=product_id).all()

    def get_last_price(self, product_id: int):
        return self.session.query(ZaraWomanPrices).filter_by(product_id=product_id)\
            .order_by(ZaraWomanPrices.created.desc()).first()


def start():
    session = SessionLocal()
    products_crud = WomanProductsCrud(session)
    url = 'https://www.zara.com/kz/ru/платье-с-широкими-рукавами-и-блестящеи-нитью-p05584465.html?v1=203180287&v2=2111785'
    product = products_crud.get_by_url(url)
    product_from_source = {}
    products_crud.update(product_from_source)
    products_crud.delete(product.product_id)
    print(product)


if __name__ == "__main__":
    start()
