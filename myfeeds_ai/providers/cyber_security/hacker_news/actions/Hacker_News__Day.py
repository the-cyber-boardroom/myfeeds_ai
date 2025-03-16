from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                        import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.config.Config__Hacker_News                 import FILE_ID__DAY__TEXT_ENTITIES
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Now               import Hacker_News__File__Now
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Day__Text_Entities    import Schema__Feed__Day__Text_Entities
from myfeeds_ai.utils.My_Feeds__Utils                                                           import path_to__date_time
from osbot_utils.helpers.safe_str.Safe_Str__File__Path                                          import Safe_Str__File__Path
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe


class Hacker_News__Day(Type_Safe):
    path__folder__data : Safe_Str__File__Path

    def now(self):
        if self.path__folder__data:
            return path_to__date_time(self.path__folder__data)

    def file_merged_day_entities(self):
        return Hacker_News__File__Now(file_id=FILE_ID__DAY__TEXT_ENTITIES, extension=S3_Key__File_Extension.JSON, now=self.now())

    def file_merged_day_entities__png(self):
        kwargs_file = dict(file_id      = FILE_ID__DAY__TEXT_ENTITIES       ,
                           extension    = S3_Key__File_Extension.MGRAPH__PNG,
                           content_type = "image/png"                       ,
                           now          = self.now()                        )

        return Hacker_News__File__Now(**kwargs_file)

    def file_merged_day_entities__load(self):
        with self.file_merged_day_entities() as _:
            if _.exists():
                json_data = _.load()
                return Schema__Feed__Day__Text_Entities.from_json(json_data)
        return Schema__Feed__Day__Text_Entities()