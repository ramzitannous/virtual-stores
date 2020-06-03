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


class Gender(str, Enum):
    M = "M"
    F = "F"

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class SocialProviders(str, Enum):
    Facebook = "Facebook"
    Google = "Google"
    Instagram = "Instagram"

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
