import pytest
from unittest                                                                                   import TestCase
from mgraph_db.mgraph.MGraph                                                                    import MGraph
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Article__Entities     import Hacker_News__Article__Entities
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Text_Entities         import Hacker_News__Text_Entities
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article              import Schema__Feed__Article
from osbot_utils.helpers.Obj_Id                                                                 import Obj_Id
from osbot_utils.utils.Dev                                                                      import pprint
from osbot_utils.utils.Files                                                                    import file_create_from_bytes
from tests.integration.data_feeds__objs_for_tests                                               import myfeeds_tests__setup_local_stack


class test_Hacker_News__Text_Entities(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()                                                                              # make sure we are using the LocalStack
        cls.text_entities   = Hacker_News__Text_Entities().setup()                                                      # get the main helper class
        cls.articles_step_5 = cls.text_entities.file_articles_current.next_step__5__merge_text_entities_graphs()
        if not cls.articles_step_5:                                                                                     # make sure there are article with data that we can use in the tests
            pytest.skip("can't run test because there are no step 5 articles to use as example")                        # todo: create synthetic data to be used here instead of the data from LocalStack
        cls.article           = cls.articles_step_5[3]                                                                    # use the first article as example
        cls.article_id        = cls.article.article_id
        cls.article_entities  = cls.text_entities.article_entities(article_id=cls.article_id)                           # get the article_entities object

    def test__setUpClass__(self):
        assert type(self.text_entities   ) is Hacker_News__Text_Entities
        assert type(self.articles_step_5 ) is list
        assert type(self.article         ) is Schema__Feed__Article
        assert type(self.article_id      ) is Obj_Id

    def test_article_entities(self):
        with self.text_entities as _:
            article_entities = _.article_entities(article_id=self.article_id)
            assert type(article_entities)                                                 is Hacker_News__Article__Entities         # confirm it was loaded ok
            assert article_entities.article_id                                            == self.article_id                        # with the expected article_id
            assert article_entities.file___text__entities__description__mgraph().exists() is True                                   # and that both title and description
            assert article_entities.file___text__entities__title__mgraph      ().exists() is True                                   #     mgraphs exist

    def test_mgraph_for_article__text_entities__title(self):
        with self.text_entities as _:
            mgraph = _.mgraph__for_article__text_entities__title(article_entities=self.article_entities)
            assert type(mgraph) is MGraph

    def test_png_bytes__for_article__text_entities__description(self):
        pprint(self.article_entities.article_id)
        with self.text_entities as _:
            png_bytes = _.png_bytes__for_article__text_entities__description(article_entities=self.article_entities)
            assert type(png_bytes) is bytes
            assert len (png_bytes) > 255
            file_create_from_bytes(path=f'{self.__class__.__name__}__description.png', bytes=png_bytes)
            pprint(len(png_bytes))

    def test_png_bytes__for_article__text_entities__title(self):
        with self.text_entities as _:
            png_bytes = _.png_bytes__for_article__text_entities__title(article_entities=self.article_entities)
            assert type(png_bytes) is bytes
            assert len (png_bytes) > 255
            file_create_from_bytes(path=f'{self.__class__.__name__}__title.png', bytes=png_bytes)
            pprint(len(png_bytes))


    def test_add_text_entities_mgraph(self):
        # pprint(self.article.json())
        # with self.article_entities as _:
        #     print()
        #     print(_.file___text__entities__description__png     ().delete__now())
        #     print(_.file___text__entities__description__mgraph  ().delete__now())
        #     print(_.file___text__entities__title__mgraph        ().delete__now())
        #     print(_.file___text__entities__title__png           ().delete__now())
        # return

        with self.text_entities as _:
            article_entities                  = _.article_entities(article_id=self.article_id)
            article_id                        = article_entities.article_id
            mgraph_text_entities__title       = _.mgraph__for_article__text_entities__title      (article_entities=article_entities)
            mgraph_text_entities__description = _.mgraph__for_article__text_entities__description(article_entities=article_entities)

            #pprint(self.article.json())
            _.add_text_entities_mgraph(article_id=article_id, mgraph_text_entities=mgraph_text_entities__title      )
            # print('-----')
            _.add_text_entities_mgraph(article_id=article_id, mgraph_text_entities=mgraph_text_entities__description)


            # _.screenshot__setup()
            # _.screenshot().save_to(f'{self.__class__.__name__}.png').dot()

