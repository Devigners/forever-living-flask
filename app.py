import os
from flask import Flask, render_template, redirect, url_for, request, Markup
from utilities import *
from flask_mobility import Mobility
import regex as re
import math
import sqlalchemy as db
import dotenv
dotenv.load_dotenv()

# footer links
footer_country_code = {'australia': 'aus',
                       'unitedstates': 'usa', 'canada': 'can', 'greatbritain': 'gbr'}

title_country = {'australia': 'Australia',
                 'unitedstates': 'UnitedStates', 'canada': 'Canada', 'greatbritain': 'GreatBritain'}

character_limit_title_country = {'Australia': 'Australia',
                                 'United States': 'USA', 'Great Britain': 'UK', 'Canada': 'Canada'}

country_specific = {
    'usa': {
        'shipping': 'https://thealoeveraco.shop/jfYACnZc',
        '5%_off': 'https://thealoeveraco.shop/HEYrCuwo',
        '10%_off': 'https://thealoeveraco.shop/QIunDW3C',
        '15%_off': 'https://thealoeveraco.shop/wbQW2rEH',
        'phone': '+1 888 440 2563',
        'home': 'https://cdn.foreverliving.com/content/products/images/start_your_journey_pak_pd_main_512_X_512_1569428747899.png',
        'content': '• 12 pack of 330mL aloe vera gel minis • Forever ARGI+ • Forever Lemon and Lavender Essential Oils • Forever Arctic Sea • Forever Active Pro-B • Aloe Vera Gelly • Aloe Heat Lotion • Aloe Propolis Creme • Aloe Moisturizing Lotion • Aloe Liquid Soap • Forever Aloe Scrub • Forever Bright Toothgel • Aloe Lips • English Product Catalog • Aloe as Nature Intended (single) • Why Forever Value Pak'.upper()
    },
    'gbr': {
        '5%_off': 'https://thealoeveraco.shop/ZHJSRv5m',
        '10%_off': 'https://thealoeveraco.shop/WOVGEHb8',
        '15%_off': 'https://thealoeveraco.shop/7MV6ZkIG',
        'phone': '+44 1926 626 629',
        'home': 'https://cdn.foreverliving.com/content/products/images/start_your_journey_pack_pd_main_512_X_512_1664568997643.jpg',
        'content': '• Forever Aloe Vera Gel x 2 • Forever Aloe Berry Nectar x 2 • Forever Bright Toothgel x 2 • Aloe Ever-Shield Deodorant x 2 • Aloe Propolis Crème x 2 • Aloe Vera Gelly x 2 • Aloe Lips x 2 • Forever Lite Ultra – 15 serving pouch – Vanilla x 2 • Aloe Moisturising Lotion x 2 • Avocado Face & Body Soap x 2 • Aloe Shot Glass x 1 • Receipt Pad x 1 • Product Brochure x 1 • FBO Order form x 1 • First Steps to Manager Brochure x 1 • Aloe Flyer x 10 • Welcome Booklet x 1 • Eagle Pin x 1 • Product Manual x 1 • DSA Earnings Opportunities x 1 • DSA Shopping at home x 1 • Document Case • Product Information Flyer A5 x 10 • Business Information Flyer A5 x 10 • Contact Marketing Cards A6 folded x 25 • Collagen Flyer x 1 • Price List x 1'.upper()
    },
    'can': {
        '5%_off': 'https://thealoeveraco.shop/fTvVBTAm',
        '10%_off': 'https://thealoeveraco.shop/J0527gGp',
        '15%_off': 'https://thealoeveraco.shop/DLolWip7',
        'phone': '+1 888 440 2563',
        'home': 'https://cdn.foreverliving.com/content/products/images/start_your_journey_pak_pd_main_512_X_512_1569434726154.png',
        'content': '• Forever Lite Ultra Vanilla • Aloe Lips (2) • Forever Bright (2) • Propolis Crème (2) • Aloe Vera Gelly (2) • Moisturizing Lotion (2) • Aloe Heat Lotion (2) • Ever Shield • Aloe MSM Gel • Aloe Scrub • Arctic Sea • Forever Active PRO-B • Jojoba Shampoo • Jojoba Conditioning Rinse • Aloe Liquid Soap Soap • Aloe Vera Gel (2) • Aloe Berry Nectar • Why Forever (Single) • Aloe Brochure • Product Brochure'.upper()
    },
    'aus': {
        '5%_off': 'https://thealoeveraco.shop/m1m6hsyO',
        '10%_off': 'https://thealoeveraco.shop/1QLH7Eh9',
        '15%_off': 'https://thealoeveraco.shop/i2Y5dJzQ',
        'phone': '+61 2 9635 3011',
        'home': 'https://cdn.foreverliving.com/content/products/images/syj_c9_combo_pack_pd_main_512_X_512_1656638991235.jpg',
        'content': Markup('C9 Combo Pack 1: • ALOE VERA GEL - 1LTR x2 • FOREVER LITE POUCH - VANILLA x 1 • FOREVER FIBER x1 • GARCINIA PLUS x 1 • THERM x 1<br>C9 Combo Pack 2: • ALOE VERA GEL - 1LTR x2 • FOREVER LITE POUCH - CHOCOLATE x 1 • FOREVER FIBER x1 • GARCINIA PLUS x 1 • THERM x 1'.upper())
    }
}

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

# flask integration with database
engine = db.create_engine(os.environ.get("MONGO_DB_URI"))
connection = engine.connect()
metadata = db.MetaData()

# fetching cards data from Mysql Database
census = db.Table('cards', metadata, autoload=True, autoload_with=engine)
columns = census.columns.keys()
query = db.select([census])
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()

cards = {}
for set in ResultSet:
    cards[set[1]] = {}
    for col in columns:
        cards[set[1]][col] = set[columns.index(col)]


@app.context_processor
def utility_processor():
    return dict(str=str, len=len)


def update_var(new_country, restArea=None):
    global product_with_categories, localities, categories, country, states, country_specific
    if (country == None or country != new_country):
        country = new_country
        # during setting country, we get all the data from small products file as wel. self.products is set now.
        controller.setCountry(new_country)
        # categories were already set. We are just fetching it now.
        categories = controller.categories
        # getting products group by category will -> should give {'category_name': [list of products]}
        product_with_categories = controller.getProductsGroupByCategory()

    states, localities = controller.findLocalities(new_country, restArea)


@app.route('/', methods=['GET', 'POST'])
@app.route('/<country>/', methods=['GET', 'POST'])
@app.route('/<country>/<restArea>/', methods=['GET', 'POST'])
def index(country=None, restArea=None):
    pageType = 'index'
    address = []
    if (not country):
        country = 'unitedstates'
    else:
        pageType = 'country'

    state_of_restArea = None
    if (restArea):
        pageType = 'state'
        if ('-' in restArea):
            pageType = 'restarea'

        state_of_restArea = " ".join(l for l in re.findall(
            '[A-Z][^A-Z]*', restArea.split('-')[0]))

    # updating var if we don't get any error
    # else we are going to redirect to index page
    try:
        update_var(country, state_of_restArea)
    except:
        return redirect(url_for('index'))

    global product_with_categories, localities, categories, states, country_specific, cards, footer_country_code

    # getting flag data from the controller
    # creating address of the place we are
    address.append(title_country[country])
    if (restArea):
        name, img_file = controller.getFlag(country, state_of_restArea)
        address.extend(restArea.split('-'))
    else:
        name, img_file = controller.getFlag(country)

    # showing the address in the correct format on the homepage
    address = [" ".join(l for l in re.findall(
        '[A-Z][^A-Z]*', i.split('-')[0])) for i in address]

    # sending following information to the template page
    context = {
        'pageType': pageType,
        'offer_cards': cards,
        'footer_country_code': footer_country_code[country],
        'categories': categories,
        'productsGroupByCategory': product_with_categories,
        'localities': localities,
        'states': states,
        'flag_data': (name, img_file),
        'title_country': title_country,
        'offer_links': country_specific,
        'country': country,
        'state_of_restArea': state_of_restArea,
        'restArea': restArea,
        'address': address,
        'character_limit_title_country': character_limit_title_country
    }

    return render_template('web/pages/home.html', **context)


# index page with country name
@app.route('/<country>/<restArea>/shop', methods=['GET', 'POST'])
@app.route('/<country>/shop', methods=['GET', 'POST'])
def country(country, restArea=None):
    update_var(country)
    global product_with_categories, localities, categories, all_products, controller, country_specific, cards

    if (restArea):
        name, img_file = controller.getFlag(country, ' '.join(
            re.split('(?<=.)(?=[A-Z])', restArea.split('-')[0])))
    else:
        name, img_file = controller.getFlag(country)

    context = {
        'offer_links': country_specific,
        'offer_cards': cards,
        'footer_country_code': footer_country_code[country],
        'categories': categories,
        'productsGroupByCategory': product_with_categories,
        'country': country,
        'localities': localities,
        'restArea': restArea,
        'title_country': title_country,
        'flag_data': (name, img_file)
    }
    return render_template('web/pages/index.html', **context)


# about us page
@app.route('/<country>/<restArea>/products', methods=['GET', 'POST'])
@app.route('/<country>/products', methods=['GET', 'POST'])
def shop(country, restArea=None):
    update_var(country)
    global product_with_categories, localities, categories, country_specific, cards, title_country

    if (restArea):
        name, img_file = controller.getFlag(country, ' '.join(
            re.split('(?<=.)(?=[A-Z])', restArea.split('-')[0])))
    else:
        name, img_file = controller.getFlag(country)

    context = {
        'offer_links': country_specific,
        'offer_cards': cards,
        'footer_country_code': footer_country_code[country],
        'categories': categories,
        'productsGroupByCategory': product_with_categories,
        'country': country,
        'localities': localities,
        'restArea': restArea,
        'flag_data': (name, img_file),
        'title_country': title_country
    }

    return render_template('web/pages/shop.html', **context)


# blog page
@app.route('/<country>/<restArea>/blogs', methods=['GET', 'POST'])
@app.route('/<country>/blogs', methods=['GET', 'POST'])
def blogs(country, restArea=None):
    update_var(country)
    global localities, product_with_categories, blogs, country_specific, cards
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

    context = {
        'offer_links': country_specific,
        'blog_categories': blog_categories,
        'offer_cards': cards,
        'blogs': blogs,
        'footer_country_code': footer_country_code[country],
        'country': country,
        'localities': localities,
        'restArea': restArea,
        'productsGroupByCategory': product_with_categories,
        'title_country': title_country
    }

    return render_template('web/pages/blogs.html', **context)


# blog details page
@app.route('/<country>/<restArea>/blog-details/<id>', methods=['GET', 'POST'])
@app.route('/<country>/blog-details/<id>', methods=['GET', 'POST'])
def blogDetails(country, id, restArea=None):
    update_var(country)
    global localities, product_with_categories, blogs, country_specific, cards
    if (localities == None):
        localities = controller.findLocalities(country)

    blogs = controller.getBlogs()
    id = int(id)

    context = {
        'id': id,
        'offer_links': country_specific,
        'blog': blogs[id],
        'footer_country_code': footer_country_code[country],
        'country': country,
        'offer_cards': cards,
        'localities': localities,
        'restArea': restArea,
        'productsGroupByCategory': product_with_categories,
        'title_country': title_country
    }

    return render_template('web/pages/blog-details.html', **context)


# product details page
@app.route('/<country>/<restArea>/product/<category>/<name>', methods=['GET', 'POST'])
@app.route('/<country>/product/<category>/<name>', methods=['GET', 'POST'])
def productDetails(country, name, category, restArea=None):
    original_category = category
    update_var(country)
    global product_with_categories, localities, categories, country_specific, cards
    product = controller.getProduct_with_name(name)

    category = ' '.join(category.split('-')).title()

    if (product):
        product = product[0]

        if (category not in categories):
            category = 'All Products'

        for i in range(len(product)):
            print(i, ": ", product[i])

        context = {
            'offer_links': country_specific,
            'footer_country_code': footer_country_code[country],
            'product_tags': product[14].split(','),
            'country': country,
            'name': name,
            'productsGroupByCategory': product_with_categories,
            'offer_cards': cards,
            'product_category': category,
            'category': original_category,
            'localities': localities,
            'restArea': restArea,
            'product': product,
            'title_country': title_country
        }
        return render_template('web/pages/single-product.html', **context)
    else:
        return redirect(url_for('country', country=country, restArea=restArea), code=302)


@app.route('/admin/dashboard/<name>/<password>', methods=['GET', 'POST'])
def adminDashboard(name=None, password=None):
    if (name == 'kapilsingla' and password == '268468'):
        global db, cards, census, connection
        if request.method == 'POST':

            needed_columns = {
                'discount': ['discount', 'validUntil', 'vUnitedStates', 'lUnitedStates', 'vGreatBritain', 'lGreatBritain', 'vAustralia', 'lAustralia', 'vCanada', 'lCanada'],
                'shipping': ['vUnitedStates', 'lUnitedStates'],
                'visit': ['vUnitedStates', 'lUnitedStates', 'vGreatBritain', 'lGreatBritain', 'vAustralia', 'lAustralia', 'vCanada', 'lCanada'],
                'join': ['vUnitedStates', 'lUnitedStates', 'vGreatBritain', 'lGreatBritain', 'vAustralia', 'lAustralia', 'vCanada', 'lCanada']
            }

            data_dict = {}
            card = request.form.get('cardType')

            data_dict[card] = {}
            for form_field in needed_columns[card]:

                if (form_field.startswith('v') and not form_field.startswith('va')):
                    data_dict[card][form_field] = 1 if request.form.get(
                        card+'_'+form_field) == 'on' else 0
                else:
                    data_dict[card][form_field] = request.form.get(
                        card+'_'+form_field)

            # updating database entry
            engine = db.create_engine(os.environ.get("MONGO_DB_URI"))
            connection = engine.connect()
            metadata = db.MetaData()

            # fetching cards data from Mysql Database
            census = db.Table('cards', metadata,
                              autoload=True, autoload_with=engine)
            query = db.update(census).where(
                census.columns.cardType == card).values(data_dict[card])
            results = connection.execute(query)

        engine = db.create_engine(os.environ.get("MONGO_DB_URI"))
        connection = engine.connect()
        metadata = db.MetaData()

        # fetching cards data from Mysql Database
        census = db.Table('cards', metadata, autoload=True,
                          autoload_with=engine)
        columns = census.columns.keys()
        query = db.select([census])
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchall()

        cards = {}
        for set in ResultSet:
            cards[set[1]] = {}
            for col in columns:
                cards[set[1]][col] = set[columns.index(col)]

        cards = {}
        for set in ResultSet:
            cards[set[1]] = {}
            for col in columns:
                cards[set[1]][col] = set[columns.index(col)]

        context = {
            'name': name,
            'password': password,
            'cards': cards
        }

        return render_template('admin/pages/dashboard.html', **context)
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    # app.run(host='192.168.1.215')
    app.run(debug=True)
