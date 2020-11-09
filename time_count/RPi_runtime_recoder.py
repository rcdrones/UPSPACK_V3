#!/usr/bin/python3
import os
import time


def start_timer():
    
    print("RPi time count proc v0.1\n")
    mins = 0

    while True:
        time.sleep(60)
        strtime = time.strftime("Time = %Y-%m-%d %H:%M:%S", \
                                time.localtime(time.time()))
        strtime += " mins="
        strtime += str(mins) + str("\n")
        
        print(strtime)
        
        with open("time_log.txt","a+") as f:
            f.write(strtime)
        
        mins += 1
        

start_timer()