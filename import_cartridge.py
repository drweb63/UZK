from openpyxl import load_workbook
from models import Customers, Cartridges
from database import session
wb = load_workbook(filename='Картриджи.xlsx', read_only=True)
sheet = wb.get_sheet_names()
ws = wb['Лист1'] # ws is now an IterableWorksheet

for row in ws.rows:
    a = 0
    b = 0
    for cell in row:
        if a == 0 :
            a = cell.value
        else: b = cell.value
    print (a,b)
    customer = Cartridges(name=a,toner=0, opc=0, pcr=0, wiper_blade=0, recovery_blade=0, develop_blade=0, doctor_blade=0, printers='')
    session.add(customer)


session.commit()
session.flush()

