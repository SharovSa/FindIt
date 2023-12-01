from playwright.sync_api import sync_playwright
from product_info import ProductInfo
from time import sleep
import stuff as st


class OzonSearch:
    def __init__(self, query, sort_by=st.SortType.popularity):
        self.query = query
        self.sort_by = sort_by
        self.products_list = []

    def __get_product_info(self, url):
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            self.context = browser.new_context()
            self.context.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, '
                              'like Gecko) Chrome/73.0.3683.75 Safari/537.36'})
            page = self.context.new_page()
            page.goto(url)
            sleep(3)
            name = page.query_selector('div[data-widget="webProductHeading"]').query_selector('h1').inner_text()
            prices = page.query_selector('div[data-widget="webPrice"]').query_selector_all('span')
            if len(prices) == 2:
                price, discounted_price = prices[1].inner_text(), prices[0].inner_text()
            else:
                price, discounted_price = prices[4].inner_text(), prices[1].inner_text()
            rating = 5
            img = page.query_selector('div[data-widget="webGallery"]').query_selector('img[loading="eager"]').get_attribute('src')
            self.products_list.append(ProductInfo(name, st.make_digital_price(price),
                                                  st.make_digital_price(discounted_price), rating, img, url))

    def parse(self):
        product_urls = self.__get_links_on_products()
        pref_url = ""
        count = 0
        for product_url in product_urls:
            if count == st.COUNT_SEARCHED_PRODUCTS:
                break
            if product_url == pref_url:
                continue
            count += 1
            pref_url = product_url
            self.__get_product_info(product_url)

    def __get_links_on_products(self):
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
                return []
            else:
                page.wait_for_selector("#paginatorContent")
                product_urls = ["https://www.ozon.ru" + el.get_attribute('href') for el in page.query_selector_all('a[href^="/product"]')]
                return product_urls

    def get_products(self):
        self.parse()
        return self.products_list
