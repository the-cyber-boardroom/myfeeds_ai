from enum import Enum

class Schema__Http__Request__Methods(Enum):
    GET     :str = 'GET'
    POST    :str = 'POST'
    PUT     :str = 'PUT'
    PATCH   :str = 'PATCH'
    DELETE  :str = 'DELETE'
    HEAD    :str = 'HEAD'
    OPTIONS :str = 'OPTIONS'
    TRACE   :str = 'TRACE'
    CONNECT :str = 'CONNECT'