from cbr_custom_news_feeds.providers.cyber_security.hacker_news.Hacker_News__S3__Key_Generator              import Hacker_News__S3__Key_Generator
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.models.Model__Hacker_News__Areas            import Model__Hacker_News__Areas
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.models.Model__Hacker_News__Raw_Data__Feed   import Model__Hacker_News__Raw_Data__Feed
from osbot_aws.aws.s3.S3__DB_Base                                                                           import S3__DB_Base
from osbot_utils.decorators.methods.type_safe                                                               import type_safe
from osbot_utils.utils.Http                                                                                 import url_join_safe

S3_BUCKET_PREFIX__NEWS_FEEDS  = 'news-feeds'
S3_BUCKET_SUFFIX__HACKER_NEWS = 'hacker-news'
S3_FILE_NAME__FEED_XML        = 'feed_xml'

class Hacker_News__S3_DB(S3__DB_Base):
    bucket_name__prefix   : str                = S3_BUCKET_PREFIX__NEWS_FEEDS
    bucket_name__suffix   : str                = S3_BUCKET_SUFFIX__HACKER_NEWS
    save_as_gz            : bool
    s3_key_generator      : Hacker_News__S3__Key_Generator

    def raw_data__all_files(self):
        return self.s3_folder_files__all(folder=self.s3_folder__for_raw_data(), full_path=False)

    @type_safe
    def raw_data__feed__save(self, raw_data_feed: Model__Hacker_News__Raw_Data__Feed):
        s3_path     = self.s3_path__raw_data__feed_xml__now()
        s3_key      = self.s3_key__for_path(s3_path)
        file_data   = raw_data_feed.json()

        save_status = self.s3_save_data(file_data, s3_key)
        return dict(s3_path     = s3_path     ,
                    file_data   = file_data  ,
                    save_status = save_status)

    def raw_data__feed__load__current(self):
        s3_path        = self.s3_path__raw_data__feed_xml__now()
        raw_data_feed = self.raw_data__feed__load__from_path(s3_path)
        return raw_data_feed

    def raw_data__feed__load__from_path(self, s3_path:str):
        s3_key        = self.s3_key__for_path(s3_path)
        file_data     = self.s3_file_data(s3_key)
        raw_data_feed = Model__Hacker_News__Raw_Data__Feed.from_json(file_data)
        return raw_data_feed

    def raw_data__feed__load__from_date(self, year:int, month:int, day:int, hour:int):
        s3_path = self.s3_key_generator.s3_path(year, month, day, hour, S3_FILE_NAME__FEED_XML)
        return self.raw_data__feed__load__from_path(s3_path)

    # methods for s3 folders and files

    def s3_folder__for_raw_data(self):
        return self.s3_key_generator.s3_folder__for_area(area=Model__Hacker_News__Areas.RAW_DATA)

    def s3_key__for_path(self, s3_path):
        return url_join_safe(self.s3_folder__for_raw_data(), s3_path)

    def s3_key__raw_data__feed_xml(self):
         return self.s3_key_generator.s3_key(area=Model__Hacker_News__Areas.RAW_DATA, file_id=S3_FILE_NAME__FEED_XML)

    def s3_path__raw_data__feed_xml__now(self):
        return self.s3_key_generator.s3_path__now(file_id=S3_FILE_NAME__FEED_XML)