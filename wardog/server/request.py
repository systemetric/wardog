class WarDogRequest:
    def __init__(self, request, params):
        self.__REQUEST = request
        self.__PARAMS = params

    def __str__(self):
        s = f"Request: '{self.__REQUEST}'\nParams:\n"

        for p in self.__PARAMS:
            s += f"\t'{p}': '{self.__PARAMS[p]}'\n"

        return s

    @staticmethod
    def from_json(s):
        try:
            w = WarDogRequest(s["request"], s["params"])
        except KeyError:
            raise ValueError(
                "JSON request must contain 'request', and 'params' fields.")
        return w

    @property
    def request(self):
        return self.__REQUEST

    @property
    def params(self):
        return self.__PARAMS
