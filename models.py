from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, MetaData
from sqlalchemy.orm import relationship

from database import Base, engine


class ZaraWomanProducts(Base):
    __tablename__ = "zara_w_products"
    id = Column(Integer, primary_key=True, index=True)
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
    id = Column(Integer, primary_key=True, index=True)
    created = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    discount = Column(String)
    product_id = Column(Integer, ForeignKey(ZaraWomanProducts.id))

    product = relationship("ZaraWomanProducts", back_populates="prices")


class ZaraManProducts(Base):
    __tablename__ = "zara_m_products"
    id = Column(Integer, primary_key=True, index=True)
    created = Column(String, nullable=False)
    market = Column(String, nullable=False)
    url = Column(String, nullable=False)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    category = Column(String)
    description = Column(String)
    availability = Column(String)
    image = Column(String, nullable=False)

    prices = relationship("ZaraManPrices", back_populates="product")


class ZaraManPrices(Base):
    __tablename__ = "zara_m_prices"
    id = Column(Integer, primary_key=True, index=True)
    created = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    discount = Column(String)
    product_id = Column(Integer, ForeignKey(ZaraManProducts.id))

    product = relationship("ZaraManProducts", back_populates="prices")


Base.metadata.create_all(engine)


