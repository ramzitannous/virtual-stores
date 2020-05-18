from enum import Enum


class ProductSize(str, Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"
    XXXL = "XXL"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value
