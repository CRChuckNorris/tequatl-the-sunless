from server import db
from server import User
from server import Transaction
from server import Product

db.create_all()

diablo = Product('Diablo 3', '25.00', 'Xbox One')
sc2 = Product('Starcraft 2', '20.00', 'PC')
gw2 = Product('Guild Wars 2', '40.00', 'PC')
crypt = Product('Crypt of the Necrodancer', '10.00', 'PC')
csgo = Product('CSGO', '15.00', 'PC')
ds2 = Product('Dark Souls 2', '35.00', 'Xbox One')
bb = Product('Bloodborne', '35.00', 'PS4')
iss = Product('Infamous Second Son', '45.00', 'PS4')
last = Product('The last of us remastered', '40.00', 'PS4')
ki = Product('Killer Instinct', '35.00', 'Xbox One')
dk = Product('Donkey Kong Country Tropical Freeze', '25.00', 'Wii U') 
hy = Product('Hyrule Warriors', '45.00', 'Wii U') 
mk = Product('Mario Kart 8', '30.00', 'Wii U') 

db.session.add(diablo)
db.session.add(sc2)
db.session.add(gw2)
db.session.add(crypt)
db.session.add(csgo)
db.session.add(ds2)
db.session.add(bb)
db.session.add(iss)
db.session.add(last)
db.session.add(ki)
db.session.add(dk)
db.session.add(hy)
db.session.add(mk)

db.session.commit()
