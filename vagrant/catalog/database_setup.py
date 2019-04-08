import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    first_name = Column(String(80))
    last_name = Column(String(80))
    picture = Column(String(250))
    email = Column(String(80))

class Store(Base):
    __tablename__ = 'store'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    picture = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }

class Item(Base):
    __tablename__ = 'item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    store_id = Column(Integer, ForeignKey('store.id'))
    store = relationship(Store)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    picture = Column(String(250))

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
        }

engine = create_engine('sqlite:///itemCatalog.db')


Base.metadata.create_all(engine)