# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 17:37:48 2018

@author: AGKremkow
"""

# %%
import matplotlib.pyplot as plt
from psychopy import visual
from psychopy import monitors
from psychopy import event
import numpy as np

# %%
#monitor_name = 'NEC_20181113'
#monitor_name = 'NEC_20181115good'
#monitor_name = 'DellCARO20181128bis'
#monitor_name = 'NEC_20190227good'
#monitor_name = 'Dell_20190418' #WARNING this was done on the screen S2716DG
#monitor_name = 'Dell_20190626' #WARNING this was done on the screen S2716DG
#monitor_name = 'NEC_20190709good'
#monitor_name = 'NEC_20191202good'
monitor_name = 'NEC_20191202good_Seewiesen20200106'
monitor_name = 'Ababax_screen'

background_color = [0.,0.,0.]

DellMonitor = monitors.Monitor(monitor_name)
win= visual.Window(monitor = DellMonitor,screen=0,waitBlanking=True,size=[2560, 1440],fullscr=False,allowGUI=False,units='deg',color=background_color,winType='pygame')
#win= visual.Window(monitor = DellMonitor,screen=0,waitBlanking=True,size=[1280, 800],fullscr=True,allowGUI=False,units='deg',color=background_color,useFBO=True)
#win= visual.Window(monitor = DellMonitor,screen=1,waitBlanking=True,size=[1280, 800],fullscr=True,allowGUI=False,units='deg',color=background_color, useFBO=True)
 
# if a new monitor name was selected the gammaGrid should be 0,1,1
DellMonitor.calibs

# %% This will be the input
inputs = np.linspace(-1.,1,11)


 # %% generate images
images = {}
for index, value in enumerate(inputs):
    images[str(index)]=visual.ImageStim(win,np.ones([1,1])*value,size=[2560,1440])
    #images[str(index)]=visual.ImageStim(win,np.ones([1,1])*value,size=[1280,800])
    
# present stimuli
for index, value in enumerate(inputs):
    images[str(index)].draw()
    win.flip()
    tmp = raw_input('enter values for: '+str(value)+' :')        

# %%
# here we have to fill the output lums
#lums = [0.34,1.75,5.52,11.73,21.04,34.92,49.45,69.07,93.21,122.69,156.47] # @ 20180918 14:47
#lums = [0.49,3.10,9.22,19.33,34.77,55.61,81.11,112.4,152.45,201.03,258.45] # @ 20180928 8:47
#lums = [0.28,0.66,2.58,7.7,16.50,28.66,42.72,57.10,71.86,84.39,91.78] # @ 20181114 15:00
#lums = [0.48,1.13,4.12,12.94,27.65,48.2,72.25,96.2,123,145,157] # @ 20181115 12:00
#lums = [0.56,1.64,7.05,21.6,46.8,82.5,123.7,166,209,246.6,267] # @ 20181115 14:00
#lums = [0.46,2.90,9.36,19.81,35.82,57.46,83.85,116.35,158.25,209.33,270.15] # @ 20181128 17:13 Caro
#lums = [0.46,2.97,9.47,20.43,36.40,58.20,83.43,116.22,157.96,206.78,267.60] # @ 20181128 17:37 Caro
#lums = [0.46,3.4,10.5,21.6,38.2,60.1,86.50,118.7,159.3,208.07,265.1] # @ 20181128 17:37 Caro
#lums = [0.96,2.20,8.40,25.62,55.5,98.8,149.8,201.6,255,300.5,328] # @ 20190201 15.00 jerem
#lums = [0.51,16.4,57.4,107.9,167.6,215,261,309,350,385,400] # @ 20190227 18.00 jerem
#lums = [0.48,3.4,12.15,27,50.2,83.1,125.16,180.26,257.1,329.5,335.13] # @ 20190418 18.00 jerem
#lums = [1.6,3.4,10.2,30.1,72,135,213,298.2,378.4,435.5,436.5] # @ 20190709 19.18 jerem NEC projector
#lums = [1.6,6.9,24.5,63.7,119.5,188.2,266,338,402,431,434] # @ 20190709 19.18 jerem NEC projector
#lums = [1.24,9.8,35.6,78,132,192,253,305,354,363,364] # @ 20191203 19.18 jerem NEC projector
lums = [2.15,5.64,20.54,52.21,97.55,154.56,220.20,280.35,336.09, 359.42, 360.73] # @ 20200105 seewiesen dome

plt.plot(inputs,lums,'o')

inputs_fit = np.linspace(0,1.,11)
g = monitors.GammaCalculator(inputs=inputs_fit,lums=lums)

print('Gamma: '+str(g.gamma)+' min: '+str(g.min)+' max: '+str(g.max))

# %% now we save the gamm values in the monitor
gammaGrid = np.ones([4,3])
gammaGrid[:,0] = g.min # min
gammaGrid[:,1] = g.max # max
gammaGrid[:,2] = g.gamma # max

DellMonitor.setGammaGrid(gammaGrid)
DellMonitor.save()
# %%
# we flip one more time to make the screen gray
win.close()
    
# %%
# %%
DellMonitor = monitors.Monitor(monitor_name)
win= visual.Window(monitor = DellMonitor,screen=0,waitBlanking=True,size=[2560, 1440],fullscr=True,allowGUI=False,units='pix',color=background_color,winType='pygame')
#win= visual.Window(monitor = DellMonitor,screen=1,waitBlanking=True,size=[1280, 800],fullscr=False,allowGUI=False,units='pix',color=background_color,winType='pygame')
 
# now the calibration should be in the monitor
DellMonitor.calibs

# %%
inputv = 0.
image = visual.ImageStim(win,np.ones([1,1])*inputv,size=[1280,800])
#image = visual.ImageStim(win,np.ones([1,1])*inputv,size=[2560,1440])
image.draw()
win.flip()


# %%
win.close()
