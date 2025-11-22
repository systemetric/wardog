from hopper.client import *
from hopper.common import *


class WarDogClient:
    def __init__(self, name):
        if str(name).strip("\t\n_ ") == "":
            raise ValueError("Bad pipe identifier")

        self.__HOPPER_CLIENT = HopperClient()
        self.__INPUT_PIPE = PipeName(
            (PipeType.OUTPUT, "hardware", str(name).strip("\t\n_ ")), "/home/pi/pipes")
        self.__OUTPUT_PIPE = PipeName(
            (PipeType.INPUT, "hardware", str(name).strip("\t\n_ ")), "/home/pi/pipes")
        self.__HOPPER_CLIENT.open_pipe(
            self.__INPUT_PIPE, delete=True, create=True)
        self.__HOPPER_CLIENT.open_pipe(
            self.__OUTPUT_PIPE, delete=True, create=True, blocking=True)
        self.__JSON_READER = JsonReader(
            self.__HOPPER_CLIENT, self.__INPUT_PIPE, read_validator=self.validate_message)

    @staticmethod
    def validate_message(msg):
        if type(msg) != dict:
            return False
        if "code" in msg.keys() and "results" in msg.keys():
            return True
        return False
        
    def send_message(self, request):
        self.__HOPPER_CLIENT.write(
            self.__OUTPUT_PIPE, str(request).encode("utf-8"))
        return self.__JSON_READER.read()
