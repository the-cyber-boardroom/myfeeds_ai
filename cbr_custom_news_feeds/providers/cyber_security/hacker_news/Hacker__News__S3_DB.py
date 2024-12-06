from cbr_custom_news_feeds.providers.cyber_security.hacker_news.Hacker_News__S3__Key_Generator              import Hacker_News__S3__Key_Generator
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.models.Model__Hacker_News__Areas            import Model__Hacker_News__Areas
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.models.Model__Hacker_News__Raw_Data__Feed   import Model__Hacker_News__Raw_Data__Feed
from osbot_aws.aws.s3.S3__DB_Base                                                                           import S3__DB_Base
from osbot_utils.decorators.methods.type_safe                                                               import type_safe

S3_BUCKET_PREFIX__NEWS_FEEDS  = 'news-feeds'
S3_BUCKET_SUFFIX__HACKER_NEWS = 'hacker-news'
S3_FILE_NAME__FEED_XML        = 'feed_xml'

class Hacker_News__S3_DB(S3__DB_Base):
    bucket_name__prefix   : str                = S3_BUCKET_PREFIX__NEWS_FEEDS
    bucket_name__suffix   : str                = S3_BUCKET_SUFFIX__HACKER_NEWS
    save_as_gz            : bool
    s3_key_generator      : Hacker_News__S3__Key_Generator

    def raw_data__all_files(self):
        return self.s3_folder_files__all()
    @type_safe
    def raw_data__feed_xml__save(self, raw_data_feed: Model__Hacker_News__Raw_Data__Feed):
        s3_key = self.s3_key__for_raw_data__feed_xml()
        return s3_key
        #return self.s3_save_data(raw_data_feed, s3_key)

    def s3_folder__for_raw_data(self):
        return self.s3_key_generator.s3_folder__for_day()

    def s3_key__for_raw_data__feed_xml(self):
         return self.s3_key_generator.s3_key(area=Model__Hacker_News__Areas.RAW_DATA, file_id=S3_FILE_NAME__FEED_XML)
