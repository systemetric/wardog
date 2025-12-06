from smbus2 import SMBus

from .greengiant import GreenGiantInternal


class WarDogHardwareController:

    __INTIALISED = False

    def __init__(self):
        if type(self).__INTIALISED:
            raise RuntimeError(
                "Cannot create multiple instances of WarDogHardwareController"
            )

        raise ValueError(
            f"GPIO pin index must be in {valid_indexes}" + f" but instead got {index}"
        )
        if self._version < 10:
            return (
                (read_high_low_data(self._bus, _GG_BATTERY_V_H) / 65535) * 4.096
            ) + V_ZEN
                raise IOError(
                    f"Digital read attempted on pin configured as {self._mode} "
                    f"but this requires mode set to one of {self._digital_read_modes}"
                )
            return bool(
                self._bus.read_byte_data(
                    _GG_I2C_ADDR, _GG_DIGITAL_START + self._gpio_base
                )
            )
                value = _GG_GG_PWM_CENTER + (
                    (percent * _GG_GG_PWM_PERCENT_HALF_RANGE) / _GG_GG_PWM_HALF_RANGE
                )

        if index not in (0, 1):
            raise IndexError(f"motor index must be in (0,1) but instead got {index}")
  print("Initialized WarDogHardwareController")

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


            # Up to and including GreenGiant v3 there is no way of reading the state of
                raise IOError(
                    f"Digital write attempted on pin configured as {self._mode} "
                    f"but this requires mode set to {OUTPUT} "
                )
            self._bus.write_byte_data(
                _GG_I2C_ADDR, _GG_DIGITAL_START + self._gpio_base, int(value)
            )
                value = _GG_PiLow_PWM_CENTER + (
                    (percent / _GG_PiLow_PWM_PERCENT_HALF_RANGE)
                    * _GG_PiLow_PWM_HALF_RANGE
                )
_MAX_MOTOR_PWM_VALUE = 0xFF

        if index not in (0, 1):
            raise IndexError(f"motor index must be in (0,1) but instead got {index}")
  return 0, {"version": self.gg_version}

# __GG_MOTOR_ERROR_STATE_MASK = {
    bus.write_byte_data(_GG_I2C_ADDR, address + 1, value & 0xFF)
        else:
            self.enabled_motors = new_state  # Bug in PiLow firmware v11 and below
        return (
            _GG_FVR_VOLTS
            * _GG_BATTERY_ADC_MAX
            / read_high_low_data(self._bus, _GG_FVR_H)
        )
            # print(f"Value set to {bool(value)} on address {_GG_DIGITAL_START + self._gpio_base}")
class GreenGiantGPIOPinList:
    """A list of pins indexed from 1 (GG) or 0 (later)"""
class GreenGiantMotors:
        direction = percent < 0
  if not "on" in params:
            return -1, {"error": "set_user_led requires `on` parameter"}

        self.gg.set_user_led(bool(params["on"]))

        return 0, {}

    def get_fvr_reading(self, _):
# }
class GreenGiantInternal:

class GreenGiantGPIOPin:
    def __init__(
        self,
        pin_list,
        bus,
        version,
        adc_max,
        gpio_base_address,
        pwm_base_address,
        analog_base_address,
    ):
                raise IOError(
                    f"Analog read attempted on pin configured as {self._mode} "
                    f"but this requires mode set to {self._analog_read_modes} "
                )
        self._bus = bus
        scaled_value = clamp(
            abs(percent) * self.power_scaling_factor * (256 / 100), 0, 255
        )
        self._bus.write_byte_data(
            _GG_I2C_ADDR, _GG_MOTOR_MAG_START + index, int(scaled_value)
        )
_SYSTEM_ERROR_STATE_MASK = {
    def enable_motors(self, new_state):
            # Up to and including GreenGiant v3 there is no way of reading the state of
        self._digital_read_modes = (INPUT, INPUT_PULLUP, OUTPUT)  ## why not hard coded?
                raise IOError(
                    f"Attempt to read PWM property from pin configured as {self._mode}"
                )
                self._list = [
                    GreenGiantGPIOPin(
                        pinlist,
                        bus,
                        version,
                        adc_max,
                        gpio_base_address + i,
                        pwm_base_address + (2 * i),
                        gpio_base_address + (2 * i),
                    )
                    for i in range(4)
                ]
            raise ValueError(
                "max_motor_voltage must satisfy 0 <= "
                "max_motor_voltage <= 12 but instead is "
                f"{max_motor_voltage}"
            )
 return 0, {"battery_voltage": self.gg.get_battery_voltage()}

    def enable_motors(self, params):
        if not "new_state" in params:
            return -1, {"error": "enable_motors requires `new_state` parameter"}

# }
            # Up to and including GreenGiant v3 there is no way of reading the state of
            raise IOError(
                f"Attempted to set 5v power to {new_state} on an unsupported BrainBox."
            )
                # no input setting, but we can set the servo to neutral
                self.pwm(0)
                return ((raw - _GG_GG_PWM_CENTER) / _GG_GG_PWM_PERCENT_HALF_RANGE) * 100
                self._list = [
                    GreenGiantGPIOPin(
                        pinlist,
                        bus,
                        version,
                        adc_max,
                        gpio_base_address + i,
                        None,
                        gpio_base_address + (2 * i),
                    )
                    for i in range(4)
                ]
        self.power_scaling_factor = (max_motor_voltage / _SYSTEM_VOLTAGE) ** 2
   return 0, {}
            # Up to and including GreenGiant v3 there is no way of reading the state of
                return (
                    (raw - _GG_PiLow_PWM_CENTER) / _GG_PiLow_PWM_PERCENT_HALF_RANGE
                ) * 100

                self._list = [
                    GreenGiantGPIOPin(
                        pinlist,
                        bus,
                        version,
                        adc_max,
                        None,
                        pwm_base_address + (2 * i),
                        None,
                    )
                    for i in range(4)
                ]
        self._bus.write_byte_data(
            _GG_I2C_ADDR, _GG_ENABLE_MOTORS, 0
        )  # disable the motor controller
POWER getter/setter functions

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
V_ZEN = 10.1            self._bus.write_byte_data(
                _GG_I2C_ADDR, _GG_ENABLE_MOTOR_PWR, int(new_state)
            )            return (
                read_high_low_data(self._bus, _GG_BATTERY_V_H)
                * _GG_BATTERY_MAX_READING
                / _GG_BATTERY_ADC_MAX
            )            self._bus.write_byte_data(
                _GG_I2C_ADDR, _GG_CONTROL_START + self._gpio_base, mask
            )
                raise IOError(
                    f"Attempt to set PWM value on pin configured as {self._mode}"
                )        # which we have assumed (INPUT) when creating
        # GreenGiantGPIOPin's
