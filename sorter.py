from stuff import SortType
from ozon_search import OzonSearch
from wb_search import WBSearch
from yandex_market_search import YaMarketSearch
from product_info import ProductInfo


class Sorter:
    def __init__(self, query, sort_by=SortType.popularity):
        self.query = query
        self.sort_by = sort_by
        self.sorted_products = []

    def set_sort_type(self, sort_by: SortType):
        self.sort_by = sort_by

    def __sort_products(self):
        self.sorted_products = (
                                WBSearch(self.query, self.sort_by).get_products() +
                                YaMarketSearch(self.query, self.sort_by).get_products())
        if self.sort_by == SortType.price_up:
            self.sorted_products.sort(key=ProductInfo.get_discounted_price)
        elif self.sort_by == SortType.price_down:
            self.sorted_products.sort(key=ProductInfo.get_discounted_price, reverse=True)

    def get_sorted_products(self):
        self.__sort_products()
        return self.sorted_products

    def set_query(self, new_query):
        self.query = new_query
