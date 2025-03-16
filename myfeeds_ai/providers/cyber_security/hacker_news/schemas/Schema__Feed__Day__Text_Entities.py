from typing                                             import List
from mgraph_db.mgraph.MGraph                            import MGraph
from osbot_utils.helpers.Obj_Id                         import Obj_Id
from osbot_utils.helpers.Timestamp_Now                  import Timestamp_Now
from osbot_utils.helpers.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

class Schema__Feed__Day__Text_Entities(Type_Safe):
    articles_ids   : set[Obj_Id]
    files_loaded   : set[Safe_Str__File__Path]
    last_updated   : Timestamp_Now
    mgraph_entities: MGraph