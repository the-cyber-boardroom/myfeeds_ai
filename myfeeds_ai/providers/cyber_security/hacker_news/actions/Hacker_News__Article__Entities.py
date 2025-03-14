from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.config.Config__Hacker_News import \
    FILE_ID__ARTICLE__TEXT__ENTITIES__TITLE, FILE_ID__ARTICLE__TEXT__ENTITIES__DESCRIPTION
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Article__Text_Entities import Hacker_News__File__Article__Text_Entities
from myfeeds_ai.providers.cyber_security.hacker_news.llms.prompts.LLM__Prompt__Extract_Entities import \
    LLM__Prompt__Extract_Entities
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Text__Entities import \
    Schema__Feed__Article__Text__Entities
from myfeeds_ai.utils.My_Feeds__Utils import path_to__date_time
from osbot_utils.helpers.Obj_Id                                                                      import Obj_Id
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe


class Hacker_News__Article__Entities(Type_Safe):
    article_id              : Obj_Id
    path__folder__data      : str
    prompt_extract_entities : LLM__Prompt__Extract_Entities

    def file___text__entities__description(self):
        kwargs = dict(article_id = self.article_id                               ,
                      file_id    = FILE_ID__ARTICLE__TEXT__ENTITIES__DESCRIPTION ,
                      now        = self.now()                                    )
        return Hacker_News__File__Article__Text_Entities(**kwargs)

    def file___text__entities__title(self):
        kwargs = dict(article_id = self.article_id                         ,
                      file_id    = FILE_ID__ARTICLE__TEXT__ENTITIES__TITLE ,
                      now        = self.now()                              )
        return Hacker_News__File__Article__Text_Entities(**kwargs)

    def file___text__entities__title__png(self):
        with self.file___text__entities__title() as _:
            _.extension     = S3_Key__File_Extension.PNG
            _.content_type = "image/png"
            return _

    def file___text__entities__description__png(self):
        with self.file___text__entities__description() as _:
            _.extension     = S3_Key__File_Extension.PNG
            _.content_type = "image/png"
            return _

    def create_text_entities_graph__title(self):
        title__json_data              = self.file___text__entities__title().load()
        title__text_entities          = Schema__Feed__Article__Text__Entities.from_json(title__json_data).text_entities
        title__text_entities.entities = title__text_entities.entities

        with self.file___text__entities__title__png() as _:
            if _.exists() is False:
                png_bytes = self.prompt_extract_entities.create_entities_png_bytes(entities=title__text_entities)
                return _.save_data(png_bytes)
            return _.path_now()

    def create_text_entities_graph__description(self):
        description__json_data              = self.file___text__entities__description().load()
        description__text_entities          = Schema__Feed__Article__Text__Entities.from_json(description__json_data).text_entities
        description__text_entities.entities = description__text_entities.entities

        with self.file___text__entities__description__png() as _:
            if _.exists() is False:
                png_bytes = self.prompt_extract_entities.create_entities_png_bytes(entities=description__text_entities)
                return _.save_data(png_bytes)
            return _.path_now()


    def now(self):
        if self.path__folder__data:
            return path_to__date_time(self.path__folder__data)