from unittest                                                                                      import TestCase
from unittest.mock                                                                                 import patch
from cbr_custom_data_feeds.providers.cyber_security.hacker_news.Hacker_News__Http_Content          import Hacker_News__Http_Content
from cbr_custom_data_feeds.providers.cyber_security.hacker_news.models.Model__Hacker_News__Article import Model__Hacker_News__Article
from cbr_custom_data_feeds.providers.cyber_security.hacker_news.models.Model__Hacker_News__Feed    import Model__Hacker_News__Feed

class test_Hacker_News__Http_Content(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.http_content = Hacker_News__Http_Content()
        cls.sample_feed = Model__Hacker_News__Feed( title="The Hacker News",
                                                    link="https://thehackernews.com",
                                                    description="Most trusted cybersecurity news source",
                                                    language="en-us",
                                                    last_build_date="Thu, 05 Dec 2024 02:15:56 +0530",
                                                    update_period="hourly",
                                                    update_frequency=1,
                                                    articles=[Model__Hacker_News__Article( title="Test Article",
                                                                                           description="Test Description",
                                                                                           link="https://example.com",
                                                                                           pub_date="Wed, 04 Dec 2024 22:53:00 +0530",
                                                                                           author="Test Author",
                                                                                           image_url="https://example.com/image.jpg" )])

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
            content = target.feed_content()
            assert isinstance(content, str)
            assert len(content) > 0
            assert '<?xml' in content
            assert '<rss' in content
            assert '<channel>' in content
            assert '<title>The Hacker News</title>' in content

    def test_get_feed_data(self):
        with self.http_content as target:
            news_feed = target.feed_data()
            data      = news_feed.json()
            assert type(news_feed) is Model__Hacker_News__Feed
            assert type(data     ) is dict
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
            #assert 'guid'        in article
            assert 'pub_date'    in article
            assert 'author'      in article
            assert 'image_url'   in article

    # todo: remove this patch once we have added the DB_S3 support
    @patch('cbr_custom_data_feeds.providers.cyber_security.hacker_news.Hacker_News__Http_Content.Hacker_News__Http_Content.feed_data')
    def test_get_prompt_schema(self, mock_feed_data):  # Test schema prompt creation
        mock_feed_data.return_value = self.sample_feed

        with self.http_content as _:
            prompt = _.feed_prompt(size=1)

            assert "The Hacker News" in prompt  # Check feed details
            assert "Test Article" in prompt  # Check article content
            assert "Hacker News schema" in prompt  # Check schema information

            mock_feed_data.assert_called_once()  # Verify feed data was fetched

    # @patch('cbr_custom_data_feeds.providers.cyber_security.hacker_news.Hacker_News__Http_Content.Hacker_News__Http_Content.get_feed_data')
    # def test_get_prompt_analysis(self, mock_get_feed_data):  # Test analysis prompt creation
    #     mock_get_feed_data.return_value = self.sample_feed
    #
    #     with self.http_content as _:
    #         prompt = _.get_prompt_analysis(size=1)
    #
    #         assert "The Hacker News" in prompt  # Check feed details
    #         assert "Test Article" in prompt  # Check article content
    #         assert "current cybersecurity landscape" in prompt  # Check prompt format
    #
    #         mock_get_feed_data.assert_called_once()  # Verify feed data was fetched

    # @patch('cbr_custom_data_feeds.providers.cyber_security.hacker_news.Hacker_News__Http_Content.Hacker_News__Http_Content.get_feed_data')
    # def test_get_prompt_executive(self, mock_get_feed_data):  # Test executive prompt creation
    #     mock_get_feed_data.return_value = self.sample_feed
    #
    #     with self.http_content as _:
    #         prompt = _.get_prompt_executive(size=1)
    #
    #         assert "Test Article" in prompt  # Check article title
    #         assert "cybersecurity news headlines" in prompt  # Check prompt format
    #         assert "Test Description" not in prompt  # Verify only headlines included
    #
    #         mock_get_feed_data.assert_called_once()