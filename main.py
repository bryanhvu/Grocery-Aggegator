#TODO Implement web scraper to retrieve product pricing from specified retailer websites
from bs4 import BeautifulSoup
import requests
import lxml
import re
import json

#TODO Krogers

# requires authorization and probably use of their API
#debug url
# kroger_url = "https://www.kroger.com/p/sprite-lemon-lime-soda/0004900002892?fulfillment=PICKUP&searchType=default_search"

# response = requests.get(kroger_url)
# kroger_soup = BeautifulSoup(response.content, "lxml")

# print(kroger_soup)

#debug url's
tt_url = "https://www.tomthumb.com/shop/product-details.188260007.html"
url2 = "https://www.tomthumb.com/shop/product-details.188020017.html"

tt_response = requests.get(tt_url)
tt_soup = BeautifulSoup(tt_response.content, "lxml")
tt_price = float(json.loads(tt_soup.findAll(text=re.compile('price'))[-1])['offers']['price'])
# print(tt_price)


#TODO Setup SQLite and PostgreSQL database with SQLAlchemy to store products

#TODO Design REST API to handle adding, deleting, and updating product database

#TODO Display basic webpages with product data

#TODO Include tag metadata in database to allow filtering/sorting products in webpage

#TODO Run webscraper daily to routinely update product pricing

#TODO Compile comprehensive list of relevant products in database

#TODO Beautify HTML and CSS

#TODO Deploy website with Heroku