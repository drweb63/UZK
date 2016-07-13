from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from database import engine
metadata = MetaData()
users_table = Table('archive_orders', metadata,
    Column('id', Integer, primary_key=True),
    Column('cartridge', Integer, nullable=True, default=''),
    Column('customer', Integer, nullable=True, default=''),
    Column('toner', Integer, nullable=True, default=''),
    Column('opc', Integer, nullable=True, default=''),
    Column('pcr', Integer, nullable=True, default=''),
    Column('wiper_blade', Integer, nullable=True, default=''),
    Column('recovery_blade', Integer, nullable=True, default=''),
    Column('develop_blade', Integer, nullable=True, default=''),
    Column('doctor_blade', Integer, nullable=True, default=''),
    Column('barcode', Integer, nullable=True, default=''),
    Column('mark', String, nullable=True, default=''),
    Column('user_close', String, nullable=True, default=''),
    Column('date', String, nullable=True, default=''),
    Column('date_close', String, nullable=True, default=''),

)

metadata.create_all(engine)