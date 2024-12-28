import requests

from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Raw_Data   import Model__Data_Feeds__Raw_Data
from osbot_utils.context_managers.capture_duration              import capture_duration
from osbot_utils.base_classes.Type_Safe                         import Type_Safe


class RSS_Feeds(Type_Safe):

    def raw_feed_xml(self, url='', params=None):
        with capture_duration() as duration:
            response = requests.get(url, params=params)

        kwargs = dict(duration   = duration.seconds,
                      raw_data   = response.text   ,
                      source_url = response.url    )

        return Model__Data_Feeds__Raw_Data.from_json(kwargs)