from myfeeds_ai.data_feeds.Data_Feeds__Files                                                   import Data_Feeds__Files
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Http_Content                 import Hacker_News__Http_Content
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Parser                       import Hacker_News__Parser
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__S3_DB                        import Hacker_News__S3_DB
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Timeline__Png    import Hacker_News__File__Timeline__Png
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Data__Feed     import Model__Hacker_News__Data__Feed
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Raw_Data__Feed import Model__Hacker_News__Raw_Data__Feed
from osbot_utils.helpers.duration.decorators.capture_duration                                  import capture_duration

RAW_FEED__CREATED__BY = 'Hacker_News__Files.xml_feed__current'

# todo: this entire class needs to be refactored with just about all the logic moved into Flows
class Hacker_News__Files(Data_Feeds__Files):
    s3_db        : Hacker_News__S3_DB
    http_content : Hacker_News__Http_Content

    def files_paths__latest(self):
        with self.s3_db as _:
            now    = dict( feed_xml             = _.s3_path__raw_data__feed_xml__now       (),
                           feed_data            = _.s3_path__raw_data__feed_data__now      ())
                           # timeline_mgraph_dot  = _.s3_path__timeline__now__mgraph__dot    (),
                           # timeline_mgraph_json = _.s3_path__timeline__now__mgraph__json   (),
                           # timeline_mgraph_png  = _.s3_path__timeline__now__mgraph__png    ())
            latest = dict( feed_xml             = _.s3_path__raw_data__feed_xml__latest    (),
                           feed_data            = _.s3_path__raw_data__feed_data__latest   ())
                           # timeline_mgraph_dot  = _.s3_path__timeline__latest__mgraph__dot (),
                           # timeline_mgraph_json = _.s3_path__timeline__latest__mgraph__json(),
                           # timeline_mgraph_png  = _.s3_path__timeline__latest__mgraph__png ())
        return dict(now    = now    ,
                    latest = latest )

    def xml_feed__raw_data__current(self, refresh=False):
        xml_feed = self.s3_db.raw_data__feed__load__current()
        if refresh or not xml_feed or not xml_feed.feed_xml:
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
            feed_data = self.feed_data__load_rss_and_parse(refresh=refresh)
        return feed_data

    def feed_data__load_rss_and_parse(self, refresh=False):
        feed_raw_data = self.xml_feed__raw_data__current(refresh=refresh)
        if feed_raw_data.feed_xml == "":
            raise ValueError("in feed_data__current, the feed_raw_data.feed_xml was empty")
        if feed_raw_data:
            parser           = Hacker_News__Parser().setup(feed_raw_data.feed_xml)
            parsed_feed_data = parser.parse_feed()
            if len(parsed_feed_data.articles) ==0:
                raise ValueError("in feed_data__current len(parsed_feed_data.articles) was zero")
            kwargs = dict(created_by = feed_raw_data.created_by,
                          duration   = feed_raw_data.duration  ,
                          feed_data  = parsed_feed_data )
            feed_data = Model__Hacker_News__Data__Feed(**kwargs)
            self.s3_db.feed_data__save(feed_data)
            feed_data = self.s3_db.feed_data__load__current()
            return feed_data

    def feed_data__from_date(self, year:int, month:int, day:int, hour:int):
        feed_data = self.s3_db.feed_data__load__from_date(year, month, day, hour)
        if not feed_data:
            feed_raw_data = self.xml_feed__raw_data__from_date(year, month, day, hour)
            if feed_raw_data and feed_raw_data.feed_xml:
                parser = Hacker_News__Parser().setup(feed_raw_data.feed_xml)
                kwargs = dict(created_by = feed_raw_data.created_by,
                              duration   = feed_raw_data.duration  ,
                              feed_data  = parser.parse_feed()    )
                feed_data = Model__Hacker_News__Data__Feed(**kwargs)
                self.s3_db.feed_data__save(feed_data)
                feed_data = self.s3_db.feed_data__load__current()
        return feed_data

    def timeline_png__latest(self):
        with Hacker_News__File__Timeline__Png() as _:
            if _.exists():
                return _.load()