import requests
from requests                                                       import Session
from myfeeds_ai.shared.http.Http__Request__Execute                  import Http__Request__Execute
from myfeeds_ai.shared.http.schemas.Schema__Http__Request           import Schema__Http__Request
from myfeeds_ai.shared.http.schemas.Schema__Http__Request__Methods  import Schema__Http__Request__Methods
from osbot_utils.helpers.duration.decorators.capture_duration       import capture_duration


class Http__Request__Execute__Requests(Http__Request__Execute):
    session : Session                                                       # todo: see if there are any side effects of doing this

    def execute__http_request(self, request: Schema__Http__Request, headers:dict=None):
        response = None
        with capture_duration() as duration:
            if request.method == Schema__Http__Request__Methods.GET:
                params = request.data
                response = self.session.get(request.url, params=params, headers=headers)

        if response is not None:
            return self.create_http_response(response=response, duration=duration.seconds)