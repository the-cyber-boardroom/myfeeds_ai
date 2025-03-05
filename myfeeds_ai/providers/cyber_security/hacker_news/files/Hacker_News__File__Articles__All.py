from myfeeds_ai.providers.cyber_security.hacker_news.config.Config__Hacker_News         import FILE_ID__ARTICLES__ALL
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles  import Hacker_News__File__Articles
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article      import Schema__Feed__Article


class Hacker_News__File__Articles__All(Hacker_News__File__Articles):
    file_id = FILE_ID__ARTICLES__ALL

    def add_article(self, article: Schema__Feed__Article):
        self.load()
        self.articles.articles[article.article_id] = article
        self.save()
