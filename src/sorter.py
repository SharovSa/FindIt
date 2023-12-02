from stuff import SortType
from ozon_search import OzonSearch
from wb_search import WBSearch
from db import DbManager
from yandex_market_search import YaMarketSearch
from product_info import ProductInfo


class Sorter:
    def __init__(self, query, sort_by=SortType.popularity):
        self.query = query
        self.sort_by = sort_by
        self.sorted_products = []
        self.pref_query = 'start_query'
        self.pref_sort_by = SortType.popularity

    def set_sort_type(self, sort_by: SortType):
        self.pref_sort_by = self.sort_by
        self.sort_by = sort_by

    def __sort_products(self):
        self.sorted_products = (OzonSearch(self.query, self.sort_by).get_products() +
                                WBSearch(self.query, self.sort_by).get_products() +
                                YaMarketSearch(self.query, self.sort_by).get_products())
        if self.sort_by == SortType.price_up:
            self.sorted_products.sort(key=ProductInfo.get_discounted_price)
        elif self.sort_by == SortType.price_down:
            self.sorted_products.sort(key=ProductInfo.get_discounted_price, reverse=True)

    def __check_favorite(self):
        db = DbManager()
        for i in range(len(self.sorted_products)):
            if db.at(self.sorted_products[i].get_url()):
                self.sorted_products[i].set_favorite(True)
            else:
                self.sorted_products[i].set_favorite(False)

    def get_sorted_products(self) -> list[ProductInfo]:
        if self.query != self.pref_query or self.sort_by != self.pref_sort_by:
            self.__sort_products()
        if len(self.sorted_products) == 0:
            return self.sorted_products
        self.__check_favorite()
        self.pref_query = self.query
        self.pref_sort_by = self.sort_by
        return self.sorted_products

    def set_query(self, new_query):
        self.pref_query = self.query
        self.query = new_query
