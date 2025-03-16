from io                                                                                                   import BytesIO
from osbot_fast_api.api.Fast_API_Routes                                                                   import Fast_API_Routes
from starlette.responses                                                                                  import PlainTextResponse, StreamingResponse
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Files                                   import Hacker_News__Files
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Http_Content                            import Hacker_News__Http_Content
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Data                            import Hacker_News__Data
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__2__Create_Articles_Timeline import Flow__Hacker_News__2__Create_Articles_Timeline
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__1__Download_RSS_Feed        import Flow__Hacker_News__1__Download_RSS_Feed
from osbot_utils.helpers.safe_str.Safe_Str__File__Path import Safe_Str__File__Path
from osbot_utils.utils.Lists                                                                              import list_filter_contains
from osbot_utils.utils.Status                                                                             import status_ok, status_error

ROUTE_PATH__HACKER_NEWS = 'hacker-news'

ROUTES_PATHS__HACKER_NEWS = [ f'/{ROUTE_PATH__HACKER_NEWS}/data-feed'             ,
                              f'/{ROUTE_PATH__HACKER_NEWS}/data-feed-current'     ,
                              f'/{ROUTE_PATH__HACKER_NEWS}/timeline-latest-png'   ,
                              f'/{ROUTE_PATH__HACKER_NEWS}/feed'                  ,
                              f'/{ROUTE_PATH__HACKER_NEWS}/feed-prompt'           ,
                              #f'/{ROUTE_PATH__HACKER_NEWS}/flow-new-articles'     ,
                              # f'/{ROUTE_PATH__HACKER_NEWS}/flow-process-articles' ,
                              f'/{ROUTE_PATH__HACKER_NEWS}/flow-process-rss'      ,
                              # f'/{ROUTE_PATH__HACKER_NEWS}/flow-graph-rag-mgraphs',
                              f'/{ROUTE_PATH__HACKER_NEWS}/files-paths'           ,
                              f'/{ROUTE_PATH__HACKER_NEWS}/new-articles'          ,
                              f'/{ROUTE_PATH__HACKER_NEWS}/files-in-day'          ,
                              f'/{ROUTE_PATH__HACKER_NEWS}/raw-data-all-files'    ,
                              f'/{ROUTE_PATH__HACKER_NEWS}/raw-data-feed'         ,
                              f'/{ROUTE_PATH__HACKER_NEWS}/raw-data-feed-current' ]


class Routes__Hacker_News(Fast_API_Routes):
    tag                 : str                       = 'hacker-news'
    http_content        : Hacker_News__Http_Content
    files               : Hacker_News__Files
    hacker_news_data    : Hacker_News__Data


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

    def flow_process_rss(self):
        flow_process_rss        = Flow__Hacker_News__1__Download_RSS_Feed         ().run().flow_return_value
        flow__articles_timeline = Flow__Hacker_News__2__Create_Articles_Timeline().run().flow_return_value
        # flow_new_articles     = Flow__Hacker_News__Extract_New_Articles().run().flow_return_value
        # flow_process_articles = Flow__Hacker_News__Process_Articles    ().run().flow_return_value
        return dict(flow_process_rss      = flow_process_rss        ,
                    flow__articles_timeline = flow__articles_timeline)
                    # flow_new_articles     = flow_new_articles       ,
                    # flow_process_articles = flow_process_articles   )

    # def flow_new_articles(self, current__path:str ='2025/02/23/22'):
    #     flow = Flow__Hacker_News__3__Extract_New_Articles(current__path=current__path)
    #     flow.run()
    #     return flow.new__config_new_articles.json()



    # def flow_graph_rag_mgraphs(self):
    #     flow = Flow__Hacker_News__Create__Graph_RAG__MGraphs()
    #     flow.run()
    #     return flow.result__processed_files

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
        data_feed = self.files.feed_data__current(refresh=False)
        if data_feed:
            return status_ok(data=data_feed.json())
        return status_error(f'No data found')

    def feed_prompt(self, size:int=5):
        #return { "prompt" : self.http_content.get_prompt_schema(size=size) }
        return PlainTextResponse(self.http_content.feed_prompt(size=size))

    # def current_articles(self):
    #     return self.hacker_news_data.current_articles().json()

    def new_articles(self):
        return self.hacker_news_data.new_articles().json()

    def timeline_latest_png(self):
        bytes__timeline = self.files.timeline_png__latest()
        img_io          = BytesIO(bytes__timeline)  # Wrap in memory stream
        img_io.seek(0)  # Reset stream position
        return StreamingResponse(img_io, media_type="image/png")

    # def graph_entities_png(self, path='2025/02/19/22/articles/b65f80c0'):
    #     path += '/graph-entities.mgraph.png'
    #     from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage import Hacker_News__Storage
    #     png_bytes = Hacker_News__Storage().path__load_bytes(path)
    #     img_io = BytesIO(png_bytes)                                 # Wrap in memory stream
    #     img_io.seek(0)                                              # Reset stream position
    #     return StreamingResponse(img_io, media_type="image/png")


    def files_in_day(self, day: str='2025/03/13/23', include_sub_folders: bool =False):
        path   = Safe_Str__File__Path(day)
        files = self.hacker_news_data.storage.files_in__path(path=path, include_sub_folders=include_sub_folders)
        return sorted(files)

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
        self.add_route_get(self.data_feed             )
        self.add_route_get(self.data_feed_current     )
        self.add_route_get(self.files_paths           )
        #self.add_route_get(self.flow_new_articles     )
        #self.add_route_get(self.flow_process_articles )
        self.add_route_get(self.flow_process_rss      )
        #self.add_route_get(self.flow_graph_rag_mgraphs)
        self.add_route_get(self.feed                  )
        self.add_route_get(self.feed_prompt           )
        self.add_route_get(self.new_articles          )
        self.add_route_get(self.timeline_latest_png   )
        self.add_route_get(self.files_in_day          )
        self.add_route_get(self.raw_data_all_files    )
        self.add_route_get(self.raw_data_feed_current )
        self.add_route_get(self.raw_data_feed         )