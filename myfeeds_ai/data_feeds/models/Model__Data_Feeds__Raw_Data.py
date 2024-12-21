from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.helpers.Random_Guid    import Random_Guid
from osbot_utils.helpers.Timestamp_Now  import Timestamp_Now

class Model__Data_Feeds__Raw_Data(Type_Safe):
    created_timestamp : Timestamp_Now
    raw_data_id       : Random_Guid
    raw_data          : str
    duration          : float
    source_url        : str
    storage_path      : str

