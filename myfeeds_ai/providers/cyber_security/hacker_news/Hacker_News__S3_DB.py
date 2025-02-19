from myfeeds_ai.data_feeds.Data_Feeds__S3_DB                                                    import Data_Feeds__S3_DB
from myfeeds_ai.data_feeds.Data_Feeds__Shared_Constants                                         import S3_FILE_NAME__RAW__FEED_DATA, S3_FILE_NAME__RAW__FEED_XML, S3_FOLDER_NAME__LATEST, S3_FOLDER_NAME__ARTICLES
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Data__Feed      import Model__Hacker_News__Data__Feed
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Raw_Data__Feed  import Model__Hacker_News__Raw_Data__Feed
from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Providers                                  import Model__Data_Feeds__Providers
from osbot_utils.helpers.Obj_Id                                                                 import Obj_Id
from osbot_utils.type_safe.decorators.type_safe                                                 import type_safe
from osbot_utils.utils.Http                                                                     import url_join_safe

S3_FILE_NAME__ARTICLE__FEED_ARTICLE = 'feed-article'

class Hacker_News__S3_DB(Data_Feeds__S3_DB):
    provider_name = Model__Data_Feeds__Providers.HACKER_NEWS

    def feed_data__load__current(self):
        s3_path = self.s3_path__raw_data__feed_data__now()
        return self.feed_data__load__from_path(s3_path)

    def feed_data__load__from_path(self, s3_path):
        s3_key    = self.s3_key__for_provider_path(s3_path)
        file_data = self.s3_file_data(s3_key)
        if file_data:
            data_feed = Model__Hacker_News__Data__Feed.from_json(file_data)
            return data_feed

    def feed_data__load__from_date(self, year:int, month:int, day:int, hour:int):
        s3_path = self.s3_key_generator.s3_path(year, month, day, hour, S3_FILE_NAME__RAW__FEED_DATA)
        return self.feed_data__load__from_path(s3_path)


    @type_safe
    def feed_data__save(self, data_feed: Model__Hacker_News__Data__Feed):
        s3_path             = self.s3_path__raw_data__feed_data__now()
        s3_path_latest      = self.s3_path__raw_data__feed_data__latest()
        s3_key              = self.s3_key__for_provider_path(s3_path)
        s3_key_latest       = self.s3_key__for_provider_path(s3_path_latest)
        data_feed.file_path = s3_path                                       # set this value here
        file_data = data_feed.json()

        self.s3_save_data(file_data, s3_key       )
        self.s3_save_data(file_data, s3_key_latest)

        return dict(s3_path     = s3_path,
                    file_data   = file_data)



    @type_safe
    def raw_data__feed__save(self, raw_data_feed: Model__Hacker_News__Raw_Data__Feed):
        s3_path        = self.s3_path__raw_data__feed_xml__now   ()
        s3_path_latest = self.s3_path__raw_data__feed_xml__latest()
        s3_key         = self.s3_key__for_provider_path(s3_path)
        s3_key_latest  = self.s3_key__for_provider_path(s3_path_latest)

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
        s3_key        = self.s3_key__for_provider_path(s3_path)
        file_data     = self.s3_file_data(s3_key)
        raw_data_feed = Model__Hacker_News__Raw_Data__Feed.from_json(file_data)
        return raw_data_feed

    def raw_data__feed__load__from_date(self, year:int, month:int, day:int, hour:int):
        s3_path = self.s3_key_generator.s3_path(year, month, day, hour, S3_FILE_NAME__RAW__FEED_XML)
        return self.raw_data__feed__load__from_path(s3_path)

    # methods for s3 folders and files

    def s3_path__article__now(self, article_obj_id: Obj_Id):
        articles_folder = self.s3_path__articles__now()
        article_folder  = url_join_safe(articles_folder, article_obj_id)
        return article_folder

    def s3_path__articles__now(self):
        return self.s3_key_generator.s3_path__folder__now(folder_id=S3_FOLDER_NAME__ARTICLES)

    def s3_path__when(self):
        return self.s3_key_generator.path__for_date_time__now_utc()

    def s3_path__latest(self, file_id):
        return url_join_safe(S3_FOLDER_NAME__LATEST, file_id + '.json')

    def s3_path__raw_data__feed_data__now(self):
        return self.s3_key_generator.s3_path__now(file_id=S3_FILE_NAME__RAW__FEED_DATA)

    def s3_path__raw_data__feed_xml__now(self):
        return self.s3_key_generator.s3_path__now(file_id=S3_FILE_NAME__RAW__FEED_XML)

    def s3_path__raw_data__feed_data__latest(self):
        return f'{S3_FOLDER_NAME__LATEST}/{S3_FILE_NAME__RAW__FEED_DATA}.json'

    def s3_path__raw_data__feed_xml__latest(self):
        return f'{S3_FOLDER_NAME__LATEST}/{S3_FILE_NAME__RAW__FEED_XML}.json'

    def s3_key___article__feed_article__now(self, article_obj_id: Obj_Id):
        s3_folder__article = self.s3_path__article__now(article_obj_id)
        return url_join_safe(s3_folder__article,S3_FILE_NAME__ARTICLE__FEED_ARTICLE + '.json')

    def s3_key__raw_data__feed_xml(self):
         return self.s3_key_generator.s3_key(area=Model__Data_Feeds__Providers.HACKER_NEWS, file_id=S3_FILE_NAME__RAW__FEED_XML)