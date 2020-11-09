#!/usr/bin/python3

import serial
import re
import RPi.GPIO as GPIO
import os,sys
import time

class UPS2:
    def __init__(self,port):
        self.ser  = serial.Serial(port,9600)        
        
    def get_data(self,nums):
        while True:
            self.count = self.ser.inWaiting()
            
            if self.count !=0:
                self.recv = self.ser.read(nums)
                return self.recv
    
    def decode_uart(self):
        self.uart_string = self.get_data(100)
#    print(uart_string)
        self.data = self.uart_string.decode('ascii','ignore')
#    print(data)
        self.pattern = r'\$ (.*?) \$'
        self.result = re.findall(self.pattern,self.data,re.S)
    
        self.tmp = self.result[0]
    
        self.pattern = r'SmartUPS (.*?),'
        self.version = re.findall(self.pattern,self.tmp)
    
        self.pattern = r',Vin (.*?),'
        self.vin = re.findall(self.pattern,self.tmp)
        
        self.pattern = r'BATCAP (.*?),'
        self.batcap = re.findall(self.pattern,self.tmp)
        
        self.pattern = r',Vout (.*)'
        self.vout = re.findall(self.pattern,self.tmp)

        return self.version[0],self.vin[0],self.batcap[0],self.vout[0]
    
class UPS2_IO:
    def __init__(self,bcm_io=18):
        self.shutdown_check_pin = bcm_io
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.shutdown_check_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.shutdown_check_pin, GPIO.FALLING, callback= self.RPI_shutdown,bouncetime=1000)


    def RPI_shutdown(self,channel):
        print("detect bat LOW, system will shutdown in 10s!")
        for i in range(10,0,-1):
            print(i,end = ' ',flush=True)
            time.sleep(1)
            
        print("\nexecute System shudown!\n")
        os.system("sudo shutdown -t now")
        sys.exit()
    

    def cleanup():
        print("clean up GPIO.")
        GPIO.cleanup() 



if __name__ == "__main__":
    print("This is UPS v2 class file")
#    test = UPS2("/dev/ttyAMA0")
#    version,vin,batcap,vout = test.decode_uart()
#    print("--------------------------------")
#    print("       UPS Version:"+version)
#    print("--------------------------------")
#    
#    i = 1
#    
#    while True:
#        version,vin,batcap,vout = test.decode_uart()
#        
#        print("-%s-" %i)
#        
#        if vin == "NG":
#            print("USB input adapter : NOT connected!")
#        else:
#            print("USB input adapter : connected!")
#        print("Battery Capacity: "+batcap+"%")
#        print("UPS Output Voltage: "+vout+" mV")
#        print("\n")
#        
#        i = i+1
#        
#        if i == 10000:
#            i = 1
   
        
        
    