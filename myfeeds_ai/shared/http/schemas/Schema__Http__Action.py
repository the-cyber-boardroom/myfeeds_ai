from myfeeds_ai.shared.http.schemas.Schema__Http__Request   import Schema__Http__Request
from myfeeds_ai.shared.http.schemas.Schema__Http__Response  import Schema__Http__Response
from osbot_utils.helpers.Obj_Id                             import Obj_Id
from osbot_utils.helpers.Timestamp_Now                      import Timestamp_Now
from osbot_utils.type_safe.Type_Safe                        import Type_Safe


class Schema__Http__Action(Type_Safe):
    cache_id : Obj_Id                       = None
    request  : Schema__Http__Request        = None
    response : Schema__Http__Response       = None
    timestamp: Timestamp_Now