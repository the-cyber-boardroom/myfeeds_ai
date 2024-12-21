from myfeeds_ai.data_feeds.Data_Feeds__Files import Data_Feeds__Files
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Http_Content                 import Hacker_News__Http_Content
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Parser                       import Hacker_News__Parser
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__S3_DB                        import Hacker_News__S3_DB
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Data__Feed     import Model__Hacker_News__Data__Feed
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Raw_Data__Feed import Model__Hacker_News__Raw_Data__Feed
from osbot_utils.context_managers.capture_duration                                                        import capture_duration

RAW_FEED__CREATED__BY = 'Hacker_News__Files.xml_feed__current'

class Hacker_News__Files(Data_Feeds__Files):
    s3_db        : Hacker_News__S3_DB
    http_content : Hacker_News__Http_Content

    def files_paths__latest(self):
        with self.s3_db as _:
            latest_feed_xml  = _.s3_path__raw_data__feed_xml__now()
            latest_feed_data = _.s3_path__raw_data__feed_data__now()
        return dict(latest_feed_xml  =latest_feed_xml  ,
                    latest_feed_data =latest_feed_data )

    def xml_feed__raw_data__current(self, refresh=False):
        xml_feed = self.s3_db.raw_data__feed__load__current()
        if refresh or not xml_feed:
            with capture_duration() as duration:
                feed_xml      = self.http_content.feed_content()
            kwargs = dict(created_by = RAW_FEED__CREATED__BY,
                          duration   = duration.seconds     ,
                          feed_xml   = feed_xml             )
            raw_data_feed = Model__Hacker_News__Raw_Data__Feed(**kwargs)
            self.s3_db.raw_data__feed__save(raw_data_feed)
            xml_feed = self.s3_db.raw_data__feed__load__current()
        return xml_feed

    def xml_feed__raw_data__from_date(self, year:int, month:int, day:int, hour:int):
        return self.s3_db.raw_data__feed__load__from_date(year, month, day, hour)

    def feed_data__current(self, refresh=False) -> Model__Hacker_News__Data__Feed:
        feed_data = self.s3_db.feed_data__load__current()
        if refresh or not feed_data:
            feed_raw_data = self.xml_feed__raw_data__current()
            if feed_raw_data:
                parser = Hacker_News__Parser().setup(feed_raw_data.feed_xml)
                kwargs = dict(created_by = feed_raw_data.created_by,
                              duration   = feed_raw_data.duration  ,
                              feed_data  = parser.parse_feed()    )
                feed_data = Model__Hacker_News__Data__Feed(**kwargs)
                self.s3_db.feed_data__save(feed_data)
                feed_data = self.s3_db.feed_data__load__current()
        return feed_data

    def feed_data__from_date(self, year:int, month:int, day:int, hour:int):
        feed_data = self.s3_db.feed_data__load__from_date(year, month, day, hour)
        if not feed_data:
            feed_raw_data = self.xml_feed__raw_data__from_date(year, month, day, hour)
            if feed_raw_data:
                parser = Hacker_News__Parser().setup(feed_raw_data.feed_xml)
                kwargs = dict(created_by = feed_raw_data.created_by,
                              duration   = feed_raw_data.duration  ,
                              feed_data  = parser.parse_feed()    )
                feed_data = Model__Hacker_News__Data__Feed(**kwargs)
                self.s3_db.feed_data__save(feed_data)
                feed_data = self.s3_db.feed_data__load__current()
        return feed_data
