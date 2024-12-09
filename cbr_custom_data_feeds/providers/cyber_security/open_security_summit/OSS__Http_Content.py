from cbr_custom_data_feeds.data_feeds.Data_Feeds__Http_Content import Data_Feeds__Http_Content


class OSS__Http_Content(Data_Feeds__Http_Content):
    server : str = 'https://open-security-summit.org/'

    def raw_content(self):
        return self.requests_get('content.json').json()