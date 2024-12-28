from datetime                                                                           import datetime, timezone
from typing                                                                             import List
from xml.etree.ElementTree                                                              import Element
from myfeeds_ai.data_feeds.Data_Feeds__Parser                                           import Data_Feeds__Parser
from osbot_utils.helpers.Guid                                                           import Guid
from osbot_utils.utils.Dev                                                              import pprint
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Article import Model__Hacker_News__Article
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Feed    import Model__Hacker_News__Feed
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__When    import Model__Hacker_News__When

XML__NAMESPACES__Hacker_News = { 'atom'   : 'http://www.w3.org/2005/Atom'                  ,
                                 'content': 'http://purl.org/rss/1.0/modules/content/'     ,
                                 'sy'     : 'http://purl.org/rss/1.0/modules/syndication/' }

class Hacker_News__Parser(Data_Feeds__Parser):                                             # Parser for The Hacker News RSS feed

    def parse_when(self, raw_value:str):
        if not raw_value:
            return Model__Hacker_News__When()

        date_format = '%a, %d %b %Y %H:%M:%S %z'
        local_time                 = datetime.strptime(raw_value, date_format)
        date_time_utc              = local_time.astimezone(timezone.utc)
        timestamp_utc              = int(date_time_utc.timestamp())


        now_utc         = datetime.now(timezone.utc)                        # Calculate time difference
        time_difference = now_utc - date_time_utc
        days            = time_difference.days                              # Create a human-readable format
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes = remainder // 60

        if days > 0:
            time_since = f"{days} day(s) ago"
        elif hours > 0:
            time_since = f"{hours} hour(s) ago"
        else:
            time_since = f"{minutes} minute(s) ago"

        kwargs = dict(raw_value     = raw_value                                         ,
                      date_utc      = date_time_utc.strftime('%Y-%m-%d'            )    ,
                      date_time_utc = date_time_utc.strftime('%Y-%m-%d %H:%M:%S %z')    ,
                      time_utc      = date_time_utc.strftime('%H:%M'               )    ,
                      time_since    = time_since                                        ,
                      timestamp_utc = timestamp_utc                                     )

        publish_data = Model__Hacker_News__When(**kwargs)
        return publish_data

    def get_element_text_ns(self, element: Element, tag: str, default: str = ""): # Helper method to get text from an XML element with namespace
        elem = element.find(tag, XML__NAMESPACES__Hacker_News)
        return elem.text if elem is not None else default

    def parse_feed(self) -> Model__Hacker_News__Feed:                            # Parse the RSS feed and return a Model__Hacker_News__Feed object
        if self.channel is None:
            raise ValueError("Could not find channel element in RSS feed")

        try:
            update_frequency = int(self.get_element_text_ns(self.channel, './/sy:updateFrequency', '1'))
        except ValueError:
            update_frequency = 1

        title           = self.get_element_text(self.channel, 'title'        )
        link            = self.get_element_text(self.channel, 'link'         )
        description     = self.get_element_text(self.channel, 'description'  )
        language        = self.get_element_text(self.channel, 'language'     )
        last_build_date = self.get_element_text(self.channel, 'lastBuildDate')
        when            = self.parse_when(last_build_date)

        return Model__Hacker_News__Feed(title             = title            ,
                                        link              = link             ,
                                        description       = description      ,
                                        language          = language         ,
                                        update_period     = self.get_element_text_ns(self.channel, './/sy:updatePeriod', 'hourly'),
                                        update_frequency  = update_frequency                                                      ,
                                        when              = when                                                                  ,
                                        articles          = self.parse_articles()                                                 )

    def parse_articles(self) -> List[Model__Hacker_News__Article]:               # Parse all articles in the feed
        articles = []
        items    = self.channel.findall('item')

        for item in items:
            try:
                article = self.parse_article(item)
                articles.append(article)
            except Exception as e:
                pprint(f"Error parsing article: {str(e)}")
                continue

        return articles

    def parse_article(self, item: Element) -> Model__Hacker_News__Article:       # Parse a single article from an item element
        image_url = None
        enclosure = item.find('enclosure')
        if enclosure is not None:
            image_url = enclosure.get('url')

        description = self.get_element_text(item, 'description')
        description = description.strip()
        if description.startswith('<![CDATA['):
            description = description[9:]
        if description.endswith(']]>'):
            description = description[:-3]
        description = description.strip()

        title       = self.get_element_text(item, 'title')
        description = description
        link        = self.get_element_text(item, 'link')
        article_id = Guid(self.get_element_text(item, 'guid'))
        author      = self.get_element_text(item, 'author')
        pub_date    = self.get_element_text(item, 'pubDate')
        when        = self.parse_when(pub_date)
        return Model__Hacker_News__Article(article_id   = article_id   ,
                                           title        = title        ,
                                           description  = description  ,
                                           link         = link         ,
                                           when         = when         ,
                                           author       = author       ,
                                           image_url    = image_url    )