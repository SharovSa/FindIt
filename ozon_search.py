from seleniumbase import SB
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
            browser = pw.chromium.launch(headless=False)
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
        with SB(uc=True) as sb:
            sb.driver.get("https://www.ozon.ru/")
            sb.type('input', self.query)
            sb.click('button[type="submit"]')
            sb.sleep(1)
            url = sb.get_current_url()
            pos = url.find('text')
            if self.sort_by == st.SortType.popularity:
                new_url = url
            elif self.sort_by == st.SortType.price_up:
                new_url = url[:pos] + 'sorting=price&' + url[pos:]
            elif self.sort_by == st.SortType.price_down:
                new_url = url[:pos] + 'sorting=price_desc&' + url[pos:]
            else:
                new_url = url[:pos] + 'sorting=new&' + url[pos:]
            sb.driver.get(new_url)
            if not sb.is_text_visible(self.query, 'strong'):
                tmp = sb.get_current_url()
                sb.get_new_driver(undetectable=True)
                sb.driver.get(tmp)
                sb.sleep(1)
            sb.wait_for_element("#paginatorContent")
            product_urls = [el.get_attribute('href') for el in sb.find_elements('a[href^="/product"]')]
            return product_urls

    def get_products(self):
        self.parse()
        return self.products_list
