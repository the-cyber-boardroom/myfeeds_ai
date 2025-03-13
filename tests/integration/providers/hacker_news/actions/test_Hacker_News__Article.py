from unittest                                                                     import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Article import Hacker_News__Article

class test_Hacker_News__Article(TestCase):

    def test_file_article(self):
        article_id         = '9153bba8'
        path__folder__data = '1955/11/12/22'
        with Hacker_News__Article(article_id=article_id, path__folder__data=path__folder__data) as _:
            file_article = _.file_article()
            assert file_article.path_now        () == f'{path__folder__data}/articles/{article_id}/feed-article.json'
            assert file_article.folder__path_now() == f'{path__folder__data}/articles/{article_id}'

