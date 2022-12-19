from os import listdir
import pandas as pd

needed_columns = ['Image', 'post_title', 'Price', 'Description', 'Usage', 'quantities', 'Ingredients', 'Tags', 'review_stars', 'Original URL', 'aus_categories']
products = pd.read_csv('static/data/products/forever_products_en_au.csv')
products['review_stars'].fillna(0.0, inplace = True)
products['total_reviews'].fillna('', inplace = True)
products['quantities'].fillna('', inplace = True)
products['Usage'].fillna('', inplace = True)

locality_dict = {}

def getCategories():
    return list(set(products['aus_categories'].to_list()))

def getProductsCards(return_list=True):
    if(return_list):
        return products[['Image', 'post_title', 'Price']].values.tolist()
    else:
        return products[['Image', 'post_title', 'Price']]

def getProducts(return_list=True):
    if(return_list):
        return products[needed_columns].values.tolist()
    else:
        return products[needed_columns]

def getProductsWithCategory(category, return_list=True):
    specific_category_products = products[products['aus_categories'] == category]
    if(return_list):
        return specific_category_products[needed_columns].values.tolist()
    else:
        return specific_category_products[needed_columns]

def getProductsGroupByCategory():
    category_json = {}
    for category in getCategories():
        category_json[category] = getProductsWithCategory(category)
    return category_json

def findLocalities(required_country = 'unitedstates'):
    countries_codes = {'australia': 'AU', 'unitedstates':'US', 'canada':'CA', 'great britain':'GB'}
    required_country_code = countries_codes[required_country]
    data = pd.read_csv('static\\data\\countries\\'+required_country_code+' data.csv').values.tolist()

    localities = []
    for row in data:
        entry = []
        for item in row:
            if isinstance(item, str):
                entry.append(item)
        localities.append(entry)

    country_localities = []
    for locality in localities:
        # add your search url here
        country_localities.append({'name': ', '.join(locality), 'url': '#'})
    
    return country_localities