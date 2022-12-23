from flask import Flask, render_template
from utilities import *

# folders to work with
controller = data()
all_products = None

# flask app name
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    global all_products
    country = 'unitedstates'
    controller.setCountry(country)
    all_products = controller.getProducts()

    return render_template('pages/index.html', categories=controller.getCategories(), products=all_products, productsGroupByCategory=controller.getProductsGroupByCategory(), country=country, localities=controller.findLocalities(country))


# index page with country name


@app.route('/home/<country>', methods=['GET', 'POST'])
@app.route('/home/<country>/<restArea>', methods=['GET', 'POST'])
def country(country, restArea=None):
    global all_products
    controller.setCountry(country)
    return render_template('pages/index.html', categories=controller.getCategories(), products=all_products, productsGroupByCategory=controller.getProductsGroupByCategory(), country=country, localities=controller.findLocalities(country), restArea=restArea)

# shop page


@app.route('/<country>/<restArea>/shop', methods=['GET', 'POST'])
@app.route('/<country>/shop', methods=['GET', 'POST'])
def shop(country, restArea=None):
    global all_products
    return render_template('pages/shop.html', categories=controller.getCategories(), products=all_products, country=country, localities=controller.findLocalities(country), restArea=restArea)


# blog page
@app.route('/<country>/<restArea>/blogs', methods=['GET', 'POST'])
@app.route('/<country>/blogs', methods=['GET', 'POST'])
def blogs(country, restArea=None):
    return render_template('pages/blogs.html', country=country, localities=controller.findLocalities(country), restArea=restArea)


# blog page
@app.route('/<country>/<restArea>/blog-details', methods=['GET', 'POST'])
@app.route('/<country>/blog-details', methods=['GET', 'POST'])
def blogDetails(country, restArea=None):
    return render_template('pages/blog-details.html', country=country, localities=controller.findLocalities(country), restArea=restArea)


# product details
@app.route('/<country>/<restArea>/product/details/<int:id>', methods=['GET', 'POST'])
@app.route('/<country>/product/details/<int:id>', methods=['GET', 'POST'])
def productDetails(country, id, restArea=None):
    print('Category:', all_products[id][10])
    print('Items:', len(controller.getProductsWithCategory(
        category=all_products[id][10])))
    return render_template('pages/single-product.html', country=country, product=all_products[id], product_tags=all_products[id][7].split(','), similar_products=controller.getProductsWithCategory(category=all_products[id][10]), all_products=all_products, localities=controller.findLocalities(country), restArea=restArea)


if __name__ == '__main__':
    app.run(debug=True)
