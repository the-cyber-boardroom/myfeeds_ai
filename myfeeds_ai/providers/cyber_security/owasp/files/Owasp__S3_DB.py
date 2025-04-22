from typing                                                         import List
from myfeeds_ai.data_feeds.Data_Feeds__S3_DB                        import Data_Feeds__S3_DB
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator            import S3_Key__File__Extension
from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Providers      import Model__Data_Feeds__Providers
from osbot_utils.helpers.Safe_Id                                    import Safe_Id


class Owasp__S3_DB(Data_Feeds__S3_DB):
    provider_name  : Model__Data_Feeds__Providers  = Model__Data_Feeds__Providers.OWASP

    def s3_path__now(self, file_id   : Safe_Id                 = None,
                           extension : S3_Key__File__Extension = None,
                           areas     : List[Safe_Id]           = None) -> str:
        path = ''                                                               # we don't use the now (i.e. datetime) path in the owasp files

        if areas:
            path += '/'.join(str(area) for area in areas)

        if file_id and extension:
            path += f'/{file_id}.{extension.value}'

        return path



