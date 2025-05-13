from myfeeds_ai.shared.http.Http__Request__Cache                    import Http__Request__Cache
from myfeeds_ai.shared.http.schemas.Schema__Http__Action import Schema__Http__Action
from myfeeds_ai.shared.http.schemas.Schema__Http__Request           import Schema__Http__Request
from myfeeds_ai.shared.http.schemas.Schema__Http__Request__Methods  import Schema__Http__Request__Methods
from myfeeds_ai.shared.http.schemas.Schema__Http__Response          import Schema__Http__Response
from osbot_utils.helpers.safe_str.Safe_Str__Hash                    import safe_str_hash
from osbot_utils.helpers.safe_str.Safe_Str__Url                     import Safe_Str__Url
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                     import type_safe

HTTP__HEADERS__DEFAULT = {  'accept'                    : 'text/html,application/xhtml+xml'                  ,
                            'accept-language'           : 'en-GB,en;q=0.9'                                   ,
                            'user-agent'                : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
                            }

# todo: refactor the use of this class with the Http__Request__Cache.py and Http__Request__Execute (which has http cache support)
class Http__Request__Execute(Type_Safe):
    http_request_cache : Http__Request__Cache
    use_cache          : bool                   = True
    refresh_cache      : bool                 = False

    def create_http_request(self, method: Schema__Http__Request__Methods,
                                  url   : Safe_Str__Url                 ,
                                  params: dict          = None
                              )-> Schema__Http__Request :
        request_hash   = self.http_request_cache.calculate_hash(method=method, url=url, params=params)
        request_kwargs = dict(cache__hash = request_hash   ,
                              method        = method       ,
                              url           = url          )
        request        = Schema__Http__Request(**request_kwargs)
        return request

    def create_http_response(self, response, duration: float) -> Schema__Http__Response:
        content_type             = response.headers.get('Content-Type' , '').lower()
        status_code              = response.status_code
        text                     = response.text
        etag                     = response.headers.get('ETag'         , '')
        last_modified            = response.headers.get('Last-Modified', '')
        text_hash                = safe_str_hash(text)
        http__response__kwargs = dict(content_type    = content_type  ,
                                      duration        = duration      ,
                                      status_code     = status_code   ,
                                      text            = text          ,
                                      text__hash      = text_hash     ,
                                      etag            = etag          ,
                                      last_modified   = last_modified )
        response = Schema__Http__Response(**http__response__kwargs)
        return response


    @type_safe
    def execute(self, request: Schema__Http__Request,
                      headers : dict         = None
                  )-> Schema__Http__Response :
        if headers is None:
            headers = HTTP__HEADERS__DEFAULT
        response = self.execute__http_request(request=request, headers=headers)
        return response


    def execute__http_request(self, request: Schema__Http__Request, headers:dict=None):
        raise NotImplemented()

    @type_safe
    def execute__get(self, url    : Safe_Str__Url,
                           params : dict         = None,
                           headers: dict         = None
                      ) -> Schema__Http__Action  :
        method   = Schema__Http__Request__Methods.GET
        request  = self.create_http_request(method, url, params)
        response = self.execute(request=request, headers=headers)
        return Schema__Http__Action(request=request, response=response)