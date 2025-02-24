from mgraph_db.mgraph.schemas.Schema__MGraph__Diff__Values  import Schema__MGraph__Diff__Values
from osbot_utils.type_safe.Type_Safe                        import Type_Safe


class Schema__Feed__Config__New_Articles(Type_Safe):
    path__current               : str                          = None
    path__previous              : str                          = None
    timeline_diff               : Schema__MGraph__Diff__Values = None
