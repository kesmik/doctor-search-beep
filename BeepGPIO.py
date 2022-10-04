import platform
import io
if platform.system() == 'Linux':
    import gpiod

# TODO: better OS separation for IO controls!


class BeepGPIO():
    def __init__(self) -> None:
        self.hw_has_gpio = False

    def beep_on(self):
        if self.hw_has_gpio == True:
            self.line.set_value(1)
        else:
            print("HW BEEP ON")

    def beep_off(self):
        if self.hw_has_gpio == True:
            self.line.set_value(0)
        else:
            print("HW BEEP OFF")


class LaFriteBeepGPIO(BeepGPIO):
    def __init__(self) -> None:
        super().__init__()

        if self.check_if_lafrite() == True:
            # PIN40 on pin header
            self.gpiochip = gpiod.chip("gpiochip1")
            self.line = self.gpiochip.get_line(83)

            self.req_cfg = gpiod.line_request()
            self.req_cfg.consumer = "LaFrite Beeper"
            self.req_cfg.request_type = gpiod.line_request.DIRECTION_OUTPUT
            self.line.request(self.req_cfg)

    def check_if_lafrite(self):
        self.hw_has_gpio = False

        try:
            with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
                if 'Libre Computer AML-S805X-AC'.lower() in m.read().lower():
                    self.hw_has_gpio = True
        except Exception:
            pass

        print("Computer == lafrite: ", self.hw_has_gpio)
        return self.hw_has_gpio
