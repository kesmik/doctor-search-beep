from time import sleep
from LaFrite import LaFriteDetector

import platform
if platform.system() == 'Windows':
    import winsound
elif platform.system() == 'Linux':
    from sysfs_pwm import SysfsPWM

def LaFriteCapableMelodyPlayer():
    if LaFriteDetector().im_lafrite == True:
        return LaFriteMelodyPlayerImpl()
    else:
        return None


class LaFriteMelodyPlayerImpl:
    def __init__(self) -> None:
        self.pwm = SysfsPWM(pwm_chip=0, pwm_channel=0,
                            pwm_period=20000, is_period_hz=True)
        self.pwm.set_duty_cycle(0)

    def play_note(self, freq, duration):
        duration = duration / 1000
        self.pwm.set_period(freq, True)
        self.pwm.set_duty_cycle_percent(50)
        sleep(duration)
        self.pwm.set_duty_cycle(0)

# TODO remove!

from pynoteplayer.Melody import Melody
from pynoteplayer.Note import Note


class SamsungNotification(Melody):
    def __init__(self, player=None) -> None:
        self.tempo_bpm = 290
        self.time_signature = {
            'beats': 4,
            'beat-type': 4
        }
        super().__init__(self.tempo_bpm, self.time_signature, player)

        self.notes = [
            Note('B4', 4), Note('Ds5', 4), Note('B5', 4),
            Note('As5', 8), Note('REST', 8), Note('REST', 8),
            Note('REST', 4), Note('Fs5', 8), Note('REST ', 8),
        ]


SamsungNotification(LaFriteCapableMelodyPlayer()).play()