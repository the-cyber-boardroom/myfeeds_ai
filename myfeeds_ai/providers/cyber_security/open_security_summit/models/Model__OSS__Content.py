from typing                                                                                                 import List
from myfeeds_ai.providers.cyber_security.open_security_summit.models.Model__OSS__Participant     import Model__OSS__Participant
from myfeeds_ai.providers.cyber_security.open_security_summit.models.Model__OSS__Session         import Model__OSS__Session
from osbot_utils.type_safe.Type_Safe                                                                         import Type_Safe


class Model__OSS__Content(Type_Safe):
    participants: List[Model__OSS__Participant]
    sessions    : List[Model__OSS__Session]
