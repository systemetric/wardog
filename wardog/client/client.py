from hopper.client import *
from hopper.common import *
import json


class WarDogClient:
    def __init__(self, name):
        if str(name).strip("\t\n_ ") == "":
            raise ValueError("Bad pipe identifier")

        self.__HOPPER_CLIENT = HopperClient()
        self.__INPUT_PIPE = PipeName(
            (PipeType.OUTPUT, "hardware-rx", str(name).strip("\t\n_ ")),
            "/home/pi/pipes",
        )
        self.__OUTPUT_PIPE = PipeName(
            (PipeType.INPUT, "hardware-tx", str(name).strip("\t\n_ ")), "/home/pi/pipes"
        )
        self.__HOPPER_CLIENT.open_pipe(
            self.__INPUT_PIPE, delete=True, create=True, blocking=True
        )
        self.__HOPPER_CLIENT.open_pipe(
            self.__OUTPUT_PIPE, delete=True, create=True, blocking=True
        )
        self.__JSON_READER = JsonReader(
            self.__HOPPER_CLIENT,
            self.__INPUT_PIPE,
            read_validator=self.validate_message,
        )

    @staticmethod
    def validate_message(msg):
        if type(msg) != dict:
            return False
        if "code" in msg.keys() and "results" in msg.keys():
            return True
        return False

    def send_message(self, request):
        self.__HOPPER_CLIENT.write(self.__OUTPUT_PIPE, str(request).encode("utf-8"))
        return WarDogResponse(self.__JSON_READER.read())


class WarDogError(Exception):
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

    def __str__(self):
        return f"WarDogError({self.error_code}): {self.message}"


class WarDogRequest:
    def __init__(self, request, params={}):
        self.__REQUEST = str(request)
        self.__PARAMS = dict(params)

    def __repr__(self):
        return json.dumps({"request": self.__REQUEST, "params": self.__PARAMS})


class WarDogResponse:
    def __init__(self, response):
        # print(response)

        self.__CODE = response["code"]
        self.__RESULT = response["results"]

        if self.__CODE != 0:
            raise WarDogError(self.__RESULT["error"], self.__CODE)

    @property
    def code(self):
        return self.__CODE

    @property
    def result(self):
        return self.__RESULT

    def __getitem__(self, name):
        return self.__RESULT[name]
