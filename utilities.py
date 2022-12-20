from flask import Flask, render_template, request, redirect, url_for
from os import listdir
import pandas as pd

class data():
    def __init__(self) -> None:
        self.country = None
        self.needed_columns = None
        self.products = None
        self.country_categoryNames = {'australia': 'aus_categories', 'unitedstates':'us_categories', 'canada':'can_categories', 'greatbritain':'uk_categories'}
        self.country_code = {'australia': 'au', 'unitedstates':'us', 'canada':'ca', 'greatbritain':'GB'}

    def setCountry(self, country):
        self.country = country
        self.needed_columns = ['Image', 'post_title', 'Price', 'Description', 'Usage', 'quantities', 'Ingredients', 'Tags', 'review_stars', 'Original URL', self.country_categoryNames[self.country]]
        self.products = pd.read_csv('static/data/products/forever_products_en_'+self.country_code[self.country]+'.csv')
        self.products['review_stars'].fillna(0.0, inplace = True)
        self.products['total_reviews'].fillna('', inplace = True)
        self.products['quantities'].fillna('', inplace = True)
        self.products['Usage'].fillna('', inplace = True)
    
    def getCountry(self):
        return self.country
    
    def getCategories(self):
        return list(set(self.products[self.country_categoryNames[self.country]].to_list()))

    def getProductsCards(self, return_list=True):
        if(return_list):
            return self.products[['Image', 'post_title', 'Price']].values.tolist()
        else:
            return self.products[['Image', 'post_title', 'Price']]

    def getProducts(self, return_list=True):
        if(return_list):
            return self.products[self.needed_columns].values.tolist()
        else:
            return self.products[self.needed_columns]

    def getProductsWithCategory(self, category, return_list=True):
        specific_category_products = self.products[self.products[self.country_categoryNames[self.country]] == category]
        if(return_list):
            return specific_category_products[self.needed_columns].values.tolist()
        else:
            return specific_category_products[self.needed_columns]

    def getProductsGroupByCategory(self):
        category_json = {}
        for category in self.getCategories():
            category_json[category] = self.getProductsWithCategory(category)
        return category_json

    def findLocalities(self, required_country):
        countries_codes_file = {'australia': 'AU', 'unitedstates':'US', 'canada':'CA', 'greatbritain':'GB'}
        required_country_code = countries_codes_file[required_country]
        data = pd.read_csv('static//data//countries//'+required_country_code+' data.csv').values.tolist()

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
            country_localities.append({'name': ', '.join(locality), 'url': url_for('country', country=required_country, restArea='-'.join([i.replace(' ','') for i in locality]))})
        
        return country_localities