from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from utilities import *
import os

# folders to work with 
countries_folder = os.path.join('static', 'data', 'countries')
countries_folder = os.path.join('static', 'data', 'products')
images_folder = os.path.join('static', 'images')
countries = ['AU', 'US', 'CA', 'GB']
controller = data()
all_products = None

# flask app name 
app = Flask(__name__)
app.config['IMAGE_FOLDER'] = images_folder
app.config['COUNTRY_FOLDER'] = countries_folder

# allowed data file extensions
ALLOWED_EXTENSIONS = {'csv'}

# index page
@app.route('/', methods=['GET', 'POST'])
def index():
    global all_products
    country = 'unitedstates'
    controller.setCountry(country)
    all_products = controller.getProducts()
    
    return render_template('pages/index.html', categories=controller.getCategories(), products = all_products, productsGroupByCategory = controller.getProductsGroupByCategory(), country=country, localities = controller.findLocalities(country))

# index page with country name
@app.route('/country/<country>', methods=['GET', 'POST'])
@app.route('/country/<country>/<restArea>', methods=['GET', 'POST'])
def country(country, restArea = None):
    global all_products
    controller.setCountry(country)
    all_products = controller.getProducts()
    
    return render_template('pages/index.html', categories=controller.getCategories(), products = all_products, productsGroupByCategory = controller.getProductsGroupByCategory(), country=country, localities = controller.findLocalities(country))

# shop page
@app.route('/<country>/shop', methods=['GET', 'POST'])
def shop(country):
    global all_products
    return render_template('pages/shop.html', categories=controller.getCategories(), products=all_products, country=country, localities = controller.findLocalities(country))


# blog page
@app.route('/<country>/blogs', methods=['GET', 'POST'])
def blogs(country):
    return render_template('pages/blogs.html',country=country , localities = controller.findLocalities(country))


# blog page
@app.route('/<country>/blog-details', methods=['GET', 'POST'])
def blogDetails(country):
    return render_template('pages/blog-details.html',country=country , localities = controller.findLocalities(country))


# product details
@app.route('/<country>/product/details/<int:id>', methods=['GET', 'POST'])
def productDetails(country, id):
    print('Category:', all_products[id][10])
    print('Items:', len(controller.getProductsWithCategory(category=all_products[id][10])))
    return render_template('pages/single-product.html', country=country, product = all_products[id], similar_products = controller.getProductsWithCategory(category=all_products[id][10]), all_products=all_products, localities = controller.findLocalities(country))


if __name__ == '__main__':
    app.run(debug=True)
