# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 11:41:29 2021
 this is playground for working with laptop rss32
@author: sharo
"""
import serial
import time

ser = serial.Serial(
            port='COM11',
            baudrate=9600,
            bytesize=serial.SEVENBITS,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE)

msg = bytearray([0x02, 0x08, 0x10, 0x7F,  0x00,  0x00, 0x03,     0x00])

ser.write(msg)
time.sleep(0.1)

# %% send custom code
code_list=range(0,256)
for i in code_list:
    # bytes_code =bytearray( i.to_bytes(8, 'little'))
    ser.write(i) # maybe send itegers
    print(i)
    # print(bytes_code) # send bytes
    # time.sleep(0.1)
    time.sleep(0.5)

# %% send zero
zero=bytearray([0x00, 0x00, 0x00, 0x00,  0x00,  0x00, 0x00, 0x00])
ser.write(msg)
time.sleep(0.1)

# %%  send 3
zero=bytearray([0x1, 0x01, 0x01, 0x00,  0x00,  0x00, 0x00, 0x00])
ser.write(msg)
time.sleep(0.1)

# %%  send 2
zero=bytearray([0x1, 0x01, 0x0, 0x00,  0x00,  0x00, 0x00, 0x00])
ser.write(msg)
time.sleep(0.1)

# %%  send 2
zero=bytearray([0x1, 0x01, 0x0, 0x00,  0x00,  0x00, 0x00, 0x00])
ser.write(msg)
time.sleep(0.1)



# %% all
zero=bytearray([0x1, 0x1, 0x1, 0x1,  0x1,  0x1, 0x1, 0x1])
ser.write(msg)
time.sleep(0.1)

