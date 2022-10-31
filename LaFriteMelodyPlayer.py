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
        self.pwm.enable()
        sleep(duration)
        self.pwm.set_duty_cycle(0)
        self.pwm.disable()

# TODO remove!

from pynoteplayer.Melody import Melody
from pynoteplayer.Note import Note


class HarryPoterHedwigsTheme(Melody):
    def __init__(self, player=None) -> None:
        self.tempo_bpm = 144
        self.time_signature = {
            'beats': 3,
            'beat-type': 4
        }
        super().__init__(self.tempo_bpm, self.time_signature, player)

        self.notes = [
            Note('REST', 2), Note('D4', 4),
            Note('G4', 4, 1), Note('As4', 8), Note('A4', 4),
            Note('G4', 2), Note('D5', 4),
            Note('C5', 2, 1),
            Note('A4', 2, 1),
            Note('G4', 4, 1), Note('As4', 8), Note('A4', 4),
            Note('F4', 2), Note('Gs4', 4),
            Note('D4', 1, 1),
            Note('D4', 4),

            Note('G4', 4, 1), Note('As4', 8), Note('A4', 4),
            Note('G4', 2), Note('D5', 4),
            Note('F5', 2), Note('E5', 4),
            Note('Ds5', 2), Note('B4', 4),
            Note('Ds5', 4, 1), Note('D5', 8), Note('Cs5', 4),
            Note('Cs4', 2), Note('B4', 4),
            Note('G4', 1, 1),
            Note('As4', 4),

            Note('D5', 2), Note('As4', 4),
            Note('D5', 2), Note('As4', 4),
            Note('Ds5', 2), Note('D5', 4),
            Note('Cs5', 2), Note('A4', 4),
            Note('As4', 4, 1), Note('D5', 8), Note('Cs5', 4),
            Note('Cs4', 2), Note('D4', 4),
            Note('D5', 1, 1),
            Note('REST', 4), Note('As4', 4),

            Note('D5', 2), Note('As4', 4),
            Note('D5', 2), Note('As4', 4),
            Note('F5', 2), Note('E5', 4),
            Note('Ds5', 2), Note('B4', 4),
            Note('Ds5', 4, 1), Note('D5', 8), Note('Cs5', 4),
            Note('Cs4', 2), Note('As4', 4),
            Note('G4', 1, 1)
        ]


HarryPoterHedwigsTheme(LaFriteCapableMelodyPlayer()).play()
