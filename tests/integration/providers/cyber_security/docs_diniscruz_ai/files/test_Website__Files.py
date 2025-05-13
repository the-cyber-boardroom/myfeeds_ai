from unittest                                                                       import TestCase
from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Providers                      import Model__Data_Feeds__Providers
from myfeeds_ai.providers.cyber_security.docs_diniscruz_ai.files.Website__Files     import Website__Files, FILE_ID__HOME_PAGE
from myfeeds_ai.providers.cyber_security.docs_diniscruz_ai.files.Website__Storage   import Website__Storage
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File        import Hacker_News__File
from tests.integration.data_feeds__objs_for_tests                                   import myfeeds_tests__setup_local_stack


class test_Website__Files(TestCase):
    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.provider_name   = Model__Data_Feeds__Providers.DOCS_DINISCRUZ_AI
        cls.website_files   = Website__Files(provider_name=cls.provider_name)
        cls.folder_now      = cls.website_files.website_storage.path__folder_now()

    def test_homepage(self):
        with self.website_files.file__home_page() as _:
            assert type(_)                                                                is Hacker_News__File
            assert type(_.hacker_news_storage)                                            is Website__Storage
            assert _.path_now   ()                                                        == f'{self.folder_now}/{FILE_ID__HOME_PAGE}.json'
            assert _.path_latest()                                                        == f'latest/{FILE_ID__HOME_PAGE}.json'
            assert _.hacker_news_storage.s3_db.s3_key__for_provider_path(_.path_latest()) == f'public-data/{self.provider_name.value}/latest/homepage.json'