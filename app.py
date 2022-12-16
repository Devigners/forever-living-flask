# import flask and render_template
from flask import Flask, render_template

app = Flask(__name__)


# index page
@app.route('/')
def index():
    return render_template('index.html')


# shop page
@app.route('/shop')
def shop():
    return render_template('shop.html')


# blog page
@app.route('/blogs')
def blogs():
    return render_template('blogs.html')


# blog page
@app.route('/blog-details')
def blogDetails():
    return render_template('blog-details.html')


# product details
@app.route('/product/details')
def productDetails():
    return render_template('single-product.html')


if __name__ == '__main__':
    app.run(debug=True)
