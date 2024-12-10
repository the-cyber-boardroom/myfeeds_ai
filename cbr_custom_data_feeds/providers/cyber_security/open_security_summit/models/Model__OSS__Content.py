from typing                                                                                                 import List
from cbr_custom_data_feeds.providers.cyber_security.open_security_summit.models.Model__OSS__Participant     import Model__OSS__Participant
from cbr_custom_data_feeds.providers.cyber_security.open_security_summit.models.Model__OSS__Working_Session import Model__OSS__Working_Session
from osbot_utils.base_classes.Type_Safe                                                                     import Type_Safe


class Model__OSS__Content(Type_Safe):
    participants    : List[Model__OSS__Participant]
    working_sessions: List[Model__OSS__Working_Session]