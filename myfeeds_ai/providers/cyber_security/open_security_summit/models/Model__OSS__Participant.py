from typing                                                                                      import List
from myfeeds_ai.providers.cyber_security.open_security_summit.models.Model__OSS__Base import Model_OSS__Base


class Model__OSS__Participant(Model_OSS__Base):                          # Participant model with specific fields
    company        : str
    job_title      : str
    linkedin       : str
    twitter        : str
    facebook       : str
    website        : List[str]
    image          : str