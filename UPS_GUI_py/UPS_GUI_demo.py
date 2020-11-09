#!/usr/bin/python3

from upspackv2 import *
import tkinter as tk
import re
import serial
import time


test = UPS2("/dev/ttyAMA0")


def reflash_data():
    version,vin,batcap,vout = test.decode_uart()
#    loc_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    cur_time = time.time()
    cur_time = cur_time - load_time
#    print(cur_time)
    
    
    
    time_var.set("Running: "+str(int(cur_time)) + "s")
    
    
    
    batcap_int = int(batcap)
#    print(type(batcap_int))
    
    if vin == "NG":
        vin_lable.config(bg = "red")
        vin_var.set("Power NOT connected!")
    else:
        vin_lable.config(bg = "green")
        vin_var.set("Power connected!")
                  
    if batcap_int< 30:
        cap_lable.config(bg = "red")
        if batcap_int == 1:
            cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            stop_time = "\nHalt time :"+cur_time
            with open("log.txt","a+") as f:
                f.write(stop_time)
            os.system("sudo shutdown -t now")
            sys.exit()            
    else:
        cap_lable.config(bg = "green")
    
    
    cap_var.set("Battery Capacity: "+str(batcap)+"%")
    vout_var.set("Output Voltage: "+vout+" mV")

    window.after(1000,reflash_data)

def hit_exit():
    window.destroy()

    

#loc_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#print(loc_time) 
load_time = time.time()

#cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
#start_time = "\nStart time :"+cur_time

#with open("log.txt","a+") as f:
#    f.write(start_time)

window = tk.Tk()
window.title("UPS GUI demo")
window.geometry("400x200")

time_var = tk.StringVar()
ver_var = tk.StringVar()
vin_var = tk.StringVar()
vout_var = tk.StringVar()
cap_var = tk.StringVar()

version,vin,batcap,vout = test.decode_uart()
ver_var.set("Smart UPS "+version)

ver_lable = tk.Label( window,
          textvariable = ver_var,
#                      bg = "green",
          font = ("Arial",12),
          width = 20,height = 2)
ver_lable.pack()



time_lable = tk.Label( window,
          textvariable = time_var,
          bg = "green",
          font = ("Arial",12),
          width = 20,height = 2)

time_lable.place(x=10, y=50, anchor='nw')



vin_lable = tk.Label( window,
          textvariable = vin_var,
          bg = "green",
          font = ("Arial",12),
          width = 20,height = 2)

vin_lable.place(x=210, y=50, anchor='nw')


cap_lable = tk.Label( window,
          textvariable = cap_var,
          bg = "green",
          font = ("Arial",12),
          width = 20,height = 2)

cap_lable.place(x=10, y=100, anchor='nw')


vout_lable = tk.Label( window,
          textvariable = vout_var,
          bg = "green",
          font = ("Arial",12),
          width = 20,height = 2)

vout_lable.place(x=210, y=100, anchor='nw')


b1 = tk.Button(window,
  text = "Exit",
  width = 30,height = 2,
  command = hit_exit)
b1.place(x=70, y=150, anchor='nw')


window.after(100,reflash_data)

window.mainloop()

