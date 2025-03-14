from myfeeds_ai.providers.cyber_security.hacker_news.config.Config__Hacker_News import \
    FILE_ID__ARTICLE__TEXT__ENTITIES__TITLE, FILE_ID__ARTICLE__TEXT__ENTITIES__DESCRIPTION
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Article__Text_Entities import Hacker_News__File__Article__Text_Entities
from myfeeds_ai.utils.My_Feeds__Utils import path_to__date_time
from osbot_utils.helpers.Obj_Id                                                                      import Obj_Id
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe


class Hacker_News__Article__Entities(Type_Safe):
    article_id        : Obj_Id
    path__folder__data: str

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


    def now(self):
        if self.path__folder__data:
            return path_to__date_time(self.path__folder__data)