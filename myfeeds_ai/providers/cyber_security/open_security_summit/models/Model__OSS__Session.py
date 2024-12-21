from typing                                                                                      import List
from myfeeds_ai.providers.cyber_security.open_security_summit.models.Model__OSS__Base import Model_OSS__Base


class Model__OSS__Session(Model_OSS__Base):                      # Working session model with specific fields
    event          : str
    organizers     : List[str]
    topics         : List[str]
    track          : str
    youtube_link   : str
    zoom_link      : str
    hey_summit     : str
    session_type   : str