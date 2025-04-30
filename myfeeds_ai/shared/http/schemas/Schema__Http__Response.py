from osbot_utils.helpers.safe_str.Safe_Str import Safe_Str
from osbot_utils.helpers.safe_str.Safe_Str__HTML import Safe_Str__HTML
from osbot_utils.helpers.safe_str.Safe_Str__Hash  import Safe_Str__Hash
from osbot_utils.type_safe.Type_Safe              import Type_Safe


class Schema__Http__Response(Type_Safe):
    content_type  : Safe_Str             = None
    etag          : Safe_Str             = None
    last_modified : Safe_Str             = None
    text          : Safe_Str__HTML       = None                  # has a limit of 64k which should be enough for all
    text__hash    : Safe_Str__Hash       = None                  # capture the current hash of the html_raw
    status_code   : int                  = None
    duration      : float                = None