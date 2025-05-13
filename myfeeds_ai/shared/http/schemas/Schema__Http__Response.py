from osbot_utils.helpers.safe_str.Safe_Str__Hash                        import Safe_Str__Hash
from osbot_utils.helpers.safe_str.http.Safe_Str__Http__Content_Type     import Safe_Str__Http__Content_Type
from osbot_utils.helpers.safe_str.http.Safe_Str__Http__ETag             import Safe_Str__Http__ETag
from osbot_utils.helpers.safe_str.http.Safe_Str__Http__Last_Modified    import Safe_Str__Http__Last_Modified
from osbot_utils.helpers.safe_str.http.Safe_Str__Http__Text             import Safe_Str__Http__Text
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe

# todo: see if we need to add support for binary data (which will  need to be stored as base64, or in a separate .bytes file (for performance reasons)
# todo: see if we need to decouple from here the need to store html, text and binary data (like images, zips, sqlite3 files) . Maybe we could refactor this into Schema__Http__Response__Html, Schema__Http__Response__Text (where we keep the content

class Schema__Http__Response(Type_Safe):
    content_type  : Safe_Str__Http__Content_Type     = None
    duration      : float                            = None
    etag          : Safe_Str__Http__ETag             = None
    last_modified : Safe_Str__Http__Last_Modified    = None
    text          : Safe_Str__Http__Text             = None                  # use to store html or text code has a limit of 1Mb which should be enough for all
    text__hash    : Safe_Str__Hash                   = None                  # capture the current hash of the html_raw
    status_code   : int                              = None