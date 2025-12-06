import json

from .request import WarDogRequest
from .state import WarDogState

from hopper.client import *
from hopper.common import *


class WarDogServer:
    def __init__(self):
        self.HOPPER_CLIENT = HopperClient()
        self.INPUT_PIPE = PipeName(
            (PipeType.OUTPUT, "hardware-tx", "wardog"), "/home/pi/pipes"
        )
        self.OUTPUT_PIPE = PipeName(
            (PipeType.INPUT, "hardware-rx", "wardog"), "/home/pi/pipes"
        )
        self.HOPPER_CLIENT.open_pipe(
            self.INPUT_PIPE, delete=True, create=True, blocking=True
        )
        self.HOPPER_CLIENT.open_pipe(self.OUTPUT_PIPE, delete=True, create=True)
        self.STATE = WarDogState()
        self.JSON_READER = JsonReader(
            self.HOPPER_CLIENT, self.INPUT_PIPE, read_validator=self.validate_message
        )
        print("Initialized WarDogServer")

    @staticmethod
    def validate_message(msg):
        if type(msg) != dict:
            return False
        if "request" in msg.keys() and "params" in msg.keys():
            return True
        return False

    def run(self):
        while 1:
            s = self.JSON_READER.read()

            print(s)

            r = WarDogRequest.from_json(s)

            result = self.STATE.run_request(r)

            self.HOPPER_CLIENT.write(self.OUTPUT_PIPE, str(result).encode("utf-8"))
