import requests

from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Raw_Data           import Model__Data_Feeds__Raw_Data
from myfeeds_ai.shared.http.schemas.Schema__Http__Request__Data         import Schema__HTTP__Request__Data
from osbot_utils.helpers.html.Html_To_Dict                              import html_to_dict
from osbot_utils.helpers.safe_str.Safe_Str__Hash                        import safe_str_hash
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe
from osbot_utils.helpers.duration.decorators.capture_duration           import capture_duration
from osbot_utils.utils.Http                                             import url_join_safe
from osbot_utils.utils.Json                                             import str_to_json

HTTP__HEADERS__DEFAULT = {  'accept'                    : 'text/html,application/xhtml+xml'                  ,
                            'accept-language'           : 'en-GB,en;q=0.9'                                   ,
                            'user-agent'                : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
                            }

class My_Feeds__Http_Content(Type_Safe):
    server : str

    def requests_get(self, path='', params=None, headers=None):          # Makes HTTP GET request to the server
        if not self.server:
            raise ValueError('server not set')
        url = url_join_safe(self.server, path)
        if headers is None:
            headers = HTTP__HEADERS__DEFAULT

        response = requests.get(url, params=params, headers=headers)
        return response

    def requests_get__data(self, path='', params=None, headers=None) -> Schema__HTTP__Request__Data:
        with capture_duration() as duration:
            response                 = self.requests_get(path, params=params, headers=headers)
            response_url             = response.url
            content_type             = response.headers.get('Content-Type' , '').lower()
            status_code              = response.status_code
            text                     = response.text
            etag                     = response.headers.get('ETag'         , '')
            last_modified            = response.headers.get('Last-Modified', '')
            url_hash                 = safe_str_hash(response_url)
            text_hash                = safe_str_hash(text)
            method                   = response.request.method
            html__dict               = None
            json__data               = None
            if 'application/json' in content_type:
                json__data           = str_to_json(text)
            elif 'text/html' in content_type:
                html__dict           = html_to_dict(text)                       # todo: look at the errors we are getting when trying to use Dict_To_Tags (and see if that would help)

            request_data__kwargs = dict(content_type    = content_type  ,
                                        json__data      = json__data    ,
                                        method          = method        ,
                                        status_code     = status_code   ,
                                        text            = text          ,
                                        text__hash      = text_hash     ,
                                        html__dict      = html__dict    ,
                                        url             = response_url  ,
                                        url__hash       = url_hash      ,
                                        etag            = etag          ,
                                        last_modified   = last_modified)
            request_data = Schema__HTTP__Request__Data(**request_data__kwargs)


        request_data.duration = duration.seconds
        return request_data


    def requests_get__raw_data(self, path='', params=None):
        with capture_duration() as duration:
            response = self.requests_get(path, params)

        kwargs = dict(duration   = duration.seconds,
                      raw_data   = response.text   ,
                      source_url = response.url    )

        return Model__Data_Feeds__Raw_Data.from_json(kwargs)