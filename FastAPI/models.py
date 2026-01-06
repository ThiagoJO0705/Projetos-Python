from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import ChoiceType

#conexão
db = create_engine('sqlite:///banco.db')

#base
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String)
    email = Column('email', String, nullable=False)
    password = Column('password', String)
    active = Column('active', Boolean)
    admin = Column('admin', Boolean, default=False)

    def __init__(self, name, email, password, active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin

class Order(Base):
    __tablename__ = 'orders'


    # ORDER_STATUS = (
    #     ('PENDENTE', 'PENDENTE'),
    #     ('CANCELADO', 'CANCELADO'),
    #     ('FINALIZADO', 'FINALIZADO')
    # )


    id = Column('id', Integer, primary_key=True, autoincrement=True)
    status = Column('status', String) #ChoiceType(ORDER_STATUS)
    user = Column('user', ForeignKey('users.id'))
    price = Column('price', Float)

    def __init__(self, user, status='PENDENTE', price=0):
        self.user = user
        self.price = price
        self.status = status

class OrderItem(Base):

    __tablename__ = 'order_items'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    quantity = Column('quantity', Integer)
    flavor = Column('flavor', String)
    size = Column('size', String)
    unit_price = Column('unit_price', Float)
    order = Column('order', ForeignKey('orders.id'))

    def __init__(self, quantity, flavor, size, unit_price, order):
        self.quantity = quantity
        self.flavor = flavor
        self.size = size
        self.unit_price = unit_price
        self.order = order