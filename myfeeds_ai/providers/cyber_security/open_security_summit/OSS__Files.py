from myfeeds_ai.data_feeds.Data_Feeds__Files                                    import Data_Feeds__Files
from myfeeds_ai.providers.cyber_security.open_security_summit.OSS__Http_Content import OSS__Http_Content
from myfeeds_ai.providers.cyber_security.open_security_summit.OSS__Parser       import OSS__Parser
from myfeeds_ai.providers.cyber_security.open_security_summit.OSS__S3_DB        import OSS__S3_DB

RAW_FEED__CREATED__BY = 'OSS__Files.raw_content__current'

class OSS__Files(Data_Feeds__Files):
    s3_db       : OSS__S3_DB
    oss_content : OSS__Http_Content
    oss_parser  : OSS__Parser

    def current_event(self, refresh=False):
        from myfeeds_ai.providers.cyber_security.open_security_summit.OSS__Events import OSS__Events
        current_event = self.s3_db.current_event__load()
        if not current_event or refresh:
            oss_events    = OSS__Events(oss_files=self)
            current_event = oss_events.current_event()
            self.s3_db.current_event__save(current_event)
        return current_event

    def current_event_prompt(self, refresh=False):
        from myfeeds_ai.providers.cyber_security.open_security_summit.OSS__Prompts import OSS__Prompts
        current_event__prompt = self.s3_db.current_event__prompt__load()
        if not current_event__prompt or refresh:
            oss_prompts    = OSS__Prompts(oss_files=self)
            current_event__prompt = oss_prompts.current_event(refresh=refresh)
            self.s3_db.current_event__prompt__save(current_event__prompt)
        return current_event__prompt

    def latest_versions(self):
        return self.s3_db.latest_versions__load()

    def raw_content__current(self, refresh=False):
        raw_content = self.s3_db.raw_content__load__now()
        if refresh or not raw_content:
            raw_content = self.oss_content.raw_content()
            result      = self.s3_db.raw_content__save(raw_content)
        return raw_content

    def content__current(self, refresh=False):
        content = self.s3_db.content__load__now()
        if refresh or not content:
            raw_content = self.oss_content.raw_content()
            content     = self.oss_parser.parse_raw_content(raw_content.raw_data)
            self.s3_db.content__save(content)
        return content
