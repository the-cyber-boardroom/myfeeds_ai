import xml.etree.ElementTree   as ET
from typing                                                                                        import List
from xml.etree.ElementTree                                                                         import Element
from osbot_utils.base_classes.Type_Safe                                                            import Type_Safe
from osbot_utils.utils.Dev                                                                         import pprint
from cbr_custom_data_feeds.providers.cyber_security.hacker_news.models.Model__Hacker_News__Article import Model__Hacker_News__Article
from cbr_custom_data_feeds.providers.cyber_security.hacker_news.models.Model__Hacker_News__Feed    import Model__Hacker_News__Feed

XML__NAMESPACES__Hacker_News = { 'atom'   : 'http://www.w3.org/2005/Atom'                  ,
                                 'content': 'http://purl.org/rss/1.0/modules/content/'     ,
                                 'sy'     : 'http://purl.org/rss/1.0/modules/syndication/' }

class Hacker_News__Parser(Type_Safe):                                             # Parser for The Hacker News RSS feed
    root            : Element = None
    xml_content     : str     = None
    channel         : Element = None

    def setup(self, xml_content: str):                                            # Store and parse the XML content
        self.xml_content = xml_content
        self.root        = ET.fromstring(xml_content)
        self.channel     = self.root.find('channel')
        return self

    def get_element_text(self, element: Element, tag: str, default: str = ""):    # Helper method to safely get text from an XML element
        elem = element.find(tag)
        return elem.text if elem is not None else default

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

        return Model__Hacker_News__Feed(title           = self.get_element_text(self.channel, 'title'        )                  ,
                                      link              = self.get_element_text(self.channel, 'link'         )                  ,
                                      description       = self.get_element_text(self.channel, 'description'  )                  ,
                                      language          = self.get_element_text(self.channel, 'language'     )                  ,
                                      last_build_date   = self.get_element_text(self.channel, 'lastBuildDate')                  ,
                                      update_period     = self.get_element_text_ns(self.channel, './/sy:updatePeriod', 'hourly'),
                                      update_frequency  = update_frequency                                                      ,
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

        return Model__Hacker_News__Article(title       = self.get_element_text(item, 'title')      ,
                                         description  = description                                 ,
                                         link        = self.get_element_text(item, 'link')         ,
                                         #guid        = self.get_element_text(item, 'guid')         ,       # todo: review this since in the current feed the guid is just the link
                                         pub_date    = self.get_element_text(item, 'pubDate')      ,
                                         author      = self.get_element_text(item, 'author')       ,
                                         image_url   = image_url                                   )