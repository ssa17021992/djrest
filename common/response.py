from copy import deepcopy

from rest_framework.response import Response as _Response
from rest_framework.status import is_client_error

from . import errors


class Response(_Response):
    """Response"""

    def __init__(self, *args, **kwargs):
        if is_client_error(kwargs['status']):
            kwargs['data'] = [self.__get_error_data(k, v)
                for k, v in kwargs.get('data', {}).items()]

        super(self.__class__, self).__init__(*args, **kwargs)

    def __get_error_data(self, k, v):
        if isinstance(v, dict):
            error_data = deepcopy(v)
        else:
            error_data = deepcopy(errors.FORM_ERROR)
            error_data['detail'] = v[0]

        error_data['field'] = k
        return error_data
