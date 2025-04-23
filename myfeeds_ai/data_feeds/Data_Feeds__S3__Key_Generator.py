from datetime                                           import datetime
from enum                                               import Enum
from typing                                             import List
from myfeeds_ai.data_feeds.Data_Feeds__Shared_Constants import S3_FOLDER__ROOT_FOLDER__PUBLIC_DATA
from osbot_aws.aws.s3.S3__Key_Generator                 import S3__Key_Generator
from osbot_utils.helpers.Safe_Id                        import Safe_Id
from osbot_utils.type_safe.decorators.type_safe         import type_safe


class S3_Key__File__Content_Type(Enum):
    HTML       : str = 'text/html; charset=utf-8'
    JSON       : str = 'application/json; charset=utf-8'
    MARKDOWN   : str = "text/markdown"
    MGRAPH__DOT: str = "text/vnd.graphviz"
    PNG        : str = 'image/png'
    TXT        : str = 'text/plain; charset=utf-8'

    def __str__(self):
        return self.value


class S3_Key__File__Extension(Enum):
    HTML         : str = 'html'
    JSON         : str = 'json'
    PNG          : str = 'png'
    MARKDOWN     : str = 'md'
    MGRAPH__DOT  : str = 'mgraph.dot'
    MGRAPH__JSON : str = 'mgraph.json'
    MGRAPH__PNG  : str = 'mgraph.png'
    TXT          : str = 'txt'

    def __str__(self):
        return self.value

DEFAULT__S3_Key__FILE_EXTENSION = S3_Key__File__Extension.JSON

class Data_Feeds__S3__Key_Generator(S3__Key_Generator):                # todo: refactor this to a generic class (for multiple feeds)
    root_folder            = S3_FOLDER__ROOT_FOLDER__PUBLIC_DATA
    split_when      : bool = True
    use_minutes     : bool = False

    @type_safe
    def s3_path(self, year     : int,
                      month    : int,
                      day      : int,
                      hour     : int,
                      areas    : List[Safe_Id]          = None,
                      file_id  : Safe_Id                = None,
                      extension: S3_Key__File__Extension = None
                 ) -> str:
        path = f'{year:04}/{month:02}/{day:02}/{hour:02}'

        if areas:
            path += '/' + '/'.join(str(area) for area in areas)

        if file_id and extension:
            path += f'/{file_id}.{extension.value}'

        return path

    def s3_path__date_time(self, date_time: datetime,
                                 areas    : List[Safe_Id]          = None,
                                 file_id  : Safe_Id                = None,
                                 extension: S3_Key__File__Extension = None
                            ) -> str:
        kwargs = dict(year    = date_time.year ,
                      month   = date_time.month,
                      day     = date_time.day  ,
                      hour    = date_time.hour ,
                      areas   = areas          ,
                      file_id = file_id        ,
                      extension = extension    )
        return self.s3_path(**kwargs)

    def s3_path__now(self, file_id: Safe_Id=None, extension: S3_Key__File__Extension=None, areas: List[Safe_Id] = None):                # todo:refactor the name of this method which is not consistent with the other s3_path__now__** methods
        year, month, day, hour = self.path__for_date_time__now_utc().split('/')
        return self.s3_path(int(year), int(month), int(day), int(hour), file_id=file_id, extension=extension, areas=areas)


    def s3_path__now__utc(self):
        return self.path__for_date_time__now_utc()

    def s3_path_folder(self, year: int, month: int, day: int, hour: int, folder_id: Safe_Id):
        return f'{year:04}/{month:02}/{day:02}/{hour:02}/{folder_id}'

    def s3_path__folder__now(self, folder_id: Safe_Id):
        year, month, day, hour = self.path__for_date_time__now_utc().split('/')
        return self.s3_path_folder(year, month, day, hour, folder_id)



