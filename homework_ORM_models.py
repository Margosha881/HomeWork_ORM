import sqlalchemy as sq
from sqlalchemy.orm import declarative_base,relationship
import datetime as dt


Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'
    id = sq.Column(sq.Integer,primary_key = True)
    name = sq.Column(sq.String(50), unique = True)

    #publisher_book = relationship('Book', back_populates = 'book_publisher')

    def __str__(self):
        return f'{self.id}:{self.name}'

class Book(Base):
    __tablename__ = 'book'
    id = sq.Column(sq.Integer, primary_key = True)
    title = sq.Column(sq.String,nullable= False)
    id_publisher = sq.Column(sq.Integer,sq.ForeignKey('publisher.id'))

    publisher = relationship(Publisher,backref = 'book')
    #stock = relationship('Stock', back_populates = 'stock_book')
    
    def __str__(self):
        return f'{self.title}'

class Shop(Base):
    __tablename__ = 'shop'
    id = sq.Column(sq.Integer, primary_key = True)
    name = sq.Column(sq.String,unique = True)

    #shop_stock = relationship('Stock', back_populates = 'stock_shop')

    def __str__(self):
        return f'{self.name}' 

class Stock(Base):
    __tablename__ = 'stock'
    id = sq.Column(sq.Integer, primary_key = True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'))
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'))
    count = sq.Column(sq.Integer,nullable = False)

    shop = relationship(Shop, backref = 'stock')
    book = relationship(Book, backref = 'stock')
    #stock_sale = relationship('Sale', back_populates = 'sale_stock')

    def __str__(self):
        return f'{self.id_book}:{self.id_shop}:{self.count}'

class Sale(Base):
    __tablename__ = 'sale'
    id =  sq.Column(sq.Integer,primary_key = True)
    price = sq.Column(sq.FLOAT, nullable = False)
    date_sale = sq.Column(sq.DateTime,default = dt.datetime.now)
    id_stock = sq.Column(sq.Integer,sq.ForeignKey('stock.id'))
    count = sq.Column(sq.Integer, nullable = False)

    stock = relationship(Stock, backref = 'sale')

    def __str__(self):
        return f'{self.price} | {self.date_sale}'


def recreate_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)



    







