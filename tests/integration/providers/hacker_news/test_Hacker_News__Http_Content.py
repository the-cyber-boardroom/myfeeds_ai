from unittest                                                                             import TestCase
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.Hacker_News__Http_Content import Hacker_News__Http_Content


class test_Hacker_News__Http_Content(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.http_content = Hacker_News__Http_Content()

    def test_requests_get(self):
        with self.http_content as target:
            path = 'TheHackersNews'
            response = target.requests_get(path)
            assert response.status_code == 200
            assert response.headers['content-type'             ] == 'text/xml; charset=utf-8'
            assert response.headers['content-encoding'         ] == 'gzip'
            assert response.headers['server'                   ] == 'ESF'


    def test_get_feed_content(self):
        with self.http_content as target:
            content = target.get_feed_content()
            assert isinstance(content, str)
            assert len(content) > 0
            assert '<?xml' in content
            assert '<rss' in content
            assert '<channel>' in content
            assert '<title>The Hacker News</title>' in content

    def test_get_feed_data(self):
        with self.http_content as target:
            data = target.get_feed_data()
            assert isinstance(data, dict)
            assert isinstance(data['articles'], list)
            assert 'title'           in data
            assert 'link'            in data
            assert 'description'     in data
            assert 'language'        in data
            assert data['title']     == 'The Hacker News'
            assert data['link']      == 'https://thehackernews.com'
            assert data['language']  == 'en-us'

            assert len(data['articles']) > 0

            # Check structure of first article
            article = data['articles'][0]
            assert 'title'        in article
            assert 'description' in article
            assert 'link'        in article
            assert 'guid'        in article
            assert 'pub_date'    in article
            assert 'author'      in article
            assert 'image_url'   in article