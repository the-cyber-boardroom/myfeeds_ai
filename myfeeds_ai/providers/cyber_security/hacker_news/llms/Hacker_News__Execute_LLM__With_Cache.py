from myfeeds_ai.providers.cyber_security.hacker_news.llms.Virtual_Storage__S3 import Virtual_Storage__S3
from osbot_utils.decorators.methods.cache_on_self                       import cache_on_self
from osbot_utils.helpers.llms.actions.LLM_Request__Execute              import LLM_Request__Execute
from osbot_utils.helpers.llms.builders.LLM_Request__Builder__Open_AI    import LLM_Request__Builder__Open_AI
from osbot_utils.helpers.llms.cache.LLM_Request__Cache__File_System     import LLM_Request__Cache__File_System
from osbot_utils.helpers.llms.cache.Virtual_Storage__Local__Folder      import Virtual_Storage__Local__Folder
from osbot_utils.helpers.llms.platforms.open_ai.API__LLM__Open_AI       import ENV_NAME_OPEN_AI__API_KEY, API__LLM__Open_AI
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request               import Schema__LLM_Request
from osbot_utils.helpers.safe_str.Safe_Str__File__Path                  import Safe_Str__File__Path
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                         import type_safe
from osbot_utils.utils.Env                                              import get_env
from osbot_utils.utils.Files                                            import folder_create

FOLDER__CACHE__HACKER_NEWS__EXECUTE_LLM = '/tmp/_my-feeds-llm-cache/Hacker_News__Execute_LLM__With_Cache'

class Hacker_News__Execute_LLM__With_Cache(Type_Safe):
    cache_root_folder : Safe_Str__File__Path            = Safe_Str__File__Path(folder_create(FOLDER__CACHE__HACKER_NEWS__EXECUTE_LLM))
    virtual_storage   : Virtual_Storage__S3                         # Virtual_Storage__Local__Folder  = None
    llm_cache         : LLM_Request__Cache__File_System = None
    llm_execute       : LLM_Request__Execute            = None
    llm_api           : API__LLM__Open_AI
    request_builder   : LLM_Request__Builder__Open_AI


    def setup(self):
        #self.virtual_storage   = Virtual_Storage__Local__Folder  ( root_folder     = self.cache_root_folder )
        self.llm_cache         = LLM_Request__Cache__File_System ( virtual_storage = self.virtual_storage   ).setup()
        self.llm_execute       = LLM_Request__Execute            ( llm_cache       = self.llm_cache         ,
                                                                   llm_api         = self.llm_api           ,
                                                                   request_builder = self.request_builder   )
        return self

    @cache_on_self
    def enabled(self):
        return get_env(ENV_NAME_OPEN_AI__API_KEY)

    @type_safe
    def execute__llm_request(self, llm_request: Schema__LLM_Request):
        if self.enabled():
            return self.llm_execute.execute(llm_request)

    def refresh_llm_cache(self, value=True):
        self.llm_execute.refresh_cache = value
        return self
