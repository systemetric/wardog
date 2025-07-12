class WarDogRequest:
    def __init__(self, serial, request, params):
        self.__SERIAL = serial
        self.__REQUEST = request
        self.__PARAMS = params

    def __str__(self):
        s = f"Serial: {self.__SERIAL}\nRequest: '{self.__REQUEST}'\nParams:\n"

        for p in self.__PARAMS:
            s += f"\t'{p}': '{self.__PARAMS[p]}'\n"

        return s

    @staticmethod
    def from_json(s):
        try:
            w = WarDogRequest(s["serial"], s["request"], s["params"])
        except KeyError:
            raise ValueError(
                "JSON request must contain 'serial', 'request', and 'params' fields.")
        return w
