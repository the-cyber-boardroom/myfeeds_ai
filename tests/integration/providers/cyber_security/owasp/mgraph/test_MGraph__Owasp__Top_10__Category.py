import pytest
from unittest                                                                           import TestCase
from myfeeds_ai.providers.cyber_security.owasp.mgraphs.MGraph__Owasp__Top_10__Category  import MGraph__Owasp__Top_10__Category
from myfeeds_ai.providers.cyber_security.owasp.schemas.Owasp__Top_10__Category          import Owasp__Top_10__Category
from myfeeds_ai.providers.cyber_security.owasp.schemas.Schema__Owasp__Top_10__Category  import Schema__Owasp__Top_10__Category
from osbot_utils.utils.Env                                                              import load_dotenv, in_github_action
from tests.integration.data_feeds__objs_for_tests                                       import myfeeds_tests__setup_local_stack


class test_MGraph__Owasp__Top_10__Category(TestCase):

    @classmethod
    def setUpClass(cls):
        if in_github_action():
            pytest.skip('Skipping test')
        myfeeds_tests__setup_local_stack()
        cls.category               = Owasp__Top_10__Category.A03_2021__INJECTION
        cls.mgraph_top_10_category = MGraph__Owasp__Top_10__Category(category=cls.category)
        cls.mgraph_top_10_category.save_png = False

    def test_build(self):
        load_dotenv()
        with self.mgraph_top_10_category as _:
            result = _.build()
            #pprint(result)
            assert _.screenshot().startswith(b'\x89PNG\r\n')
        # with self.mgraph_top_10_category.mgraph as _:
        #     _.print()
        # with self.mgraph_top_10_category.mgraph.screenshot() as _:
        #     _.save_to('./_top_10_category.png').dot()


    def test_raw_data_json(self):
        with self.mgraph_top_10_category as _:
            raw_data_json = _.raw_data_json()
            assert type(raw_data_json) is Schema__Owasp__Top_10__Category
            #raw_data_json.print()