class ProductInfo:
    _name = ''
    _price = 0
    _discounted_price = 0
    _rating = 0
    _img = ''
    _url = ''

    def __init__(self, name, price, discounted_price, rating, img, url, in_favorite=False):
        self._name = name
        self._price = price
        self._discounted_price = discounted_price
        self._rating = rating
        self._img = img
        self.in_favorite = in_favorite
        self._url = url

    def get_name(self):
        return self._name

    def get_price(self):
        return self._price

    def get_discounted_price(self):
        return self._discounted_price

    def get_rating(self):
        return self._rating

    def get_img(self):
        return self._img

    def get_url(self):
        return self._url

    def is_in_favorite(self):
        return self.in_favorite

    def set_favorite(self, flag):
        self.in_favorite = flag
