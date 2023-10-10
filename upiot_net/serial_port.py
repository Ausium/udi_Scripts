#! /bin/python3
# coding = utf-8
"""与车上的4G模块的串口通信,获取流量卡的ICCID"""

import serial
from time import sleep

serial = serial.Serial('/dev/ttyUSB2', 9600, timeout=3600)
if serial.isOpen():
    print('open success')
else:
    print('open failed')
send_data = 'AT+QIMI\r\n'
send_data2 = 'AT+QCCID\r\n'
serial.write(send_data.encode())
data = serial.read(1)
sleep(0.1)
data = (data + serial.read(serial.inWaiting())).decode()
print('IMSI: '+data.split()[2])
serial.write(send_data2.encode())
data = serial.read(1)
sleep(0.1)
data = (data + serial.read(serial.inWaiting())).decode()
# ICCID的最后一位是校验位，不需要
print('ICCID: '+data.split()[2][:-1])
