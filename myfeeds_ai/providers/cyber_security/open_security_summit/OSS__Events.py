from myfeeds_ai.providers.cyber_security.open_security_summit.OSS__Files                 import OSS__Files
from myfeeds_ai.providers.cyber_security.open_security_summit.models.Model__OSS__Event   import Model__OSS__Event
from osbot_utils.base_classes.Type_Safe                                                             import Type_Safe
from osbot_utils.utils.Lists                                                                        import unique

OSS_EVENTS__CURRENT__YEAR  = 2024
OSS_EVENTS__CURRENT__MONTH = 'Dec'

class OSS__Events(Type_Safe):
    oss_files: OSS__Files

    def current_event(self):
        event              = Model__OSS__Event()
        event.month        = OSS_EVENTS__CURRENT__MONTH
        event.year         = OSS_EVENTS__CURRENT__YEAR
        self.add_participants_and_sessions(event)
        return event

    def add_participants_and_sessions(self, event):
        all_data = self.oss_files.content__current()
        organizers_names = []

        for session in all_data.sessions:
            if session.when_year == event.year and session.when_month == event.month:
                organizers_names.extend(session.organizers)
                event.sessions[session.title] = session

        organizers_names = unique(organizers_names)
        for participant in all_data.participants:
            organizer_name = participant.title
            if organizer_name in organizers_names:
                event.organizers[organizer_name] = participant


