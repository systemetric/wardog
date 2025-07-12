from .hardware import WarDogHardwareController
from .dispatch import WarDogHardwareDispatch


class WarDogState:
    def __init__(self):
        self.hwc = WarDogHardwareController()
        self.dispatch = WarDogHardwareDispatch(self)

        def reset_hwc(params):
            return self.init_hwc(params)

        self.dispatch.add_dispatch("init_hwc", reset_hwc)

    def init_hwc(self, params):
        self.hwc.reset()
        return (0, {})

    def run_request(self, rq):
        return self.dispatch.dispatch(rq)
