from unittest                                                  import TestCase
from cbr_custom_news_feeds.fast_api.routes.Routes__Hacker_News import Routes__Hacker_News
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.Hacker_News__Prompt_Creator import \
    PROMPT_SCHEMA__HACKER_NEWS


class test__int__Routes__Hacker_News(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.routes_hacker_news = Routes__Hacker_News()

    def test_routes_setup(self):
        with self.routes_hacker_news as _:
            assert _.tag == 'hacker-news'
            _.setup_routes()
            assert '/feed'      in _.routes_paths()
            #assert '/articles'  in _.routes_paths()

    def test_get_feed(self):
        with self.routes_hacker_news as _:
            feed_data = _.feed()
            assert isinstance(feed_data, dict)
            assert 'title'       in feed_data
            assert 'link'        in feed_data
            assert 'description' in feed_data
            assert 'articles'    in feed_data
            assert feed_data['title'] == 'The Hacker News'
            for article in feed_data['articles']:
                assert 'title'        in article
                assert 'description'  in article
                assert 'link'         in article
                #assert 'guid'         in article
                assert 'pub_date'     in article
                assert 'author'       in article
                assert 'image_url'    in article

    def test_feed_prompt(self):
        expected_start_text = PROMPT_SCHEMA__HACKER_NEWS[0:26]
        with self.routes_hacker_news as _:
            feed_prompt = _.feed_prompt()
            assert feed_prompt.body.decode().startswith(expected_start_text) is True
