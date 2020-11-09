#!/usr/bin/python3

import RPi.GPIO as GPIO
import os
import time
from threading import Thread


def shutdown_check():
    print("start shutdown check")
    shutdown_pin = 18
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(shutdown_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    start_time = "Start time :"+cur_time + "\n"

    with open("/home/pi/log.txt","a+") as f:
        f.write(start_time)

    while True:
        plusetime = 1
        GPIO.wait_for_edge(shutdown_pin, GPIO.RISING)
        time.sleep(0.01)
        while GPIO.input(shutdown_pin) == GPIO.HIGH:
            time.sleep(0.01)
            plusetime += 1

        #print(plusetime)

        if plusetime >=2 and plusetime <=3:
            break

    print("active halt...")
    cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    stop_time = "active halt...Halt time :"+ cur_time + "\n\n"
    with open("/home/pi/log.txt","a+") as f:
        f.write(stop_time)
    os.system("sudo sync")
    time.sleep(1)
    os.system("sudo shutdown now -h")



if __name__ == "__main__":
    try:
        t1 = Thread( target = shutdown_check )
        t1.start()
    except:
        t1.stop()
        GPIO.cleanup()

