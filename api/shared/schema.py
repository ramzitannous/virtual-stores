from drf_yasg.inspectors import SwaggerAutoSchema


class StoreSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        operation_keys = operation_keys or self.operation_keys

        tags = self.overrides.get('tags')
        if not tags:
            if len(operation_keys) > 2:
                tags = [operation_keys[2].title()]
            else:
                tags = [operation_keys[0].title()]

        return tags
