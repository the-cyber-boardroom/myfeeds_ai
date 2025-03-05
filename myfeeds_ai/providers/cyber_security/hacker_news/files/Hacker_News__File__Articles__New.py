from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                    import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Live_Data         import Hacker_News__Live_Data
from myfeeds_ai.providers.cyber_security.hacker_news.config.Config__Hacker_News import FILE_ID__ARTICLES__CURRENT, \
    FILE_ID__ARTICLES__NEW
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File                import Hacker_News__File
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Config__New_Articles import \
    Schema__Feed__Config__New_Articles
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Articles import Schema__Feed__Articles


# todo: refactor to class that we only need to provide the file_id and the type (in this case Schema__Feed__Articles)
class Hacker_News__File__Articles__New(Hacker_News__File):
    file_id           = FILE_ID__ARTICLES__NEW
    extension         = S3_Key__File_Extension.JSON
    new_articles      : Schema__Feed__Config__New_Articles


    def load(self):
        json_data = super().load()
        if json_data:                                                                       # if it exists
            self.new_articles = Schema__Feed__Config__New_Articles.from_json(json_data)     #   load data and assign it to self.current_articles
        return self.new_articles                                                            # if not, return the default value of self.current_articles

    def save(self):
        if self.new_articles:
            self.file_data = self.new_articles.json()
            super().save()

    def save_data(self, data):
        self.new_articles = Schema__Feed__Config__New_Articles.from_json(data)
        self.save()