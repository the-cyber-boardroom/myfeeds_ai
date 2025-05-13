from typing import Dict, Optional
from myfeeds_ai.shared.http.schemas.Schema__Http__Request               import Schema__Http__Request
from myfeeds_ai.shared.http.schemas.Schema__Http__Request__Cache__Entry import Schema__Http__Request__Cache__Entry
from myfeeds_ai.shared.http.schemas.Schema__Http__Request__Cache__Index import Schema__Http__Request__Cache__Index
from myfeeds_ai.shared.http.schemas.Schema__Http__Request__Methods      import Schema__Http__Request__Methods
from myfeeds_ai.shared.http.schemas.Schema__Http__Response              import Schema__Http__Response
from osbot_utils.helpers.Obj_Id                                         import Obj_Id
from osbot_utils.helpers.safe_str.Safe_Str__Hash                        import safe_str_hash, Safe_Str__Hash
from osbot_utils.helpers.safe_str.Safe_Str__Url                         import Safe_Str__Url
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                         import type_safe

# this is the in-memory version of the Http__Request__Cache
class Http__Request__Cache(Type_Safe):
    cache_index          : Schema__Http__Request__Cache__Index                                          # Index mapping request hashes to cache entries
    cache_entries        : Dict[Obj_Id, Schema__Http__Request__Cache__Entry]                            # In-memory storage of cache entries
    #http_request_execute: Http__Request__Execute

    @type_safe
    def calculate_hash (self, method: Schema__Http__Request__Methods, url: Safe_Str__Url, params: dict=None) -> Safe_Str__Hash:
        hash_string = (f"Method: {method.value}\n"
                       f"Url   : {url}")
        if params:
            hash_string += f"Params: {params}"
        request_hash = Safe_Str__Hash(safe_str_hash(hash_string))
        return request_hash

    @type_safe
    def add__cache_entry(self, request : Schema__Http__Request ,  # Request to cache
                  response: Schema__Http__Response,  # Response to store
             ) -> Obj_Id:

        cache_entry = Schema__Http__Request__Cache__Entry(request=request, response=response)
        cache_hash  = cache_entry.request.cache__hash
        cache_id    = cache_entry.cache_id

        self.cache_index.cache_id__from__hash__request[cache_hash] = cache_id                                      # Update the cache index
        self.cache_entries                            [cache_id  ] = cache_entry                                   # Store in memory
        return cache_id

    def exists(self, request: Schema__Http__Request) -> bool:
        return request.cache__hash in self.cache_index.cache_id__from__hash__request

    @type_safe
    def get__cache_entry__from__request(self, request: Schema__Http__Request) -> Optional[Schema__Http__Request__Cache__Entry]:                                      # Cached response or None
        cache__hash = request.cache__hash
        if request.cache__hash in self.cache_index.cache_id__from__hash__request:
            cache_id    = self.cache_index.cache_id__from__hash__request[cache__hash]
            cache_entry = self.get__cache_entry__from__cache_id(cache_id)
            return cache_entry

        return None

    @type_safe
    def get__cache_entry__from__cache_id(self, cache_id: Obj_Id) -> Optional[Schema__Http__Request__Cache__Entry]:  # Get cache entry by ID
        if cache_id:
            return self.cache_entries.get(cache_id)

    def get__response__by_id(self, cache_id) -> Optional[Schema__Http__Response]:
        cache_entry = self.get__cache_entry__from__cache_id(cache_id)
        if cache_entry:
            return cache_entry.response
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

    def delete__using__request(self, request : Schema__Http__Request) -> bool:                                                            # Success status
        return self.delete__using__request__hash(request.cache__hash)

    def delete__using__request__hash(self, cache_hash: Safe_Str__Hash) -> bool:                                                            # Success status
        if cache_hash not in self.cache_index.cache_id__from__hash__request:
            return False
        else:
            cache_id = self.cache_index.cache_id__from__hash__request[cache_hash]
            del self.cache_index.cache_id__from__hash__request[cache_hash]
            if cache_id in self.cache_entries:                                                                              # Remove from memory
                del self.cache_entries[cache_id]
            return self.save()

    def save(self) -> bool:                                                                 # For overriding in subclasses
        return True