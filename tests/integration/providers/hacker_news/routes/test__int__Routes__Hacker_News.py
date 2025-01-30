import pytest
from unittest                                                                    import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Prompt_Creator import PROMPT_SCHEMA__HACKER_NEWS
from myfeeds_ai.providers.cyber_security.hacker_news.routes.Routes__Hacker_News  import Routes__Hacker_News
from osbot_utils.utils.Objects                                                   import obj, __
from tests.integration.data_feeds__objs_for_tests                                import cbr_website__assert_local_stack


class test__int__Routes__Hacker_News(TestCase):

    @classmethod
    def setUpClass(cls):
        cbr_website__assert_local_stack()
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
                assert 'when'         in article
                assert 'author'       in article
                assert 'image_url'    in article

    def test_feed_prompt(self):
        expected_start_text = PROMPT_SCHEMA__HACKER_NEWS[0:26]
        with self.routes_hacker_news as _:
            feed_prompt = _.feed_prompt()
            assert feed_prompt.body.decode().startswith(expected_start_text) is True

    def test_files_paths(self):
        with self.routes_hacker_news as _:
            path_when = _.files.s3_db.s3_path__when()
            assert obj(_.files_paths()) == __(data    =__(latest_feed_xml =f'{path_when}/feed-xml.json',
                                                          latest_feed_data=f'{path_when}/feed-data.json'),
                                              error   = None    ,
                                              message =''       ,
                                              status  ='ok'     )

    def test_raw_data__all_file(self):
        with self.routes_hacker_news as _:
            assert type(_.raw_data_all_files()) is list

    def test_raw_data_feed_current(self):
        with self.routes_hacker_news as _:
            current_feed = _.raw_data_feed_current()
            year, month, day, hour = _.files.s3_db.s3_key_generator.path__for_date_time__now_utc().split('/')
            assert _.raw_data_feed(year, month, day, hour) == current_feed

    def test_data_feed_current(self):
        with self.routes_hacker_news as _:
            current_feed = _.data_feed_current()
            assert current_feed.get('status') == 'ok'
            assert len(obj(current_feed).data.feed_data.articles) >0


            #year, month, day, hour = _.files.s3_db.s3_key_generator.path__for_date_time__now_utc().split('/')
            #assert _.raw_data_feed(year, month, day, hour) == current_feed


