# Подключается к БД любого типа на ваш выбор (например, к PostgreSQL). +
# Импортирует необходимые модели данных. +
# Принимает имя или идентификатор издателя (publisher), например через input(). Выводит построчно факты покупки книг этого издателя:
import os
import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class Publisher(Base):
    __table__ = 'publisher'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60), unique=True)


class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=60), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(Publisher, backref='book')

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60), unique=True)

class Stock(Base):
    _tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

class Sale(Base):
    _tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Integer, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock'), nullable=False)
    count = sq.Column(sq.Integer,nullable=False)



def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

DSN = "postgresql://postgres:postgres@localhost:5432/ormdb"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

folder = os.getcwd()
files = os.listdir()

def load_data():
    pass

def show_sales():
    pass

run = True
def show_help():
    print('''
    help - show help
    load - load data from datasets
    sales - show sales
    exit - exit
    ''')
    return

while run:
    i = input('Введите команду (h- помощь): ')
    if i == 'c':
        load_data()
    elif i == 'help':
        show_help()
    elif i == 'sales':
        show_sales()
    elif i == 'exit':
        run = False
