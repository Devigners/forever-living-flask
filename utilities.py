import pandas as pd
import json
import regex as re


class data():
    def __init__(self) -> None:
        self.country = None
        self.needed_columns = None
        self.products = None
        self.country_categoryNames = {'australia': 'aus_categories', 'unitedstates': 'us_categories',
                                      'canada': 'can_categories', 'greatbritain': 'uk_categories'}
        self.country_code = {
            'australia': 'au', 'unitedstates': 'us', 'canada': 'ca', 'greatbritain': 'gb'}

        self.country_fullName = {
            'australia': 'Australia', 'unitedstates': 'United States', 'canada': 'Canada', 'greatbritain': 'Great Britain'}

        self.categories = None
        self.category_json = None

    def removeSpecialChars(self, input_string):
        return re.sub(r'[^a-zA-Z0-9- ]+', '', input_string)

    def setCountry(self, country):
        self.country = country
        self.categories = self.getCategories()

        self.needed_columns = ['Image', 'post_title', 'Price', 'Description', 'Usage', 'quantities',
                               'Ingredients', 'Tags', 'review_stars', 'affiliate_link',
                               'SKU', 'short_description', 'total_reviews', 'url_name', 'canonical_category'] + self.categories

        self.products = pd.read_csv(
            'static/web-assets/data/products/forever_products_en_'+self.country_code[self.country]+'_small_utf.csv')

        # firstly, it removed REGISTERED signs
        self.products['url_name'] = [
            re.sub(r'[ ]+', ' ', self.removeSpecialChars(i).replace('-', ' ').title()).replace(' ', '-') for i in self.products['post_title'].values.tolist()]

        canonical_categories = []
        for product_categories in self.products[self.categories].values.tolist():
            for category_index in range(len(product_categories)):
                if (self.categories[category_index] not in ['New Products', 'Best Sellers'] and product_categories[category_index] == 1):
                    canonical_categories.append(
                        self.categories[category_index].replace(' ', '-'))
                    break

        self.products['canonical_category'] = canonical_categories

        self.products['review_stars'].fillna(0.0, inplace=True)
        self.products['total_reviews'].fillna('', inplace=True)
        self.products['quantities'].fillna('', inplace=True)
        self.products['Usage'].fillna('', inplace=True)

    def getCategories(self):
        with open('static/web-assets/data/products/categories.json') as json_file:
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
            for prod in prods:
                if (prod not in self.category_json['All Products']):
                    self.category_json['All Products'].append(prod)

        return self.category_json

    def findLocalities(self, required_country, restArea=None):
        my_file = open("static/web-assets/data/countries/" +
                       self.country_code[required_country] + " data.txt", "r", encoding='windows-1252')
        data = my_file.read()
        data_into_list = [re.sub(r'[^a-zA-Z0-9-, ]+', '', da)
                          for da in data.split("\n")]

        my_file.close()

        # finding states
        states = []

        if (restArea):
            for entry in data_into_list:
                if (entry.startswith(restArea+', ')):
                    state = entry.split(', ')[1]
                    if (state not in states):
                        print(state, ':> ', self.removeSpecialChars(state))
                        states.append(self.removeSpecialChars(state))
        else:
            for entry in data_into_list:
                if (',' not in entry):
                    if (entry not in states):
                        print(entry, ':> ', self.removeSpecialChars(entry))
                        states.append(self.removeSpecialChars(entry))
                else:
                    break

        return states, data_into_list

    def getFlag(self, country, restArea=None):
        with open('static/web-assets/data/flags/'+self.country_code[country]+'.json') as json_file:
            data = json.load(json_file)

        if (restArea):
            if (restArea in data.keys()):
                return restArea, data[restArea]
            else:
                return self.country_fullName[country], data['Country']
        else:

            return self.country_fullName[country], data['Country']

    def getBlogs(self):
        blogs_df = pd.read_csv('static/web-assets/data/blogs/blogs_small.csv')
        return blogs_df.to_dict('ID')
