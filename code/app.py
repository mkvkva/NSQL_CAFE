import codecs
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.dialects.sqlite import insert

from redis import Redis
from pymongo import MongoClient
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import time

#from wtforms.fields import datetime
from forms import MenuForm, AddOrderForm, OrderForm, DelOrderForm, OrderInfoForm, SaveOrderForm, ReservationForm

USER_IMG_FOLDER = 'static/img/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = USER_IMG_FOLDER
app.config['SECRET_KEY'] = 'kseniya_secret_key2023'

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///baza.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

redis_db = Redis(host='localhost', port=6379)

user_login = "ksenia"

engine = db.create_engine("sqlite:///baza.db")
conn = engine.connect()
metadata = db.MetaData()

products = db.Table('products', metadata,
                    db.Column('id', db.Integer, primary_key=True),
                    db.Column('name', db.String),
                    db.Column('price', db.Integer),
                    db.Column('img', db.String)
                    )


#metadata.create_all(engine)

#insertion_query = products.insert().values([
#    {'name': 'Coffee "Coffee "Americano" classic, 230 ml', 'price': 35,
#     'img': 'CoffeeAmericanoLarge product-header-desktop.jpg'},
#    {'name': 'Coffee "Americano with milk" classic 275 ml', 'price': 44,
#     'img': 'CoffeeAmericanoWithMilkMedium product-header-desktop'},
#    {'name': 'Coffee "Coffee "Cappuccino" classic 245 ml', 'price': 30,
#     'img': 'CoffeeCapuccinoLarge product-header-desktop.jpg'},
#    {'name': 'Coffee "Latte" classic 295 ml', 'price': 35, 'img': 'CoffeeLatteLarge product-header-desktop.jpg'},
#    {'name': 'Coffee "Flat White" 155 ml', 'price': 30, 'img': 'CoffeeFlatWhite product-header-desktop.jpg'},
#    {'name': 'Mocha classic, 295 ml', 'price': 35, 'img': 'McC_CoffeeMoccoClassic product-header-desktop.jpg'},
#    {'name': 'Latte Brownie, 300 ml', 'price': 40, 'img': 'Drink_Brownie_Latte product-header-desktop.jpg'},
#    {'name': 'Cocoa classic, 300 ml', 'price': 30, 'img': 'CocoaMedium product-header-desktop.jpg'},
#    {'name': 'Coca-Cola® mala 250 ml', 'price': 45, 'img': 'Cola_250ml product-header-desktop.jpg'},
#    {'name': 'Fanta® is small, 250 ml', 'price': 45, 'img': 'Fanta_250ml product-header-desktop.jpg'},
#    {'name': 'Sprite® is small, 250 ml', 'price': 20, 'img': 'Sprite_250ml product-header-desktop.jpg'},
#    {'name': 'Orange juice is small, 300 ml', 'price': 30, 'img': 'JuiceOrangeSmall product-header-desktop.jpg'},
#    {'name': 'Green tea with citrus fruits, 300 ml', 'price': 10, 'img': 'TeaGreen product-header-desktop.jpg'}
#])

#conn.execute(insertion_query)
#conn.commit()

news = db.Table('news', metadata,
                    db.Column('id', db.Integer, primary_key=True),
                    db.Column('title', db.String),
                    db.Column('text', db.Integer),
                    db.Column('img', db.String)
                    )


metadata.create_all(engine)

#insertion_query = news.insert().values([
#    {'title': 'Lecture about aliens philosophy', 'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean sit amet viverra augue. Nulla consectetur velit urna, sit amet porta massa ornare sed. Nulla egestas pretium nibh. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Suspendisse vel maximus velit. Aenean ac mauris non enim mattis vehicula. Vivamus posuere eleifend nunc sed euismod.Integer feugiat nulla a libero scelerisque gravida. Mauris vel eros est. Morbi facilisis, tortor pellentesque congue porttitor, diam nisl tincidunt orci, vel hendrerit justo magna ut dolor. Praesent luctus efficitur sapien, sit amet venenatis ligula. Nullam feugiat felis pulvinar, ultrices tortor sit amet, pulvinar velit. Pellentesque tempor tellus vel nibh pharetra, non luctus dui malesuada. Nulla a tincidunt ante, a pretium tellus. Suspendisse venenatis urna pellentesque odio tristique bibendum. Curabitur lobortis at odio vel luctus. Sed quis purus interdum, hendrerit metus sed, pharetra lectus. Quisque tempus orci sed quam aliquam, non commodo turpis venenatis.',
#     'img': 'novyna1.jpg'},
#    {'title': 'Shipnado', 'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean sit amet viverra augue.Nulla consectetur velit urna, sit amet porta massa ornare sed. Nulla egestas pretium nibh. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Suspendisse vel maximus velit. Aenean ac mauris non enim mattis vehicula. Vivamus posuere eleifend nunc sed euismod.Integer feugiat nulla a libero scelerisque gravida. Mauris vel eros est. Morbi facilisis, tortor pellentesque congue porttitor, diam nisl tincidunt orci, vel hendrerit justo magna ut dolor. Praesent luctus efficitur sapien, sit amet venenatis ligula. Nullam feugiat felis pulvinar, ultrices tortor sit amet, pulvinar velit. Pellentesque tempor tellus vel nibh pharetra, non luctus dui malesuada. Nulla a tincidunt ante, a pretium tellus. Suspendisse venenatis urna pellentesque odio tristique bibendum. Curabitur lobortis at odio vel luctus. Sed quis purus interdum, hendrerit metus sed, pharetra lectus. Quisque tempus orci sed quam aliquam, non commodo turpis',
#     'img': 'novyna2.jpg'}
#])

#conn.execute(insertion_query)
#conn.commit()


def get_db_connection_mongo():
    # Create a MongoClient instance
    client = MongoClient(host='localhost', port=27017)
    return client


@app.route('/')
def index():
    select_all_queryn = db.select(news)
    newss = conn.execute(select_all_queryn)
    return render_template('index.html', newss=newss)


@app.route("/order", methods=['GET', 'POST'])
def order():
    form = OrderForm()
    orderlist = redis_db.hgetall(user_login)

    pps = []
    for pos in orderlist:
        select_id_query = db.select(products).where(products.columns.id == str(pos, encoding='utf-8'))
        select_id_results = conn.execute(select_id_query)
        seq = []
        for s in select_id_results.fetchall():
            for s1 in s:
                seq.append(s1)
        seq.append(str(orderlist[pos], encoding='utf-8'))
        pps.append(seq)

    return render_template('order.html', form=form, pps=pps)


@app.route("/delorder", methods=["GET", "POST"])
def delorder():
    if request.method == 'POST':
        id_product = request.form['id_product']
        result = "Product removed from order"
        redis_db.hdel(user_login, int(id_product))

        delproduct = []
        select_id_query = db.select(products).where(products.columns.id == id_product)
        select_id_results = conn.execute(select_id_query)
        seq = []
        for s in select_id_results.fetchall():
            for s1 in s:
                delproduct.append(s1)

    DelOrderForms = DelOrderForm()
    return render_template('delorder.html', delproduct=delproduct, result=result,
                           DelOrderForms=DelOrderForms)


@app.route("/addorder", methods=["GET", "POST"])
def addorder():
    if request.method == 'POST':
        countproduct = request.form['count']
        id_product = request.form['id_product']
        result = "Product added to cart"
        if redis_db.hget(user_login, id_product):
            result = "Previously added product information has been updated"
            redis_db.hset(user_login, id_product, countproduct)
        else:
            redis_db.hset(user_login, id_product, countproduct)

        addproduct = []
        select_id_query = db.select(products).where(products.columns.id == id_product)
        select_id_results = conn.execute(select_id_query)
        seq = []
        for s in select_id_results.fetchall():
            for s1 in s:
                addproduct.append(s1)

    AddOrderForms = AddOrderForm()
    return render_template('addorder.html', addproduct=addproduct, countproduct=countproduct, result=result,
                           AddOrderForms=AddOrderForms)


@app.route("/menu", methods=["GET", "POST"])
def menu():
    select_all_query = db.select(products)
    select_all_results = conn.execute(select_all_query)

    menus = []
    for s in select_all_results.fetchall():
        seq = []
        for s1 in s:
            seq.append(s1)
        menus.append(seq)

    fmenus = MenuForm()
    return render_template('menu.html', menus=menus, fmenus=fmenus)


@app.route("/orderinfo", methods=["GET", "POST"])
def orderinfo():
    form = OrderInfoForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('Všechna pole jsou povinná')
            return render_template('orderinfo.html', form=form)
        else:
            return render_template("conforder")
    elif request.method == 'GET':
        return render_template('orderinfo.html', form=form)


@app.route("/saveorder", methods=["GET", "POST"])
def saveorder():
    form = SaveOrderForm()

    if request.method == 'POST':

        orders_cart = redis_db.hgetall(user_login)

        client = get_db_connection_mongo()
        db_mongo = client['Cafe']
        orders_collection = db_mongo['orders']

        pps = []
        for product in orders_cart:
            countproduct = int(orders_cart[product])

            saveproduct = []
            select_id_query = db.select(products).where(products.columns.id == str(product, encoding='utf-8'))
            select_id_results = conn.execute(select_id_query)
            seq = []
            for s in select_id_results.fetchall():
                for s1 in s:
                    saveproduct.append(s1)

            pps.append({'product_id': saveproduct[0], 'quantity': countproduct, 'img': saveproduct[3],
                        'name': saveproduct[1], 'price': int(saveproduct[2])})

        order_list = {
            'first_name': request.form['orderfirstname'],
            'last_name': request.form['orderlastname'],
            'user_login': user_login,
            'number_order': '#2023001',
            'date_order': datetime.now(),
            'products': pps
        }

        orders_collection.insert_one(order_list)

        redis_db.delete(user_login)
        client.close()

    return render_template('saveorder.html', form=form)


@app.route("/reservation", methods=["GET", "POST"])
def reservation():
    form = ReservationForm()

    if request.method == 'POST':
        client = get_db_connection_mongo()
        db_mongo = client['Cafe']
        reservation_collection = db_mongo['reservations']

        if form.validate() == False:
            flash('Všechna pole jsou povinná')
            return render_template('reservation.html', form=form)
        else:
            reservation_list = {
                'first_name': form.firstname.data,
                'last_name': form.lastname.data,
                'phone_number': form.phone.data,
                'email': form.email.data,
                'guests': form.guest.data,
            }
            reservation_collection.insert_one(reservation_list)
            client.close()
        return render_template('conf.html')

    elif request.method == 'GET':
        return render_template('reservation.html', form=form)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
