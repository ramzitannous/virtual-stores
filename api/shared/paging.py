from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def paginate_queryset(self, queryset, request, view=None):
        page_number = request.query_params.get(self.page_query_param, None)
        if page_number is None:
            self.page_size = len(queryset)
        return super().paginate_queryset(queryset, request, view)
