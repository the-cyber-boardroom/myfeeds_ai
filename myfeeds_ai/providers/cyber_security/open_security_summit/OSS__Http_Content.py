from myfeeds_ai.data_feeds.Data_Feeds__Http_Content           import Data_Feeds__Http_Content
from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Raw_Data import Model__Data_Feeds__Raw_Data



class OSS__Http_Content(Data_Feeds__Http_Content):
    server : str = 'https://open-security-summit.org/'

    def raw_content(self) -> Model__Data_Feeds__Raw_Data:
        return self.requests_get__raw_data('content.json')