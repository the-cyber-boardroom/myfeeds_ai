from osbot_utils.helpers.Obj_Id                                                      import Obj_Id
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.helpers.Guid                                                        import Guid
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__When import Model__Hacker_News__When


class Model__Hacker_News__Article(Type_Safe):  # Schema for a single Hacker News article
    article_id    : Guid
    article_obj_id: Obj_Id
    author        : str
    description   : str
    image_url     : str
    link          : str
    title         : str
    when          : Model__Hacker_News__When