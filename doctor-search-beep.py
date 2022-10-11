from threading import Thread, Event, Lock
from time import sleep
import httpx
from BeepGPIO import LaFriteBeepGPIO
from PwmWavPlayer import LaFritePwmPlayer

LONG_BEEP_TMO_S = 1
SHORT_BEEP_TMO_S = 0.3
ERROR_BEEP_TMO_S = 0.1

exit_evt = Event()
beep_lock = Lock()


def user_notifier(notification):
    beep_lock.acquire()
    # small delay between notifications if multiple requests handling
    sleep(0.2)
    try:
        beep_gpio = LaFriteBeepGPIO()
        try:
            pwm_sound = LaFritePwmPlayer(notification['sound'])
            pwm_sound.play()
        except Exception as e:
            print(f"No sound, trying to beep! {type(e).__name__}: {e}")
            # Beep to notify
            beep_gpio.beep(notification['beep'])
            pass
        except:
            print("Beep and sound not found")
        # handle exit of program
        if exit_evt.is_set():
            print("BEEPER EXIT")
    except Exception as e:
        print("Beeper failed: ", e)
    finally:
        beep_lock.release()


def get_data(notifications):

    requests = {
        "SANTA": {
            "url": "https://ipr.esveikata.lt/api/searches/appointments/times?"
            "municipalityId=66&organizationId=1000097058&professionCode=221228"
            "&healthcareServiceId=91&page=0&size=50",
            "sounds": {
                "ok": "santa.wav",
                "err": "error.wav"
            }
        },
        "ALL": {
            "url": "https://ipr.esveikata.lt/api/searches/appointments/times?"
            "municipalityId=66&professionCode=221228&healthcareServiceId=91&page=0&size=50",
            "long_beep_s": 0.5
        }
    }

    http_client = httpx.Client()

    notifications.clear()
    for k, v in requests.items():
        notifications[k] = dict()
        sound = dict()
        if 'sounds' in v.keys():
            sound['ok'] = v['sounds']['ok']
            if v['sounds']['err']:
                sound['err'] = v['sounds']['err']
            else:
                sound['err'] = "error.wav"
        try:
            json = http_client.get(v['url']).json()
            print(f"Checking slots for {k}...", end=" ")
            if json['data']:
                print("FOUND")
                beep = LONG_BEEP_TMO_S
                if 'long_beep_s' in v.keys():
                    beep = v['long_beep_s']

                if 'ok' in sound:
                    notifications[k]['sound'] = sound['ok']
                notifications[k]['beep'] = beep
            else:
                print("DID NOT FIND ANY")
                if 'err' in sound:
                    notifications[k]['sound'] = sound['err']
                notifications[k]['beep'] = SHORT_BEEP_TMO_S

        except Exception as e:
            print("HTTP FAILED: ", e)
            if 'err' in sound:
                notifications[k]['sound'] = sound['err']
            notifications[k]['beep'] = ERROR_BEEP_TMO_S
    # beep after update instantly
    distrib_notif(notifications)


def distrib_notif(notifications):
    for notification in notifications.values():
        t = Thread(target=user_notifier, args=(notification, ))
        t.start()


def main():
    notifications = dict()
    tick_s = 0.5

    jobs = {
        "FETCH_DATA": {
            "interval_s": 1800,
            "tmo_s": 0,
            "cb": get_data
        },
        "BEEP_PERIODICLY": {
            "interval_s": 600,
            "tmo_s": 600,
            "cb": distrib_notif
        }
    }

    while True:
        try:
            for job_name, job in jobs.items():
                if job['tmo_s'] > 0:
                    job['tmo_s'] -= tick_s
                else:
                    print(f"Executing {job_name}")
                    job['tmo_s'] = job['interval_s']
                    job['cb'](notifications)
            sleep(tick_s)
        except KeyboardInterrupt:
            # TODO: beeper threads are not collected and waited after exit
            exit_evt.set()
            break


if __name__ == "__main__":
    main()
