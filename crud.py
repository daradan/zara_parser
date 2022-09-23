from sqlalchemy.orm import Session

from models import ZaraWomanProducts
from database import SessionLocal


class ProductsCrud:
    def __init__(self, session: Session):
        self.session = session

    def get(self, pk: int) -> ZaraWomanProducts:
        return self.session.get(ZaraWomanProducts, pk)

    def get_by_url(self, url: str) -> ZaraWomanProducts:
        return self.session.query(ZaraWomanProducts).filter_by(url=url).first()


def start():
    session = SessionLocal()
    products_crud = ProductsCrud(session)
    url = 'https://www.zara.com/kz/ru/платье-с-широкими-рукавами-и-блестящеи-нитью-p05584465.html?v1=203180287&v2=2111785'
    product = products_crud.get_by_url(url)
    print(product)


if __name__ == "__main__":
    start()
