from sqlalchemy.sql import insert
from models import Customers
from settings import engine

ins = Customers.insert().values(name='Фабрика', inn='23454645')
str(ins)
conn = engine.connect()
result = conn.execute(ins)