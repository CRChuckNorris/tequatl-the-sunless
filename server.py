import os
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.login import login_user , logout_user , current_user , login_required
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask import Flask,session, request, flash, url_for, redirect, render_template, abort ,g
from flask.ext.login import UserMixin
import sys
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
app.secret_key = 'gazeburndecay'
db = SQLAlchemy(app)
db.create_all()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['username'] , request.form['password'],request.form['email'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))
 
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username,password=password).first()
    print registered_user
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))
	
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/checkout', methods=['GET','POST'])
@login_required
def checkout():
    trans = Transaction.query.filter_by(user_id=g.user.username)
    return render_template('checkout.html', cart = trans)
	
@app.route('/pay', methods=['GET','POST'])
@login_required
def pay():
    trans = Transaction.query.filter_by(user_id=g.user.username)
    return render_template('pay.html', cart = trans)
	
@app.route('/about')
def about():
    return render_template('about.html')
	
@app.route('/games', methods=['GET','POST'])
def games():
    return render_template('games.html')
    
@app.before_request
def before_request():
    g.user = current_user
	
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column('user_id',db.Integer , primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String(10))
    email = db.Column('email',db.String(50), index=True)
    registered_on = db.Column('registered_on' , db.DateTime)
    transaction = db.relationship('Transaction', backref='owner', lazy='dynamic')
 
    def __init__(self , username ,password , email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()
		
	def is_authenticated(self):
		return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
 
    def __repr__(self):
        return '<User %r>' % (self.username)

class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key = True)
    product = db.Column(db.String(20), db.ForeignKey('products.name'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    
    def __init__(self , product ,user_id):
        self.product = product
        self.user_id = user_id

    def __repr__(self):
        return '<Transaction %r>' % (self.product)
		
class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    price = db.Column(db.Integer)
    
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return '<Product %r>' % (self.name)
		
@app.route('/')
def index():
	return render_template("index.html")
 
@app.route('/', methods=['POST'])
def postcodeReturn():
  
	client = foursquare.Foursquare(client_id='ILM2KRYYDZVPE3KVMLH1K34JQBKKBALXZL3C1ZGHKIRA23UP',client_secret='MUZXSHLAUP4FZWIHJYU5YBNVS52KPDOKOONTPBVZDP3ZDBGP')

	pc = PostCoder()

	houseN = request.form['houseNo'].strip()
	postcode = request.form['post'].strip()
	amenity = request.form['amenity'].strip()

	result = pc.get(postcode)

	lat = result['geo']['lat']
	lng = result['geo']['lng']

	ll = str(lat) + "," + str(lng)

	params = {}
	params['ll'] = ll
   
	if amenity != "":
	
		params['query'] = amenity
	 
	output = client.venues.search(params)

	op = output['venues']

	nameList = []
	addressList = []

	for venue in op:
	
		nameList.append(venue['name'].strip())
		address = venue['location']['formattedAddress']
		addressList.append(address)

	nums = []
   
	for i in range(len(nameList)):
	
		nums.append(i)

	return render_template('showAms.html', ams=nameList, adds=addressList, num=nums, postc = postcode, hn= houseN)  


if __name__ == '__main__':
	app.debug = True
	app.secret_key = 'super secret key'
	app.run(host='0.0.0.0')
