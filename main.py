import requests
import lxml
import re
import json
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


#TODO Setup PostgreSQL database to use when deployed with Heroku
# make SQLite default for local testing
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#TODO add unit price
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.String(250))
    category = db.Column(db.String(250), nullable=False)
    store = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(500), unique=True, nullable=False)
    img = db.Column(db.String(500), unique=True)


db.create_all()


# display database results (manipulate index.html)
@app.route("/", methods=["GET", "POST"])
def home():
    all_products = Product.query.all()
    stores = set([product.store for product in all_products])
    categories = set([product.category for product in all_products])

    if request.method == "POST":
        select_products = [product for product in all_products if product.store in request.form.getlist('stores')]
        select_products = [product for product in select_products if product.category in request.form.getlist('categories')]

        sorting = request.form.get('sorting')
        if sorting == "Ascending-Alphabetical":
            select_products.sort(key=lambda x: x.name)
        elif sorting == "Descending-Alphabetical":
            select_products.sort(key=lambda x: x.name, reverse=True)
        elif sorting == "Ascending-Price":
            select_products.sort(key=lambda x: x.price)
        elif sorting == "Descending-Price":
            select_products.sort(key=lambda x: x.price, reverse=True)
        # TODO add unit price to Product class and scrape and process it
        # comparing unit price for meat
        # elif select_categories.count("meat") == len(select_categories):
        #     if price_sorting == "Ascending-Unit-Price":
        #         pass
        #     if price_sorting == "Descending-Unit-Price":
        #         pass

        return render_template("index.html", products=select_products, stores=stores, categories=categories)
    else:
        return render_template("index.html", products=all_products, stores=stores, categories=categories)


@app.route("/update-products", methods=["GET", "POST"])
def update_products():
    """Update product price and image."""
    for product in Product.query.all():
        response = requests.get(product.url)
        soup = BeautifulSoup(response.content, "lxml")
        if product.store.title() == "Tom Thumb":
            product.price = (json.loads(soup.findAll(text=re.compile('price'))[-1])['offers']['price'])
            # product.unit_price = ()
            product.img = soup.find("img", {"alt": product.name})["src"]
            db.session.commit()
    # TODO Add more stores
    # Krogers

    # requires authorization and probably use of their API
    # debug url
    # kroger_url = "https://www.kroger.com/p/sprite-lemon-lime-soda/0004900002892?fulfillment=PICKUP&searchType=default_search"

    # response = requests.get(kroger_url)
    # kroger_soup = BeautifulSoup(response.content, "lxml")

    # print(kroger_soup)

    return redirect(url_for("home"))


@app.route("/remove-product/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    pass


if __name__ == '__main__':
    app.run(debug=True)


#TODO Compile comprehensive list of relevant products in database


#TODO Deploy website with Heroku
