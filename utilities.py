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

    def setCountry(self, country):
        self.country = country
        self.needed_columns = ['Image', 'post_title', 'Price', 'Description', 'Usage', 'quantities',
                               'Ingredients', 'Tags', 'review_stars', 'affiliate_link',
                               self.country_categoryNames[self.country],
                               'SKU', 'short_description', 'total_reviews']
        self.products = pd.read_csv(
            'static/data/products/forever_products_en_'+self.country_code[self.country]+'.csv')
        self.products['review_stars'].fillna(0.0, inplace=True)
        self.products['total_reviews'].fillna('', inplace=True)
        self.products['quantities'].fillna('', inplace=True)
        self.products['Usage'].fillna('', inplace=True)
        self.categories = self.getCategories()

    def getCountry(self):
        return self.country

    def getCategories(self):
        with open('static/data/products/categories.json') as json_file:
            data = json.load(json_file)
        return data[self.country_code[self.country]]

    def getProduct_with_name(self, name, return_list=True):
        all_products = self.getProducts(return_list=False)

        if (return_list):
            return all_products[all_products['post_title'] == name].values.tolist()
        else:
            return all_products[all_products['post_title'] == name]

    def getProducts(self, return_list=True):
        if (return_list):
            return self.products[self.needed_columns].values.tolist()
        else:
            return self.products[self.needed_columns]

    def getProductsWithCategory(self, category, return_list=True):
        specific_category_products = self.products[self.products[
            self.country_categoryNames[self.country]] == category]
        if (return_list):
            return specific_category_products[self.needed_columns].values.tolist()
        else:
            return specific_category_products[self.needed_columns]

    def getProductsGroupByCategory(self):
        category_json = {}
        for category in self.getCategories():
            category_json[category] = self.getProductsWithCategory(category)
        return category_json

    def findLocalities(self, required_country):
        my_file = open("static/data/countries/" +
                       self.country_code[required_country] + " data.txt", "r")
        data = my_file.read()
        data_into_list = data.split("\n")
        my_file.close()
        return data_into_list
