import requests

from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Raw_Data import Model__Data_Feeds__Raw_Data
from osbot_utils.base_classes.Type_Safe                                  import Type_Safe
from osbot_utils.context_managers.capture_duration                       import capture_duration
from osbot_utils.utils.Http                                              import url_join_safe

class Data_Feeds__Http_Content(Type_Safe):
    server : str

    def requests_get(self, path='', params=None):          # Makes HTTP GET request to the server
        if not self.server:
            raise ValueError('server not set')
        url = url_join_safe(self.server, path)
        return requests.get(url, params=params)

    def requests_get__raw_data(self, path='', params=None):
        with capture_duration() as duration:
            response = self.requests_get(path, params)

        kwargs = dict(duration   = duration.seconds,
                      raw_data   = response.text   ,
                      source_url = response.url    )

        return Model__Data_Feeds__Raw_Data.from_json(kwargs)