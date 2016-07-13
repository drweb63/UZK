from database import session
import re
from sqlalchemy import text, insert, select, desc, update
from models import Barcode
from bar_gen import Code128
from settings import path_barcode

barcodes = session.query(Barcode.barcode).all()

for barcode in barcodes:
    barc = str(barcode)
    code = re.sub("[^\w\s]+", '', barc).strip()
    full_barcode = path_barcode
    Code128(code).save(formats=['gif'],outDir=full_barcode, fnRoot=code )
    print (code)
