from unittest                                                                                       import TestCase
from myfeeds_ai.data_feeds.Data__Feeds__Shared_Constants                                 import S3_FOLDER_NAME__LATEST
from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Prompt                              import Model__Data_Feeds__Prompt
from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Raw_Data                            import Model__Data_Feeds__Raw_Data
from myfeeds_ai.providers.cyber_security.open_security_summit.OSS__Events                import OSS_EVENTS__CURRENT__YEAR, OSS_EVENTS__CURRENT__MONTH
from myfeeds_ai.providers.cyber_security.open_security_summit.OSS__Files                 import OSS__Files
from myfeeds_ai.providers.cyber_security.open_security_summit.OSS__Prompts               import PROMPT__OSS__CURRENT_SESSIONS
from myfeeds_ai.providers.cyber_security.open_security_summit.OSS__S3_DB                 import S3_FILE_NAME__OSS__CURRENT_EVENT, S3_FILE_NAME__OSS__CURRENT_EVENT__PROMPT
from myfeeds_ai.providers.cyber_security.open_security_summit.models.Model__OSS__Event   import Model__OSS__Event
from osbot_utils.utils.Env                                                                          import in_github_action
from osbot_utils.utils.Misc                                                                         import list_set
from tests.integration.data_feeds__objs_for_tests                                                   import cbr_website__assert_local_stack

class test_OSS__Files(TestCase):

        @classmethod
        def setUpClass(cls):
            cbr_website__assert_local_stack()
            cls.oss_files = OSS__Files()
            cls.refresh_data = in_github_action()

        def test_current_event(self):
            with self.oss_files as _:
                current_event = _.current_event(refresh=self.refresh_data)
                s3_path       = _.s3_db.s3_path__current_event()
                assert type(current_event)                       is Model__OSS__Event
                assert current_event.year                        == OSS_EVENTS__CURRENT__YEAR
                assert current_event.month                       == OSS_EVENTS__CURRENT__MONTH
                assert 20 > len(current_event.sessions  )         > 5
                assert 20 > len(current_event.organizers)         > 5
                assert  s3_path                                  == f'{S3_FOLDER_NAME__LATEST}/{S3_FILE_NAME__OSS__CURRENT_EVENT}.json'
                assert _.s3_db.s3_path__exists(s3_path)          is True
                assert _.latest_versions().s3_path__latest_event == s3_path

        def test_current_event_prompt(self):
            expected_start_text = PROMPT__OSS__CURRENT_SESSIONS[0:26]
            with self.oss_files as _:
                current_event_prompt = _.current_event_prompt(refresh=self.refresh_data)
                s3_path              = _.s3_db.s3_path__current_event__prompt()
                assert type(current_event_prompt)                                       is Model__Data_Feeds__Prompt
                assert current_event_prompt.prompt_text.startswith(expected_start_text) is True
                assert  s3_path                                                         == f'{S3_FOLDER_NAME__LATEST}/{S3_FILE_NAME__OSS__CURRENT_EVENT__PROMPT}.json'
                assert _.s3_db.s3_path__exists(s3_path)                                 is True
                assert _.latest_versions().s3_path__latest_event__prompt                == s3_path



        def test_raw_content__current(self):
            with self.oss_files as _:
                raw_content = _.raw_content__current(refresh=self.refresh_data)
                s3_path     = _.s3_db.s3_path__raw_content__now()
                assert type(raw_content)         is Model__Data_Feeds__Raw_Data
                assert len(raw_content.raw_data)  > 3500000
                assert list_set(raw_content)     == ['created_timestamp', 'duration', 'raw_data', 'raw_data_id', 'source_url', 'storage_path']
                assert raw_content.storage_path  in _.all_files()

                assert _.latest_versions().s3_path__raw_content == s3_path

        def test_content__current(self):
            with self.oss_files as _:
                content = _.content__current(refresh=self.refresh_data)
                assert 500 > len(content.participants    ) > 200
                assert 500 > len(content.sessions) > 300

        # def test_latest_versions__save(self):
        #     with self.oss_files as _:
        #         s3_path_latest_version = f'{S3_FOLDER_NAME__LATEST}/{S3_FILE_NAME__LATEST__VERSIONS}.json'
        #         s3_path__raw_content   = 'abc'
        #         latest_version         = Model__OSS__Latest_Versions()
        #         assert list_set(latest_version)                                             == ['s3_path__raw_content']
        #         assert _.latest_versions__save(latest_version)                              == s3_path_latest_version
        #         assert _.latest_versions__update(s3_path__raw_content=s3_path__raw_content) == s3_path_latest_version
        #         assert _.latest_versions__load().s3_path__raw_content == s3_path__raw_content