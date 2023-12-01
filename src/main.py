from flask import Flask, render_template, request
from sorter import Sorter
from stuff import SortType
from db import DbManager
from product_info import ProductInfo


app = Flask(__name__)


sorter = Sorter('start_query')
db = DbManager()


@app.route('/')
def show():
    return render_template('start.html', products=db.get_products())


@app.route('/search/', methods=['POST'])
@app.route('/sort_type=popularity/search', methods=['POST'])
@app.route('/sort_type=price_up/search', methods=['POST'])
@app.route('/sort_type=price_down/search', methods=['POST'])
@app.route('/sort_type=newly/search', methods=['POST'])
def search():
    text = request.form['text']
    sorter.set_query(text)
    return render_template('products.html', products=enumerate(sorter.get_sorted_products()), search_text=text, len=len(sorter.get_sorted_products()))


@app.route('/sort_type=popularity/', methods=['POST'])
def get_sort_by_popularity():
    sorter.set_sort_type(SortType.popularity)
    if sorter.query == 'start_query':
        return render_template('start.html')
    else:
        return render_template('products.html', products=enumerate(enumerate(sorter.get_sorted_products())), search_text=sorter.query, len=len(sorter.get_sorted_products()))


@app.route('/sort_type=price_up/', methods=['POST'])
def get_sort_by_price_up():
    sorter.set_sort_type(SortType.price_up)
    if sorter.query == 'start_query':
        return render_template('start.html')
    else:
        return render_template('products.html', products=enumerate(enumerate(sorter.get_sorted_products())), search_text=sorter.query, len=len(sorter.get_sorted_products()))


@app.route('/sort_type=price_down/', methods=['POST'])
def get_sort_by_price_down():
    sorter.set_sort_type(SortType.price_down)
    if sorter.query == 'start_query':
        return render_template('start.html')
    else:
        return render_template('products.html', products=enumerate(enumerate(sorter.get_sorted_products())), search_text=sorter.query, len=len(sorter.get_sorted_products()))


@app.route('/sort_type=newly/', methods=['POST'])
def get_sort_by_newly():
    sorter.set_sort_type(SortType.newly)
    if sorter.query == 'start_query':
        return render_template('start.html')
    else:
        return render_template('products.html', products=enumerate(enumerate(sorter.get_sorted_products())), search_text=sorter.query, len=len(sorter.get_sorted_products()))


@app.route('/make_favorite/', methods=['POST'])
def make_favorite():
    id = int(request.form.get('prod_id'))
    product = sorter.get_sorted_products()[id]
    if product.is_in_favorite():
        db.delete_product(product.get_url())
    else:
        db.add_product(product)
    return render_template('products.html', products=enumerate(enumerate(sorter.get_sorted_products())), search_text=sorter.query, len=len(sorter.get_sorted_products()))


@app.route('/favorite/')
def show_favorite():
    return render_template('start.html', products=db.get_products())


@app.route('/favorite/', methods=['POST'])
def change_favorite():
    url = request.form.get('prod_url')
    db.delete_product(url)
    return render_template('start.html', products=db.get_products())

app.run(host='0.0.0.0', port=5000)
