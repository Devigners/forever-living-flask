from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from utilities import *
import os
import random

# folders to work with 
countries_folder = os.path.join('static', 'data', 'countries')
countries_folder = os.path.join('static', 'data', 'products')
images_folder = os.path.join('static', 'images')
countries = ['AU', 'US', 'CA', 'GB']
all_products = getProducts()

# flask app name 
app = Flask(__name__)
app.config['IMAGE_FOLDER'] = images_folder
app.config['COUNTRY_FOLDER'] = countries_folder

# allowed data file extensions
ALLOWED_EXTENSIONS = {'csv'}

# index page with country name
@app.route('/country/<country>', methods=['GET', 'POST'])
def country(country = 'unitedstates'):
    return render_template('pages/index.html', categories=getCategories(), products = all_products, productsGroupByCategory = getProductsGroupByCategory(), country=country, localities = findLocalities(country))

# index page
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('pages/index.html', categories=getCategories(), products = all_products, productsGroupByCategory = getProductsGroupByCategory(), country="unitedstates", localities = findLocalities('unitedstates'))


# shop page
@app.route('/shop', methods=['GET', 'POST'])
def shop():
    return render_template('pages/shop.html', categories=getCategories(), products=all_products)


# blog page
@app.route('/blogs', methods=['GET', 'POST'])
def blogs():
    return render_template('pages/blogs.html')


# blog page
@app.route('/blog-details', methods=['GET', 'POST'])
def blogDetails():
    return render_template('pages/blog-details.html')


# product details
@app.route('/product/details/<int:id>', methods=['GET', 'POST'])
def productDetails(id):
    print('Category:', all_products[id][10])
    print('Items:', len(getProductsWithCategory(category=all_products[id][10])))
    return render_template('pages/single-product.html', product = all_products[id], similar_products = getProductsWithCategory(category=all_products[id][10]), all_products=all_products)


if __name__ == '__main__':
    app.run(debug=True)
