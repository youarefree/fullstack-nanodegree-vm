from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Store, Base, Item, User

engine = create_engine('sqlite:///itemCatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


store1 = Store(name="Anna's Item Catalog")

Item1 = Item(user_id=1, name="Jacket Transparent", description="Vinyl Transparent Jacket",
                     price="$70.00", picture="https://images-na.ssl-images-amazon.com/images/I/71XVeZYv5-L._UX679_.jpg" ,store=store1)

session.add(Item1)
session.commit()


Item2 = Item(user_id=1, name="Pants", description="Casual pants",
                     price="$15.00", picture="https://cdn.shopify.com/s/files/1/0407/7545/products/NHW_2886_e80f9352-d092-467f-94f6-14bb408a40f4.jpg?v=1505818644",store=store1)

session.add(Item2)
session.commit()

session.add(store1)
session.commit()

print("database populated items!")