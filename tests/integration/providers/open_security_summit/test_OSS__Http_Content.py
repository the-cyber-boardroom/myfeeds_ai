from unittest                                                                               import TestCase
from cbr_custom_data_feeds.data_feeds.models.Model__Data_Feeds__Raw_Data                    import Model__Data_Feeds__Raw_Data
from osbot_utils.utils.Json                                                                 import str_to_json
from osbot_utils.utils.Misc                                                                 import list_set
from cbr_custom_data_feeds.providers.cyber_security.open_security_summit.OSS__Http_Content  import OSS__Http_Content
from tests.integration.data_feeds__objs_for_tests                                           import cbr_website__assert_local_stack

EXPECTED__OSS__RAW_CONTENT__FIELDS = ['company', 'content', 'date', 'description', 'dir', 'event', 'expirydate',
                                      'facebook', 'fuzzywordcount', 'hey_summit', 'image', 'job_title', 'kind',
                                      'lang', 'lastmod', 'layout', 'linkedin', 'notes', 'objectID', 'organizers',
                                      'permalink', 'project', 'publishdate', 'readingtime', 'relpermalink', 'section',
                                      'status', 'summary', 'title', 'topics', 'track', 'twitter', 'type', 'url',
                                      'website', 'weight', 'when_day', 'when_month', 'when_time', 'when_year',
                                      'wordcount', 'youtube_link', 'zoom_link']

class test_OSS__Http_Content(TestCase):

    @classmethod
    def setUpClass(cls):
        cbr_website__assert_local_stack()
        cls.oss_http_content = OSS__Http_Content()

    def test_raw_content(self):
        with self.oss_http_content as _:
            raw_content   = _.raw_content()
            oss_raw_data  = str_to_json(raw_content.raw_data)
            assert type(raw_content)            is Model__Data_Feeds__Raw_Data
            assert 1000 > len(oss_raw_data)      > 750
            assert list_set(oss_raw_data[0])    == EXPECTED__OSS__RAW_CONTENT__FIELDS

            assert raw_content.source_url       == 'https://open-security-summit.org/content.json'
            assert raw_content.storage_path     == ''                                                   # should not be set here

