from unittest                                                                                             import TestCase
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.Hacker_News__Files                        import Hacker_News__Files, RAW_FEED__CREATED__BY
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.models.Model__Hacker_News__Data__Feed     import Model__Hacker_News__Data__Feed
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.models.Model__Hacker_News__Raw_Data__Feed import Model__Hacker_News__Raw_Data__Feed
from tests.integration.news_feeds__objs_for_tests                                                         import cbr_website__assert_local_stack

class test_Hacker_News__Files(TestCase):

    @classmethod
    def setUpClass(cls):
        cbr_website__assert_local_stack()
        cls.hacker_news__files = Hacker_News__Files()

    def test_xml_feed__raw_data__current(self):
        with self.hacker_news__files as _:
            model                  = _.xml_feed__raw_data__current(refresh=True)
            xml_feed__raw_data     = model.obj()
            year, month, day, hour = _.s3_db.s3_key_generator.path__for_date_time__now_utc().split('/')
            expected_xml_start     = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'

            assert type(model)                                                   is Model__Hacker_News__Raw_Data__Feed
            assert xml_feed__raw_data.created_by                                 == RAW_FEED__CREATED__BY
            assert xml_feed__raw_data.duration                                   < 1.0
            assert xml_feed__raw_data.feed_xml.startswith(expected_xml_start)    is True
            assert _.xml_feed__raw_data__from_date(year, month, day, hour).obj() == xml_feed__raw_data

    def test_xml_feed__data__current(self):
        with self.hacker_news__files as _:
            model     = _.xml_feed__data__current()
            data_feed = model.obj()

            assert type(model)                  is Model__Hacker_News__Data__Feed
            assert data_feed.feed_data.title    == 'The Hacker News'
            assert data_feed.feed_data.language == 'en-us'



