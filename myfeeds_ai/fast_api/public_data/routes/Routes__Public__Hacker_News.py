from fastapi                                                                        import Path
from fastapi.responses                                                              import Response
from osbot_utils.utils.Status                                                       import status_error
from osbot_fast_api.api.Fast_API_Routes                                             import Fast_API_Routes
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Files             import Hacker_News__Files
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage   import Hacker_News__Storage


ROUTES__TAG__PUBLIC__HACKER_NEWS   = 'hacker-news'
ROUTES__PATHS__PUBLIC__HACKER_NEWS = [f'/{ROUTES__TAG__PUBLIC__HACKER_NEWS}/ping']

class Routes__Public__Hacker_News(Fast_API_Routes):
    tag                 : str                = ROUTES__TAG__PUBLIC__HACKER_NEWS
    hacker_news_storage : Hacker_News__Storage

    files: Hacker_News__Files

    def latest__feed_data(self):
        data_feed = self.files.feed_data__current()
        if data_feed:
            return data_feed.json()
        return {}

    def file_exists(self, file_path: str = Path(...)):
        with self.hacker_news_storage as _:
            return {'file_exists': _.path__exists(file_path),
                    'file_path'  : file_path                }

    def file_info(self, file_path: str = Path(...)):
        with self.hacker_news_storage as _:
            if _.path__exists(file_path):
                return _.path__file_info(file_path)
            return status_error(error='file not found', data=dict(file_path=file_path))

    def file_contents(self, file_path: str = Path(...)):
        with self.hacker_news_storage as _:
            if _.path__exists(file_path):
                file_info    = _.path__file_info(file_path)
                content_type = file_info.get('ContentType')
                bytes_data   = _.path__load_bytes(file_path)
                return Response(content    = bytes_data  ,
                                media_type = content_type)
            else:
                return status_error(error='file not found', data=dict(file_path=file_path))

    def ping(self):
        return 'pong'

    def setup_routes(self):
        self.add_route_get       (self.ping)
        self.router.add_api_route(path='/latest/feed-data.json'  , endpoint=self.latest__feed_data, methods=['GET'])
        self.router.add_api_route(path='/{file_path:path}/exists', endpoint=self.file_exists      , methods=['GET'])
        self.router.add_api_route(path='/{file_path:path}/info'  , endpoint=self.file_info        , methods=['GET'])
        self.router.add_api_route(path='/{file_path:path}'       , endpoint=self.file_contents    , methods=['GET'])

