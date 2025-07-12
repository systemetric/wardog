import json

from .request import WarDogRequest
from .state import WarDogState
from .dispatch import WarDogHardwareDispatch

from hopper.client import *
from hopper.common import *


class WarDogServer:
    def __init__(self):
        self.HOPPER_CLIENT = HopperClient()
        self.INPUT_PIPE = PipeName(
            (PipeType.OUTPUT, "hardware", "wardog"), "/home/pi/pipes")
        self.OUTPUT_PIPE = PipeName(
            (PipeType.INPUT, "hardware", "wardog"), "/home/pi/pipes")
        self.HOPPER_CLIENT.open_pipe(
            self.INPUT_PIPE, delete=True, create=True, blocking=True)
        self.HOPPER_CLIENT.open_pipe(
            self.OUTPUT_PIPE, delete=True, create=True)
        self.STATE = WarDogState()
        print("Initialized WarDogServer")

    def run(self):
        while (1):
            d = self.HOPPER_CLIENT.read(self.INPUT_PIPE)

            try:
                s = json.loads(d)
            except json.decoder.JSONDecodeError:
                print("WARN: Recieved bad JSON string!")
                continue

            r = WarDogRequest.from_json(s)

            r.run_request(self.STATE)

            self.HOPPER_CLIENT.write(
                self.OUTPUT_PIPE, str(r.result).encode("utf-8"))
