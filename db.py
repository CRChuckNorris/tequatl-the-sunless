from server import db
from server import User
from server import Transaction
from server import Product

db.create_all()

productA = Product('A', '5')

db.session.add(productA)

db.session.commit()

db.session.commit()