[Update firmware tutorial](./update_ups_fw_en.md)

# RPi UPSPack V3 Product User Guide

UPSPack v3 is the latest model of the new generation of Raspberry Pie UPS uninterruptible power supply expansion boards released in September 2020. Based on iterative upgrades from previous v1 and v2 versions, v3 is the most stable power supply solution available for Raspberry Pie.

![UPS3](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/UPS3.jpg)

## catalogues

* [Function upgrades](#Function-upgrades)
* [Performance parameters](#Performance-parameters)
  * [Output Current](#Output-Current)
  * [Endurance time](#Endurance-time)
  * [Power failure without restart](#Power-failure-without-restart)
  * [Low-voltage detection of start-up and automatic shutdown and start-up](#Low-voltage-detection-of-start-up-and-automatic-shutdown-and-start-up)
* [Hardware Description](#Hardware-Description)
  * [Interface Description](#Interface-Description)
  * [UPS power supply method](#UPS-power-supply-method)
  * [LED display](#LED-display)
  * [Battery connector](#Battery-connector)
  * [Communication interface](#Communication-interface)
  * [Mechanical dimensional drawings](#Mechanical-dimensional-drawings)
* [Software Drivers](#Software-Drivers)
  * [Safety shutdown](#Safety-shutdown)
  * [UART software](#UART-software)





### Function upgrades

The following lists the product differences between UPS v3 and v2 versions.

| Features                                                     | RPi UPSPack V3                                               | RPi UPSPack V2                                               |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Input interface                                              | TYPE-C connector (power cord compatible with the latest Pi4) | Micro-USB port (compatible with Pi3 and older Pi models)     |
| Output max current                                           | 5V 3A                                                        | 5V 3A                                                        |
| External power outage, Pi continuous power (no reboot)       | support                                                      | support                                                      |
| Hardware on/off switch                                       | support                                                      | support                                                      |
| GPIO power interface and UART and halt signal interface.     | support                                                      | support                                                      |
| Lithium Battery Statistics                                   | support                                                      | support                                                      |
| Start-up low voltage check                                   | support                                                      | NOT support                                                  |
| Power adapter anomaly detection (power outage detection)     | support                                                      | support                                                      |
| USB-A socket output voltage detection                        | support                                                      | support                                                      |
| Automatic shutdown notification before battery exhaustion    | support                                                      | support                                                      |
| After a power failure, the program starts automatically      | Support (no human intervention, program is on)               | NOT support（requires manual intervention to power up）      |
| After a power failure, the UPS automatically switches to hibernation mode. | support                                                      | NOT support                                                  |
| firmware update                                              | support                                                      | NOT support                                                  |
|                                                              |                                                              |                                                              |
| **The UPS communicates with the Pi's serial port (UART):**   |                                                              |                                                              |
| Setting                                                      | 9600 bps 8N1                                                 | 9600 bps 8N1                                                 |
| Protocol version                                             | V3.1 (and higher)                                            | V1.0                                                         |
| Protocol backwards compatibility                             | UPS communication protocol compatible with V2 old version    | compatible                                                   |
|                                                              |                                                              |                                                              |
| **Single bus communication between UPS and Pi (System halt signal)** |                                                              |                                                              |
| Communication IO port                                        | The STA port on the UPS motherboard connects to the Raspberry GPIO18 (BCM 18) | UPS motherboard's STA port connects to the Raspberry GPIO18 (BCM18) |
| communications protocol                                      | Pulse method                                                 | Leveling method                                              |
| Software compatibility                                       | More reliable with pulse detection in V3 (not compatible with V2 software) | Level detection method                                       |





### Performance parameters

Here are a few aspects of UPS v3 output maximum current, endurance, power failure without restarting, safe shutdown before battery drain, and auto-on, to explain UPS v3 performance and considerations.

#### Output Current

Through the EBC-A10H to UPS v3 current limit test. The maximum output current can reach 5V 3A. after the actual test Pi4 running the official Raspbian system, the normal power consumption is about 5V 1A, such as inserting the camera and U disk and other peripherals, the power consumption gradually increases to 5V 2A. so using UPS v3 to power the Pi4, there is a large margin. And with an output of 3A. The 2.54-row pin interface can also guarantee more than 5V power. Users should note that **5V and GND must be used with a silicone dupont cable**. If a normal Dupont wire is used, it will cause a larger wire loss when the current is higher, thus the low voltage symbol of lightning is observed on the screen on the Pi4.

![3a](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/3a.jpg)

![test3a](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/test3a.gif)





#### Endurance time

The UPS v3 on-board battery interface is in a PH 2.0 package (compatible with previous older UPS motherboards) with printed positive and negative markings on the PCB board. There are three different battery sizes available for customers to choose from. Customers can also be connected to different capacity, rated voltage of 3.7V lithium polymer batteries, or 3.7V 18650/21700/21650 battery pack. Note: The voltage range of the input UPS battery port must be less than or equal to 4.2V. (All battery packs must be connected in parallel, no series connection of cells). **3.65v lithium iron phosphate packs are not supported**.UPS v3 Standard Finished Product offers 3 lithium batteries in different capacities and volumes for customers to choose from.	

| Battery model                                               | Volume (length x width x thickness) |
| ----------------------------------------------------------- | ----------------------------------- |
| 4000mAh (3.7V nominal voltage, built-in battery protector)  | 70mm x 41mm x 9.5mm                 |
| 6500mAh (3.7V nominal voltage, built-in battery protector)  | 116mm x 50mm x 8mm                  |
| 10000mAh (3.7V nominal voltage, built-in battery protector) | 115mm x 65mm x 9mm                  |



We built different combinations of applications and got the following endurance data.

| battery capacity | Pi4 stand-alone | Pi4+ official 7" screen (DSI interface) | Pi4+3.5" (GPIO) | Pi4+5"(HDMI) | Pi+7"(HDMI) |
| :--------------: | :-------------: | :-------------------------------------: | :-------------: | :----------: | :---------: |
|     4000mAh      |      5.5h       |                  2.5h                   |      4.0h       |     3.3h     |    2.0h     |
|     6500mAh      |      9.0h       |                  4.0h                   |      6.5h       |     5.2h     |    3.2h     |
|     10000mAh     |      14.5h      |                  6.0h                   |      10.0h      |     8.5h     |    5.0h     |

Test Method：

1. All data above are in hours.
2. The running system is: 2020-05-27-raspios-buster-full-armhf , the system does not make any setting changes. The system only runs a RPi_runtime_recoder.py in the background for time statistics.
3. The 3 capacity batteries are fully charged and then connected to the Raspberry Pie and use the program for time logging. The discharge as of the point the UPS lets the Raspberry Pie shut down automatically, and the log file is used to see how long it actually runs.
4. Download, and run UPSPACK_V3/time_count/RPi_runtime_recoder.py for time logging. When the Raspberry Pie is powered off, connect the power adapter to read the time_log.txt in the program directory to check the endurance time.





#### Power failure without restart

Power failure without restarting is a basic UPS v3 feature. The following demonstration shows that both the Pi4 and 7" HDMI screens are powered by the UPS v3. Manual unplugging of the input TYPE-C power cable is used to simulate an external power outage. both Pi4 and HDMI screens will remain stable.

<img src="https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/pwr_off.gif" alt="pwr_off" style="zoom:200%;" />





#### Low-voltage detection of start-up and automatic shutdown and start-up

When the UPS is powered by battery alone, the battery can run out of power. So we have designed a series of automated power-on and power-off strategies to enable the UPS to work in an unattended environment.

* Power on low voltage detection: When the inserted battery voltage is less than 3.48V, the UPS will determine the current battery is about to run out of state. At this time, although the output switch to ON state, the UPS will not output 5V, low-voltage state UPS will turn off all outputs and go to sleep on its own. (The reason for this is that in the battery depleted state, forced power on, the battery protection board may stop output before the Raspberry is booted to the desktop. (Without this protection policy, the Raspberry Pie system may break system files due to an illegal shutdown). Only when the TYPE-C charging cable is plugged in, the UPS will automatically wake up and enter the charging process, charging to a certain level to automatically turn on the external power output.

* Auto shutdown: When the external power adapter loses power, the UPS automatically uses the battery as a backup power source to power the Raspberry Pie. Before the battery is about to run out, the UPS motherboard will notify the Raspberry Pie of an early shutdown via System halt signal. The UPS motherboard will then automatically cut off the main power to the Raspberry Pie and the UPS will automatically go into sleep mode, waiting for the external power supply to resume.
* Auto Power On: When the external power supply is restored, the UPS motherboard will automatically resume operation and start charging the battery. After a period of time to charge, the UPS motherboard will automatically turn on the main power supply to the Raspberry Pie, thus allowing the Raspberry Pie to resume operation.

The following uses programmable power analog battery low voltage power up, the UPS motherboard automatically enters low voltage hibernation, 5V is not output. When the TYPE-C line is connected, the entire process of automatic resumption of operation and voltage output.

<img src="https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/low_bat.gif" alt="low_bat" style="zoom:200%;" />






### Hardware Description

#### Interface Description

![main_board](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/main_board.jpg)

| NO   | names                                | description                                                  |
| ---- | ------------------------------------ | ------------------------------------------------------------ |
| 1    | TYPE-C power adapter charging port   | External 5V power supply for UPS power supply interface, power supply requirements 5V 2A-3A |
| 2    | USB-A docks                          | Two USB-A docks power the Raspberry Pie motherboard.         |
| 3    | LED power indicator                  | 4 LEDs (D1-D4) to indicate the current charge of lithium batteries |
| 4    | UPS motherboard test port            | Factory used for burning UPS programs and automatically testing the motherboard. This interface is not useful to users. |
| 5    | MCU Controller                       | Used for charge/discharge path management, communicating with the Raspberry Pie motherboard and other functions. |
| 6    | Dual Power Manage Unit               | 2 battery charge/discharge, path management chip (chip is encrypted) |
| 7    | PH2.0 Li-ion battery input interface | Support 1S 3.7V Li-ion battery, compatible with 3.7V 18650 / 21700 etc. battery pack (3.7V nominal voltage of battery pack required) |
| 8    | UPS output switch                    | ON / OFF switch, when the switch hits ON, the UPS outputs 5V to the Raspberry Pie motherboard.OFF is the opposite. (External power failure and low battery voltage, the program will automatically turn off the power output) |
| 9    | 2.54mm spigot                        | 3P Pin Header Port: single wire communication and UART port for connecting to the GPIO port on the Raspberry Pie motherboard for communication.<br />2P power port: 5V power supply through the Raspberry Pie GPIO power interface.<br />The product comes with a free pin by default, customer who need to use to the above interface need soldering. |
| 10   | Power output LEDs                    | When the 5V output is stable, the green LED lights up.       |





#### UPS power supply method

##### Power adapter to power UPS

The UPS v3 motherboard is powered by the TPYE-C cable. The UPS has an internal power path management system that automatically adjusts the input current. For example, when there is no external load, or when the load is light and the UPS has a full battery on board. The input current will be approximately equal to the current consumed by the load. the TYPC-C input charging cable, try to use a short and thick power cord, so that the wire loss is small, so that the charging power to reach the main board of the UPS is sufficient.

**Tip: If the power supply header nominal parameters for 5V 3A, UPS work in the state of discharge while charging, the battery power has been reducing the reasons, may be the input TYPE-C line loss is larger (or the power supply header parameters dummy), the actual power adapter to reach the TYPE-C interface power is not enough to simultaneously supply power to the load and at the same time to charge the battery caused by. Solution: Replace the quality and reliability of the big brand power supply head and brand charging cable (thicker). **



##### UPS Power to Raspberry Pie Motherboard

The UPS motherboard can power the Raspberry Pie using the USB-A dock, or the Raspberry Pie can be powered via the GPIO 5V port. Either one of the two power supply options is sufficient.

| Power supply method                                   | explain                                                      |
| ----------------------------------------------------- | ------------------------------------------------------------ |
| Powering the Raspberry Pie Motherboard with USB-A     | The UPS plugs into the TYPE-C power cable to power the Pi4. (Pi3 and older versions can be connected using a Micro-USB cable). Pros: No soldering required, easy to use. Disadvantages: the USB interface is a little more resistant, suitable for Pi4 regular applications, please choose a USB cable as short and thick as possible to reduce the line loss voltage drop and prevent the Pi4 from flashing. If the lightning symbol still appears, you can use the following GPIO direct power supply solution to power the Pi4. |
| Powering the Raspberry Pie through the GPIO Interface | Solder a 5V row pin on the UPS and power the Pi4 with 22AWG short and thick **silicone dupont wire**. Use a **flexible silicone dupont cable** that can withstand up to 5A of current and has less internal resistance. Do not use a regular aluminum-clad copper signal duPont cable, as this will introduce greater internal resistance, which will result in high line loss voltage drop and a low-voltage lightning bolt symbol on the Pi screen. |


|   Type of electricity supply (choose 1 of 2 below)    |                    **Examples of wiring**                    |
| :---------------------------------------------------: | :----------------------------------------------------------: |
|   Powering the Raspberry Pie Motherboard with USB-A   | ![cable_power](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/cable_power.jpg) |
| Powering the Raspberry Pie through the GPIO Interface | ![gpio_power](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/gpio_power.jpg) |



#### LED display

6 LEDs onboard on the UPS main board.

* Green LEDs: D1, D2, D3, D4 for battery charge indication.
* Red LED: Charge Status is the charge status indicator. (hereafter referred to as CS lamp)
  * When the UPS is off output and the user is only charging the UPS: the CS lamp flashes when the battery is not fully charged. When the battery is fully charged, the CS lamp is always on.
  * When the UPS is operating in a flush and discharge state: the CS lamp is always flashing. Only when the load is light, such as when powering a Pi Zero or similar light load, will the CS lamp appear to be on after a long charge. The light is controlled by the PMU management chip output and will flash when the battery is not fully charged.
  * When the UPS switch is off and the TYPE-C is off to charge the UPS: The CS lamp stays on constantly for 20s and then turns off automatically.
* Green LED: The Power LED is the output power indicator. This light is lit when the UPS outputs 5V power to the Raspberry Pie motherboard.

LED power indicator.

| D4   | D3   | D2   | D1    | Battery voltage   |
| ---- | ---- | ---- | ----- | ----------------- |
| off  | off  | off  | blink | less than 3.45v   |
| off  | off  | off  | on    | 3.55v             |
| off  | off  | on   | on    | 3.72v             |
| off  | on   | on   | on    | 3.89v             |
| on   | on   | on   | on    | greater than 4.0v |

When both D1-D4 are always on and the CS light is also always on, the battery is fully charged.



#### Battery connector

Battery interface of UPS main board:**PH2.0 holder**. The lithium battery protection plate has been integrated inside the factory-matched battery pack. If users want to access the DIY battery pack on their own, please note the following precautions.

* The battery output cable has a PH 2.0 male connector, **note the positive and negative poles of the connector! If the battery cable is reversed, the UPS will burn out! **

* Autonomous battery pack is 1S 3.7V lithium battery: rated voltage 3.7V, full voltage 4.2V battery pack. Conventional compatible models: 18650, 21700, 21650 and other battery packs are compatible. ** Not compatible with LiFePO4 battery. **

* No special capacity requirement, but the best capacity for Pi4 is more than 4000mAh.

* Self-assembled battery pack try to bring 6A and above high current lithium battery protection plate: the parameters of the conventional lithium battery protection plate on the market is 3A-4A, when the external need for high current, the protection current is too small protection plate may lead to output hiccups.

![bat_info](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/bat_info.jpg)



#### Communication interface

The UPS V3 communicates with the Raspberry Pie in two ways: via UART and STA single bus interfaces. Access richer information about what UPS is currently doing.

The role of the 2 interfaces is as follows.

* UART interface: the UPS communicates with the onboard serial port of the Raspberry Pie. Information available to the Raspberry Pie: communication heartbeat packets, whether there is an external power failure, percentage of battery capacity, outgoing voltage value.
* STA Single Bus Interface: the UPS motherboard sends a pulse message (Halt signal) to the Raspberry Pie motherboard before the battery runs out, allowing the Raspberry Pie to safely perform a software shutdown. Once the Raspberry Pie is safely shut down, the Raspberry Pie's 5V mains power supply is cut off again. (Both the USB-A and the 2P socket are programmed to do so). When the external power is restored, the UPS motherboard will automatically enter the charging process, and when the battery charge reaches a certain capacity, it will automatically restore power to the Raspberry Pie.

![gpio](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/gpio.jpg)



#### Mechanical dimensional drawings

![dim](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/dim.png)



### Software Drivers

##### Safety shutdown

1. Unzip the product package to `/home/pi/UPSPACK_V3` directory. Check that the full directory for **shutdown_check.py** is

    > **shutdown_check.py** The full directory is as follows.
    >
    > /home/pi/UPSPACK_V3/shutdown_check.py

2. Change `/etc/rc.local` to add automatic shutdown to boot up.

    > ```shell
    > sudo nano /etc/rc.local
    > 
    > #Add the following to the line above the exit at the bottom of the page
    > 
    > sudo python3 /home/pi/UPSPACK_V3/shutdown_check.py &
    > 
    > ```

![rc](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/rc.png)

3. By completing the above steps, you can achieve the automatic safe shutdown of the Raspberry Pie when the battery runs out before. And when power is restored externally, the UPS board will automatically charge. When the battery is charged to a certain level, the UPS will automatically power on the Raspberry Pie.



##### UART software

The UPS and the Raspberry Pie interact with each other via the UART interface for a much richer set of information.

* UPS uptime
* Is the external TPYE-C power supply port working properly? (GOOD or Not Good)
* Current percentage of battery charge
* UPS current output voltage value

Installation:

1. Connect the UPS v3's UART ports (TX, RX) to the Raspberry Pie's UART port [see: Communication Interface](#Communication Interface).

2. EDIT /boot/config.txt

   ```
   sudo nano /boot/config.txt
   ```

3. Add 2 lines of content and ctrl+x to save the exit

   ```
   # For 2020-08-20 - Raspberry Pi OS and newer versions
   enable_uart=1
   dtoverlay=disable-bt
   ```
   ![uart1](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/uart1.png)
   ```
   # For 2020-05-27 - Raspberry Pi OS and older
   enable_uart=1
   dtoverlay=pi3-miniuart-bt
   ```
   
4. Use `ls -l /dev` again to look at the pointing relationship between serial0 and serial1. Mainly check the pointing relationship of **serial0 -> ttyAMA0**. The following figure shows that this is correct.
   
   ![uart2](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/uart2.png)
   
5. Restarting Raspberry Pie

   ```
   sudo reboot
   ```

6. Verify that the Raspberry Pie's serial port 0 and the UPS are communicating properly through the minicom serial port software.

   ```
   sudo apt-get install minicom -y
   sudo minicom -D /dev/ttyAMA0 -b 9600
   ```
   You can see the protocol packets sent by UPS to the Raspberry Pie. Since '\n' on Linux is only a line feed, it doesn't go back to the beginning of the line. So the protocols seen on the minicom will be beyond the screen. It doesn't matter, we can use python later to filter this information.

   > Tip 1: Exit the minicom button: Ctrl+A --> z --> x 
   >
   > Tip 2: If you do not see the communication protocol packet, the UART connection is incorrect, refer to [Communication Interface](#Communication Interface). Alternatively, **serial0 -> ttyAMA0** is not pointing correctly. Follow the above steps to double check.

7. Go to the program directory /home/pi/UPSPACK_V3/UPS_GUI_py, double click `UPS_GUI_demo.py`, a dialog box will pop up and you can click OK to run the Python GUI program. You can see the current working status of the UPS.

![click](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/click.png)


![python_gui](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/python_gui.png)





<!---
##### Terminal-based terminal program

For some Raspberry Pi OS hosts that do not run a graphical interface. A terminal program developed in python is also provided here. The terminal program interacts with the UPS v3 motherboard via the UART interface, so first make sure to connect the communication cable. [See: Communication Interface for more details](#Communication Interface)

1. Check that the program's path `/home/pi/UPSPACK_V3/console_py/ups_cmd.py` is correct.
2. running program
    ```
    sudo python3 /home/pi/UPSPACK_V3/console_py/ups_cmd.py
    ```

-->
