from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                        import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.config.Config__Hacker_News import \
    FILE_ID__FEED__TEXT_ENTITIES__TITLES, FILE_ID__FEED__TEXT_ENTITIES__DESCRIPTIONS, FILE_ID__FEED__TEXT_ENTITIES, \
    FILE_ID__FEED__TEXT_ENTITIES__TITLES__TREE
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File    import Hacker_News__File
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe


class Hacker_News__Feed__Text_Entities(Type_Safe):

    def file__feed_text_entities(self):
        return Hacker_News__File(file_id=FILE_ID__FEED__TEXT_ENTITIES              , extension=S3_Key__File_Extension.MGRAPH__JSON)

    def file__feed_text_entities_descriptions(self):
        return Hacker_News__File(file_id=FILE_ID__FEED__TEXT_ENTITIES__DESCRIPTIONS, extension=S3_Key__File_Extension.MGRAPH__JSON)

    def file__feed_text_entities_titles(self):
        return Hacker_News__File(file_id=FILE_ID__FEED__TEXT_ENTITIES__TITLES       , extension=S3_Key__File_Extension.MGRAPH__JSON)

    def file__feed_text_entities_titles__tree(self):
        return Hacker_News__File(file_id=FILE_ID__FEED__TEXT_ENTITIES__TITLES__TREE , extension=S3_Key__File_Extension.TXT, content_type="text/plain; charset=utf-8")