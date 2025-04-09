from fastapi                                                                    import Path
from osbot_fast_api.api.Fast_API_Routes                                         import Fast_API_Routes
from myfeeds_ai.providers.cyber_security.hacker_news.llms.Virtual_Storage__S3   import Virtual_Storage__S3
from osbot_utils.utils.Http                                                     import url_join_safe
from osbot_utils.utils.Status                                                   import status_error

ROUTES__BASE_PATH = ''

class Routes__LLM_Cache__Data(Fast_API_Routes):
    tag                : str = 'data'
    virtual_storage_s3 : Virtual_Storage__S3

    def all_files(self):
        return self.virtual_storage_s3.files__all()

    def file_contents(self, file_path: str = Path(...)):
        s3_key = url_join_safe(f'llm-cache/data',file_path)
        if self.virtual_storage_s3.file__exists(s3_key):
            return self.virtual_storage_s3.json__load(s3_key)
        return status_error(message="file not found", data=s3_key)

    def setup_routes(self):
        self.add_route_get(self.all_files)
        self.router.add_api_route(path='/{file_path:path}', endpoint=self.file_contents, methods=['GET'])