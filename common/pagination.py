from rest_framework.pagination import PageNumberPagination as _PageNumberPagination


class PageNumberPagination(_PageNumberPagination):
    """Page number pagination"""

    page_size = 10
    max_page_size = 100
    page_query_param = 'page'
    page_size_query_param = 'size'
