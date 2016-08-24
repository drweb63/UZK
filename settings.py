from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://uzk:080166@localhost/uzk')
path_barcode = 'static/barcode/'