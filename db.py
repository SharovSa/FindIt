import psycopg2
from product_info import ProductInfo


class DbManager:
    def __init__(self):
        with psycopg2.connect(dbname='finditdb', user='user', password='1234', host='localhost', port='5432') as conn:
            cur = conn.cursor()
            cur.execute('create table if not exists favorite_products(name TEXT, '
                        'url TEXT, img_url TEXT, price INTEGER, discounted_price INTEGER)')
            conn.commit()

    def add_product(self, product: ProductInfo):
        with psycopg2.connect(dbname='finditdb', user='user', password='1234', host='localhost', port='5432') as conn:
            cur = conn.cursor()
            cur.execute(f"insert into favorite_products values"
                        f" ('{product.get_name()}', '{product.get_url()}', '{product.get_img()}',"
                        f" {product.get_price()}, {product.get_discounted_price()})")
            conn.commit()

    def get_products(self):
        with psycopg2.connect(dbname='finditdb', user='user', password='1234', host='localhost', port='5432') as conn:
            cur = conn.cursor()
            cur.execute('select * from favorite_products')
            products = []
            for product in cur.fetchall():
                print(product)
                products.append(ProductInfo(product[0], product[3], product[4], 5, product[2], product[1],
                                            in_favorite=True))
            return products
