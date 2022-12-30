from flask import Flask, render_template, redirect
from utilities import *
from flask_mobility import Mobility
import regex as re
import math

# footer links
footer_country_code = {'australia': 'aus',
                       'unitedstates': 'usa', 'canada': 'can', 'greatbritain': 'gbr'}


# folders to work with
controller = data()
categories = None
localities = None
states = None
country = None
product_with_categories = None
blogs = None

# flask app name
app = Flask(__name__)
Mobility(app)


def update_var(new_country):
    global product_with_categories, localities, categories, country, states
    if (country == None or country != new_country):
        country = new_country
        # during setting country, we get all the data from small products file as wel. self.products is set now.
        controller.setCountry(new_country)
        # categories were already set. We are just fetching it now.
        categories = controller.categories
        # getting products group by category will -> should give {'category_name': [list of products]}
        product_with_categories = controller.getProductsGroupByCategory()
        states, localities = controller.findLocalities(new_country)


@ app.route('/', methods=['GET', 'POST'])
@ app.route('/<country>/', methods=['GET', 'POST'])
@ app.route('/<country>/<restArea>/', methods=['GET', 'POST'])
def index(country=None, restArea=None):
    if (not country):
        country = 'unitedstates'
    update_var(country)
    global product_with_categories, localities, categories, states

    if (restArea):
        name, img_file = controller.getFlag(country, ' '.join(
            re.split('(?<=.)(?=[A-Z])', restArea.split('-')[0])))
    else:
        name, img_file = controller.getFlag(country)

    return render_template('web/pages/home.html', footer_country_code=footer_country_code[country], categories=categories, productsGroupByCategory=product_with_categories, country=country, restArea=restArea, localities=localities, states=states, flag_data=(name, img_file))


# Admin Panel Page
@ app.route('/admin/kapilsingla/268468', methods=['GET', 'POST'])
def admin():
    return render_template('web/pages/admin.html')


# index page with country name
@ app.route('/<country>/<restArea>/shop', methods=['GET', 'POST'])
@ app.route('/<country>/shop', methods=['GET', 'POST'])
def country(country, restArea=None):
    update_var(country)
    global product_with_categories, localities, categories, all_products, controller

    if (restArea):
        name, img_file = controller.getFlag(country, ' '.join(
            re.split('(?<=.)(?=[A-Z])', restArea.split('-')[0])))
    else:
        name, img_file = controller.getFlag(country)

    return render_template('web/pages/index.html', footer_country_code=footer_country_code[country], categories=categories, productsGroupByCategory=product_with_categories, country=country, localities=localities, restArea=restArea, flag_data=(name, img_file))


# about us page
@ app.route('/<country>/<restArea>/products', methods=['GET', 'POST'])
@ app.route('/<country>/products', methods=['GET', 'POST'])
def shop(country, restArea=None):
    update_var(country)
    global product_with_categories, localities, categories
    return render_template('web/pages/shop.html', footer_country_code=footer_country_code[country], categories=categories, productsGroupByCategory=product_with_categories, country=country, localities=localities, restArea=restArea)


# blog page
@ app.route('/<country>/<restArea>/blogs', methods=['GET', 'POST'])
@ app.route('/<country>/blogs', methods=['GET', 'POST'])
def blogs(country, restArea=None):
    update_var(country)
    global localities, product_with_categories, blogs
    if (localities == None):
        localities = controller.findLocalities(country)

    blogs = controller.getBlogs()

    blog_categories = []
    for blog_id in blogs.keys():
        for category in blogs[blog_id]['Categories'].split(','):
            if (category not in blog_categories):
                blog_categories.append(category)

    if ('Uncategorized' in blog_categories):
        blog_categories.remove('Uncategorized')

    return render_template('web/pages/blogs.html', blog_categories=blog_categories, blogs=blogs, footer_country_code=footer_country_code[country], country=country, localities=localities, restArea=restArea, productsGroupByCategory=product_with_categories)


# blog details page
@ app.route('/<country>/<restArea>/blog-details/<id>', methods=['GET', 'POST'])
@ app.route('/<country>/blog-details/<id>', methods=['GET', 'POST'])
def blogDetails(country, id, restArea=None):
    update_var(country)
    global localities, product_with_categories, blogs
    if (localities == None):
        localities = controller.findLocalities(country)

    blogs = controller.getBlogs()
    id = int(id)

    return render_template('web/pages/blog-details.html', blog=blogs[id], footer_country_code=footer_country_code[country], country=country, localities=localities, restArea=restArea, productsGroupByCategory=product_with_categories)

# good thing found for using python functions in templates


@app.context_processor
def utility_processor():
    return dict(str=str)

# product details page


@ app.route('/<country>/<restArea>/product/<category>/<name>', methods=['GET', 'POST'])
@ app.route('/<country>/product/<category>/<name>', methods=['GET', 'POST'])
def productDetails(country, name, category, restArea=None):
    update_var(country)
    global product_with_categories, localities, categories
    product = controller.getProduct_with_name(name)

    category = ' '.join(category.split('-')).title()

    if (product):
        product = product[0]

        return render_template('web/pages/single-product.html', product=product, product_tags=product[14].split(','), country=country, productsGroupByCategory=product_with_categories, product_category=category, localities=localities, restArea=restArea)
    else:
        return redirect(url_for('country', footer_country_code=footer_country_code[country], country=country, restArea=restArea), code=302)


if __name__ == '__main__':
    app.run(debug=True)
