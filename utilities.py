from flask import url_for
import pandas as pd
import json


class data():
    def __init__(self) -> None:
        self.country = None
        self.needed_columns = None
        self.products = None
        self.country_categoryNames = {'australia': 'aus_categories', 'unitedstates': 'us_categories',
                                      'canada': 'can_categories', 'greatbritain': 'uk_categories'}
        self.country_code = {
            'australia': 'au', 'unitedstates': 'us', 'canada': 'ca', 'greatbritain': 'gb'}
        self.categories = None
        self.category_json = None

    def setCountry(self, country):
        self.country = country
        self.categories = self.getCategories()

        self.needed_columns = ['Image', 'post_title', 'Price', 'Description', 'Usage', 'quantities',
                               'Ingredients', 'Tags', 'review_stars', 'affiliate_link',
                               'SKU', 'short_description', 'total_reviews', 'url_name'] + self.categories

        self.products = pd.read_csv(
            'static/data/products/forever_products_en_'+self.country_code[self.country]+'_small.csv')
        self.products['url_name'] = [
            i.replace(' ', '-') for i in self.products['post_title'].values.tolist()]
        self.products['review_stars'].fillna(0.0, inplace=True)
        self.products['total_reviews'].fillna('', inplace=True)
        self.products['quantities'].fillna('', inplace=True)
        self.products['Usage'].fillna('', inplace=True)

    def getCategories(self):
        with open('static/data/products/categories.json') as json_file:
            data = json.load(json_file)
        return data[self.country_code[self.country]]

    def getProduct_with_name(self, name, return_list=True):
        all_products = self.products
        product = all_products[all_products['url_name'] == name]

        if (len(product.values.tolist()) > 0):
            if (return_list):
                return product.values.tolist()
            else:
                return product
        else:
            return False

    def getProductsWithCategory(self, category, return_list=True):
        specific_category_products = self.products[self.products[category] == 1]

        if (return_list):
            return specific_category_products[self.needed_columns].values.tolist()
        else:
            return specific_category_products[self.needed_columns]

    def getProductsGroupByCategory(self):
        self.category_json = {}
        self.category_json['All Products'] = []
        for category in self.categories:
            prods = self.getProductsWithCategory(category)
            self.category_json[category] = prods
            self.category_json['All Products'].extend(prods)

        return self.category_json

    def findLocalities(self, required_country):
        my_file = open("static/data/countries/" +
                       self.country_code[required_country] + " data.txt", "r")
        data = my_file.read()
        data_into_list = data.split("\n")
        my_file.close()
        return data_into_list
