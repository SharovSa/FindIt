from time import sleep
import playwright.sync_api
from playwright.sync_api import expect
from playwright.sync_api import sync_playwright
from product_info import ProductInfo
import stuff as st


class YaMarketSearch:
    def __init__(self, query: str, sort_by=st.SortType.popularity):
        self._query = query
        self.sort_by = sort_by
        self.product = ProductInfo()

    def __get_product_info(self, product_card: playwright.sync_api.ElementHandle):
        url = "https://market.yandex.ru" + product_card.query_selector('a').get_attribute('href')
        img = product_card.query_selector('img').get_attribute('src')
        if product_card.query_selector('h3[data-auto="snippet-price-current"]') is not None:
            discounted_price = product_card.query_selector('h3[data-auto="snippet-price-current"]').inner_text()
            price = product_card.query_selector('span[data-auto="snippet-price-old"]').inner_text()
        elif product_card.query_selector('span[data-auto="mainPrice"]') is not None:
            price = product_card.query_selector('span[data-auto="mainPrice"]').inner_text()
            discounted_price = price
        else:
            price = product_card.query_selector('h3[data-auto="price-block"]').inner_text()
            discounted_price = price
        if product_card.query_selector('a[data-baobab-name="title"]') is not None:
            name = product_card.query_selector('a[data-baobab-name="title"]').inner_text()
        else:
            name = product_card.query_selector('h3[data-baobab-name="title"]').inner_text()
        self.product = ProductInfo(name, st.make_digital_price(price), st.make_digital_price(discounted_price), img, url)

    def __get_product_info_from_page(self):
        self.page.wait_for_selector('#cardContent')
        url = self._query
        name = self.page.query_selector('h1[data-auto="productCardTitle"]').inner_text()
        if self.page.query_selector('h3[data-auto="snippet-price-current"]') is not None:
            discounted_price = self.page.query_selector('h3[data-auto="snippet-price-current"]').inner_text()
            price = self.page.query_selector('span[data-auto="snippet-price-old"]').query_selector('s').inner_text()
        elif self.page.query_selector('span[data-auto="mainPrice"]') is not None:
            price = self.page.query_selector('span[data-auto="mainPrice"]').inner_text()
            discounted_price = price
        else:
            price = self.page.query_selector('h3[data-auto="price-block"]').inner_text()
            discounted_price = price
        img = self.page.query_selector('div[data-zone-name="media-viewer-gallery"]').query_selector('img').get_attribute('src')
        self.product = ProductInfo(name, price, st.make_digital_price(discounted_price), img, url)

    def __get_link_on_product(self):
        if self.page.get_by_text('Этого мы не нашли').is_visible():
            return
        else:
            if self.sort_by != st.SortType.popularity:
                if self.sort_by == st.SortType.price_up:
                    self.page.get_by_text('по цене').click()
                elif self.sort_by == st.SortType.price_down:
                    try:
                        self.page.get_by_text('по цене').click()
                        self.page.wait_for_selector('button[data-zone-name="ShowAllButton"]', timeout=5000)
                        self.page.get_by_text('по цене').click()
                    except playwright.sync_api.TimeoutError:
                        print("Error")
                        self.page.get_by_text('по цене').click()
            self.page.wait_for_selector("#searchResults")
            sleep(2)
            search_result = self.page.query_selector("#searchResults")
            product = search_result.query_selector('article[data-baobab-name="productSnippet"]')
            self.__get_product_info(product)

    def parse(self):
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            self.context = browser.new_context()
            self.context.set_extra_http_headers({'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) '
                                                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                              'Chrome/73.0.3683.75 Safari/537.36'})
            self.page = self.context.new_page()
            if self._query.find('https', 0) != -1:
                self.page.goto(self._query)
                self.__get_product_info_from_page()
            else:
                self.page.goto("https://market.yandex.ru/")
                self.page.get_by_placeholder("Искать товары").type(text=self._query, delay=0.9)
                self.page.query_selector("button[type='submit']").click()
                self.__get_link_on_product()

    def get_product(self):
        self.parse()
        return self.product
