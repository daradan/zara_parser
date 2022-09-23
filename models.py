from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class ZaraWomanProducts(Base):
    __tablename__ = "zara_w_products"
    product_id = Column(Integer, primary_key=True, index=True)
    created = Column(String, nullable=False)
    market = Column(String, nullable=False)
    url = Column(String, nullable=False)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    category = Column(String)
    description = Column(String)
    availability = Column(String)
    image = Column(String, nullable=False)

    prices = relationship("ZaraWomanPrices", back_populates="product")


class ZaraWomanPrices(Base):
    __tablename__ = "zara_w_prices"
    price_id = Column(Integer, primary_key=True, index=True)
    created = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    discount = Column(String)
    product_id = Column(Integer, ForeignKey(ZaraWomanProducts.product_id))

    product = relationship("ZaraWomanProducts", back_populates="prices")
