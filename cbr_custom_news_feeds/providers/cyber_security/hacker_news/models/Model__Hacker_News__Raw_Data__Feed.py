from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.helpers.Random_Guid    import Random_Guid
from osbot_utils.helpers.Timestamp_Now  import Timestamp_Now


class Model__Hacker_News__Raw_Data__Feed(Type_Safe):
    created_timestamp : Timestamp_Now
    feed_id           : Random_Guid
    feed_xml          : str
    created_by        : str
    duration          : float
