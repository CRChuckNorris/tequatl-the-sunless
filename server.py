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
    total = 0
    for tran in trans:
        prods = Product.query.filter_by(name=tran.product)
        for prod in prods:
		    total += prod.price
    return render_template('checkout.html', cart = trans, total=total)
	
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
    prods = Product.query.all()
    return render_template('games.html', games = prods)
    
@app.before_request
def before_request():
    g.user = current_user

@app.route('/atc', methods=['POST'])
def add_to_cart():
    print [request.form['game_to_add']]
    for i in [request.form['game_to_add']]:
	    name = i
    tran = Transaction(name, g.user.username)
    db.session.add(tran)
    db.session.commit()
    return redirect(url_for('checkout'))
	
@app.route('/rfc', methods=['POST'])
def remove_from_cart():
    trans = Transaction.query.filter_by(user_id=g.user.username)
    for tran in trans:
	    db.session.delete(tran)
    db.session.commit()
    return redirect(url_for('success'))
	
@app.route('/success')
def success():
    return render_template('success.html')
	
@app.route('/xbox')
def xbox():
    prods = Product.query.filter_by(console='Xbox One')
    return render_template('console.html', games=prods)
	
@app.route('/ps')
def ps():
    prods = Product.query.filter_by(console='PS4')
    return render_template('console.html', games=prods)
	
@app.route('/pc')
def pc():
    prods = Product.query.filter_by(console='PC')
    return render_template('console.html', games=prods)
	
@app.route('/wii')
def wii():
    prods = Product.query.filter_by(console='Wii U')
    return render_template('console.html', games=prods)
	
	
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
    price = db.Column(db.Float)
    console = db.Column(db.String(20))
    
    def __init__(self, name, price, console):
        self.name = name
        self.price = price
        self.console = console

    def __repr__(self):
        return '<Product %r>' % (self.name)
		
@app.route('/')
def index():
	return render_template("index.html")

if __name__ == '__main__':
	app.debug = True
	app.secret_key = 'super secret key'
	app.run(host='0.0.0.0')
