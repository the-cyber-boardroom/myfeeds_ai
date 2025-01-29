from unittest                                                   import TestCase
from osbot_utils.helpers.xml.rss.RSS__Feed                      import RSS__Feed
from osbot_utils.utils.Misc                                     import list_set
from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Raw_Data   import Model__Data_Feeds__Raw_Data
from myfeeds_ai.providers.RSS_Providers                         import RSS_Providers
from myfeeds_ai.rss_feeds.RSS_Feeds                             import RSS_Feeds
from osbot_utils.helpers.xml.Xml__File                          import Xml__File
from tests.integration.data_feeds__objs_for_tests               import cbr_website__assert_local_stack

class test_RSS_Feeds(TestCase):

    @classmethod
    def setUpClass(cls):
        cbr_website__assert_local_stack()
        cls.rss_feeds     = RSS_Feeds()
        cls.rss_providers = RSS_Providers().data()
        cls.provider_id   = 'hacker-news' # 'cso-online'
        cls.rss_provider  = cls.rss_providers.providers[cls.provider_id]
        cls.rss_url_feed  = cls.rss_provider.url_feed

    def test_feed_url__to__xml(self):
        with self.rss_feeds as _:
            feed_xml = _.feed_url__to__xml(self.rss_url_feed)
            assert type(feed_xml) is Model__Data_Feeds__Raw_Data

    def test_feed_url__to__xml_file(self):
        with self.rss_feeds as _:
            xml_file = _.feed_url__to__xml_file(self.rss_url_feed)
            assert type(xml_file)                                    is Xml__File
            assert xml_file.root_element.attributes['version'].value == '2.0'

    def test_feed_url__to__json(self):
        with self.rss_feeds as _:
            xml_dict = _.feed_url__to__json(self.rss_url_feed)
            assert list_set(xml_dict.get('channel')) == ['description', 'item', 'language', 'lastBuildDate',
                                                         'link', 'title', 'updateFrequency', 'updatePeriod']

    def test_feed_url__to__rss_feed(self):
        with self.rss_feeds as _:
            rss_feed = _.feed_url__to__rss_feed(self.rss_url_feed)
            assert type(rss_feed) is RSS__Feed
            assert rss_feed.channel.title == self.rss_provider.title


