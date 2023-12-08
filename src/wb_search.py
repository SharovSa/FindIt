from playwright.sync_api import sync_playwright
from time import sleep
import stuff as st
from product_info import ProductInfo


class WBSearch:
    def __init__(self, query, sort_by=st.SortType.popularity):
        self.query = query
        self.sort_by = sort_by
        self.product = ProductInfo()

    def __get_product_info(self, product_card):
        url = product_card.query_selector('a').get_attribute('href')
        name = product_card.query_selector('a').get_attribute('aria-label')
        if product_card.query_selector('ins') is not None:
            discounted_price = product_card.query_selector('ins').inner_text()
            price = product_card.query_selector('del').inner_text()
        else:
            discounted_price = product_card.query_selector('span[class="price__lower-price"]').inner_text()
            price = discounted_price
        img = product_card.query_selector('img').get_attribute('src')
        self.product = ProductInfo(name, st.make_digital_price(price), st.make_digital_price(discounted_price), img, url)

    def __get_product_info_from_page(self):
        name = self.page.query_selector('.product-page__header').inner_text()
        url = self.query
        if self.page.query_selector('ins') is not None:
            discounted_price = self.page.query_selector('ins').inner_text()
            price = self.page.query_selector('del').inner_text()
        else:
            discounted_price = self.page.query_selector('span[class="price__lower-price"]').inner_text()
            price = discounted_price
        img = self.page.query_selector('#imageContainer').query_selector('img').get_attribute('src')
        self.product = ProductInfo(name, price, discounted_price, img, url)

    def parse(self):
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            self.context = browser.new_context()
            self.context.set_extra_http_headers({
                                                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) '
                                                                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                                  'Chrome/73.0.3683.75 Safari/537.36'})
            self.page = self.context.new_page()
            if self.query.find('https', 0) != -1:
                self.page.goto(self.query)
                self.page.wait_for_selector('.product-page__grid')
                self.__get_product_info_from_page()
            else:
                self.page.goto("https://www.wildberries.ru/")
                sleep(1)
                self.page.query_selector('#searchInput').type(text=self.query, delay=0.9)
                self.page.query_selector('#applySearchBtn').click()
                sleep(1)
                if self.page.query_selector('div[class="not-found-search__wrap"]') is not None:
                    return
                else:
                    if self.sort_by != st.SortType.popularity:
                        self.page.wait_for_selector("button[class='dropdown-filter__btn dropdown-filter__btn--sorter']",
                                                    state='attached').click()
                        if self.sort_by == st.SortType.price_up:
                            self.page.get_by_text('По возрастанию цены').click()
                        elif self.sort_by == st.SortType.price_down:
                            self.page.get_by_text('По убыванию цены').click()
                        else:
                            self.page.get_by_text('По новинкам').click()
                    sleep(1)
                    self.page.wait_for_selector(".product-card-overflow", state='attached')
                    self.__get_product_info(self.page.query_selector('.product-card__wrapper'))

    def get_product(self):
        self.parse()
        return self.product
