from settings import Base
from settings import engine
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    MetaData,
    ForeignKey,
    Date
)

metadata = MetaData()
metadata.bind=engine

class Customers(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, default='')
    inn = Column(String(250), nullable=True, default='')

    orders = relationship("Orders", backref="Customers")

    def __str__(self):
        return self.name

class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    cartridge = Column(Integer, ForeignKey('cartridges.id'), nullable=False, default='')
    customer = Column(Integer, ForeignKey('customers.id'), nullable=True, default='')
    tow = Column(Integer, ForeignKey('tow.id'), nullable=True, default='')
    barcode = Column(Integer, nullable=True, default='')
    mark = Column(String(250), nullable=True, default='')
    date = Column(Date, nullable=True, default='')

    def __int__(self):
        return self.id

class Close_orders(Base):
    __tablename__ = 'close_orders'

    id = Column(Integer, primary_key=True)
    cartridge = Column(Integer, nullable=False, default='')
    customer = Column(Integer, nullable=True, default='')
    toner = Column(Integer, nullable=True, default='0')
    opc = Column(Integer, nullable=True, default='0')
    pcr = Column(Integer, nullable=True, default='0')
    wiper_blade = Column(Integer, nullable=True, default='0')
    recovery_blade = Column(Integer, nullable=True, default='0')
    develop_blade = Column(Integer, nullable=True, default='0')
    doctor_blade = Column(Integer, nullable=True, default='0')
    barcode = Column(Integer, nullable=True, default='')
    mark = Column(String(250), nullable=True, default='')
    user_close = Column(String(250), nullable=True, default='0')
    date = Column(Date, nullable=True, default='')
    date_close = Column(Date, nullable=True, default='')
    status = Column(String(250), nullable=True, default='')
    comment = Column(String(250), nullable=True, default='')

    def __int__(self):
        return self.id

class Archive_orders(Base):
    __tablename__ = 'archive_orders'

    id = Column(Integer, primary_key=True)
    cartridge = Column(Integer, nullable=False, default='')
    customer = Column(Integer, nullable=True, default='')
    toner = Column(Integer, nullable=True, default='0')
    opc = Column(Integer, nullable=True, default='0')
    pcr = Column(Integer, nullable=True, default='0')
    wiper_blade = Column(Integer, nullable=True, default='0')
    recovery_blade = Column(Integer, nullable=True, default='0')
    develop_blade = Column(Integer, nullable=True, default='0')
    doctor_blade = Column(Integer, nullable=True, default='0')
    barcode = Column(Integer, nullable=True, default='')
    mark = Column(String(250), nullable=True, default='')
    user_close = Column(String(250), nullable=True, default='0')
    date = Column(Date, nullable=True, default='')
    date_close = Column(Date, nullable=True, default='')
    status = Column(String(250), nullable=True, default='')
    comment = Column(String(250), nullable=True, default='')

    def __int__(self):
        return self.id

class Barcode(Base):
    __tablename__ = 'barcode'

    id = Column(Integer, primary_key=True)
    cartridge = Column(Integer, nullable=False, default='')
    customer = Column(Integer, nullable=True, default='')
    barcode = Column(Integer, nullable=True, default='', unique=True)

    def __str__(self):
        return self.name

class Cartridges(Base):
    __tablename__ = 'cartridges'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, default='')
    toner = Column(Integer, nullable=True, default='')
    opc = Column(Integer, nullable=True, default='')
    pcr = Column(Integer, nullable=True, default='')
    wiper_blade = Column(Integer, nullable=True, default='')
    recovery_blade = Column(Integer, nullable=True, default='')
    develop_blade = Column(Integer, nullable=True, default='')
    doctor_blade = Column(Integer, nullable=True, default='')
    printers = Column(String(250), nullable=True, default='')

    def __str__(self):
        return self.name

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, default='', unique=True)

    def __str__(self):
        return self.name

class Tow(Base):
    __tablename__ = 'tow'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, default='')
    fullname = Column(String(250), nullable=True, default='')

    def __str__(self):
        return self.fullname

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, default='')
    fullname = Column(String(250), nullable=False, default='')
    password = Column(String(250), nullable=False, default='')
    privilegies = Column(Integer, nullable=False, default='0')
    vision = Column(Integer, nullable=False, default='1')



    def __str__(self):
        return self.name

class Logs(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    user = Column(String(250), nullable=True, default='')
    time = Column(String(250), nullable=True, default='')
    message = Column(Date, nullable=True, default='')

    def __str__(self):
        return self.user