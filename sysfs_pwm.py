import os
import atexit

NANOSEC_IN_SEC = 1e+9


class SysfsPWM:
    pwm_base_path = "/sys/class/pwm"

    def __init__(self, pwm_chip, pwm_channel, pwm_period, is_period_hz=False):
        self.pwm_chip = pwm_chip
        self.pwm_channel = pwm_channel

        # Do not change order, because all functions registered are called in
        # last in, first out order (ref: https://docs.python.org/3/library/atexit.html)
        atexit.register(self.unexport)
        atexit.register(self.disable)

        self.__set_period_ns__(pwm_period, is_period_hz)

        if type(pwm_chip) != int:
            raise TypeError("[pwm_chip] must be 'integer' type")

        if type(pwm_channel) != int:
            raise TypeError("[pwm_channel] must be 'integer' type")

        if type(pwm_period) != int:
            raise TypeError("[pwm_period] must be 'integer' type")

        if type(is_period_hz) != bool:
            raise TypeError("[is_period_hz] must be 'bool' type")

        if os.path.exists(self.get_pwmchip_path()) == False:
            raise FileNotFoundError(
                f"'{self.get_pwmchip_path()}' is not present on the system!")

        # since duty cycle is expected to be changed frequently avoid
        # addidtional function calls to get path each time
        self.pwm_channel_duty_cycle_path = self.get_pwm_channel_duty_cycle_path()

        # Try to disable and unexported of channel was left exported before
        self.disable()
        self.unexport()

        self.export()
        self.set_period(self.pwm_period_ns)
        self.set_duty_cycle(0)

    @staticmethod
    def par_w(path, value):
        with open(path, 'w') as f:
            f.write(str(value))

    @staticmethod
    def par_r(path):
        with open(path, 'r') as f:
            return f.read()

    @staticmethod
    def __hz_ns_conv__(hs_or_ns):
        try:
            return int(NANOSEC_IN_SEC/hs_or_ns)
        except ZeroDivisionError:
            pass

        return hs_or_ns

    def __set_period_ns__(self, period, is_period_hz=False):
        if is_period_hz == False:
            self.pwm_period_ns = period
        else:
            self.pwm_period_ns = SysfsPWM.__hz_ns_conv__(period)

    # /sys/class/pwm/pwmchip* paths (pwm chip paths)
    def get_pwmchip_path(self):
        return os.path.join(SysfsPWM.pwm_base_path, f"pwmchip{self.pwm_chip}")

    def get_pwmchip_export_path(self):
        return os.path.join(self.get_pwmchip_path(), "export")

    def get_pwmchip_unexport_path(self):
        return os.path.join(self.get_pwmchip_path(), "unexport")

    def get_pwmchip_npwm_path(self):
        return os.path.join(self.get_pwmchip_path(), "npwm")

    # /sys/class/pwm/pwmchip*/pwm* paths (pwm channel paths)
    def get_pwm_channel_path(self):
        return os.path.join(self.get_pwmchip_path(), f"pwm{self.pwm_channel}")

    def get_pwm_channel_enable_path(self):
        return os.path.join(self.get_pwm_channel_path(), "enable")

    def get_pwm_channel_period_path(self):
        return os.path.join(self.get_pwm_channel_path(), "period")

    def get_pwm_channel_duty_cycle_path(self):
        return os.path.join(self.get_pwm_channel_path(), "duty_cycle")

    def get_pwm_channel_polarity_path(self):
        return os.path.join(self.get_pwm_channel_path(), "polarity")

    # sysfs PWM API functions
    def export(self):
        if os.path.exists(self.get_pwm_channel_path()) == False:
            SysfsPWM.par_w(self.get_pwmchip_export_path(), self.pwm_channel)
        else:
            print("PWM channel already exported!")

    def unexport(self):
        if os.path.exists(self.get_pwm_channel_path()) == True:
            SysfsPWM.par_w(self.get_pwmchip_unexport_path(), self.pwm_channel)
        else:
            print("[UNEXPORT] PWM channel is not exported!")

    def get_npwm(self):
        return SysfsPWM.par_r(self.get_pwmchip_npwm_path())

    def enable(self):
        if os.path.exists(self.get_pwm_channel_path()) == True:
            SysfsPWM.par_w(self.get_pwm_channel_enable_path(), 1)
        else:
            print("[ENABLE] PWM channel is not exported!")

    def disable(self):
        if os.path.exists(self.get_pwm_channel_path()) == True:
            SysfsPWM.par_w(self.get_pwm_channel_enable_path(), 0)
        else:
            print("[DISABLE] PWM channel is not exported!")

    def set_period(self, period, is_period_hz=False):
        self.__set_period_ns__(period, is_period_hz)
        SysfsPWM.par_w(self.get_pwm_channel_period_path(), self.pwm_period_ns)

    # TODO: get_period since it is read/write capable

    def set_duty_cycle(self, duty_cycle_ns):
        SysfsPWM.par_w(self.pwm_channel_duty_cycle_path, duty_cycle_ns)

    def set_duty_cycle_percent(self, percent):
        duty_cycle_ns = int(self.pwm_period_ns * percent / 100)
        SysfsPWM.par_w(self.pwm_channel_duty_cycle_path, duty_cycle_ns)

    # TODO: set_duty_cycle/set_duty_cycle_percent since it is read/write capable

    def set_polarity(self, polarity):
        SysfsPWM.par_w(self.get_pwm_channel_polarity_path(), polarity)

    def get_polarity(self, polarity):
        SysfsPWM.par_w(self.get_pwm_channel_polarity_path(), polarity)


if __name__ == "__main__":
    from time import sleep

    try:
        pwm = SysfsPWM(0, 0, int(input("Enter freq in HZ: ")), True)
        print("PWM channels: ", pwm.get_npwm())

        while True:
            duty = input("Enter duty cycle (percent [0-100]): ")
            pwm.enable()
            pwm.set_duty_cycle_percent(int(duty))
            sleep(2)
            pwm.disable()
    except KeyboardInterrupt:
        print("Bye")
        pwm.disable()
        pwm.unexport()
