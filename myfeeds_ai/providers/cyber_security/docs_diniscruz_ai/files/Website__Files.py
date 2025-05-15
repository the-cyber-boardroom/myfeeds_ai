from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                            import S3_Key__File__Extension, S3_Key__File__Content_Type
from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Providers                      import Model__Data_Feeds__Providers
from myfeeds_ai.mgraphs.html_to_mgraph.Html_MGraph                                  import Html_MGraph
from myfeeds_ai.providers.cyber_security.docs_diniscruz_ai.files.Website__Storage   import Website__Storage
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File        import Hacker_News__File
from myfeeds_ai.shared.http.schemas.Schema__Http__Action                            import Schema__Http__Action
from osbot_utils.helpers.Safe_Id                                                    import Safe_Id
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe

FILE_ID__HOME_PAGE  = Safe_Id('homepage')

class Website__Files(Type_Safe):
    website_storage : Website__Storage

    def __init__(self, provider_name: Model__Data_Feeds__Providers, **kwargs):
        self.website_storage = Website__Storage(provider_name=provider_name)
        super().__init__(**kwargs)


    def file__home_page(self):
        kwargs_file = dict(file_id             = FILE_ID__HOME_PAGE             ,
                           extension           = S3_Key__File__Extension.JSON   ,
                           data_type           = Schema__Http__Action           ,
                           hacker_news_storage = self.website_storage           )
        return Hacker_News__File(**kwargs_file)

    def file__home_page__mgraph(self):
        kwargs_file = dict(file_id             = FILE_ID__HOME_PAGE                  ,
                           extension           = S3_Key__File__Extension.MGRAPH__JSON,
                           data_type           = Html_MGraph                         ,
                           hacker_news_storage = self.website_storage                )
        return Hacker_News__File(**kwargs_file)
