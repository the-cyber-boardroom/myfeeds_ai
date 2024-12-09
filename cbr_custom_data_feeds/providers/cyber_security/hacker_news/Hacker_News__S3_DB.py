from cbr_custom_data_feeds.config.Custom_News__Shared_Constants                                            import S3_BUCKET_PREFIX__NEWS_FEEDS, S3_BUCKET_SUFFIX__HACKER_NEWS, S3_FILE_NAME__RAW__FEED_XML, S3_FILE_NAME__RAW__FEED_DATA, S3_FOLDER_NAME__LATEST
from cbr_custom_data_feeds.providers.cyber_security.hacker_news.Hacker_News__S3__Key_Generator             import Hacker_News__S3__Key_Generator
from cbr_custom_data_feeds.providers.cyber_security.hacker_news.models.Model__Hacker_News__Data__Feed      import Model__Hacker_News__Data__Feed
from cbr_custom_data_feeds.providers.cyber_security.hacker_news.models.Model__Hacker_News__Raw_Data__Feed  import Model__Hacker_News__Raw_Data__Feed
from cbr_custom_data_feeds.providers.models.Model__Data_Feeds__Providers                                   import Model__Data_Feeds__Providers
from osbot_aws.aws.s3.S3__DB_Base                                                                          import S3__DB_Base
from osbot_utils.decorators.methods.type_safe                                                              import type_safe
from osbot_utils.utils.Http                                                                                import url_join_safe


class Hacker_News__S3_DB(S3__DB_Base):
    bucket_name__prefix   : str                = S3_BUCKET_PREFIX__NEWS_FEEDS
    bucket_name__suffix   : str                = S3_BUCKET_SUFFIX__HACKER_NEWS
    save_as_gz            : bool
    s3_key_generator      : Hacker_News__S3__Key_Generator

    def feed_data__load__current(self):
        s3_path = self.s3_path__raw_data__feed_data__now()
        return self.feed_data__load__from_path(s3_path)

    def feed_data__load__from_path(self, s3_path):
        s3_key    = self.s3_key__for_path__raw_data(s3_path)
        file_data = self.s3_file_data(s3_key)
        data_feed = Model__Hacker_News__Data__Feed.from_json(file_data)
        return data_feed

    def feed_data__load__from_date(self, year:int, month:int, day:int, hour:int):
        s3_path = self.s3_key_generator.s3_path(year, month, day, hour, S3_FILE_NAME__RAW__FEED_DATA)
        return self.feed_data__load__from_path(s3_path)


    @type_safe
    def feed_data__save(self, data_feed: Model__Hacker_News__Data__Feed):
        s3_path             = self.s3_path__raw_data__feed_data__now()
        s3_path_latest      = self.s3_path__raw_data__feed_data__latest()
        s3_key              = self.s3_key__for_path__raw_data(s3_path)
        s3_key_latest       = self.s3_key__for_path__raw_data(s3_path_latest)
        data_feed.file_path = s3_path                                       # set this value here
        file_data = data_feed.json()

        self.s3_save_data(file_data, s3_key       )
        self.s3_save_data(file_data, s3_key_latest)

        return dict(s3_path     = s3_path,
                    file_data   = file_data)

    def raw_data__all_files(self):
        return self.s3_folder_files__all(folder=self.s3_folder__for_raw_data(), full_path=False)

    @type_safe
    def raw_data__feed__save(self, raw_data_feed: Model__Hacker_News__Raw_Data__Feed):
        s3_path        = self.s3_path__raw_data__feed_xml__now   ()
        s3_path_latest = self.s3_path__raw_data__feed_xml__latest()
        s3_key         = self.s3_key__for_path__raw_data(s3_path)
        s3_key_latest  = self.s3_key__for_path__raw_data(s3_path_latest)

        file_data   = raw_data_feed.json()
        self.s3_save_data(file_data, s3_key        )
        self.s3_save_data(file_data, s3_key_latest )
        return dict(s3_path     = s3_path          ,
                    file_data   = file_data        )

    def raw_data__feed__load__current(self):
        s3_path        = self.s3_path__raw_data__feed_xml__now()
        raw_data_feed = self.raw_data__feed__load__from_path(s3_path)
        return raw_data_feed

    def raw_data__feed__load__from_path(self, s3_path:str):
        s3_key        = self.s3_key__for_path__raw_data(s3_path)
        file_data     = self.s3_file_data(s3_key)
        raw_data_feed = Model__Hacker_News__Raw_Data__Feed.from_json(file_data)
        return raw_data_feed

    def raw_data__feed__load__from_date(self, year:int, month:int, day:int, hour:int):
        s3_path = self.s3_key_generator.s3_path(year, month, day, hour, S3_FILE_NAME__RAW__FEED_XML)
        return self.raw_data__feed__load__from_path(s3_path)

    # methods for s3 folders and files

    def s3_folder__for_raw_data(self):
        return self.s3_key_generator.s3_folder__for_area(area=Model__Data_Feeds__Providers.HACKER_NEWS)

    def s3_key__for_path__raw_data(self, s3_path):
        return url_join_safe(self.s3_folder__for_raw_data(), s3_path)

    def s3_key__raw_data__feed_xml(self):
         return self.s3_key_generator.s3_key(area=Model__Data_Feeds__Providers.HACKER_NEWS, file_id=S3_FILE_NAME__RAW__FEED_XML)

    def s3_path__raw_data__feed_data__now(self):
        return self.s3_key_generator.s3_path__now(file_id=S3_FILE_NAME__RAW__FEED_DATA)

    def s3_path__raw_data__feed_xml__now(self):
        return self.s3_key_generator.s3_path__now(file_id=S3_FILE_NAME__RAW__FEED_XML)

    def s3_path__raw_data__feed_data__latest(self):
        return f'{S3_FOLDER_NAME__LATEST}/{S3_FILE_NAME__RAW__FEED_DATA}.json'

    def s3_path__raw_data__feed_xml__latest(self):
        return f'{S3_FOLDER_NAME__LATEST}/{S3_FILE_NAME__RAW__FEED_XML}.json'
