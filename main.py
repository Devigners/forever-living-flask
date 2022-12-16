from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

# folders to work with 
countries_folder = os.path.join('static', 'data', 'countries')
countries_folder = os.path.join('static', 'data', 'products')
images_folder = os.path.join('static', 'images')
countries = ['AU', 'US', 'CA', 'GB']

# flask app name 
app = Flask(__name__)
app.config['IMAGE_FOLDER'] = images_folder
app.config['COUNTRY_FOLDER'] = countries_folder

# allowed data file extensions
ALLOWED_EXTENSIONS = {'csv'}

# index page
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('pages/index.html')


# shop page
@app.route('/shop', methods=['GET', 'POST'])
def shop():
    return render_template('pages/shop.html')


# blog page
@app.route('/blogs', methods=['GET', 'POST'])
def blogs():
    return render_template('pages/blogs.html')


# blog page
@app.route('/blog-details', methods=['GET', 'POST'])
def blogDetails():
    return render_template('pages/blog-details.html')


# product details
@app.route('/product/details', methods=['GET', 'POST'])
def productDetails():
    return render_template('pages/single-product.html')


if __name__ == '__main__':
    app.run(debug=True)
