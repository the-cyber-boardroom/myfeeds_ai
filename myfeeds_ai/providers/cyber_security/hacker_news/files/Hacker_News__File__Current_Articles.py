from typing import Dict, List

from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                    import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.config.Config__Hacker_News             import FILE_ID__CURRENT_ARTICLES
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File                import Hacker_News__File
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Current_Articles import \
    Schema__Feed__Current_Articles, Schema__Feed__Current_Article__Status, Schema__Feed__Current_Article
from osbot_utils.utils.Lists import list_group_by


# todo: refactor to class that we only need to provide the file_id and the type (in this case Schema__Feed__Current_Articles)
class Hacker_News__File__Current_Articles(Hacker_News__File):
    file_id               = FILE_ID__CURRENT_ARTICLES
    extension             = S3_Key__File_Extension.JSON
    current_articles      : Schema__Feed__Current_Articles

    def load(self):
        json_data = super().load()
        if json_data:                                                                       # if it exists
            self.current_articles = Schema__Feed__Current_Articles.from_json(json_data)     #   load data and assign it to self.current_articles
        return self.current_articles                                                        # if not, return the default value of self.current_articles

    def save(self):
        if self.current_articles:
            self.file_data = self.current_articles.json()
            super().save()

    def group_by_status(self) -> Dict[str, List[Schema__Feed__Current_Article]]:                                        # Group current articles by their status, preserving the typed objects.
        results = {}
        if self.current_articles and self.current_articles.articles:
            for article_id, article in self.current_articles.articles.items():
                status_name = article.status.name
                if status_name not in results:
                    results[status_name] = []
                results[status_name].append(article)
        return results

    def to__process(self) -> List[Schema__Feed__Current_Article]:
        status = Schema__Feed__Current_Article__Status.TO_PROCESS.name
        return self.group_by_status().get(status, [])


        # self.current_articles = self.hacker_news_data.current_articles()
        # for article_id, article in self.current_articles.articles.items():
        #     if article.status == Schema__Feed__Current_Article__Status.TO_PROCESS:
        #         self.articles_to_process[article_id]=article
