from unittest                                                                                  import TestCase
from myfeeds_ai.providers.cyber_security.docs_diniscruz_ai.Html_Graph__Site__docs_diniscruz_ai import Html_Graph__Site__docs_diniscruz_ai


class test_Html_Graph__Site__docs_diniscruz_ai(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.site_mgraph = Html_Graph__Site__docs_diniscruz_ai()

    def test_html__homepage(self):
        with self.site_mgraph as _:
            html = _.html__homepage()
            print(html)
