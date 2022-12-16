
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/blogs')
def blogs():
        return 'These are my blogs'
    
    
@app.route('/blog-details')
def blogsDetails():
        return 'These are my blog details'
    
@app.route('/products')
def blogsDetails():
        return 'These are my products'