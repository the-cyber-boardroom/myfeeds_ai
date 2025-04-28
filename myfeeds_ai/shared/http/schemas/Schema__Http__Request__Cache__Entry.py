from osbot_utils.helpers.Obj_Id                             import Obj_Id
from osbot_utils.helpers.Timestamp_Now                      import Timestamp_Now
from osbot_utils.helpers.safe_str.Safe_Str                  import Safe_Str
from osbot_utils.helpers.safe_str.Safe_Str__Hash            import Safe_Str__Hash
from osbot_utils.helpers.safe_str.Safe_Str__Text__Dangerous import Safe_Str__HTML
from osbot_utils.helpers.safe_str.Safe_Str__Url             import Safe_Str__Url
from osbot_utils.type_safe.Type_Safe                        import Type_Safe


class Schema__Http__Request__Cache__Entry(Type_Safe):
    cache_id      : Obj_Id
    content_type  : Safe_Str             = None
    duration      : float                = None
    etag          : Safe_Str             = None
    html__dict    : dict                 = None
    json__data    : dict                 = None
    last_modified : Safe_Str             = None
    method        : Safe_Str             = None
    request__hash : Safe_Str__Hash       = None
    status_code   : int                  = None
    text          : Safe_Str__HTML       = None                  # has a limit of 64k which should be enough for all
    text__hash    : Safe_Str__Hash       = None                  # capture the current hash of the html_raw
    timestamp     : Timestamp_Now                                # this is the only value we can setup automatically
    url            : Safe_Str__Url       = None                  # full url for this request
    url__hash    : Safe_Str__Hash        = None                  # hash of the url