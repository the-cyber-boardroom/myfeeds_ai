import requests

from cbr_custom_news_feeds.providers.cyber_security.hacker_news.Hacker__News__S3_DB         import Hacker_News__S3_DB
from osbot_utils.base_classes.Type_Safe                                                     import Type_Safe
from osbot_utils.utils.Http                                                                 import url_join_safe
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.Hacker_News__Parser         import Hacker_News__Parser
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.Hacker_News__Prompt_Creator import Hacker_News__Prompt_Creator


class Hacker_News__Http_Content(Type_Safe):                 # Handler for fetching and parsing Hacker News RSS feed
    prompt_creator : Hacker_News__Prompt_Creator
    server         : str = 'https://feeds.feedburner.com'
    s3_db          : Hacker_News__S3_DB

    #@cache_on_self                                        # todo: add a better caching architecture (for example one based on S3_DB__Cache)
    def requests_get(self, path='', params=None):          # Makes HTTP GET request to the server
        url = url_join_safe(self.server, path)
        return requests.get(url, params=params)

    def feed_content(self) -> str:                              # Fetch the RSS feed content
        path = 'TheHackersNews'
        return self.requests_get(path).text

    def feed_data(self):                                        # Fetch and parse the RSS feed into structured data
        feed_content = self.feed_content()
        parser = Hacker_News__Parser().setup(feed_content)
        return parser.parse_feed()

    def feed_prompt(self, size=5):                            # Get schema prompt from feed data with specified size
        feed_data = self.feed_data()
        return self.prompt_creator.create_prompt_schema(feed_data, size)
