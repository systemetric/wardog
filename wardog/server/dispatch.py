import json


class WarDogHardwareDispatch:
    def __init__(self, hws):
        self.hws = hws
        self.dispatch_table = {}

    def add_dispatch(self, name, handler):
        self.dispatch_table[name] = handler

    def dispatch(self, rq):
        code = -1
        results = {}

        if rq.request in self.dispatch_table.keys():
            code, results = self.dispatch_table[rq.request](rq.params)
        else:
            print(
                f"WARN: Cannot find request '{rq.request}' in dispatch table.")

        return json.dumps({
            "serial": rq.serial,
            "code": code,
            "results": results
        })
