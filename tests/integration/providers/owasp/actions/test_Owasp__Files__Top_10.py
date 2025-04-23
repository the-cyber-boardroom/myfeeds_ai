from unittest                                                                           import TestCase
from myfeeds_ai.providers.cyber_security.owasp.actions.Owasp__Files__Top_10             import Owasp__Files__Top_10
from myfeeds_ai.providers.cyber_security.owasp.files.Owasp__File__Top_10                import Owasp__File__Top_10
from myfeeds_ai.providers.cyber_security.owasp.schemas.Schema__Owasp__Top_10__Category  import Schema__Owasp__Top_10__Category
from tests.integration.data_feeds__objs_for_tests                                       import myfeeds_tests__setup_local_stack

class test_Owasp__Files__Top_10(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.owasp_files_top_10 = Owasp__Files__Top_10()

    def test_file__a01__broken_access_control__raw_Data(self):
        with self.owasp_files_top_10.file__a01__broken_access_control__raw_Data() as _:
            assert type(_)                              is Owasp__File__Top_10
            assert _.path_now()                         == 'owasp-top-10/2021/A01_2021-Broken_Access_Control/raw-data.md'

    def test_a01__broken_access_control__raw_data(self):
        with self.owasp_files_top_10 as _:
            raw_data =  _.a01__broken_access_control__raw_data()
            assert "# A01:2021 – Broken Access Control" in raw_data

    def test_a01__broken_access_control__raw_data__json(self):
        with self.owasp_files_top_10 as _:
            raw_data_json =  _.a01__broken_access_control__raw_data__json()
            assert type(raw_data_json) is Schema__Owasp__Top_10__Category

