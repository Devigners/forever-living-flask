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

# index page
@app.route('/', methods=['GET', 'POST'])
def index():
    # print( ['https://cdn.foreverliving.com/content/products/images/balancing_toner_pd_main_512_X_512_1617214805533.jpg', 'BALANCING TONER', '$32.84 AUD', 'Supports skin’s pH balance• Refreshes, soothes and hydrates• Smooths skin’s tone and texture• Minimizes the appearance of poresDoes your skin need some extra attention after cleansing? Forever’s balancing toner is designed to ensure all dirt and debris is washed off, while minimizing the appearance of pores and adding extra hydration, making it ideal for use between cleansing and moisturizing.Balancing toner provides an exclusive blend of seaweed extract and sodium hyaluronate to moisturize and soften skin while supporting a youthful appearance. The addition of cucumber extract adds another layer of soothing hydration while promoting improved skin tone and texture, thanks to naturally-occurring lignans.White tea extract is a rich antioxidant with a high polyphenolic content that works with aloe to balance fluctuations of the skin and fight free radicals. To further supercharge this powerful formula, we used hyaluronic acid, which has been called a molecular sponge because of its water attracting abilities.Only the freshest, purest aloe from our own plantations is used in balancing toner to ensure only the finest, most potent ingredients refresh and nourish your skin. Every aloe plant is carefully nurtured, hand harvested and hand filleted to extract only pure, powerful inner-leaf gel.Notice a profound difference in the way you skin looks and feels when you add balancing toner to your routine!', 'Apply a generous amount to face and neck after cleansing using a cotton ball or pad. Use twice daily to minimise the appearance of pores and hydrate skin.', '4.4 FL. OZ. (130 mL)', 'Aloe Barbadensis Leaf Juice (Stabilized Aloe Vera Gel), Water, Propanediol, Sorbitol, 1,2-Hexanediol, Chondrus Crispus Extract, Sodium Hyaluronate, Glycerin, Cucumis Sativus (Cucumber) Fruit Extract, Camellia Sinensis Leaf Extract, Beta Glucan, Sodium Lactate, Phytic Acid, Allantoin, Potassium Sorbate.', 'BALANCINGTONER,SkinCare,FLP,Australia,AUS,ForeverLivingProducts,BuyAloeProducts,BuyAloeProducts.com,AloeVera,AloeVeraProducts,Healthy,Health', nan, 'https://shopnow.foreverliving.com/aus/en-au/products/skin-care/560-BALANCING-TONER', 'Skin Care'] in all_products)
    print(getProductsWithCategory(category='Skin Care'))
    return render_template('pages/index.html', categories=getCategories(), products = getProducts(), skin_care_products = getProductsWithCategory(category='Skin Care'))


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
