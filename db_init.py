from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Date
from settings import engine, session
import models

metadata = MetaData()
Customers = Table('customers', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Integer, nullable=False, default=''),
    Column('inn', Integer, nullable=True, default='')
)
Cartridges = Table('cartridges', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(250), nullable=False, default=''),
    Column('toner', Integer, nullable=True, default=''),
    Column('opc', Integer, nullable=True, default=''),
    Column('pcr', Integer, nullable=True, default=''),
    Column('wiper_blade', Integer, nullable=True, default=''),
    Column('recovery_blade', Integer, nullable=True, default=''),
    Column('develop_blade', Integer, nullable=True, default=''),
    Column('doctor_blade', Integer, nullable=True, default=''),
    Column('printers', String(250), nullable=True, default='')
)
Tow = Table('tow', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(250), nullable=False, default=''),
    Column('fullname', String(250), nullable=True, default=''),
)
Orders = Table('orders', metadata,
    Column('id', Integer, primary_key=True),
    Column('cartridge', Integer, ForeignKey('cartridges.id'), nullable=False, default=''),
    Column('customer', Integer, ForeignKey('customers.id'), nullable=True, default=''),
    Column('tow', Integer, ForeignKey('tow.id'), nullable=True, default=''),
    Column('barcode', Integer, nullable=True, default=''),
    Column('mark', String(250), nullable=True, default=''),
    Column('date', Date, nullable=True, default=''),
)
Close_orders = Table('close_orders', metadata,
    Column('id', Integer, primary_key=True),
    Column('cartridge', Integer, nullable=True, default=''),
    Column('customer', Integer, nullable=True, default=''),
    Column('toner', Integer, nullable=False, default='0'),
    Column('opc', Integer, nullable=False, default='0'),
    Column('pcr', Integer, nullable=False, default='0'),
    Column('wiper_blade', Integer, nullable=False, default='0'),
    Column('recovery_blade', Integer, nullable=False, default='0'),
    Column('develop_blade', Integer, nullable=False, default='0'),
    Column('doctor_blade', Integer, nullable=False, default='0'),
    Column('barcode', Integer, nullable=True, default=''),
    Column('mark', String(250), nullable=True, default=''),
    Column('user_close', String(250), nullable=False, default='0'),
    Column('date', Date, nullable=True, default=''),
    Column('date_close', Date, nullable=True, default=''),
    Column('status', String(250), nullable=True, default=''),
    Column('comment', String(250), nullable=True, default='')
)
Archive_orders = Table('archive_orders', metadata,
    Column('id', Integer, primary_key=True),
    Column('cartridge', Integer, nullable=True, default=''),
    Column('customer', Integer, nullable=True, default=''),
    Column('toner', Integer, nullable=False, default='0'),
    Column('opc', Integer, nullable=False, default='0'),
    Column('pcr', Integer, nullable=False, default='0'),
    Column('wiper_blade', Integer, nullable=False, default='0'),
    Column('recovery_blade', Integer, nullable=False, default='0'),
    Column('develop_blade', Integer, nullable=False, default='0'),
    Column('doctor_blade', Integer, nullable=False, default='0'),
    Column('barcode', Integer, nullable=True, default=''),
    Column('mark', String(250), nullable=True, default=''),
    Column('user_close', String(250), nullable=False, default='0'),
    Column('date', Date, nullable=True, default=''),
    Column('date_close', Date, nullable=True, default=''),
    Column('status', String(250), nullable=True, default=''),
    Column('comment', String(250), nullable=True, default='')
)
Barcode = Table('barcode', metadata,
    Column('id', Integer, primary_key=True),
    Column('cartridge', Integer, nullable=False, default=''),
    Column('customer', Integer, nullable=True, default=''),
    Column('barcode', Integer, nullable=True, default='', unique=True)
)
Category = Table('category', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(250), nullable=False, default='', unique=True),
)
Users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(250), nullable=False, default=''),
    Column('fullname', String(250), nullable=False, default=''),
    Column('password', String(250), nullable=False, default=''),
    Column('privilegies', Integer, nullable=False, default='0'),
    Column('vision', Integer, nullable=False, default='1')
)
Logs = Table('logs', metadata,
    Column('id', Integer, primary_key=True),
    Column('user', String(250), nullable=True, default=''),
    Column('time', String(250), nullable=True, default=''),
    Column('message', Date, nullable=True, default='')
)

metadata.bind = engine
metadata.create_all(checkfirst=True)

add = models.Users(name='admin',fullname='Администратор',password='21232f297a57a5a743894a0e4a801fc3',privilegies='3',vision='0')
session.add(add)
session.commit()
session.flush()