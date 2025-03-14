from unittest                                                                                  import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Files                        import Hacker_News__Files
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Data__Feed     import Model__Hacker_News__Data__Feed
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Raw_Data__Feed import Model__Hacker_News__Raw_Data__Feed
from tests.integration.data_feeds__objs_for_tests                                              import myfeeds_tests__setup_local_stack

class test_Hacker_News__Files(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.hacker_news__files = Hacker_News__Files()

    def test_files_paths__latest(self):
        with self.hacker_news__files as _:
            paths = _.files_paths__latest()
            assert paths.get('latest').get('feed_xml' ) == self.hacker_news__files.s3_db.s3_path__raw_data__feed_xml__latest  ()
            assert paths.get('latest').get('feed_data') == self.hacker_news__files.s3_db.s3_path__raw_data__feed_data__latest ()
            assert paths.get('now'   ).get('feed_xml' ) == self.hacker_news__files.s3_db.s3_path__raw_data__feed_xml__now     ()
            assert paths.get('now'   ).get('feed_data') == self.hacker_news__files.s3_db.s3_path__raw_data__feed_data__now    ()

    def test_xml_feed__raw_data__current(self):
        with self.hacker_news__files as _:
            model                  = _.xml_feed__raw_data__current()
            xml_feed__raw_data     = model.obj()
            year, month, day, hour = _.s3_db.s3_key_generator.path__for_date_time__now_utc().split('/')
            expected_xml_start     = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'

            assert type(model)                                                   is Model__Hacker_News__Raw_Data__Feed
            #assert xml_feed__raw_data.created_by                                 == RAW_FEED__CREATED__BY
            assert xml_feed__raw_data.duration                                   < 2.0
            #assert xml_feed__raw_data.feed_xml.startswith(expected_xml_start)    is True
            assert _.xml_feed__raw_data__from_date(int(year), int(month), int(day), int(hour)).obj() == xml_feed__raw_data

    def test_xml_feed__data__current(self):
        with self.hacker_news__files as _:
            model     = _.feed_data__current()
            data_feed = model.obj()

            assert type(model)                  is Model__Hacker_News__Data__Feed
            assert data_feed.feed_data.title    == 'The Hacker News'
            assert data_feed.feed_data.language == 'en-us'

    def test_timeline_png__latest(self):
        with self.hacker_news__files as _:
            png_bytes = _.timeline_png__latest()
            if png_bytes:
                assert len(png_bytes) > 0
                assert type(png_bytes) is bytes
                assert png_bytes.startswith(b'\x89PNG\r\n')


