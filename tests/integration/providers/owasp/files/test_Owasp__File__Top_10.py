from unittest                                                               import TestCase
from myfeeds_ai.providers.cyber_security.owasp.files.Owasp__File__Top_10    import Owasp__File__Top_10
from myfeeds_ai.providers.cyber_security.owasp.config.Config__Owasp         import FILE_ID__OWASP__TOP_10
from tests.integration.data_feeds__objs_for_tests                           import myfeeds_tests__setup_local_stack


class test_Owasp__File__Top_10(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.file_id           = FILE_ID__OWASP__TOP_10
        cls.owasp_file_top_10 = Owasp__File__Top_10(file_id=cls.file_id)
        cls.storage           = cls.owasp_file_top_10.hacker_news_storage

    def test_path_now(self):
        expected__file_path    = 'owasp-top-10/2021/A01_2021-Broken_Access_Control/owasp-top-10.json'
        expected__storage_path = 'public-data/owasp'
        with self.owasp_file_top_10 as _:
            path_now         = _.path_now()
            assert path_now == expected__file_path
            # _.save_data({'a': 42})
            # _.delete__now()

        with self.storage as _:
            assert _.s3_db.s3_key__for_provider_path(path_now) == f'{expected__storage_path}/{expected__file_path}'

            #pprint(_.s3_db.s3_path__files('', True))



