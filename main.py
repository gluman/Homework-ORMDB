# Подключается к БД любого типа на ваш выбор (например, к PostgreSQL). +
# Импортирует необходимые модели данных. +
# Принимает имя или идентификатор издателя (publisher), например через input().
# Выводит построчно факты покупки книг этого издателя:

import os
import json

import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

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
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    shop = relationship(Shop, backref='shop')
    book = relationship(Book, backref='book')


class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(Stock, backref='sale')


def create_tables(engine, command):
    if command == 'create':
        Base.metadata.create_all(engine)
    elif command == 'drop':
        Base.metadata.drop_all(engine)


DSN = "postgresql+psycopg2://postgres:postgres@localhost:5432/ormdb"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine, 'create')
Session = sessionmaker(bind=engine)
session = Session()


def load_data_from_json():
    folder = os.getcwd()
    os.chdir('fixtures')
    folder = os.getcwd()
    with open(folder + '/tests_data.json', 'r') as f:
        data = json.load(f)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    try:
        session.commit()
    except:
        print('error import data')


def show_sales(publish):
    q = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
        .join(Stock, Sale.id_stock == Stock.id) \
        .join(Book, Book.id == Stock.id_book) \
        .join(Shop, Shop.id == Stock.id_shop) \
        .join(Publisher, Publisher.id == Book.id_publisher) \
        .filter(Publisher.name.ilike(publish)) \
        .all()

    print('название книги | название магазина| стоимость покупки | дата покупки')
    for s in q:
        print(s.title, '|', s.name, '|', s.price, '|', s.date_sale.strftime("%d-%m-%Y"))
        # print(s)


def show_help():
    print('''
    help    - показать помощь
    create  - создать таблицы
    drop    - удалить таблицы и все данные
    do-all  - создать, удалить таблицы, загрузить данные.
    load-json - загрузить данные из datasets
    sales   - показать продажи по автору
    exit    - выход
    ''')
    return


run = True
while run:
    i = input('Введите команду (help - помощь): ')
    if i == 'create':
        create_tables(engine, 'create')
    elif i == 'do-all':
        create_tables(engine, 'drop')
        create_tables(engine, 'create')
        load_data_from_json()
    elif i == 'load-json':
        load_data_from_json()
    elif i == 'drop':
        create_tables(engine, 'drop')
    elif i == 'help':  # .group_by(Publisher.name)\
        show_help()
    elif i == 'sales':
        publ = fr"{input('Введите издателя:')}"
        show_sales(publ)
    elif i == 'exit':
        run = False
