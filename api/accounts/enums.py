from enum import Enum


class AccountTypes(str, Enum):
    NORMAL = "NORMAL"
    BUSINESS = "BUSINESS"

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class AccountStatus(str, Enum):
    VERIFIED = "VERIFIED"
    UN_VERIFIED = "UN_VERIFIED"
    PENDING = "PENDING"

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
