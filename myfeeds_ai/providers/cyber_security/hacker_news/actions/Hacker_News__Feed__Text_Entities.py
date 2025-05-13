from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                        import S3_Key__File__Extension, S3_Key__File__Content_Type
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage               import Hacker_News__Storage
from myfeeds_ai.providers.cyber_security.hacker_news.config.Config__Hacker_News                 import FILE_ID__FEED__TEXT_ENTITIES__TITLES, FILE_ID__FEED__TEXT_ENTITIES__DESCRIPTIONS, FILE_ID__FEED__TEXT_ENTITIES, FILE_ID__FEED__TEXT_ENTITIES__TITLES__TREE, FILE_ID__FEED__TEXT_ENTITIES__FILES
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File                    import Hacker_News__File
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Text_Entities__Files import Schema__Feed__Text_Entities__Files
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe


class Hacker_News__Feed__Text_Entities(Type_Safe):
    hacker_news_storage: Hacker_News__Storage

    def file__feed_text_entities__files(self) -> Hacker_News__File:
        kwargs_file = dict(file_id   = FILE_ID__FEED__TEXT_ENTITIES__FILES,
                           extension = S3_Key__File__Extension.JSON,
                           data_type = Schema__Feed__Text_Entities__Files)
        return Hacker_News__File(**kwargs_file)

    def file__feed_text_entities(self) -> Hacker_News__File:
        return Hacker_News__File(file_id=FILE_ID__FEED__TEXT_ENTITIES, extension=S3_Key__File__Extension.MGRAPH__JSON)

    def file__feed_text_entities_descriptions(self) -> Hacker_News__File:
        return Hacker_News__File(file_id=FILE_ID__FEED__TEXT_ENTITIES__DESCRIPTIONS, extension=S3_Key__File__Extension.MGRAPH__JSON)

    def file__feed_text_entities_titles(self) -> Hacker_News__File:
        return Hacker_News__File(file_id=FILE_ID__FEED__TEXT_ENTITIES__TITLES, extension=S3_Key__File__Extension.MGRAPH__JSON)

    def file__feed_text_entities_titles__tree(self):
        return Hacker_News__File(file_id=FILE_ID__FEED__TEXT_ENTITIES__TITLES__TREE, extension=S3_Key__File__Extension.TXT, content_type=S3_Key__File__Content_Type.TXT)


    def text_entities__files(self) -> Schema__Feed__Text_Entities__Files:
        return self.file__feed_text_entities__files().data()

    def mgraph__entities__titles(self):
        with self.text_entities__files() as _:
            path_now__text_entities__titles = _.path_now__text_entities__titles
            if path_now__text_entities__titles:
                entities__titles = self.hacker_news_storage.path__load_data(path_now__text_entities__titles)
                return entities__titles

    def tree_view__entities__titles(self):
        with self.text_entities__files() as _:
            path_now__text_entities__titles__tree = _.path_now__text_entities__titles__tree
            if path_now__text_entities__titles__tree:
                tree_view__entities__titles = self.hacker_news_storage.path__load_data(path_now__text_entities__titles__tree, content_type=S3_Key__File__Content_Type.TXT)
                if tree_view__entities__titles:
                    return tree_view__entities__titles.decode()

