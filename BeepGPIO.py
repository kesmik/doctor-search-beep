import platform
import io
from time import sleep

from LaFrite import LaFriteDetector
if platform.system() == 'Linux':
    import gpiod

# TODO: better OS separation for IO controls!


class BeepGPIO():
    def __init__(self) -> None:
        super().__init__()
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

    def beep(self, tmo_s, exit_evt=None):
        tick_s = 0.05
        try:
            self.beep_on()
            while True:
                if tmo_s > 0:
                    tmo_s -= tick_s
                    sleep(tick_s)
                else:
                    break

                # handle exit of program
                if exit_evt and exit_evt.is_set():
                    print(f"{self.__class__.__name__} EXIT")
                    break
        except Exception as e:
            print(f"{self.__class__.__name__} failed: ", e)
            raise
        finally:
            self.beep_off()


class LaFriteBeepGPIO(BeepGPIO, LaFriteDetector):
    def __init__(self) -> None:
        super().__init__()

        if self.im_lafrite == True:
            try:
                # PIN40 on pin header
                self.gpiochip = gpiod.chip("gpiochip1")
                self.line = self.gpiochip.get_line(83)

                self.req_cfg = gpiod.line_request()
                self.req_cfg.consumer = "LaFrite Beeper"
                self.req_cfg.request_type = gpiod.line_request.DIRECTION_OUTPUT
                self.line.request(self.req_cfg)
                self.hw_has_gpio = True
            except:
                self.hw_has_gpio = False
                print(f"Failed to initialize {self.__class__.__name__}")
                pass
