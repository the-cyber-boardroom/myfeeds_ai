from datetime                                                                           import datetime
from typing                                                                             import List, Dict

from bs4 import BeautifulSoup

from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Prompt                  import Model__Data_Feeds__Prompt
from myfeeds_ai.providers.cyber_security.open_security_summit.OSS__Files     import OSS__Files
from osbot_utils.base_classes.Type_Safe                                                 import Type_Safe

PROMPT__OSS__CURRENT_SESSIONS   =  ("The following data is from the Open Security Summit events collected at {current_time}. \n"
                                  "There are {sessions_size} sessions scheduled for {event_month} {event_year}.")
PROMPT__OSS__SESSIONS_TITLES    = "\n\nHere are the sessions titles (followed by the session details): \n"
PROMPT__OSS__CURRENT_ORGANIZERS = "\n\nThe following organizers are involved in the event:\n\n"

class OSS__Prompts(Type_Safe):
    oss_files : OSS__Files

    def current_event(self, refresh=False) -> Model__Data_Feeds__Prompt:
        event = self.oss_files.current_event(refresh=refresh)
        if not event:
            return "No current event found"

        current_time = datetime.now().strftime("%a, %d %b %Y %H:%M:%S")

        # Create header
        prompt_header_params = dict(current_time  = current_time      ,
                                    event_month   =  event.month      ,
                                    event_year    = event.year        ,
                                    sessions_size = len(event.sessions))

        header = PROMPT__OSS__CURRENT_SESSIONS.format(**prompt_header_params)
        sessions_titles = PROMPT__OSS__SESSIONS_TITLES
        for i, title in enumerate(event.sessions, 1):
            sessions_titles += f"    {i}. {title}\n"

        # Create session summaries
        sessions_text = []
        for i, (title, session) in enumerate(event.sessions.items(), 1):
            session_text = (f"\n************************** Session {i} ****************************\n"
                            f"Title: {title}\n"
                            f"Track: {session.track}\n"
                            f"When: {session.when_day} {session.when_month} {session.when_year} at {session.when_time}\n"
                            f"Organizers: {session.organizers}\n"
                            f"Description: {self.clean_content(session.content)}\n")
            sessions_text.append(session_text)
        organizer_details = PROMPT__OSS__CURRENT_ORGANIZERS + self.get_organizer_details( event.organizers)

        # Combine all parts
        prompt = header + sessions_titles + "\n".join(sessions_text) + '\n' +  '*'*100 +  organizer_details
        return Model__Data_Feeds__Prompt(prompt_text=prompt)

    def get_organizer_details(self,  all_organizers: Dict) -> str:
        organizers_details = []
        for _, organiser in all_organizers.items():
            organiser_detail = (f"Name        : {organiser.title    }:\n"
                                f"Title       : {organiser.job_title}\n"
                                f"Company     : {organiser.company  }\n"
                                f"LinkedIn    : {organiser.linkedin }\n"
                                f"Twitter     : {organiser.twitter  }\n"
                                f"Facebook    : {organiser.facebook }\n"
                                f"Website     : {organiser.website  }\n"
                                #f"Description : {organiser.content  }\n"
                                )
            organizers_details.append(organiser_detail)
        return "\n--- organizer --- \n".join(organizers_details)

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

        transcription = content.find('<h2 id="transcript">')               # todo: add better support for transcription
        if transcription > 0:
            content = content[:transcription]

        soup = BeautifulSoup(content, 'html.parser')
        content = soup.get_text()

        return content
