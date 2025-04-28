
from myfeeds_ai.providers.cyber_security.owasp.schemas.Owasp__Top_10__Category  import Owasp__Top_10__Category
from myfeeds_ai.providers.cyber_security.owasp.schemas.Owasp__Top_10__Version   import Owasp__Top_10__Version
from myfeeds_ai.shared.data.My_Feeds__Http_Content                              import My_Feeds__Http_Content
from osbot_utils.type_safe.decorators.type_safe                                 import type_safe


class Owasp__Git_Hub__Http_Content(My_Feeds__Http_Content):
    server : str = 'https://raw.githubusercontent.com/OWASP'

    def owasp_top_10__markdown(self, version: Owasp__Top_10__Version, category: Owasp__Top_10__Category) -> str:
        path = f"Top10/refs/heads/master/{version.value}/docs/{category.value}.md"
        return self.requests_get(path).text

    @type_safe
    def owasp_top_10__category(self, category: Owasp__Top_10__Category):
        version = Owasp__Top_10__Version.TOP_10__2021
        return self.owasp_top_10__markdown(version=version, category=category)

    def owasp_top_10__a01__broken_access_control(self):
        return self.owasp_top_10__category(Owasp__Top_10__Category.A01_2021__BROKEN_ACCESS_CONTROL)

    def owasp_top_10__a04__insecure_design(self):
        return self.owasp_top_10__category(Owasp__Top_10__Category.A04_2021__INSECURE_DESIGN      )
