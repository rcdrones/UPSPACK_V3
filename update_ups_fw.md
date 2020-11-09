# UPSPack v3固件更新指南

由于UPSPack v3出厂已内置bootloader程序。所以在产品发售后，用户可以在github中下载到新版固件，用于升级UPS主板的固件。



## 更新原理和操作方法：

我们是通过Pi主板上的python程序对UPS进行固件更新。所以Pi主板需要通过电源口用外部电源进行单独供电。UPS主板插入电池，并且开关保持OFF档位。



### 升级固件的硬件连接图：

![wiring](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/wiring.jpg)



### 软件升级过程

1. 用电源适配器对树莓派进行供电（不要用UPS对树莓派进行供电，所以接线图上UPS的5V电源线和树莓派主板的VCC不连接）。 树莓派和UPS只使用**3条杜邦线**进行连接：GND、TX、RX

2. UPS插入电池，打开UPS的开关，查询当前UART固件的版本号（如果minicom运行报错：无法找到/dev/ttyAMA0，则需要参考[产品使用说明书](./README.md)，先对树莓派的串口进行正确设置）

```
sudo apt-get install minicom -y # 如果没有安装过minicom，则用这个命令进行安装
sudo minicom -D /dev/ttyAMA0 -b 9600
```

![](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/check_version.png)

3. 如果看到V3.1的版本号，表示通讯正常。此时需要**关闭ups的开关**，并且退出minicom程序。退出minicom的方法为： 先按ctrl+A ，然后按下z，此后按x，最后回车退出程序。

4. 进入fw_update的目录，运行如下命令：

```
python nu_isp.py /dev/ttyAMA0 ups_v32.bin
```

![](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/update_cmd.png)

接着会看到如下内容：

![](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/update1.png)

此时打开ups的开关：

![](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/update_finish.png)

最后会看到checksum pass，就表示升级成功。

5. 升级成功之后，先关闭ups的开关，再次打开ups的开关。**目的是让ups主板重启一次**。接着运行minicom，查询ups上的固件版本号：

```
sudo minicom -D /dev/ttyAMA0 -b 9600
```

![](https://cdn.jsdelivr.net/gh/rcdrones/UPSPACK_V3/image/check_version_finish.png)

上图能看到版本号为3.2，表示固件升级成功。退出minicom的方法为： 先按ctrl+A ，然后按下z，此后按x，最后回车退出程序。





## 软件更新记录



UPSFW_V3.2：ups_v32.bin

更新于2020.10.28：

	* 当采用UART接口通讯时，解决了串口会随机乱码的问题。（如项目只用到STA单线通讯，则不用更新V3.2固件） 

------------------

UPSFW_V3.1：ups_v31.bin

更新于2020.6.15：

    * 该版本为UPSPack Standard V3 批量生产中，工厂烧录的标准固件版本。
    * 产品内置了UPS Bootloader。用于产品的升级和软件bug的修复。




