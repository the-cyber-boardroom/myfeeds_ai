import requests

from myfeeds_ai.data_feeds.Data_Feeds__Http_Content                              import Data_Feeds__Http_Content
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Parser         import Hacker_News__Parser
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Prompt_Creator import Hacker_News__Prompt_Creator


class Hacker_News__Http_Content(Data_Feeds__Http_Content):                 # Handler for fetching and parsing Hacker News RSS feed
    prompt_creator : Hacker_News__Prompt_Creator
    server         : str = 'https://feeds.feedburner.com'

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
