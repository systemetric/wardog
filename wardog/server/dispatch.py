import json

from .response import WarDogResponse

class WarDogHardwareDispatch:
    def __init__(self, hws):
        self.hws = hws
        self.dispatch_table = {}

    def add_dispatch(self, name, handler):
        self.dispatch_table[name] = handler

    def dispatch(self, rq):
        code = -1
        results = {"error": "bad request"}

        if rq.request in self.dispatch_table.keys():
            code, results = self.dispatch_table[rq.request](rq.params)
        else:
            print(
                f"WARN: Cannot find request '{rq.request}' in dispatch table.")

        return WarDogResponse(code, results)
