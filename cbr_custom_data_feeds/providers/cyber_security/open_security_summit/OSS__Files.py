from cbr_custom_data_feeds.data_feeds.Data_Feeds__Files                                                     import Data_Feeds__Files
from cbr_custom_data_feeds.providers.cyber_security.open_security_summit.OSS__Http_Content                  import OSS__Http_Content
from cbr_custom_data_feeds.providers.cyber_security.open_security_summit.OSS__S3_DB                         import OSS__S3_DB
from cbr_custom_data_feeds.providers.cyber_security.open_security_summit.models.Model__OSS__Latest_Versions import Model__OSS__Latest_Versions
from osbot_utils.decorators.methods.type_safe                                                               import type_safe

RAW_FEED__CREATED__BY = 'OSS__Files.raw_content__current'

class OSS__Files(Data_Feeds__Files):
    s3_db        : OSS__S3_DB
    http_content : OSS__Http_Content

    @type_safe
    def latest_versions__save(self, latest_versions: Model__OSS__Latest_Versions):      # todo: create helper method to handle cases like this of a file that saves a particular class
        s3_path = self.s3_db.s3_path__latest_versions()
        s3_key  = self.s3_db.s3_key__for_provider_path(s3_path)
        self.s3_db.s3_save_data(latest_versions.json(), s3_key)
        return s3_path

    def latest_versions__load(self) -> Model__OSS__Latest_Versions:
        s3_path         = self.s3_db.s3_path__latest_versions()
        s3_key          = self.s3_db.s3_key__for_provider_path(s3_path)
        file_data       = self.s3_db.s3_file_data(s3_key)
        latest_versions = Model__OSS__Latest_Versions.from_json(file_data)
        if latest_versions:
            return latest_versions
        return Model__OSS__Latest_Versions()

    def latest_versions__update(self, **kwargs):
        latest_versions__original = self.latest_versions__load()
        latest_versions__json     = latest_versions__original.json()
        latest_versions__json.update(**kwargs)
        latest_versions__updated = Model__OSS__Latest_Versions.from_json(latest_versions__json)
        return self.latest_versions__save(latest_versions__updated)

    def raw_content__current(self, refresh=False):
        raw_content = self.s3_db.raw_content__load__now()
        if refresh or not raw_content:
            raw_content = self.http_content.raw_content()
            result      = self.s3_db.raw_content__save(raw_content)
            s3_path     = result.get('s3_path')
        return raw_content
