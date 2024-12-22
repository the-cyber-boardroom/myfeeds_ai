from osbot_utils.base_classes.Type_Safe                                              import Type_Safe
from osbot_utils.helpers.Random_Guid                                                 import Random_Guid
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__When import Model__Hacker_News__When


class Model__Hacker_News__Article(Type_Safe):  # Schema for a single Hacker News article
    author     : str
    description: str
    guid       : Random_Guid
    image_url  : str
    link       : str
    when       : Model__Hacker_News__When
    title      : str