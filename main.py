from flask import Flask, render_template, request
from sorter import Sorter
from stuff import SortType
from product_info import ProductInfo


sorter = Sorter('start_query')


app = Flask(__name__)


@app.route('/')
def show():
    return render_template('start.html')


@app.route('/search', methods=['POST'])
def search():
    text = request.form['text']
    sorter.set_query(text)
    return render_template('products.html', products=sorter.get_sorted_products(), search_text=text)


@app.route('/sort_type=popularity/', methods=['POST'])
def get_sort_by_popularity():
    sorter.set_sort_type(SortType.popularity)
    if sorter.query == 'start_query':
        return render_template('start.html')
    else:
        return render_template('products.html', products=sorter.get_sorted_products(), search_text=sorter.query)


@app.route('/sort_type=popularity/search', methods=['POST'])
def popularity_search():
    text = request.form['text']
    sorter.set_query(text)
    return render_template('products.html', products=sorter.get_sorted_products(), search_text=text)


@app.route('/sort_type=price_up/', methods=['POST'])
def get_sort_by_price_up():
    sorter.set_sort_type(SortType.price_up)
    if sorter.query == 'start_query':
        return render_template('start.html')
    else:
        return render_template('products.html', products=sorter.get_sorted_products(), search_text=sorter.query)


@app.route('/sort_type=price_up/search', methods=['POST'])
def price_up_search():
    text = request.form['text']
    sorter.set_query(text)
    return render_template('products.html', products=sorter.get_sorted_products(), search_text=text)


@app.route('/sort_type=price_down/', methods=['POST'])
def get_sort_by_price_down():
    sorter.set_sort_type(SortType.price_down)
    if sorter.query == 'start_query':
        return render_template('start.html')
    else:
        return render_template('products.html', products=sorter.get_sorted_products(), search_text=sorter.query)


@app.route('/sort_type=price_down/search', methods=['POST'])
def price_down_search():
    text = request.form['text']
    sorter.set_query(text)
    return render_template('products.html', products=sorter.get_sorted_products(), search_text=text)


@app.route('/sort_type=newly/', methods=['POST'])
def get_sort_by_newly():
    sorter.set_sort_type(SortType.newly)
    if sorter.query == 'start_query':
        return render_template('start.html')
    else:
        return render_template('products.html', products=sorter.get_sorted_products(), search_text=sorter.query)


@app.route('/sort_type=newly/search', methods=['POST'])
def newly_search():
    text = request.form['text']
    sorter.set_query(text)
    return render_template('products.html', products=sorter.get_sorted_products(), search_text=text)


app.run()
