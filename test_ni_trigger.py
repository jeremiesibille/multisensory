# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 09:49:22 2019

@author: AGKremkow
"""

# %%
import nidaqmx 
import time
# %%
task = nidaqmx.Task()
task.do_channels.add_do_chan('Dev1/port0/line0:7')
task.start()



# %%

dataout = 2

for i in range(10):
    task.write([dataout])
    time.sleep(0.5)
    task.write([0])
    time.sleep(0.5)