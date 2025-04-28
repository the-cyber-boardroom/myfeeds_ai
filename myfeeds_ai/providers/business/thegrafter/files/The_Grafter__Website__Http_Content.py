import requests

from myfeeds_ai.shared.data.My_Feeds__Http_Content                              import My_Feeds__Http_Content
from myfeeds_ai.providers.cyber_security.owasp.schemas.Owasp__Top_10__Category  import Owasp__Top_10__Category
from myfeeds_ai.providers.cyber_security.owasp.schemas.Owasp__Top_10__Version   import Owasp__Top_10__Version
from osbot_utils.helpers.html.Html_To_Dict import Html_To_Dict
from osbot_utils.type_safe.decorators.type_safe import type_safe
from osbot_utils.utils.Http import url_join_safe


class The_Grafter__Website__Http_Content(My_Feeds__Http_Content):
    server : str = 'https://thegrafter.com/'

    def http_data(self, path='/'):
        return self.requests_get__dict(path=path)
