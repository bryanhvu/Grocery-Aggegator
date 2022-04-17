#TODO Implement web scraper to retrieve product pricing from specified retailer websites
import requests
import lxml
import re
import json
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#TODO Krogers

# requires authorization and probably use of their API
#debug url
# kroger_url = "https://www.kroger.com/p/sprite-lemon-lime-soda/0004900002892?fulfillment=PICKUP&searchType=default_search"

# response = requests.get(kroger_url)
# kroger_soup = BeautifulSoup(response.content, "lxml")

# print(kroger_soup)

app = Flask(__name__)

#TODO Setup PostgreSQL database to use when deployed with Heroku
# make SQLite default for local testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#TODO add unit price
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(250), nullable=False)
    store = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(500), unique=True, nullable=False)
    img = db.Column(db.String(500), unique=True)


db.create_all()


# display database results (manipulate index.html)
@app.route("/", methods=["GET", "POST"])
def home():
    #GET
    all_products = Product.query.all()
    stores = []
    categories = []

    for product in all_products:
        if product.store not in stores:
            stores.append(product.store)
        if product.category not in categories:
            categories.append(product.category)

    if request.method == "POST":
        select_stores = request.form.getlist('stores')
        select_categories = request.form.getlist('categories')
        price_sorting = request.form.get('price-sorting')
        select_products = []

        for product in all_products:
            if select_stores and select_categories:
                if product.store in select_stores and product.category in select_categories:
                    select_products.append(product)
            elif select_stores and product.store in select_stores:
                select_products.append(product)
            elif select_categories and product.category in select_categories:
                select_products.append(product)
        if price_sorting == "Ascending":
            select_products.sort(key=lambda x: x.price)
        elif price_sorting == "Descending":
            # select_products = sorted(select_products, key=product.price, reverse=True)
            select_products.sort(key=lambda x: x.price, reverse=True)
        # TODO add unit price to Product class and scrape and process it
        # comparing unit price for meat
        elif select_categories.count("meat") == len(select_categories):
            if price_sorting == "Ascending-Unit-Price":
                pass
            if price_sorting == "Descending-Unit-Price":
                pass

        return render_template("index.html", products=select_products, stores=stores, categories=categories)
    else:
        return render_template("index.html", products=all_products, stores=stores, categories=categories)


@app.route("/update-products", methods=["GET"])
def update_products():
    """Update product price and image."""
    for product in Product.query.all():
        response = requests.get(product.url)
        soup = BeautifulSoup(response.content, "lxml")
        if product.store.title() == "Tom Thumb":
            product.price = (json.loads(soup.findAll(text=re.compile('price'))[-1])['offers']['price'])
            product.img = soup.find("img", {"alt": product.name})["src"]
            db.session.commit()
        # add more after including more stores

    return redirect(url_for("home"))


# @app.route("/update-price/<int:product_id>", methods=["PATCH"])
# def patch_new_price(product_id):
#     pass


@app.route("/remove-product/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    pass




#TODO Display basic webpages with product data

#TODO Include tag metadata in database to allow filtering/sorting products in webpage

if __name__ == '__main__':
    app.run(debug=True)

#TODO Run webscraper daily to routinely update product pricing

#TODO Compile comprehensive list of relevant products in database

#TODO Beautify HTML and CSS

#TODO Deploy website with Heroku