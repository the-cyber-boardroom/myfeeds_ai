from typing                                                                                         import List
from osbot_utils.base_classes.Type_Safe                                                             import Type_Safe
from cbr_custom_data_feeds.providers.cyber_security.hacker_news.models.Model__Hacker_News__Article  import Model__Hacker_News__Article


class Model__Hacker_News__Feed(Type_Safe):      # Schema for the entire Hacker News feed"""
    title           : str
    link            : str
    description     : str
    language        : str
    last_build_date : str
    update_period   : str
    update_frequency: int
    articles        : List[Model__Hacker_News__Article]