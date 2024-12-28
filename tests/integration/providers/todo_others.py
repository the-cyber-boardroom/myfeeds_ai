# def parse_feed(self):
#
#     xml_file_load = Xml__File__Load()
#     xml_file = xml_file_load.load_from_string(self.xml_content)
#     xml_file_to_dict = Xml__File__To_Dict()
#
#     xml_dict = xml_file_to_dict.to_dict(xml_file)
#     return xml_dict

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