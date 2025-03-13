from myfeeds_ai.providers.cyber_security.hacker_news.config.Config__Hacker_News import FILE_ID__ARTICLE__ENTITIES__TEXT
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Article__Entity import Hacker_News__File__Article__Entity
from myfeeds_ai.utils.My_Feeds__Utils import path_to__date_time
from osbot_utils.helpers.Obj_Id                                                               import Obj_Id
from osbot_utils.type_safe.Type_Safe                                                          import Type_Safe


class Hacker_News__Article__Entities(Type_Safe):
    article_id        : Obj_Id
    path__folder__data: str

    def file___entities__text(self):
        kwargs = dict(article_id = self.article_id                  ,
                      file_id    = FILE_ID__ARTICLE__ENTITIES__TEXT ,
                      now        = self.now()                       )
        return Hacker_News__File__Article__Entity(**kwargs)

    def now(self):
        if self.path__folder__data:
            return path_to__date_time(self.path__folder__data)