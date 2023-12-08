from playwright.sync_api import sync_playwright
from product_info import ProductInfo
from time import sleep
import stuff as st


class OzonSearch:
    def __init__(self, query, sort_by=st.SortType.popularity):
        self.query = query
        self.sort_by = sort_by
        self.product = None

    def __get_product_info(self, url):
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            self.context = browser.new_context()
            self.context.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, '
                              'like Gecko) Chrome/73.0.3683.75 Safari/537.36'})
            page = self.context.new_page()
            page.goto(url)
            page.wait_for_selector('div[data-widget="container"]')
            name = page.query_selector('div[data-widget="webProductHeading"]').query_selector('h1').inner_text()
            prices = page.query_selector('div[data-widget="webPrice"]').query_selector_all('span')
            if len(prices) == 2:
                price, discounted_price = prices[1].inner_text(), prices[0].inner_text()
            else:
                price, discounted_price = prices[4].inner_text(), prices[1].inner_text()
            img = page.query_selector('div[data-widget="webGallery"]').query_selector('img[loading="eager"]').get_attribute('src')
            self.product = ProductInfo(name, st.make_digital_price(price), st.make_digital_price(discounted_price), img, url)

    def parse(self):
        if self.query.find('https', 0) != -1:
            self.__get_product_info(self.query)
        else:
            product_url = self.__get_link_on_product()
            if product_url is not None:
                self.__get_product_info(product_url)

    def __get_link_on_product(self):
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            context = browser.new_context()
            context.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/73.0.3683.75 Safari/537.36'})
            page = context.new_page()
            page.goto("https://www.ozon.ru/")
            page.wait_for_selector('input')
            page.get_by_placeholder("Искать на Ozon").type(text=self.query, delay=0.5)
            page.query_selector('button[aria-label="Поиск"]').click()
            tmp_url = page.url
            browser.close()
            pos = tmp_url.find('text')
            if self.sort_by == st.SortType.popularity:
                new_url = tmp_url
            elif self.sort_by == st.SortType.price_up:
                new_url = tmp_url[:pos] + 'sorting=price&' + tmp_url[pos:]
            elif self.sort_by == st.SortType.price_down:
                new_url = tmp_url[:pos] + 'sorting=price_desc&' + tmp_url[pos:]
            else:
                new_url = tmp_url[:pos] + 'sorting=new&' + tmp_url[pos:]
            browser = pw.chromium.launch()
            context = browser.new_context()
            context.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/73.0.3683.75 Safari/537.36'})
            page = context.new_page()
            page.goto(new_url)
            sleep(3)
            if page.query_selector('div[data-widget="searchResultsError"]') is not None:
                return None
            else:
                page.wait_for_selector("#paginatorContent")
                product_url = "https://www.ozon.ru" + page.query_selector('a[href^="/product"]').get_attribute('href')
                return product_url

    def get_product(self):
        self.parse()
        return self.product
