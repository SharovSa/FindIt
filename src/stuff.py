from string import digits
from enum import Enum

COUNT_SEARCHED_PRODUCTS = 5


def make_digital_price(num):
    res = ''
    for symbl in num:
        if symbl in digits:
            res += symbl
    return int(res)


class SortType(Enum):
    popularity = 1
    price_up = 2
    price_down = 3
    newly = 4
