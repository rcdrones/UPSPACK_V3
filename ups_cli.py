#!/usr/bin/python3

from upspackv2 import *
import time
import os
import sys

test = UPS2("/dev/ttyAMA0")

def reflash_data():
    try:
        version, vin, batcap, vout = test.decode_uart()
    except Exception as e:
        print(f"Error decoding UART: {e}")
        return

    cur_time = time.time()
    cur_time = cur_time - load_time

    print("Running: " + str(int(cur_time)) + "s")

    batcap_int = int(batcap)

    if vin == "NG":
        print("Power NOT connected!")
    else:
        print("Power connected!")
                  
    if batcap_int < 30:
        if batcap_int == 1:
            cur_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            stop_time = "\nHalt time :" + cur_time
            with open("log.txt", "a+") as f:
                f.write(stop_time)
            os.system("sudo shutdown -t now")
            sys.exit()            
    else:
        print("Battery Capacity: " + str(batcap) + "%")
        print("Output Voltage: " + vout + " mV")

if __name__ == "__main__":
    load_time = time.time()

    try:
        version, vin, batcap, vout = test.decode_uart()
        print("Smart UPS " + version)
    except Exception as e:
        print(f"Error initializing UPS: {e}")
        sys.exit(1)
    
    try:
        while True:
            reflash_data()
            time.sleep(15)
    except KeyboardInterrupt:
        print("Exiting...")
        
