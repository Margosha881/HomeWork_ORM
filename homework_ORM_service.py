import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
import json
import os
from homework_ORM_models import Publisher,Book,Shop,Sale,Stock,recreate_tables
from dotenv import load_dotenv,find_dotenv
import pandas as pd

load_dotenv(find_dotenv())

database_type = os.getenv('database_type')
user = os.getenv('user')
password = os.getenv('password')
database_name = os.getenv('database_name')
host = os.getenv('host')
port = os.getenv('port')


DNS = f'{database_type}://{user}:{password}@{host}:{port}/{database_name}'
engine = sq.create_engine(DNS)


Session = sessionmaker(bind = engine)
session = Session()

recreate_tables(engine)

folder = os.getcwd()
files = os.listdir()
for file in files:
    if '.json' in file:
        path_to_file = os.path.join(folder, file)
        with open(path_to_file, 'rt', encoding='utf-8') as db:
            data = json.load(db)
            for line in data:
                method = {
                    'publisher':Publisher,
                    'shop':Shop,
                    'book':Book,
                    'stock':Stock,
                    'sale':Sale
                }[line['model']]
                session.add(method(id=line['pk'],**line.get('fields')))
session.commit()

session.close()


publ_name = input('Введите имя автора или его id: ')
if publ_name.isnumeric():
    for c in session.query(Book.title,Shop.name,
                       Sale.price,Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale).filter(
                        Publisher.id==int(publ_name)).all():
                        print(c)
    
else:
    for c in session.query(Book.title,Shop.name,
                       Sale.price,Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale).filter(
                        Publisher.name.like (f'%{publ_name}')).all():
                        print(c)   
