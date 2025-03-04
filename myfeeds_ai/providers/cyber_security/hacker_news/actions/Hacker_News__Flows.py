from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Data import Hacker_News__Data
from osbot_utils.type_safe.Type_Safe import Type_Safe
from osbot_utils.utils.Lists import list_index_by, list_group_by

# todo refactor code below to use the new file_current_articles class
class Hacker_News__Flows(Type_Safe):
    hacker_news_data: Hacker_News__Data

    # def current_articles(self):
    #     return self.hacker_news_data.current_articles()
    #
    # def current_articles__group_by__status(self):
    #     articles        = self.current_articles().json().get('articles')
    #     articles_values = list(articles.values())
    #
    #     return list_group_by(articles_values,'status')