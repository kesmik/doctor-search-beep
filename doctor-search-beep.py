from threading import Thread, Event, Lock
from time import sleep
import httpx
from BeepGPIO import LaFriteBeepGPIO

LONG_BEEP_TMO_S = 1
SHORT_BEEP_TMO_S = 0.3
ERROR_BEEP_TMO_S = 0.1

exit_evt = Event()
beep_lock = Lock()


def beeper(tmo_s):
    tick_s = 0.05
    beep_lock.acquire()
    try:
        beep_gpio = LaFriteBeepGPIO()
        # small delay between beeps
        sleep(0.2)
        beep_gpio.beep_on()
        while True:
            if tmo_s > 0:
                tmo_s -= tick_s
                sleep(tick_s)
            else:
                break

            # handle exit of program
            if exit_evt.is_set():
                print("BEEPER EXIT")
                break
    except Exception as e:
        print("Beeper failed: ", e)
    finally:
        beep_gpio.beep_off()
        beep_lock.release()


def get_data(beeps):
    requests = {
        "SANTA": {
            "url": "https://ipr.esveikata.lt/api/searches/appointments/times?"
            "municipalityId=66&organizationId=1000097058&professionCode=221228"
            "&healthcareServiceId=91&page=0&size=50"
        },
        "ALL": {
            "url": "https://ipr.esveikata.lt/api/searches/appointments/times?"
            "municipalityId=66&professionCode=221228&healthcareServiceId=91&page=0&size=50",
            "long_beep": SHORT_BEEP_TMO_S
        }
    }

    http_client = httpx.Client()
    for k, v in requests.items():
        try:
            json = http_client.get(v['url']).json()
            print(f"Checking slots for {k}...", end=" ")
            if json['data']:
                print("FOUND")
                beep = LONG_BEEP_TMO_S
                if 'long_beep' in v.keys():
                    beep = v['long_beep']
                beeps[k] = beep
            else:
                print("DID NOT FIND ANY")
                beeps[k] = SHORT_BEEP_TMO_S
        except Exception as e:
            print("HTTP FAILED: ", e)
            beeps[k] = ERROR_BEEP_TMO_S
    # beep after update instantly
    distrib_beeps(beeps)


def distrib_beeps(beeps):
    for beep in beeps.values():
        t = Thread(target=beeper, args=(beep, ))
        t.start()


def main():
    beeps = dict()
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
            "cb": distrib_beeps
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
                    job['cb'](beeps)
            sleep(tick_s)
        except KeyboardInterrupt:
            # TODO: beeper threads are not collected and waited after exit
            exit_evt.set()
            break


if __name__ == "__main__":
    main()
