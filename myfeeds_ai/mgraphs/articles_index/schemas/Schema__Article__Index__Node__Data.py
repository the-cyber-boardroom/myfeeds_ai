from typing                                         import Dict, Any, Optional
from mgraph_ai.mgraph.MGraph                          import MGraph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node    import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Types   import Schema__MGraph__Types
from osbot_utils.helpers.Obj_Id                       import Obj_Id
from osbot_utils.type_safe.Type_Safe                  import Type_Safe

class Schema__Article__Index__Node__Data(Type_Safe):        # Data for article index nodes
    article_id     : str                                    # Full article GUID
    article_obj_id : str                                    # Short article ID used in paths
    title         : str                                     # Article title for quick reference
    path          : str                                     # Full path to article JSON
    timestamp_utc : int