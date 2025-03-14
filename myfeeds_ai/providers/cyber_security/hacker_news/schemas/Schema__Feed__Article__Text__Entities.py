from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Entities__LLMs import Schema__Graph_RAG__Entities__LLMs
from osbot_utils.helpers.Obj_Id                                              import Obj_Id
from osbot_utils.helpers.Timestamp_Now                                       import Timestamp_Now
from osbot_utils.type_safe.Type_Safe                                         import Type_Safe

class Schema__Feed__Article__Text__Entities(Type_Safe):
    cache_id     : Obj_Id                               = None
    duration     : float                                = None
    text         : str                                  = None
    text_entities: Schema__Graph_RAG__Entities__LLMs    = None
    text_id      : Obj_Id
    timestamp    : Timestamp_Now
