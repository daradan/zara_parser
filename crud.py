from typing import Union

from sqlalchemy.orm import Session

from models import ZaraWomanProducts, ZaraWomanPrices, ZaraManProducts, ZaraManPrices
from database import SessionLocal


class Crud:
    def __init__(self, session: Session, schema):
        self.session = session
        self.schema = schema

    def get(self, pk):
        return self.session.get(self.schema, pk)

    def update(self, data):
        self.session.query(self.schema).filter_by(id=data['id']).update(**data)

    def delete(self, pk):
        self.session.query(self.schema).filter_by(id=pk).delete()

    def insert(self, data):
        obj = self.schema(**data)
        self.session.add(obj)
        self.session.commit()
        return obj


class ProductsCrud(Crud):
    def __init__(self, session: Session, schema):
        super().__init__(session, schema)

    def get_by_url(self, url):
        return self.session.query(self.schema).filter_by(url=url).first()

    def get_or_create(self, data):
        obj = self.get_by_url(data['url'])
        if obj:
            return obj
        return self.insert(data)


class PricesCrud(Crud):
    def __init__(self, session: Session, schema):
        super().__init__(session, schema)

    def get_by_product(self, product_id: int):
        return self.session.query(self.schema).filter_by(product_id=product_id).all()

    def get_last_price(self, product_id: int):
        return self.session.query(self.schema).filter_by(product_id=product_id)\
            .order_by(self.schema.created.desc()).first()


class WomanProductsCrud(ProductsCrud):
    def __init__(self, session: Session):
        super().__init__(session, ZaraWomanProducts)


class ManProductsCrud(ProductsCrud):
    def __init__(self, session: Session):
        super().__init__(session, ZaraManProducts)


class WomanPricesCrud(PricesCrud):
    def __init__(self, session: Session):
        super().__init__(session, ZaraWomanPrices)


class ManPricesCrud(PricesCrud):
    def __init__(self, session: Session):
        super().__init__(session, ZaraManPrices)


def start():
    session = SessionLocal()
    products_crud = WomanProductsCrud(session)
    id = 751
    product = products_crud.get(id)

    url = 'https://www.zara.com/kz/ru/платье-с-широкими-рукавами-и-блестящеи-нитью-p05584465.html?v1=203180287&v2=2111785'
    product = products_crud.get_by_url(url)
    product_from_source = {}
    products_crud.update(product_from_source)
    products_crud.delete(product.product_id)
    print(product)


if __name__ == "__main__":
    start()