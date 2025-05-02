from enum                                                           import Enum
from typing                                                         import Dict
from myfeeds_ai.shared.http.schemas.Schema__Http__Request__Methods  import Schema__Http__Request__Methods
from osbot_utils.helpers.safe_str.Safe_Str__Hash                    import Safe_Str__Hash
from osbot_utils.helpers.safe_str.Safe_Str__Url                     import Safe_Str__Url
from osbot_utils.type_safe.Type_Safe                                import Type_Safe

class Schema__Http__Request(Type_Safe):
    cache__hash: Safe_Str__Hash                 = None                  # hash of the request (to be used in for caching), created using METHOD + URL
    data       : Dict                           = None                  # todo : see if need to add support for the request type (text, json, form-encoded_)
    method     : Schema__Http__Request__Methods = None
    url        : Safe_Str__Url                  = None                  # full url for this request
