from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.helpers.Random_Guid                                                 import Random_Guid
from osbot_utils.helpers.Timestamp_Now                                               import Timestamp_Now
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Feed import Model__Hacker_News__Feed

class Model__Hacker_News__Data__Feed(Type_Safe):
    created_timestamp : Timestamp_Now
    feed_id           : Random_Guid
    feed_data         : Model__Hacker_News__Feed
    created_by        : str
    duration          : float
    file_path         : str
