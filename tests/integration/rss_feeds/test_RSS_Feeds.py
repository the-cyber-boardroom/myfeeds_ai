from unittest import TestCase

from myfeeds_ai.rss_feeds.RSS_Feeds import RSS_Feeds


class test_RSS_Feeds(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rss_feeds = RSS_Feeds()

