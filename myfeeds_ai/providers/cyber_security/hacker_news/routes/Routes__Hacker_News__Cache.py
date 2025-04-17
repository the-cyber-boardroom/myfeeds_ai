from fastapi.responses                                                          import Response
from osbot_fast_api.api.Fast_API_Routes                                         import Fast_API_Routes
from myfeeds_ai.providers.cyber_security.hacker_news.llms.Virtual_Storage__S3   import Virtual_Storage__S3
from osbot_utils.helpers.llms.cache.LLM_Request__Cache__Storage                 import FILE_NAME__CACHE_INDEX
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response__Cache               import Schema__LLM_Response__Cache
from osbot_utils.utils.Json import json_parse

ROUTE_PATH__HACKER_NEWS__CACHE      = 'cache'
ROUTES_PATHS__HACKER_NEWS__CACHE    = [f'/{ROUTE_PATH__HACKER_NEWS__CACHE}/cache-entry'    ,
                                       f'/{ROUTE_PATH__HACKER_NEWS__CACHE}/cache-prompt'   ,
                                       f'/{ROUTE_PATH__HACKER_NEWS__CACHE}/cache-response' ,
                                       f'/{ROUTE_PATH__HACKER_NEWS__CACHE}/index'          ,
                                       f'/{ROUTE_PATH__HACKER_NEWS__CACHE}/all-files'      ]

class Routes__Hacker_News__Cache(Fast_API_Routes):
    tag               : str = ROUTE_PATH__HACKER_NEWS__CACHE
    virtual_storage_s3: Virtual_Storage__S3

    def all_files(self):
        return sorted(self.virtual_storage_s3.files__all())

    def cache_entry(self, cache_id: str):
        cache_index = self.index()
        cache_path  = cache_index.get('cache_id__to__file_path', {}).get(cache_id)
        if cache_path:
            return self.virtual_storage_s3.json__load(cache_path)
        return cache_path

    def cache_prompt(self, cache_id: str):
        cache_entry = self.cache_entry(cache_id)
        prompt      = ""
        if cache_entry:
            llm_response_cache = Schema__LLM_Response__Cache.from_json(cache_entry)
            messages           = llm_response_cache.llm__request.request_data.messages
            for message in messages:
                prompt += f"======= {message.role} ======\n"
                prompt += message.content

                prompt += "\n\n"

        return Response(content=prompt, media_type="text/plain")

    def cache_response(self, cache_id: str):
        cache_entry = self.cache_entry(cache_id)
        prompt      = ""
        if cache_entry:
            llm_response_cache = Schema__LLM_Response__Cache.from_json(cache_entry)
            response_data      = llm_response_cache.llm__response.response_data
            choices            = response_data.get('choices')
            choice             = choices[0]
            message            = choice.get('message')
            content            = message.get('content')
            return json_parse(content)

    def index(self):
        return self.virtual_storage_s3.json__load(FILE_NAME__CACHE_INDEX)

    def setup_routes(self):
        self.add_route_get(self.cache_entry   )
        self.add_route_get(self.cache_prompt  )
        self.add_route_get(self.cache_response)
        self.add_route_get(self.index         )
        self.add_route_get(self.all_files     )