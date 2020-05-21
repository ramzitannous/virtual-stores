from versatileimagefield.fields import VersatileImageField
from drf_base64.fields import Base64FieldMixin


class Base64ThumbnailField(VersatileImageField, Base64FieldMixin):
    pass
