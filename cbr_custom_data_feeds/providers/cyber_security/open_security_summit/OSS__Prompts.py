from datetime                                                                           import datetime
from typing                                                                             import List, Dict
from cbr_custom_data_feeds.data_feeds.models.Model__Data_Feeds__Prompt                  import Model__Data_Feeds__Prompt
from cbr_custom_data_feeds.providers.cyber_security.open_security_summit.OSS__Files     import OSS__Files
from osbot_utils.base_classes.Type_Safe                                                 import Type_Safe

PROMPT__OSS__CURRENT_SESSIONS =  ("The following data is from the Open Security Summit events collected at {current_time}. \n"
                                  "There are {sessions_size} sessions scheduled for {event_month} {event_year}.\n\n")

class OSS__Prompts(Type_Safe):
    oss_files : OSS__Files

    def current_event(self) -> Model__Data_Feeds__Prompt:
        event = self.oss_files.current_event()
        if not event:
            return "No current event found"

        current_time = datetime.now().strftime("%a, %d %b %Y %H:%M:%S")

        # Create header
        prompt_header_params = dict(current_time  = current_time      ,
                                    event_month   =  event.month      ,
                                    event_year    = event.year        ,
                                    sessions_size = len(event.sessions))

        header = PROMPT__OSS__CURRENT_SESSIONS.format(**prompt_header_params)

        # Create session summaries
        sessions_text = []
        for i, (title, session) in enumerate(event.sessions.items(), 1):
            organizer_details = self.get_organizer_details(session.organizers, event.organizers)

            session_text = (f"Session {i}:\n"
                            f"Title: {title}\n"
                            f"Track: {session.track}\n"
                            f"When: {session.when_day} {session.when_month} {session.when_year} at {session.when_time}\n"
                            f"Organizers: {organizer_details}\n"
                            f"Description: {self.clean_content(session.content)}\n")
            sessions_text.append(session_text)

        # Combine all parts
        prompt = header + "\n".join(sessions_text)
        return Model__Data_Feeds__Prompt(prompt_text=prompt)

    def get_organizer_details(self, organizer_names: List[str], all_organizers: Dict) -> str:
        organizer_details = []
        for name in organizer_names:
            if name in all_organizers:
                org = all_organizers[name]
                detail = f"{name}"
                if org.job_title and org.company:
                    detail += f" ({org.job_title} at {org.company})"
                organizer_details.append(detail)
        return ", ".join(organizer_details)

    def clean_content(self, content: str) -> str:                          # Clean HTML content and normalize whitespace
        if not content:
            return ""

        content = content.replace("<p>", "").replace("</p>", " ")           # todo: refactor this to use beautifulsoup
        content = content.replace("<h2>", "").replace("</h2>", " ")
        content = content.replace("<ul>", "").replace("</ul>", " ")
        content = content.replace("<li>", "- ").replace("</li>", " ")

        content = " ".join(content.split())                                # Normalize whitespace

        # max_length = 500                                                 # todo: see if need this
        # if len(content) > max_length:
        #     content = content[:max_length] + "..."

        return content
