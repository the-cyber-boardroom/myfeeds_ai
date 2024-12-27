from unittest                                                                               import TestCase
from xml.etree.ElementTree                                                                  import Element

import requests

from osbot_utils.helpers.xml.Xml__File__Load import Xml__File__Load
from osbot_utils.helpers.xml.Xml__File__To_Dict import Xml__File__To_Dict
from osbot_utils.utils.Dev import pprint

from myfeeds_ai.providers.cyber_security.security_week.models.Model__Security_Week__Feed    import Model__Security_Week__Feed
from myfeeds_ai.providers.cyber_security.security_week.Security_Week__Http_Content          import Security_Week__Http_Content
from myfeeds_ai.providers.cyber_security.security_week.Security_Week__Parser                import Security_Week__Parser
from osbot_utils.utils.Objects                                                              import obj
from tests.integration.data_feeds__test_data import TEST_DATA__SECURITY_NEWS__FEED_XML


class test_Security_Week__Parser(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.http_content = Security_Week__Http_Content ()
        cls.raw_content  = cls.http_content.raw_content()
        cls.parser       = Security_Week__Parser       ()
        cls.parser.setup(xml_content=cls.raw_content.raw_data)


    def test__setUpClass(self):
        with self.parser as _:
            assert _.xml_content == self.raw_content.raw_data
            assert type(_.channel) == Element
            assert type(_.root   ) == Element


    # def test_parse_feed(self):
    #     with self.parser as _:
    #         feed = _.parse_feed()
    #
    #         #pprint(feed)
    #
    #         assert type(feed) == Model__Security_Week__Feed

            #pprint(obj(feed))

    # def test_parse_rss_feeds(self):
    #     rss_url  = 'https://krebsonsecurity.com/feed/'
    #     rss_url = 'https://talkback.sh/resources/feed/'
    #     # rss_url = 'https://www.ncsc.gov.uk/api/1/services/v1/news-rss-feed.xml'
    #     # rss_url = 'https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml'
    #     # rss_url = 'https://www.schneier.com/feed/atom/'
    #
    #     #rss_url = 'https://feeds.feedburner.com/TheHackersNews'
    #     rss_url = 'https://www.csoonline.com/feed/'
    #     rss_url = 'https://www.darkreading.com/rss.xml'
    #
    #     xml_feed = requests.get(rss_url).text
    #     #pprint(xml_feed)
    #     xml_file = Xml__File__Load().load_from_string(xml_feed)
    #     xml_dict = Xml__File__To_Dict().to_dict(xml_file)
    #     #pprint(xml_file.obj().root_element)
    #     pprint(xml_dict)
