from typing                                                                             import List
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Article import Model__Hacker_News__Article
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__When    import Model__Hacker_News__When


class Model__Hacker_News__Feed(Type_Safe):      # Schema for the entire Hacker News feed"""
    title           : str
    link            : str
    description     : str
    language        : str
    update_period   : str
    update_frequency: int
    when            : Model__Hacker_News__When
    articles        : List[Model__Hacker_News__Article]