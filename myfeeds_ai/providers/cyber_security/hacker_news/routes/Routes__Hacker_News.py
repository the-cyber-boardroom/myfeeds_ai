from osbot_fast_api.api.Fast_API_Routes                                                   import Fast_API_Routes
from starlette.responses                                                                  import PlainTextResponse
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Files        import Hacker_News__Files
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Http_Content import Hacker_News__Http_Content
from osbot_utils.utils.Lists                                                              import list_filter_contains
from osbot_utils.utils.Status                                                             import status_ok, status_error

ROUTE_PATH__HACKER_NEWS = 'hacker-news'

ROUTES_PATHS__HACKER_NEWS = [ f'/{ROUTE_PATH__HACKER_NEWS}/data-feed'              ,
                              f'/{ROUTE_PATH__HACKER_NEWS}/data-feed-current'      ,
                              f'/{ROUTE_PATH__HACKER_NEWS}/feed'                   ,
                              f'/{ROUTE_PATH__HACKER_NEWS}/feed-prompt'            ,
                              f'/{ROUTE_PATH__HACKER_NEWS}/files-paths'            ,
                              f'/{ROUTE_PATH__HACKER_NEWS}/raw-data-all-files'     ,
                              f'/{ROUTE_PATH__HACKER_NEWS}/raw-data-feed'          ,
                              f'/{ROUTE_PATH__HACKER_NEWS}/raw-data-feed-current'  ]


class Routes__Hacker_News(Fast_API_Routes):
    tag         : str                       = 'hacker-news'
    http_content: Hacker_News__Http_Content
    files       : Hacker_News__Files

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.files.s3_db.setup()

    def feed(self):                                         # Get the complete feed data
        return self.http_content.feed_data().json()

    def prompt_analysis(self, size:int=5):
        return { "prompt" : self.http_content.feed_prompt(size=size)}

    def files_paths(self):
        data = self.files.files_paths__latest()
        return status_ok(data=data)

    def data_feed(self, year:int, month:int, day:int, hour:int):
        kwargs = dict(year   = year ,
                      month  = month,
                      day    = day  ,
                      hour   = hour )
        data_feed = self.files.feed_data__from_date(**kwargs)
        if data_feed:
            return status_ok(data=data_feed.json())
        return status_error(f'No data found for {year}/{month}/{day}/{hour}')

    def data_feed_current(self):
        data_feed = self.files.feed_data__current()
        if data_feed:
            return status_ok(data=data_feed.json())
        return status_error(f'No data found')

    def feed_prompt(self, size:int=5):
        #return { "prompt" : self.http_content.get_prompt_schema(size=size) }
        return PlainTextResponse(self.http_content.feed_prompt(size=size))

    def raw_data_all_files(self, only_with:str = None):
        all_files = sorted(self.files.all_files(), reverse=True)
        if only_with:
            return list_filter_contains(all_files, only_with)
        return all_files

    def raw_data_feed_current(self, refresh:bool=False):
        raw_data_feed = self.files.xml_feed__raw_data__current(refresh=refresh)
        if raw_data_feed:
            return status_ok(data=raw_data_feed.json())
        return status_error(f'No data found')

    def raw_data_feed(self, year:int, month:int, day:int, hour:int):
        raw_data_feed = self.files.xml_feed__raw_data__from_date(year, month, day, hour)
        if raw_data_feed:
            return status_ok(data=raw_data_feed.json())
        return status_error(f'No data found for {year}/{month}/{day}/{hour}')

    def setup_routes(self):
        self.add_route_get(self.data_feed            )
        self.add_route_get(self.data_feed_current    )
        self.add_route_get(self.files_paths          )
        self.add_route_get(self.feed                 )
        self.add_route_get(self.feed_prompt          )
        self.add_route_get(self.raw_data_all_files   )
        self.add_route_get(self.raw_data_feed_current)
        self.add_route_get(self.raw_data_feed        )