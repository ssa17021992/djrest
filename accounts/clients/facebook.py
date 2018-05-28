from django.conf import settings

from common.utils import request


class FacebookClient:
    """Facebook client"""

    def __init__(self, access_token):
        self.api = settings.FACEBOOK_API
        self.access_token = access_token

    def me(self):
        response = request('GET', (
            '{}/me?access_token={}&fields=id,name,first_name,'
            'middle_name, last_name,email,birthday'
        ).format(self.api, self.access_token))
        return response
