from osbot_utils.type_safe.Type_Safe import Type_Safe
from osbot_utils.utils.Http          import GET_json

MY_FEEDS__SERVER                = 'https://dev.myfeeds.ai'
WEB_PATH__PUBLIC__HACKER_NEWS   = "public-data/hacker-news"

class Hacker_News__Live_Data(Type_Safe):

    def get_json(self, path, file_name):
        try:
            if path and file_name:
                url = self.url(path=path, file_name=file_name)
                return GET_json(url)
        except Exception:
            return ''

        #url__timeline_current = f"{MY_FEEDS__SERVER}/{WEB_PATH__PUBLIC__HACKER_NEWS}/{_.path__current}/{FILE_NAME__FEED_TIMELINE_MGRAPH}"  # todo: change this to be from the local server
        #url__timeline_previous = f"{MY_FEEDS__SERVER}/{WEB_PATH__PUBLIC__HACKER_NEWS}/{_.path__previous}/{FILE_NAME__FEED_TIMELINE_MGRAPH}"
        #data__timeline_current  = GET_json(url__timeline_current)                                                       # todo: since we really shouldn't be getting this data from the dev server
        #            data__timeline_previous = GET_json(url__timeline_previous)

    def url(self, path,file_name):
        return f'{MY_FEEDS__SERVER}/{WEB_PATH__PUBLIC__HACKER_NEWS}/{path}/{file_name}'