import json
from typing                                         import Dict, Any, List, Optional
from requests                                       import Session
from requests.auth                                  import HTTPBasicAuth
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.type_safe.Type_Safe                import Type_Safe
from osbot_utils.utils.Env                          import get_env

DEFAULT__CONFIG__HOST           = 'api.openobserve.ai'
DEFAULT__CONFIG__STREAM         = 'default'

ENV_NAME__OPEN_OBSERVE__HOST    = "OPEN_OBSERVE__HOST"
ENV_NAME__OPEN_OBSERVE__ORG     = "OPEN_OBSERVE__ORG"
ENV_NAME__OPEN_OBSERVE__STREAM  = "OPEN_OBSERVE__STREAM"
ENV_NAME__OPEN_OBSERVE__USER    = "OPEN_OBSERVE__USER"
ENV_NAME__OPEN_OBSERVE__API_KEY = "OPEN_OBSERVE__API_KEY"



class Schema__Open_Observe__Server_Config(Type_Safe):
    api_key      : str
    host         : str
    organisation : str
    stream       : str
    user         : str
    enabled      : bool

class Open_Observe__Http(Type_Safe):

    def config(self):
        api_key      = get_env(ENV_NAME__OPEN_OBSERVE__API_KEY                         )
        host         = get_env(ENV_NAME__OPEN_OBSERVE__HOST   , DEFAULT__CONFIG__HOST  )
        organisation = get_env(ENV_NAME__OPEN_OBSERVE__ORG                             )
        stream       = get_env(ENV_NAME__OPEN_OBSERVE__STREAM , DEFAULT__CONFIG__STREAM)
        user         = get_env(ENV_NAME__OPEN_OBSERVE__USER                            )
        enabled      = all(value not in [None, ''] for value in [api_key, organisation, user])
        kwargs       = dict(api_key      = api_key        ,
                            enabled      = enabled        ,
                            host         = host           ,
                            organisation = organisation   ,
                            stream       = stream         ,
                            user         = user           )
        return Schema__Open_Observe__Server_Config(**kwargs)

    @cache_on_self
    def session(self) -> Optional[Session]:                                         # Setup connection pooling
        with self.config() as _:
            if _.enabled:
                session = Session()
                session.headers.update({'Content-Type': 'application/json'})
                session.auth = HTTPBasicAuth(_.user, _.api_key)                     # Setup basic auth
                return session

    def send_data(self, data: List[Dict[str, Any]]) -> bool:                       # Send logs to OpenObserve
        url = self.url__json()
        if url:
            response = self.session().post(url, json=data)
            response.raise_for_status()
            return True
        return False

    @cache_on_self
    def url__json(self):
        with self.config() as _:
            if _.enabled:
                url = f'https://{_.host}/api/{_.organisation}/{_.stream}/_json'
                return url




    # todo: see why this is now working on O2 Cloud (I'm getting the error: "requests.exceptions.HTTPError: 502 Server Error: Bad Gateway for url:")
    # def send_batch(self, data: List[Dict[str, Any]]) -> bool:                          # Send data using bulk API
    #     url = self.url__bulk()
    #     if url:
    #         stream = self.config().stream
    #         bulk_data = "\n".join(json.dumps({"index": {"_index": stream}}) + "\n" + json.dumps(record)
    #                               for record in data) + "\n"  # Ensure final newline
    #         response = self.session__bulk().post(url, json=bulk_data)                         # Send all records in one request
    #         response.raise_for_status()
    #
    #         return True
    #     return False
    # @cache_on_self
    # def session__bulk(self) -> Optional[Session]:  # Setup connection pooling
    #     with self.config() as _:
    #         if _.enabled:
    #             session = Session()
    #             session.headers.update({'Content-Type': 'application/x-ndjson'})    # todo: trying this to see if the 502 was caused by the 'Content-Type', but it didn't work
    #             session.auth = HTTPBasicAuth(_.user, _.api_key)                     # Setup basic auth
    #             return session
    # @cache_on_self
    # def url__bulk(self):
    #     with self.config() as _:
    #         if _.enabled:
    #             url = f'https://{_.host}/api/{_.organisation}/_bulk'
    #             return url
