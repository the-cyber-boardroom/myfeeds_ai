import requests

from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.utils.Http import url_join_safe


class News_Feeds__Http_Content(Type_Safe):
    server : str

    def requests_get(self, path='', params=None):          # Makes HTTP GET request to the server
        if not self.server:
            raise ValueError('server not set')
        url = url_join_safe(self.server, path)
        return requests.get(url, params=params)