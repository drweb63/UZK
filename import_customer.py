from openpyxl import load_workbook
from models import Customers, Cartridges
from settings import session
wb = load_workbook(filename='Клиенты.xlsx', read_only=True)
sheet = wb.get_sheet_names()
ws = wb['Лист1'] # ws is now an IterableWorksheet
#gh
for row in ws.rows:
    a = 0
    b = 0
    for cell in row:
        if a == 0 :
            a = cell.value
        else: b = cell.value
    print (a,b)
    customer = Customers(name=a, inn=b)
    session.add(customer)


session.commit()
session.flush()

