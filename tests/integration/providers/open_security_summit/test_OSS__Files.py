from unittest                                                                                               import TestCase
from cbr_custom_data_feeds.data_feeds.Data__Feeds__Shared_Constants                                         import S3_FILE_NAME__LATEST__VERSIONS, S3_FOLDER_NAME__LATEST
from cbr_custom_data_feeds.data_feeds.models.Model__Data_Feeds__Raw_Data                                    import Model__Data_Feeds__Raw_Data
from cbr_custom_data_feeds.providers.cyber_security.open_security_summit.OSS__Files                         import OSS__Files
from cbr_custom_data_feeds.providers.cyber_security.open_security_summit.models.Model__OSS__Latest_Versions import Model__OSS__Latest_Versions
from osbot_utils.utils.Misc                                                                                 import list_set
from tests.integration.data_feeds__objs_for_tests                                                           import cbr_website__assert_local_stack


class test_OSS__Files(TestCase):

        @classmethod
        def setUpClass(cls):
            cbr_website__assert_local_stack()
            cls.oss_files = OSS__Files()

        def test_latest_versions__save(self):
            with self.oss_files as _:
                s3_path_latest_version = f'{S3_FOLDER_NAME__LATEST}/{S3_FILE_NAME__LATEST__VERSIONS}.json'
                s3_path__raw_content   = 'abc'
                latest_version         = Model__OSS__Latest_Versions()
                assert list_set(latest_version)                                             == ['s3_path__raw_content']
                assert _.latest_versions__save(latest_version)                              == s3_path_latest_version
                assert _.latest_versions__update(s3_path__raw_content=s3_path__raw_content) == s3_path_latest_version
                assert _.latest_versions__load().s3_path__raw_content == s3_path__raw_content

        def test_raw_content__current(self):
            with self.oss_files as _:
                raw_content = _.raw_content__current(refresh=True)
                assert type(raw_content)         is Model__Data_Feeds__Raw_Data
                assert len(raw_content.raw_data)  > 3500000
                assert list_set(raw_content)     == ['created_timestamp', 'duration', 'raw_data', 'raw_data_id', 'source_url', 'storage_path']
                assert raw_content.storage_path  in _.all_files()

                #pprint(_.latest_versions__load().json())
