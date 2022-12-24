from flask import Flask, render_template
from utilities import *

# folders to work with
controller = data()
all_products = None
categories = None
localities = None
product_with_categories = None

# flask app name
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    global all_products, categories
    country = 'unitedstates'
    controller.setCountry(country)
    categories = controller.getCategories()
    localities = controller.findLocalities(country)
    product_with_categories = controller.getProductsGroupByCategory()
    return render_template('pages/index.html', categories=categories, productsGroupByCategory=product_with_categories, country=country, localities=localities)


# index page with country name
@ app.route('/home/<country>', methods=['GET', 'POST'])
@ app.route('/home/<country>/<restArea>', methods=['GET', 'POST'])
def country(country, restArea=None):
    controller.setCountry(country)
    return render_template('pages/index.html', categories=categories, country=country, localities=localities, restArea=restArea)


# shop page
@ app.route('/<country>/<restArea>/shop', methods=['GET', 'POST'])
@ app.route('/<country>/shop', methods=['GET', 'POST'])
def shop(country, restArea=None):
    global all_products
    return render_template('pages/shop.html', categories=categories, products=all_products, country=country, localities=localities, restArea=restArea)


# blog page
@ app.route('/<country>/<restArea>/blogs', methods=['GET', 'POST'])
@ app.route('/<country>/blogs', methods=['GET', 'POST'])
def blogs(country, restArea=None):
    return render_template('pages/blogs.html', country=country, localities=localities, restArea=restArea)


# blog page
@ app.route('/<country>/<restArea>/blog-details', methods=['GET', 'POST'])
@ app.route('/<country>/blog-details', methods=['GET', 'POST'])
def blogDetails(country, restArea=None):
    return render_template('pages/blog-details.html', country=country, localities=localities, restArea=restArea)


# product details
@ app.route('/<country>/<restArea>/product/details/<int:id>', methods=['GET', 'POST'])
@ app.route('/<country>/product/details/<int:id>', methods=['GET', 'POST'])
def productDetails(country, id, restArea=None):
    return render_template('pages/single-product.html', country=country, all_products=all_products, localities=localities, restArea=restArea, id=id)


if __name__ == '__main__':
    app.run(debug=True)
