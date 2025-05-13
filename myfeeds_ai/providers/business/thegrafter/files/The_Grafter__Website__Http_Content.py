from myfeeds_ai.shared.data.My_Feeds__Http_Content                              import My_Feeds__Http_Content


class The_Grafter__Website__Http_Content(My_Feeds__Http_Content):
    server : str = 'https://thegrafter.com/'

    def http_data(self, path='/'):
        return self.requests_get__dict(path=path)
