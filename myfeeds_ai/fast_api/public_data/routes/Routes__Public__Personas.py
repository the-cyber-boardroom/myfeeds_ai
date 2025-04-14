from fastapi                                                                        import Path
from fastapi.responses                                                              import Response
from myfeeds_ai.personas.actions.My_Feeds__Personas__Storage                        import My_Feeds__Personas__Storage
from osbot_utils.utils.Status                                                       import status_error
from osbot_fast_api.api.Fast_API_Routes                                             import Fast_API_Routes


ROUTES__TAG__PUBLIC__PERSONAS   = 'personas'
ROUTES__PATHS__PUBLIC__PERSONAS = []                        # todo: wire this up since it is not currently being checked

class Routes__Public__Personas(Fast_API_Routes):
    tag              : str                         = ROUTES__TAG__PUBLIC__PERSONAS
    personas_storage : My_Feeds__Personas__Storage

    def file_exists(self, file_path: str = Path(...)):
        with self.personas_storage as _:
            return {'file_exists': _.path__exists(file_path),
                    'file_path'  : file_path                }

    def file_info(self, file_path: str = Path(...)):
        with self.personas_storage as _:
            if _.path__exists(file_path):
                return _.path__file_info(file_path)
            return status_error(error='file not found', data=dict(file_path=file_path))

    def file_contents(self, file_path: str = Path(...)):
        with self.personas_storage as _:
            if _.path__exists(file_path):
                file_info    = _.path__file_info(file_path)
                content_type = file_info.get('ContentType')
                bytes_data   = _.path__load_bytes(file_path)
                return Response(content    = bytes_data  ,
                                media_type = content_type)
            else:
                return status_error(error='file not found', data=dict(file_path=file_path))


    def setup_routes(self):
        self.router.add_api_route(path='/{file_path:path}/exists', endpoint=self.file_exists      , methods=['GET'])
        self.router.add_api_route(path='/{file_path:path}/info'  , endpoint=self.file_info        , methods=['GET'])
        self.router.add_api_route(path='/{file_path:path}'       , endpoint=self.file_contents    , methods=['GET'])

