from .hardware import WarDogHardwareController
from .dispatch import WarDogHardwareDispatch


class WarDogState:
    def __init__(self):
        self.hwc = WarDogHardwareController()
        self.dispatch = WarDogHardwareDispatch(self)

        def reset_hwc(params):
            return self.init_hwc(params)

        self.dispatch.add_dispatch("init_hwc", reset_hwc)
        self.dispatch.add_dispatch("gg_version", self.hwc.version)

        # MISC GG internal functions
        self.dispatch.add_dispatch("set_user_led", self.hwc.set_user_led)
        self.dispatch.add_dispatch("get_fvr_reading", self.hwc.get_fvr_reading)
        self.dispatch.add_dispatch("get_battery_voltage", self.hwc.get_battery_voltage)
        self.dispatch.add_dispatch("enable_motors", self.hwc.enable_motors)

        # POWER getter/setter functions
        self.dispatch.add_dispatch("set_motor_power", self.hwc.set_motor_power)
        self.dispatch.add_dispatch("get_12v_acc_power", self.hwc.get_12v_acc_power)
        self.dispatch.add_dispatch("set_12v_acc_power", self.hwc.set_12v_acc_power)
        self.dispatch.add_dispatch("get_5v_acc_power", self.hwc.get_5v_acc_power)
        self.dispatch.add_dispatch("set_5v_acc_power", self.hwc.set_5v_acc_power)

    def init_hwc(self, params):
        self.hwc.reset()
        return (0, {})

    def run_request(self, rq):
        return self.dispatch.dispatch(rq)
