from cbr_custom_news_feeds.news_feeds.News_Feeds__Http_Content import News_Feeds__Http_Content


class OSS__Http_Content(News_Feeds__Http_Content):
    server : str = 'https://open-security-summit.org/'

    def raw_content(self):
        return self.requests_get('content.json').json()