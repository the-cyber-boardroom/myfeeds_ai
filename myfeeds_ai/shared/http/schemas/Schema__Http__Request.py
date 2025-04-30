from typing import Dict
from osbot_utils.helpers.safe_str.Safe_Str import Safe_Str
from osbot_utils.helpers.safe_str.Safe_Str__Hash  import Safe_Str__Hash
from osbot_utils.helpers.safe_str.Safe_Str__Url   import Safe_Str__Url
from osbot_utils.type_safe.Type_Safe              import Type_Safe


class Schema__Http__Request(Type_Safe):
    cache__hash: Safe_Str__Hash = None                  # hash of the request (to be used in for caching), created using METHOD + URL
    method     : Safe_Str       = None                  # todo: we could use a more Strongly typed type here (for example one that only allowed valid HTTP methods to be used here)
    url        : Safe_Str__Url  = None                  # full url for this request