import requests

from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Raw_Data   import Model__Data_Feeds__Raw_Data
from osbot_utils.helpers.duration.decorators.capture_duration   import capture_duration
from osbot_utils.type_safe.Type_Safe                            import Type_Safe
from osbot_utils.helpers.xml.Xml__File__Load                    import Xml__File__Load
from osbot_utils.helpers.xml.Xml__File__To_Dict                 import Xml__File__To_Dict
from osbot_utils.helpers.xml.rss.RSS__Feed__Parser              import RSS__Feed__Parser


class RSS_Feeds(Type_Safe):

    def feed_url__to__xml(self, url=''):
        with capture_duration() as duration:
            response = requests.get(url)

        kwargs = dict(duration   = duration.seconds,
                      raw_data   = response.text   ,
                      source_url = response.url    )

        return Model__Data_Feeds__Raw_Data.from_json(kwargs)

    def feed_url__to__xml_file(self, url):
        raw_data = self.feed_url__to__xml(url).raw_data
        xml_file = Xml__File__Load().load_from_string(raw_data)
        return xml_file

    def feed_url__to__json(self, url):
        raw_data = self.feed_url__to__xml(url).raw_data
        xml_file = Xml__File__Load().load_from_string(raw_data)
        xml_dict = Xml__File__To_Dict().to_dict(xml_file)
        return xml_dict

    def feed_url__to__rss_feed(self, url):
        raw_data = self.feed_url__to__xml(url).raw_data
        xml_file = Xml__File__Load().load_from_string(raw_data)
        xml_dict = Xml__File__To_Dict().to_dict(xml_file)
        rss_dict = RSS__Feed__Parser().from_dict(xml_dict)
        return rss_dict

