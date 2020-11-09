#!/usr/bin/python

import io
import struct
import serial
import sys
import time
com = None
AP_FILE = []
AP_CHECKSUM = 0
PacketNumber = 0
def open_port(uart_port):
    global com
    com = serial.Serial(uart_port, 115200)

def error_return():
    global com
    com.close()
    sys.exit()


def UART_TRANSFER(thelist, PN):
    global com
    thelist[4] = PN & 0xff
    thelist[5] = PN >> 8 & 0xff
    thelist[6] = PN >> 16 & 0xff
    thelist[7] = PN >> 24 & 0xff

    # print 'tx package'
    # print '[{}]'.format(', '.join(hex(x) for x in thelist))

    test = com.write(thelist)
    # print test
    return_str = com.read(64)  # return by string
    return_buffer = bytearray(return_str)
    # print 'rx package'
    # print '[{}]'.format(', '.join(hex(x) for x in return_buffer))

    checksum = 0
    for i in range(64):
        checksum = checksum + thelist[i]
    # print "checksum=0x%x"%checksum
    packege_checksum = 0
    packege_checksum = return_buffer[0]
    packege_checksum = (return_buffer[1] << 8) | packege_checksum
    if checksum != packege_checksum:
        print "checksum error"
        error_return()
    RPN = 0
    RPN = return_buffer[4]
    RPN = (return_buffer[5] << 8) | RPN
    RPN = (return_buffer[6] << 16) | RPN
    RPN = (return_buffer[7] << 24) | RPN
    if RPN != (PN + 1):
        print "package number error"
        error_return()
    return return_buffer


def UART_TRANSFER_AUTO(thelist, PN):
    global com
    thelist[4] = PN & 0xff
    thelist[5] = PN >> 8 & 0xff
    thelist[6] = PN >> 16 & 0xff
    thelist[7] = PN >> 24 & 0xff

    print 'tx package'
    print '[{}]'.format(', '.join(hex(x) for x in thelist))
    while (True):
        com.flushInput()
        com.timeout = 0.5
        com.flushOutput()
        test = com.write(thelist)
        print thelist

        # time.sleep(0.1)
        return_str = com.read(64)  # return by string
        return_buffer = bytearray(return_str)
        print 'rx package'
        print '[{}]'.format(', '.join(hex(x) for x in return_buffer))
        if(len(return_buffer) != 0):
            checksum = 0
            for i in range(64):
                checksum = checksum + thelist[i]
            packege_checksum = 0
            packege_checksum = return_buffer[0]
            packege_checksum = (return_buffer[1] << 8) | packege_checksum
            if checksum != packege_checksum:
                print "checksum error"
                # error_return()
            RPN = 0
            RPN = return_buffer[4]
            RPN = (return_buffer[5] << 8) | RPN
            RPN = (return_buffer[6] << 16) | RPN
            RPN = (return_buffer[7] << 24) | RPN
            if RPN != (PN + 1):
                print "package number error"
            else:
                break
                # error_return()
    # return return_buffer


def UART_AUTO_DETECT():
    global PacketNumber
    LINK = [0 for i in range(64)]  # 64 byte data buffer is all zero
    PacketNumber = 0x01
    LINK[0] = 0xae
    UART_TRANSFER_AUTO(LINK, PacketNumber)


def LINK_FUN():
    global PacketNumber
    LINK = [0 for i in range(64)]  # 64 byte data buffer is all zero
    PacketNumber = 0x01
    LINK[0] = 0xae
    UART_TRANSFER(LINK, PacketNumber)


def SN_FUN():
    global PacketNumber
    PacketNumber = PacketNumber + 2
    SN_PACKAGE = [0 for i in range(64)]
    SN_PACKAGE[0] = 0xa4
    SN_PACKAGE[8] = PacketNumber & 0xff
    SN_PACKAGE[9] = PacketNumber >> 8 & 0xff
    SN_PACKAGE[10] = PacketNumber >> 16 & 0xff
    SN_PACKAGE[11] = PacketNumber >> 24 & 0xff
    UART_TRANSFER(SN_PACKAGE, PacketNumber)


def READ_FW_FUN():
    global PacketNumber
    PacketNumber = PacketNumber + 2
    READFW_VERSION = [0 for i in range(64)]
    READFW_VERSION[0] = 0xa6
    buf = UART_TRANSFER(READFW_VERSION, PacketNumber)
    FW_VERSION = buf[8]
    print "FW_VERSION=0x%8x" % FW_VERSION


def RUN_TO_APROM_FUN():
    global PacketNumber
    PacketNumber = PacketNumber + 2
    RUN_TO_APROM = [0 for i in range(64)]
    RUN_TO_APROM[0] = 0xab
    UART_TRANSFER(RUN_TO_APROM, PacketNumber)


def READ_PID_FUN():
    global PacketNumber
    PacketNumber = PacketNumber + 2
    READ_PID = [0 for i in range(64)]
    READ_PID[0] = 0xB1
    buf = UART_TRANSFER(READ_PID, PacketNumber)
    PID = buf[8] | buf[9] << 8 | buf[10] << 16 | buf[11] << 24
    print "PID=0x%8x" % PID


def READ_CONFIG_FUN():
    global PacketNumber
    PacketNumber = PacketNumber + 2
    READ_CONFIG = [0 for i in range(64)]
    READ_CONFIG[0] = 0xa2
    buf = UART_TRANSFER(READ_CONFIG, PacketNumber)
    CONFIG0 = buf[8] | buf[9] << 8 | buf[10] << 16 | buf[11] << 24
    CONFIG1 = buf[12] | buf[13] << 8 | buf[14] << 16 | buf[15] << 24
    print "CONFIG0=0x%8x" % CONFIG0
    print "CONFIG1=0x%8x" % CONFIG1


def READ_APROM_BIN_FILE(FILENAME):
    # open file to array
    try:
        f = open(FILENAME, 'rb')
        global AP_FILE
        global AP_CHECKSUM
        AP_CHECKSUM = 0
        while True:
            x = f.read(1)
            if x == '':
                break
            temp = struct.unpack('B', x)
            AP_FILE.append(temp[0])
            AP_CHECKSUM = AP_CHECKSUM + temp[0]
        f.close()
    except:
        print("APROM File load error")
        error_return
    # print '[{}]'.format(', '.join(hex(x) for x in AP_FILE))
    # print len(AP_FILE)


def UPDATE_APROM():
    global AP_FILE
    global PacketNumber
    PacketNumber = PacketNumber + 2
    AP_ADRESS = 0
    AP_SIZE = len(AP_FILE)
    PAP_COMMNAD = [0 for i in range(64)]
    PAP_COMMNAD[0] = 0xa0
    # APROM START ADDRESS
    PAP_COMMNAD[8] = AP_ADRESS & 0xff
    PAP_COMMNAD[9] = AP_ADRESS >> 8 & 0xff
    PAP_COMMNAD[10] = AP_ADRESS >> 16 & 0xff
    PAP_COMMNAD[11] = AP_ADRESS >> 24 & 0xff
    # APROM SIZE
    PAP_COMMNAD[12] = AP_SIZE & 0xff
    PAP_COMMNAD[13] = AP_SIZE >> 8 & 0xff
    PAP_COMMNAD[14] = AP_SIZE >> 16 & 0xff
    PAP_COMMNAD[15] = AP_SIZE >> 24 & 0xff
    PAP_COMMNAD[16:64] = AP_FILE[0:48]  # first package to copy
    # print '[{}]'.format(', '.join(hex(x) for x in PAP_COMMNAD))
    UART_TRANSFER(PAP_COMMNAD, PacketNumber)

    for i in range(48, AP_SIZE, 56):
        PacketNumber = PacketNumber + 2
        PAP1_COMMNAD = [0 for j in range(64)]
        PAP1_COMMNAD[8:64] = AP_FILE[i:(i + 56)]
        # print "test len: %d" % len(PAP1_COMMNAD)
        if len(PAP1_COMMNAD) < 64:
            for k in range(64 - len(PAP1_COMMNAD)):
                PAP1_COMMNAD.append(0xFF)
        # print '[{}]'.format(', '.join(hex(x) for x in PAP1_COMMNAD))
        if (((AP_SIZE - i) < 56) or ((AP_SIZE - i) == 56)):
            # print "end"
            buf = UART_TRANSFER(PAP1_COMMNAD, PacketNumber)
            d_checksum = buf[8] | buf[9] << 8
            if(d_checksum == (AP_CHECKSUM & 0xffff)):
                print("checksum pass")
        else:
            # print "loop"
            UART_TRANSFER(PAP1_COMMNAD, PacketNumber)


# ISP CODE START FORM THERE
if len(sys.argv) != 3:
    print "isp_command port number file name"
    print "isp_command com0 c:\\test.bin"

if __name__ == '__main__':
#def nu_isp_go():
    global com
    com = serial.Serial(sys.argv[1], 115200)
    UART_AUTO_DETECT()
    com.timeout = None
    LINK_FUN()
    SN_FUN()
    READ_PID_FUN()
    READ_FW_FUN()
    READ_CONFIG_FUN()
    READ_APROM_BIN_FILE(sys.argv[2])
    UPDATE_APROM()
    # RUN_TO_APROM_FUN();
    com.close()

