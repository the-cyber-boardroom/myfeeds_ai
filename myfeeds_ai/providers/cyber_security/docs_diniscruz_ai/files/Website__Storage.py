from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Providers                      import Model__Data_Feeds__Providers
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage   import Hacker_News__Storage


class Website__Storage(Hacker_News__Storage):
    def __init__(self, provider_name: Model__Data_Feeds__Providers,  **kwargs):
        super().__init__(**kwargs)
        self.s3_db.provider_name = provider_name