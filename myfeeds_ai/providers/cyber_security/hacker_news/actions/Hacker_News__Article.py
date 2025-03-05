from myfeeds_ai.providers.cyber_security.hacker_news.config.Config__Hacker_News         import FILE_ID__FEED_ARTICLE
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Article   import Hacker_News__File__Article
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Article import Model__Hacker_News__Article
from myfeeds_ai.utils.My_Feeds__Utils import path_to__date_time
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.helpers.Obj_Id                                                         import Obj_Id
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe


class Hacker_News__Article(Type_Safe):
    article_id         : Obj_Id
    path__folder__data : str

    def __init__(self, article_id: Obj_Id, **kwargs) -> None:
        self.article_id = article_id
        super().__init__(**kwargs)

    def now(self):
        if self.path__folder__data:
            return path_to__date_time(self.path__folder__data)

    @cache_on_self
    def file_article(self):
        return Hacker_News__File__Article(article_id=self.article_id, file_id=FILE_ID__FEED_ARTICLE, now=self.now())

    def article_data__save(self, article_data: Model__Hacker_News__Article):
        file_article = self.file_article()
        data         = article_data.json()
        article_path = file_article.save_data(data)
        return article_path
