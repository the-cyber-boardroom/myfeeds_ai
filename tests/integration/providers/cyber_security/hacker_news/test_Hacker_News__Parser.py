import xml.etree.ElementTree  as ET
from osbot_utils.utils.Objects                                                           import __
from unittest                                                                            import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Parser                 import Hacker_News__Parser
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Article  import Model__Hacker_News__Article
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Feed     import Model__Hacker_News__Feed
from tests.integration.data_feeds__test_data                                             import TEST_DATA__HACKER_NEWS__FEED_XML


class test_Hacker_News__Parser(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.parser      = Hacker_News__Parser().setup(TEST_DATA__HACKER_NEWS__FEED_XML)

    def test_get_element_text(self):
        with self.parser as target:
            assert target.get_element_text(target.channel, 'title') == "The Hacker News"
            assert target.get_element_text(target.channel, 'nonexistent') == ""
            assert target.get_element_text(target.channel, 'nonexistent', 'default') == "default"

    def test_parse_feed(self):
        with self.parser as target:
            feed = target.parse_feed()
            assert isinstance(feed, Model__Hacker_News__Feed)
            assert feed.title == "The Hacker News"
            assert feed.link == "https://thehackernews.com"
            assert feed.language == "en-us"
            assert feed.update_period == "hourly"
            assert feed.update_frequency == 1

    def test_parse_articles(self):
        with self.parser as target:
            articles = target.parse_articles()
            assert isinstance(articles, list)
            assert len(articles) == 1
            assert isinstance(articles[0], Model__Hacker_News__Article)

    def test_parse_article(self):
        with self.parser as target:
            item         = target.channel.find('item')
            article      = target.parse_article(item)
            publish_date = article.when
            assert isinstance(article, Model__Hacker_News__Article)
            assert article.obj()  == __(author         = 'info@thehackernews.com (The Hacker News)'           ,
                                        description    = 'Test Description'                                   ,
                                        article_id     = 'aef30063-2e5f-59e1-930a-69397b4ab0c0'               ,
                                        article_obj_id = 'aef30063'                                           ,
                                        image_url      = 'https://example.com/image.jpg'                      ,
                                        link           = 'https://thehackernews.com/2024/12/test-article.html',
                                        when           = __(date_time_utc = '2024-12-04 17:23:00 +0000'       ,
                                                            date_utc      = '2024-12-04'                      ,
                                                            raw_value     = 'Wed, 04 Dec 2024 22:53:00 +0530' ,
                                                            time_since    = publish_date.time_since           ,
                                                            time_utc      = '17:23'                           ,
                                                            timestamp_utc = 1733332980                        ),
                                        title          ='Test Article')
            assert ' day(s) ago' in publish_date.time_since

    def test_setup(self):
        with self.parser as target:
            assert isinstance(target.root, ET.Element)
            assert target.xml_content   == TEST_DATA__HACKER_NEWS__FEED_XML
            assert target.channel       is not None

    # run these two a the end since they reset the target value
    def test_z_error_handling(self):
        with self.parser as target:
            with self.assertRaises(ET.ParseError):
                target.setup('<rss><channel><title>Test</title></channel>')

    def test_z_missing_elements(self):
        with self.parser as target:
            minimal_xml = '''<?xml version="1.0"?>
                <rss><channel>
                    <item>
                        <title>Test</title>
                        <link>http://test.com</link>
                    </item>
                </channel></rss>'''
            target.setup(minimal_xml)
            feed = target.parse_feed()
            assert isinstance(feed, Model__Hacker_News__Feed)
            assert feed.title == ""
            articles = feed.articles
            assert len(articles) == 1
            assert articles[0].title == "Test"
            assert articles[0].description == ""
            assert articles[0].author == ""