from osbot_utils.base_classes.Type_Safe  import Type_Safe
from osbot_utils.helpers.Random_Guid     import Random_Guid
from osbot_utils.helpers.Timestamp_Now   import Timestamp_Now


class Model__Data_Feeds__Prompt(Type_Safe):
    timestamp  : Timestamp_Now
    prompt_id  : Random_Guid
    prompt_text: str
