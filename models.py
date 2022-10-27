from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from database import Base, engine


class ZaraWomanProducts(Base):
    __tablename__ = "zara_w_products"
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    market = Column(String, nullable=False)
    url = Column(String, nullable=False)
    store_id = Column(Integer, nullable=False)
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
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    price = Column(Integer, nullable=False)
    discount = Column(String)
    product_id = Column(Integer, ForeignKey(ZaraWomanProducts.id))

    product = relationship("ZaraWomanProducts", back_populates="prices")


class ZaraManProducts(Base):
    __tablename__ = "zara_m_products"
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    market = Column(String, nullable=False)
    url = Column(String, nullable=False)
    store_id = Column(Integer, nullable=False)
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
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    price = Column(Integer, nullable=False)
    discount = Column(String)
    product_id = Column(Integer, ForeignKey(ZaraManProducts.id))

    product = relationship("ZaraManProducts", back_populates="prices")


class ZaraKidProducts(Base):
    __tablename__ = "zara_k_products"
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    market = Column(String, nullable=False)
    url = Column(String, nullable=False)
    store_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    category = Column(String)
    description = Column(String)
    availability = Column(String)
    image = Column(String, nullable=False)

    prices = relationship("ZaraKidPrices", back_populates="product")


class ZaraKidPrices(Base):
    __tablename__ = "zara_k_prices"
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    price = Column(Integer, nullable=False)
    discount = Column(String)
    product_id = Column(Integer, ForeignKey(ZaraKidProducts.id))

    product = relationship("ZaraKidProducts", back_populates="prices")


class ZaraBeautyProducts(Base):
    __tablename__ = "zara_b_products"
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    market = Column(String, nullable=False)
    url = Column(String, nullable=False)
    store_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    category = Column(String)
    description = Column(String)
    availability = Column(String)
    image = Column(String, nullable=False)

    prices = relationship("ZaraBeautyPrices", back_populates="product")


class ZaraBeautyPrices(Base):
    __tablename__ = "zara_b_prices"
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    price = Column(Integer, nullable=False)
    discount = Column(String)
    product_id = Column(Integer, ForeignKey(ZaraBeautyProducts.id))

    product = relationship("ZaraBeautyProducts", back_populates="prices")


class ZaraOriginsProducts(Base):
    __tablename__ = "zara_o_products"
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    market = Column(String, nullable=False)
    url = Column(String, nullable=False)
    store_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    category = Column(String)
    description = Column(String)
    availability = Column(String)
    image = Column(String, nullable=False)

    prices = relationship("ZaraOriginsPrices", back_populates="product")


class ZaraOriginsPrices(Base):
    __tablename__ = "zara_o_prices"
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    price = Column(Integer, nullable=False)
    discount = Column(String)
    product_id = Column(Integer, ForeignKey(ZaraOriginsProducts.id))

    product = relationship("ZaraOriginsProducts", back_populates="prices")


Base.metadata.create_all(engine)
