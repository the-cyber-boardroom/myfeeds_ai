from myfeeds_ai.data_feeds.Data_Feeds__S3_DB                                                     import Data_Feeds__S3_DB
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator import S3_Key__File_Extension
from myfeeds_ai.data_feeds.Data_Feeds__Shared_Constants                                          import S3_FILE_NAME__RAW__CONTENT, S3_FILE_NAME__CONTENT
from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Prompt                                      import Model__Data_Feeds__Prompt
from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Providers                                   import Model__Data_Feeds__Providers
from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Raw_Data                                    import Model__Data_Feeds__Raw_Data
from myfeeds_ai.providers.cyber_security.open_security_summit.models.Model__OSS__Content         import Model__OSS__Content
from myfeeds_ai.providers.cyber_security.open_security_summit.models.Model__OSS__Event           import Model__OSS__Event
from myfeeds_ai.providers.cyber_security.open_security_summit.models.Model__OSS__Latest_Versions import Model__OSS__Latest_Versions
from osbot_utils.helpers.Safe_Id import Safe_Id
from osbot_utils.type_safe.decorators.type_safe                                                              import type_safe

S3_FILE_NAME__OSS__CURRENT_EVENT         = Safe_Id('current-event'       )
S3_FILE_NAME__OSS__CURRENT_EVENT__PROMPT = Safe_Id('current-event-prompt')

class OSS__S3_DB(Data_Feeds__S3_DB):
    provider_name = Model__Data_Feeds__Providers.OPEN_SECURITY_SUMMIT

    def content__load__now(self) -> Model__OSS__Content:
        s3_path   = self.s3_path__content__now()
        s3_key    = self.s3_key__for_provider_path(s3_path)
        file_data = self.s3_file_data(s3_key)
        return Model__OSS__Content.from_json(file_data)

    @type_safe
    def content__save(self, raw_data: Model__OSS__Content):
        s3_path = self.s3_path__content__now()
        s3_key  = self.s3_key__for_provider_path(s3_path)
        raw_data.storage_path = s3_path
        file_data = raw_data.json()
        self.s3_save_data(file_data, s3_key)
        self.latest_versions__update(s3_path__content=s3_path)
        return dict(s3_path=s3_path)

    @type_safe
    def current_event__load(self) -> Model__OSS__Event:  # todo: refactor this 'load' pattern in common method (or helper class)
        s3_path = self.s3_path__current_event()
        s3_key  = self.s3_key__for_provider_path(s3_path)
        file_data = self.s3_file_data(s3_key)
        return Model__OSS__Event.from_json(file_data)

    def current_event__prompt__load(self) -> Model__Data_Feeds__Prompt:  # todo: refactor this 'load' pattern in common method (or helper class)
        s3_path = self.s3_path__current_event__prompt()
        s3_key = self.s3_key__for_provider_path(s3_path)
        file_data = self.s3_file_data(s3_key)
        return Model__Data_Feeds__Prompt.from_json(file_data)

    @type_safe
    def current_event__prompt__save(self, oss_event: Model__Data_Feeds__Prompt):
        s3_path = self.s3_path__current_event__prompt()
        s3_key = self.s3_key__for_provider_path(s3_path)
        file_data = oss_event.json()
        self.s3_save_data(file_data, s3_key)
        self.latest_versions__update(s3_path__latest_event__prompt=s3_path)
        return dict(s3_path=s3_path)

    @type_safe
    def current_event__save(self, oss_event: Model__OSS__Event):
        s3_path = self.s3_path__current_event()
        s3_key = self.s3_key__for_provider_path(s3_path)
        file_data = oss_event.json()
        self.s3_save_data(file_data, s3_key)
        self.latest_versions__update(s3_path__latest_event=s3_path)
        return dict(s3_path=s3_path)

    @type_safe
    def latest_versions__save(self,latest_versions: Model__OSS__Latest_Versions):  # todo: create helper method to handle cases like this of a file that saves a particular class
        s3_path = self.s3_path__latest_versions()
        s3_key = self.s3_key__for_provider_path(s3_path)
        self.s3_save_data(latest_versions.json(), s3_key)
        return s3_path

    def latest_versions__load(self) -> Model__OSS__Latest_Versions:
        s3_path = self.s3_path__latest_versions()
        s3_key = self.s3_key__for_provider_path(s3_path)
        file_data = self.s3_file_data(s3_key)
        latest_versions = Model__OSS__Latest_Versions.from_json(file_data)
        if latest_versions:
            return latest_versions
        return Model__OSS__Latest_Versions()

    def latest_versions__update(self, **kwargs):
        latest_versions__original = self.latest_versions__load()
        latest_versions__json = latest_versions__original.json()
        latest_versions__json.update(**kwargs)
        latest_versions__updated = Model__OSS__Latest_Versions.from_json(latest_versions__json)
        return self.latest_versions__save(latest_versions__updated)


    @type_safe
    def raw_content__save(self, raw_data:Model__Data_Feeds__Raw_Data):
        s3_path               = self.s3_path__raw_content__now()
        s3_key                = self.s3_key__for_provider_path(s3_path)
        raw_data.storage_path = s3_path
        file_data             = raw_data.json()
        self.s3_save_data(file_data, s3_key)
        self.latest_versions__update(s3_path__raw_content=s3_path)
        return dict(s3_path=s3_path)

    def raw_content__load__now(self) -> Model__Data_Feeds__Raw_Data:
        s3_path   = self.s3_path__raw_content__now()
        s3_key    = self.s3_key__for_provider_path(s3_path)
        file_data = self.s3_file_data(s3_key)
        return Model__Data_Feeds__Raw_Data.from_json(file_data)


    # methods for s3 folders and files

    def s3_path__current_event(self):
        return self.s3_path__in_latest(file_id=S3_FILE_NAME__OSS__CURRENT_EVENT)

    def s3_path__current_event__prompt(self):
        return self.s3_path__in_latest(file_id=S3_FILE_NAME__OSS__CURRENT_EVENT__PROMPT)

    def s3_path__content__now(self):
        return self.s3_key_generator.s3_path__now(file_id=S3_FILE_NAME__CONTENT, extension=S3_Key__File_Extension.JSON)

    def s3_path__raw_content__now(self):
        return self.s3_key_generator.s3_path__now(file_id=S3_FILE_NAME__RAW__CONTENT, extension=S3_Key__File_Extension.JSON)
