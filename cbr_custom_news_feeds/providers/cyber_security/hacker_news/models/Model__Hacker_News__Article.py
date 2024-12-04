from osbot_utils.base_classes.Type_Safe import Type_Safe

class Model__Hacker_News__Article(Type_Safe):  # Schema for a single Hacker News article
    title      : str
    description: str
    link       : str
    guid       : str
    pub_date   : str
    author     : str
    image_url  : str