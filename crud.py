from typing import Union

from sqlalchemy.orm import Session

from models import ZaraWomanProducts, ZaraWomanPrices, ZaraManProducts, ZaraManPrices, ZaraKidProducts, ZaraKidPrices, \
    ZaraBeautyProducts, ZaraBeautyPrices, ZaraOriginsProducts, ZaraOriginsPrices
from database import SessionLocal
from schemas import ProductSchema, PriceSchema
import config


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

    def insert(self, data: Union[ProductSchema, PriceSchema]):
        obj = self.schema(**data.dict())
        self.session.add(obj)
        self.session.commit()
        return obj


class ProductsCrud(Crud):
    def __init__(self, session: Session, schema):
        super().__init__(session, schema)

    # def get_by_url(self, url):
    #     return self.session.query(self.schema).filter_by(url=url).first()

    def get_by_store_id(self, store_id):
        return self.session.query(self.schema).filter_by(store_id=store_id).first()

    def get_or_create(self, new_product: ProductSchema):
        # obj = self.get_by_url(new_product.url)
        obj = self.get_by_store_id(new_product.store_id)
        if obj:
            return obj
        return self.insert(new_product)


class PricesCrud(Crud):
    def __init__(self, session: Session, schema):
        super().__init__(session, schema)

    def get_by_product(self, product_id: int):
        return self.session.query(self.schema).filter_by(product_id=product_id).all()

    def get_last_price(self, product_id: int):
        return self.session.query(self.schema).filter_by(product_id=product_id)\
            .order_by(self.schema.created.desc()).first()

    def get_last_n_prices(self, product_id: int):
        return self.session.query(self.schema).filter_by(product_id=product_id).order_by(self.schema.created.desc()).\
            limit(config.LAST_N_PRICES).all()


class WomanProductsCrud(ProductsCrud):
    def __init__(self, session: Session):
        super().__init__(session, ZaraWomanProducts)


class ManProductsCrud(ProductsCrud):
    def __init__(self, session: Session):
        super().__init__(session, ZaraManProducts)


class KidProductsCrud(ProductsCrud):
    def __init__(self, session: Session):
        super().__init__(session, ZaraKidProducts)


class BeautyProductsCrud(ProductsCrud):
    def __init__(self, session: Session):
        super().__init__(session, ZaraBeautyProducts)


class OriginsProductsCrud(ProductsCrud):
    def __init__(self, session: Session):
        super().__init__(session, ZaraOriginsProducts)


class WomanPricesCrud(PricesCrud):
    def __init__(self, session: Session):
        super().__init__(session, ZaraWomanPrices)


class ManPricesCrud(PricesCrud):
    def __init__(self, session: Session):
        super().__init__(session, ZaraManPrices)


class KidPricesCrud(PricesCrud):
    def __init__(self, session: Session):
        super().__init__(session, ZaraKidPrices)


class BeautyPricesCrud(PricesCrud):
    def __init__(self, session: Session):
        super().__init__(session, ZaraBeautyPrices)


class OriginsPricesCrud(PricesCrud):
    def __init__(self, session: Session):
        super().__init__(session, ZaraOriginsPrices)


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
