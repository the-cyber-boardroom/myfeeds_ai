from unittest                                                                   import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Flows import Hacker_News__Flows
from osbot_utils.utils.Misc                                                     import list_set
from tests.integration.data_feeds__objs_for_tests                               import myfeeds_tests__setup_local_stack


class test_Hacker_News__Flows(TestCase):

    @classmethod                                                                       # Setup test environment
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()                                              # Ensure LocalStack is running
        cls.hacker_new__flows = Hacker_News__Flows()

    # def test_current_articles(self):
    #     with self.hacker_new__flows as _:
    #         articles = _.current_articles()
    #         #pprint(articles)
    #
    # def test_current_articles__group_by__status(self):
    #     with self.hacker_new__flows as _:
    #         articles_by_status = _.current_articles__group_by__status()
    #         #pprint(articles_by_status)
    #         for status, articles in articles_by_status.items():
    #             #pprint(status)
    #             for article in articles:
    #                 assert list_set(article) == ['article_id'                   ,
    #                                              'knowledge_graph'              ,
    #                                              'llm_prompt'                   ,
    #                                              'location'                     ,
    #                                              'path__entities_mgraph__json'  ,
    #                                              'path__entities_mgraph__png'   ,
    #                                              'path__feed_article'           ,
    #                                              'status'                       ]
    #                 assert article.get('status') == status
