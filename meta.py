from database import engine
from sqlalchemy import MetaData, types, Table, Column

metadata = MetaData()

Customers = Table('Customers', metadata,
                Column('id', types.Text(), primary_key=True),
                Column('name', types.Text()),
                Column('inn', types.Text()),
               )

metadata.bind = engine

metadata.create_all(checkfirst=True)