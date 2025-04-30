from typing                                                             import Dict
from myfeeds_ai.shared.http.schemas.Schema__Http__Request               import Schema__Http__Request
from myfeeds_ai.shared.http.schemas.Schema__Http__Request__Cache__Entry import Schema__Http__Request__Cache__Entry
from myfeeds_ai.shared.http.schemas.Schema__Http__Request__Cache__Index import Schema__Http__Request__Cache__Index
from myfeeds_ai.shared.http.schemas.Schema__Http__Response              import Schema__Http__Response
from osbot_utils.helpers.Obj_Id                                         import Obj_Id
from osbot_utils.helpers.safe_str.Safe_Str                              import Safe_Str
from osbot_utils.helpers.safe_str.Safe_Str__Hash                        import safe_str_hash, Safe_Str__Hash
from osbot_utils.helpers.safe_str.Safe_Str__Url                         import Safe_Str__Url
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                         import type_safe

class Http__Request__Cache(Type_Safe):
    cache_index          : Schema__Http__Request__Cache__Index
    cache_entries        : Dict[Obj_Id, Schema__Http__Request__Cache__Entry]                            # In-memory storage of cache entries
    #http_request_execute: Http__Request__Execute

    @type_safe
    def calculate_hash (self, method: Safe_Str, url: Safe_Str__Url, params: dict=None) -> Safe_Str__Hash:
        hash_string = (f"Method: {method}\n"
                       f"Url   : {url}")
        if params:
            hash_string += f"Params: {params}"
        request_hash = Safe_Str__Hash(safe_str_hash(hash_string))
        return request_hash

    # def requests__get(self, url: str, params:dict, headers: dict) -> dict:
    #     request_hash = self.compute_request_hash(url=url, params=params, headers=headers)
    #     #requests_get__cache_entry
    #     return request_hash
    #
    #     if request_hash in self.cache_index.cache_id__from__hash__request:                                                              # Check if we have an exact match
    #         cache_id    = self.cache_index.cache_id__from__hash__request[request_hash]
    #         cache_entry = self.get__cache_entry__from__cache_id(cache_id)
    #         if cache_entry:
    #             return cache_entry.llm__response
    #
    #     return None

    # def requests__get__cache_entry(self, url: Safe_Str__Url, params:dict=None, headers:dict=None) -> Schema__Http__Request__Cache__Entry:
    #     return self.http_request_execute.requests_get__cache_entry(url=url, params=params, headers=headers)

    def create_cache_entry(self, request: Schema__Http__Request, response: Schema__Http__Response) -> Schema__Http__Request__Cache__Entry:

        # if 'application/json' in content_type:
        #     json__data           = str_to_json(text)
        # elif 'text/html' in content_type:
        #     html__dict           = html_to_dict(text)                       # todo: move this into the workflow that creates the dict from the html

        request_data__kwargs = dict(request     = request  ,
                                    response     = response   )
        request_data = Schema__Http__Request__Cache__Entry(**request_data__kwargs)

        return request_data