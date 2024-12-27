from myfeeds_ai.data_feeds.Data_Feeds__Parser                                            import Data_Feeds__Parser
from myfeeds_ai.providers.cyber_security.security_week.models.Model__Security_Week__Feed import Model__Security_Week__Feed
from osbot_utils.helpers.xml.Xml__File__Load import Xml__File__Load
from osbot_utils.helpers.xml.Xml__File__To_Dict import Xml__File__To_Dict


class Security_Week__Parser(Data_Feeds__Parser):

    def parse_feed(self) -> Model__Security_Week__Feed:
        feed = Model__Security_Week__Feed()
        xml_file_load = Xml__File__Load()
        xml_file      = xml_file_load.load_from_string(self.xml_content)
        xml_file_to_dict = Xml__File__To_Dict()

        xml_dict = xml_file_to_dict.to_dict(xml_file)
        return xml_dict