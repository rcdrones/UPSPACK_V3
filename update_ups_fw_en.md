# UPSPack v3 Firmware Update Guide

Since UPSPack v3 has a built-in bootloader program from the factory, users can download the new firmware from github after the product is released. So after the product release, users can download the new version of the firmware from github to upgrade the firmware of the UPS motherboard.



## Updated rationale and operating methods.

We are updating the firmware of the UPS through a python program on the Pi motherboard. The UPS motherboard is plugged into the battery and the switch is kept OFF.



### Hardware connection diagram for firmware upgrade.

![wiring](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/wiring.jpg)



### Software upgrade process

1. Use a power adapter to power the Raspberry Pie (do not use a UPS to power the Raspberry Pie, so the wiring diagram does not connect the 5V power cord from the UPS to the VCC on the Raspberry Pie motherboard). The Raspberry Pie and UPS are connected using only **3 Dupont cables**: GND, TX, RX.

2. Plug in the UPS battery, turn on the UPS switch, and check the current UART firmware version number (if the minicom runs reporting error: cannot find /dev/ttyAMA0, you need to refer to the [product manual](. /README_en.md) to set the serial port of the raspberry pie correctly first)

```
sudo apt-get install minicom -y
sudo minicom -D /dev/ttyAMA0 -b 9600
```

![](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/check_version.png)

3. If you see the V3.1 version number, the communication is normal. At this time, you need to **switch-OFF UPS**, and exit the minicom program. To exit minicom, press ctrl+A first, then press z, then press x, and finally enter to exit the program.

4. Go to the fw_update directory and run the following command.

```
python nu_isp.py /dev/ttyAMA0 ups_v32.bin
```

![](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/update_cmd.png)

Next you will see the following.

![](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/update1.png)

Switch on the ups at this point.

![](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/update_finish.png)

At the end, you will see checksum pass, which means the upgrade was successful.

5. After the upgrade is successful, first turn off the ups switch, then turn on the ups switch again. **The purpose is to get the ups motherboard to reboot once**. Then run minicom and look up the firmware version number on the ups.

```
sudo minicom -D /dev/ttyAMA0 -b 9600
```

![](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/check_version_finish.png)

You can see that the version number is 3.2, which means the firmware upgrade is successful. The way to exit the minicom is: first press ctrl+A , then press z, then press x, and finally enter to exit the program.





## Software release note



UPSFW_V3.2：ups_v32.bin

Updated on 2020.10.28.

	* When using UART interface for communication, it solves the problem that the serial port will randomly garble. (No need to update V3.2 firmware if the project only uses to STA single-wire communication)  

------------------

UPSFW_V3.1：ups_v31.bin

Updated on 2020.6.15.

    * This is the factory-burned version of the standard firmware used in UPSPack Standard V3 batch production.
    * The product has a built-in UPS Bootloader for product upgrades and software bug fixes.




