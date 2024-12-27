from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Raw_Data   import Model__Data_Feeds__Raw_Data
from osbot_utils.utils.Files                                    import file_contents
from myfeeds_ai.data_feeds.Data_Feeds__Http_Content             import Data_Feeds__Http_Content


class Security_Week__Http_Content(Data_Feeds__Http_Content):
    server : str = 'https://www.securityweek.com/'

    def raw_content(self) -> Model__Data_Feeds__Raw_Data:
        #path = 'feeds'
        #return super().requests_get__raw_data(path=path)
        local_path = '/tmp/www.securityweek.com.xml'
        raw_data = file_contents(local_path)

        return Model__Data_Feeds__Raw_Data(raw_data=raw_data)
