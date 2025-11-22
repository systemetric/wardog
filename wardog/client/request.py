import json


class WarDogClientRequest:
    def __init__(self, request, params):
        self.__REQUEST = str(request)
        self.__PARAMS = dict(params)

    def __get_serial(self):
        s = json.dumps({
            "request": self.__REQUEST,
            "params": self.__PARAMS
        })

    def __repr__(self):
        return json.dumps({
            "serial": self.__get_serial(),
            "request": self.__REQUEST,
            "params": self.__PARAMS
        })
