import json


class WarDogResponse:
    def __init__(self, code, results):
        self.__CODE = int(code)
        self.__RESULTS = results

    def __repr__(self):
        return json.dumps({
            "code": self.__CODE,
            "results": self.__RESULTS
        })
