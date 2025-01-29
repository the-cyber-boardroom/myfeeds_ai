from osbot_utils.helpers.Random_Guid    import Random_Guid
from osbot_utils.helpers.Safe_Id        import Safe_Id
from osbot_utils.type_safe.Type_Safe     import Type_Safe

class Model__RSS_Provider(Type_Safe):
    provider_id : Random_Guid
    name        : Safe_Id
    title       : str
    url_website : str
    url_feed    : str        # todo: add Url class to Type_Safe set of classes
    date_added  : str        # todo: add Date class to Type_Safe set of classes
