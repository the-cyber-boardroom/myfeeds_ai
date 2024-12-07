from unittest                                                                        import TestCase
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.Hacker_News__Files   import Hacker_News__Files, RAW_FEED__CREATED__BY
from tests.integration.news_feeds__objs_for_tests                                    import cbr_website__assert_local_stack

from osbot_utils.utils.Dev import pprint


class test_Hacker_News__Files(TestCase):

    @classmethod
    def setUpClass(cls):
        cbr_website__assert_local_stack()
        cls.hacker_news__files = Hacker_News__Files()

    def test_xml_feed__raw_data__current(self):
        with self.hacker_news__files as _:
            xml_feed__raw_data = _.xml_feed__raw_data__current(refresh=True).obj()
            assert xml_feed__raw_data.created_by == RAW_FEED__CREATED__BY
            assert xml_feed__raw_data.duration   < 1.0
            assert xml_feed__raw_data.feed_xml.startswith('<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
            year, month, day, hour = _.s3_db.s3_key_generator.path__for_date_time__now_utc().split('/')
            assert _.xml_feed__raw_data__from_date(year, month, day, hour).obj() == xml_feed__raw_data


