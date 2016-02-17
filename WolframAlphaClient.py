import wolframalpha


class WolframAlphaClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = wolframalpha.Client(api_key)

    def get_query(self, query):
        res = self.client.query(query)
        return res
