import platform
from time import sleep
import wave
import os
import array
from datetime import datetime, timedelta

from LaFrite import LaFriteDetector
if platform.system() == 'Linux':
    from sysfs_pwm import SysfsPWM

# TODO: better OS separation for IO controls!


class PwmWavPlayer():
    def __init__(self, file) -> None:
        super().__init__()
        self.hw_has_pwm = False
        self.file = file
        self.wav = wave.open(os.path.join("sounds", file), 'rb')
        self.n_channels = self.wav.getnchannels()
        self.s_width = self.wav.getsampwidth()
        self.f_rate = self.wav.getframerate()

    def pwm_on(self):
        if self.hw_has_pwm == True:
            self.pwm.enable()
        else:
            print("HW PWM ON")

    def pwm_off(self):
        if self.hw_has_pwm == True:
            self.pwm.disable()
            self.pwm.unexport()
        else:
            print("HW OFF OFF")

    def play(self, exit_evt=None):
        if self.hw_has_pwm == False:
            raise ResourceWarning("HW does not support PWM")

        tick_s = 1/self.f_rate
        max_v = 256 ** self.s_width
        self.pwm_on()

        samples = self.wav.readframes(-1)
        # TODO: fix for one bytes!
        samples = array.array('h', samples)
        samples = [s + int(max_v/2) for s in samples]
        samples = [int(s*100/max_v) for s in samples]
        try:
            for duty in samples:
                end_t = datetime.now() + timedelta(seconds=tick_s)
                self.pwm.set_duty_cycle_percent(duty)
                # if duty> 55 or duty < 40:
                #     print(duty)
                while datetime.now() < end_t:
                    pass
                # sleep(tick_s)

                # handle exit of program
                if exit_evt and exit_evt.is_set():
                    print(f"{self.__class__.__name__} EXIT")
                    break
        except Exception as e:
            print(f"{self.__class__.__name__} failed: ", e)
            raise
        finally:
            self.pwm_off()


class LaFritePwmPlayer(PwmWavPlayer, LaFriteDetector):
    def __init__(self, file) -> None:
        raise NotImplemented("LaFrite PWM is not developed yet!")
        super().__init__(file)

        if self.im_lafrite == True:
            print("LaFrite PWM found")
            try:
                self.pwm = SysfsPWM(pwm_chip=0, pwm_channel=0,
                                    pwm_period=44100, is_period_hz=True)
                self.hw_has_pwm = True
            except Exception as e:
                self.hw_has_pwm = False
                print(f"Failed to initialize {self.__class__.__name__}: {e}")
                pass
