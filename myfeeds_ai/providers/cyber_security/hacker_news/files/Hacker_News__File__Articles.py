from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                            import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File        import Hacker_News__File
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Articles import Schema__Feed__Articles


# todo: refactor to class that we only need to provide the file_id and the type (in this case Schema__Feed__Articles)
class Hacker_News__File__Articles(Hacker_News__File):
    extension     = S3_Key__File_Extension.JSON
    articles      : Schema__Feed__Articles

    def load(self):
        json_data = super().load()
        if json_data:                                                                       # if it exists
            self.articles = Schema__Feed__Articles.from_json(json_data)     #   load data and assign it to self.current_articles
        return self.articles                                                        # if not, return the default value of self.current_articles

    def save(self):
        if self.articles:
            self.file_data = self.articles.json()
            return super().save()