from smbus2 import SMBus

from .greengiant import GreenGiantInternal


class WarDogHardwareController:

    __INTIALISED = False

    def __init__(self):
        if type(self).__INTIALISED:
            raise RuntimeError("Cannot create multiple instances of WarDogHardwareController")

        print("Initialized WarDogHardwareController")

        self.init_hardware()

        type(self).__INTIALISED = True

    def init_hardware(self):
        self.bus = SMBus(1)
        self.gg = GreenGiantInternal(self.bus)
        self.gg_version = self.gg.get_version()

        if self.gg_version >= 10:
            self.gg.set_motor_power(True)
            self.adc_max = 5
        else:
            self.gg.set_motor_power(True)
            self.adc_max = self.gg.get_fvr_reading()

    def reset(self):
        type(self).__INTIALISED = False
        self.__init__()

    def version(self, _):
        return 0, {"version": self.gg.get_version()}

    def set_user_led(self, params):
        if not "on" in params:
            return -1, {"error": "set_user_led requires `on` parameter"}

        self.gg.set_user_led(bool(params["on"]))

        return 0, {}

    def get_battery_voltage(self, _):
         return 0, {"battery_voltage": self.gg.get_battery_voltage()}
         
    def get_fvr_reading(self, _):
         return 0, {"fvr_reading": self.gg.get_fvr_reading()}

    def enable_motors(self, params):
        if not "new_state" in params:
            return -1, {"error": "enable_motors requires `new_state` parameter"}

        self.gg.enable_motors(bool(params["new_state"]))

        return 0, {}

#POWER getter/setter functions

    def get_12v_acc_power(self, _):
        return 0, {"12v_acc_power": self.gg.get_12v_acc_power()}

    def set_12v_acc_power(self, params):
        if not "new_state" in params:
            return -1, {"error": "set_12v_acc_power requires `new_state` parameter"}

        self.gg.set_12v_acc_power(bool(params["new_state"]))

        return 0, {}

    def get_5v_acc_power(self, _):
        return 0, {"5v_acc_power": self.gg.get_5v_acc_power()}

    def set_5v_acc_power(self, params):
        if not "new_state" in params:
            return -1, {"error": "set_5v_acc_power requires `new_state` parameter"}

        self.gg.set_5v_acc_power(bool(params["new_state"]))

        return 0, {}

    def set_motor_power(self, params):
        if not "new_state" in params:
            return -1, {"error": "set_motor_power requires `new_state` parameter"}

        self.gg.set_motor_power(bool(params["new_state"]))

        return 0, {}
