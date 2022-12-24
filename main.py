from flask import Flask, render_template
from utilities import *

# folders to work with
controller = data()
categories = None
localities = None
country = None
product_with_categories = None

# flask app name
app = Flask(__name__)


def update_var(new_country):
    global all_products, product_with_categories, localities, categories, country

    if (country == None or country != new_country):
        country = new_country
        controller.setCountry(new_country)
        categories = controller.getCategories()
        product_with_categories = controller.getProductsGroupByCategory()
        localities = controller.findLocalities(new_country)


@app.route('/', methods=['GET', 'POST'])
def index():
    country = 'unitedstates'
    update_var(country)
    global product_with_categories, localities, categories
    return render_template('pages/index.html', categories=categories, productsGroupByCategory=product_with_categories, country=country, localities=localities)


# index page with country name
@ app.route('/home/<country>', methods=['GET', 'POST'])
@ app.route('/home/<country>/<restArea>', methods=['GET', 'POST'])
def country(country, restArea=None):
    update_var(country)
    global product_with_categories, localities, categories
    return render_template('pages/index.html', categories=categories, productsGroupByCategory=product_with_categories, country=country, localities=localities, restArea=restArea)


# shop page
@ app.route('/<country>/<restArea>/shop', methods=['GET', 'POST'])
@ app.route('/<country>/shop', methods=['GET', 'POST'])
def shop(country, restArea=None):
    update_var(country)
    global product_with_categories, localities, categories
    return render_template('pages/shop.html', categories=categories, productsGroupByCategory=product_with_categories, country=country, localities=localities, restArea=restArea)


# blog page
@ app.route('/<country>/<restArea>/blogs', methods=['GET', 'POST'])
@ app.route('/<country>/blogs', methods=['GET', 'POST'])
def blogs(country, restArea=None):
    if (localities == None):
        localities = controller.findLocalities(country)
    return render_template('pages/blogs.html', country=country, localities=localities, restArea=restArea)


# blog page
@ app.route('/<country>/<restArea>/blog-details', methods=['GET', 'POST'])
@ app.route('/<country>/blog-details', methods=['GET', 'POST'])
def blogDetails(country, restArea=None):
    if (localities == None):
        localities = controller.findLocalities(country)
    return render_template('pages/blog-details.html', country=country, localities=localities, restArea=restArea)


# product details
@ app.route('/<country>/<restArea>/product/details/<name>', methods=['GET', 'POST'])
@ app.route('/<country>/product/details/<name>', methods=['GET', 'POST'])
def productDetails(country, name, restArea=None):
    update_var(country)
    global product_with_categories, localities, categories
    product = controller.getProduct_with_name(name)[0]

    return render_template('pages/single-product.html', product=product, country=country, product_with_categories=product_with_categories[categories[0]][:4], localities=localities, restArea=restArea)


if __name__ == '__main__':
    app.run(debug=True)
