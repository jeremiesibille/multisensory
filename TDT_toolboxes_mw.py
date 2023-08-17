# -*- coding: utf-8 -*-
"""
Script for generating and playing different stimuli for RZ6

These are triggered on RZ6 with "Run_all_stimuli_mp.py"

Scripts refer to the files with TDT circuits, which are in:
'C:/Users/InVivo/Desktop/RZ6_Python/'  (.rcx files)
Created on Wed Dec  8 17:17:36 2021
@author: MPW
"""




import numpy as np
import wavio
import matplotlib.pyplot as plt
import os
import time
import tdt
from tqdm import tqdm
import math

#%%

'''
Function to play 333 ms TTL between protocols
'''
def Between_protocols_TTL():

    print("Between Protocols")
    crc = tdt.DSPCircuit('C:/Users/InVivo/Desktop/RZ6_Python/Between_protocols_TTL.rcx', "RZ6", interface = 'GB', device_id = 1, start = True)
    for i in range(5):
        crc.trigger('A')
        time.sleep(200 / 1000)    
        

#%%


"""
This script PRODUCES stimulation array

FRA - log2 spaced  from 1kHz to 100kHz
Frequency Response Area 

min_freq = minimal frequency 
max step = maximal frequency
n_steps = number of frequency steps, spanning from min_freq to max_freq
attenuation = number of attenuation values (loudness) 

"""

def Produce_FRA_log(n_steps, attenuation, rep, min_freq, max_freq, randomize):
    fq_rg = np.logspace(math.log(min_freq, 2), math.log(max_freq, 2), n_steps, base = 2)
    fq_rg = fq_rg.reshape(n_steps, 1)
    fraarray = np.zeros([1,2])
    for i in attenuation:
        att = np.full(n_steps, i)
        att = att.reshape(n_steps,1)
        stimulus = np.concatenate((fq_rg, att), axis = 1)
        fraarray = np.append(fraarray, stimulus, axis = 0)
    fraarray = np.delete(fraarray, 0, 0)
    fraarray2 = np.append(fraarray, fraarray, axis = 0)
    if rep == 1:
        fraarray2 = fraarray
    elif rep > 1:
        for i in range(rep-2):
            fraarray2 = np.append(fraarray2, fraarray, axis = 0)
    index = np.array(range(n_steps * len(attenuation) * rep))
    fraarray2 = np.concatenate((fraarray2, index.reshape(n_steps * len(attenuation) * rep ,1)), axis = 1)

    if randomize == True:
        np.random.seed(42)
        fraarray2 = np.random.permutation(fraarray2)

    return fraarray2


 #%%
""" 
This script EXPOSES the generated FRA file

""" 
 
def Expose_FRA_log(local_params):
    
    n_steps     = local_params['n_steps']
    attenuation =  local_params['attenuation']
    rep         = local_params['repeats']
    pulse       = local_params['pulse']
    delay       = local_params['delay']
    min_freq    = local_params['min_freq']
    max_freq    = local_params['max_freq']
    randomize   = local_params['randomize']
    
    x = Produce_FRA_log(n_steps, attenuation, rep, min_freq, max_freq, randomize)
    crc = tdt.DSPCircuit('C:/Users/InVivo/Desktop/RZ6_Python/FRA.rcx', "RZ6", interface = 'GB', device_id = 1, start = True)
    
    for i in tqdm(x):
        crc.set_tag('pulse [ms]', pulse)
        crc.set_tag('bw_freq [Hz]', i[0])
        crc.set_tag('bw_att [dB]', i[1])
        time.sleep(delay / 1000)
        crc.trigger('A')
        time.sleep((pulse + 10)/ 1000)
    
    print("Logarythmic FRA done")
    return x


 #%%
 
 
def Produce_FRA_lin(n_steps, attenuation, rep, min_freq, max_freq, randomize):
    fq_rg = np.linspace(min_freq, max_freq, n_steps)
    fq_rg = fq_rg.reshape(n_steps, 1)
    fraarray = np.zeros([1,2])
    for i in attenuation:
        att = np.full(n_steps, i)
        att = att.reshape(n_steps,1)
        stimulus = np.concatenate((fq_rg, att), axis = 1)
        fraarray = np.append(fraarray, stimulus, axis = 0)
    fraarray = np.delete(fraarray, 0, 0)
    fraarray2 = np.append(fraarray, fraarray, axis = 0)
    if rep == 1:
        fraarray2 = fraarray
    elif rep > 1:
        for i in range(rep-2):
            fraarray2 = np.append(fraarray2, fraarray, axis = 0)
    index = np.array(range(n_steps * len(attenuation) * rep))
    fraarray2 = np.concatenate((fraarray2, index.reshape(n_steps * len(attenuation) * rep ,1)), axis = 1)

    if randomize == True:
        np.random.seed(42)
        fraarray2 = np.random.permutation(fraarray2)

    return fraarray2


 #%%
""" 
This script EXPOSES the generated FRA file

""" 
 
def Expose_FRA_lin(local_params):
    
    n_steps     = local_params['n_steps']
    attenuation = local_params['attenuation']
    rep         = local_params['repeats']
    pulse       = local_params['pulse']
    delay       = local_params['delay']
    min_freq    = local_params['min_freq']
    max_freq    = local_params['max_freq']
    randomize   = local_params['randomize']
    
    x = Produce_FRA_log(n_steps, attenuation, rep, min_freq, max_freq, randomize)
    crc = tdt.DSPCircuit('C:/Users/InVivo/Desktop/RZ6_Python/FRA.rcx', "RZ6", interface = 'GB', device_id = 1, start = True)
    
    for i in tqdm(x):
        crc.set_tag('pulse [ms]', pulse)
        crc.set_tag('bw_freq [Hz]', i[0])
        crc.set_tag('bw_att [dB]', i[1])
        time.sleep(delay/ 1000)
        crc.trigger('A')
        time.sleep((pulse + 5)/ 1000)
    
    print("Logarythmic FRA done")
    return x


 #%%
 
 
"""
Harmonic pure tone mixture (shuffle) - 5 tones
This script generates the random  matrix with 0/1 combinations - this is later used to trigger different tones on RZ6

eg [0,1,0,1,0] = tone with no fundamental frequency, first and third harmonic
   [1,1,0,0,0] = tone with fundamental and first harmonic

rep = amount of repetitions

"""


def harm_shuffle(rep):
    binary = [0,1]
    combinations = [(a,b,c,d,e) for a in binary for b in binary for c in binary for d in binary for e in binary]
    combinations = np.array(combinations)
    index = np.array(range(len(combinations) * rep))
    combinations2 = combinations
    for i in range(rep-1):
        combinations2 = np.append(combinations2, combinations, axis = 0)
    combinations = np.concatenate((combinations2, index.reshape(len(index),1)), axis = 1)
    np.random.seed(42)
    combinations = np.random.permutation(combinations)
    return combinations


#%%

""" 
This function exposes the "harmonic shuffle" with desired parameters:
    


"""

def Expose_harm_shuff(local_params):
    
    rep = local_params['repeats']
    pulse = local_params['pulse']
    delay = local_params['delay']
    f0 = local_params['f0']
    
    x = harm_shuffle(rep)
    print("Running harmonic shuffle")
    crc = tdt.DSPCircuit('C:/Users/InVivo/Desktop/RZ6_Python/harmonic shuffle.rcx', "RZ6", interface = 'GB', device_id = 1, start = True)
    
    for i in tqdm(x):
        crc.set_tag('f0', i[0] * f0 * 1)
        crc.set_tag('h1', i[1] * f0 * 2)
        crc.set_tag('h2', i[2] * f0 * 3)
        crc.set_tag('h3', i[3] * f0 * 4)
        crc.set_tag('h4', i[4] * f0 * 5)
        crc.set_tag('pulse [ms]', pulse)
        time.sleep(delay/ 1000)
        crc.trigger('A')
        time.sleep((pulse + 5)/ 1000)
    
    print("Harmonic shuffle done")
    return x

 #%%
"""
Harmonic steps

"""

def Calc_harm_steps(n, rep):
    x = np.zeros([n+1, n])
    for i in range(n+1):
        for j in range(i):
            x[i,j] = 1

    x2 = x
    index = np.array(range(len(x) * rep))
    for i in range(rep-1):
        x2 = np.append(x2, x, axis = 0)
    x = np.concatenate((x2, index.reshape(len(index),1)), axis = 1)
    np.random.seed(42)
    x = np.random.permutation(x)
    return x

#%%
def Expose_harm_steps(local_params): 
  
    n     = local_params['harm']
    f0    = local_params['f0']
    rep   = local_params['repeats']
    pulse = local_params['pulse'] 
    delay = local_params['delay'] 
    attenuation = local_params['attenuation']
    
    x = Calc_harm_steps(n, rep)
      
    print("Running harmonic steps")
    crc = tdt.DSPCircuit('C:/Users/InVivo/Desktop/RZ6_Python/harmonic steps.rcx', "RZ6", interface = 'GB', device_id = 1, start = True)
    
    for i in tqdm(x):
        crc.set_tag('f0', i[0] * f0 * 1)
        crc.set_tag('h1', i[1] * f0 * 2)
        crc.set_tag('h2', i[2] * f0 * 3)
        crc.set_tag('h3', i[3] * f0 * 4)
        crc.set_tag('h4', i[4] * f0 * 5)
        crc.set_tag('h5', i[5] * f0 * 6)
        crc.set_tag('h6', i[6] * f0 * 7)
        crc.set_tag('h7', i[7] * f0 * 8)
        crc.set_tag('h8', i[8] * f0 * 9)
        crc.set_tag('h9', i[9] * f0 * 10)
        crc.set_tag('pulse [ms]', pulse)
        crc.set_tag('bw_att [dB]', attenuation)
        time.sleep(delay/ 1000)
        crc.trigger('A')
        time.sleep((pulse + 5)/ 1000)
    
    print("Harmonic steps done")
    return x


    
 #%%

    print("Running squeaks")
    
    
    for snip in tqdm(wav):
        x = wavio.read('C:/Users/InVivo/Desktop/RZ6_Python/wav files/all files/' + snip)
        wavio.write('C:/Users/InVivo/Desktop/RZ6_Python/wav files/current file/file.wav', data = x.data, rate = x.rate, sampwidth= 2)
        crc = tdt.DSPCircuit('C:/Users/InVivo/Desktop/RZ6_Python/play wav.rcx', "RZ6", interface = 'GB', device_id = 1, start = True)    
        time.sleep(delay / 1000)
        crc.stop()
         
        
    tdt.DSPCircuit('C:/Users/InVivo/Desktop/RZ6_Python/empty.rcx', "RZ6", interface = 'GB', device_id = 1, start = True)

    print("Squeaks done")
    return wav
    return snip


#%%


def Expose_squeaks(local_params):

    wav   = os.listdir('C:/Users/InVivo/Desktop/RZ6_Python/wav files/all files')
    rep   = local_params['repeats']
    delay = local_params['delay']
    
    wav = wav * rep
    wav = np.array(wav)
    wav.reshape(len(wav), 1)    
    np.random.seed(42)
    wav = np.random.permutation(wav)
    
    print("Running squeaks")
    
    
    for snip in tqdm(wav):
        x = wavio.read('C:/Users/InVivo/Desktop/RZ6_Python/wav files/all files/' + snip)
        wavio.write('C:/Users/InVivo/Desktop/RZ6_Python/wav files/current file/file.wav', data = x.data, rate = x.rate, sampwidth= 2)
        crc = tdt.DSPCircuit('C:/Users/InVivo/Desktop/RZ6_Python/play wav.rcx', "RZ6", interface = 'GB', device_id = 1, start = True)    
        time.sleep(delay / 1000)
        crc.stop()
         
        
    tdt.DSPCircuit('C:/Users/InVivo/Desktop/RZ6_Python/empty.rcx', "RZ6", interface = 'GB', device_id = 1, start = True)

    print("Squeaks done")
    return wav
    return snip


#%%

    
def Expose_interval(local_params):
    
    rep    = local_params['repeats']
    delays = local_params['delays']
    delays = list(delays)
    delays = delays * rep
    delays = np.array(delays)
    delays = np.random.permutation(delays)
    

    print("Running interval")
    
    x = wavio.read('C:/Users/InVivo/Desktop/RZ6_Python/wav files/interval/complex_70.wav')
    wavio.write('C:/Users/InVivo/Desktop/RZ6_Python/wav files/current file/file.wav', data = x.data, rate = x.rate, sampwidth= 2)
   
    for delay in tqdm(delays):    
        tdt.DSPCircuit('C:/Users/InVivo/Desktop/RZ6_Python/play wav.rcx', "RZ6", interface = 'GB', device_id = 1, start = True)
        time.sleep(delay / 1000) 
    
    
    tdt.DSPCircuit('C:/Users/InVivo/Desktop/RZ6_Python/empty.rcx', "RZ6", interface = 'GB', device_id = 1, start = True)
    print("Intervals done")    
   
    return delays

#%%

      
def Expose_interval2(local_params):
    
    rep    = local_params['repeats']
    delays = local_params['delays']
    delays = list(delays)
    delays = delays * rep
    delays = np.array(delays)
    delays = np.random.permutation(delays)
    

    print("Running interval")

    x = wavio.read('C:/Users/InVivo/Desktop/RZ6_Python/wav files/interval2/squeak_6.wav')
    wavio.write('C:/Users/InVivo/Desktop/RZ6_Python/wav files/current file/file.wav', data = x.data, rate = x.rate, sampwidth= 2)
   
    for delay in tqdm(delays):    
        tdt.DSPCircuit('C:/Users/InVivo/Desktop/RZ6_Python/play wav.rcx', "RZ6", interface = 'GB', device_id = 1, start = True)
        time.sleep(delay / 1000) 
    
    
    tdt.DSPCircuit('C:/Users/InVivo/Desktop/RZ6_Python/empty.rcx', "RZ6", interface = 'GB', device_id = 1, start = True)
    print("Intervals done")    
   
    return delays




#%%

def Expose_looming(local_params):

    wav   = os.listdir('C:/Users/InVivo/Desktop/RZ6_Python/wav files/looming')
    rep   = local_params['repeats']
    pulse = local_params['pulse']
    delay = local_params['delay']
    
    wav = wav * rep
    wav = np.array(wav)
    wav.reshape(len(wav), 1)    
    np.random.seed(42)
    wav = np.random.permutation(wav)

    print("Running looming")
    for snip in tqdm(wav):
        x = wavio.read('C:/Users/InVivo/Desktop/RZ6_Python/wav files/looming/' + snip)
        wavio.write('C:/Users/InVivo/Desktop/RZ6_Python/wav files/current file/file.wav', data = x.data, rate = x.rate, sampwidth= 2)
        crc = tdt.DSPCircuit('C:/Users/InVivo/Desktop/RZ6_Python/play wav.rcx', "RZ6", interface = 'GB', device_id = 1, start = True)
        time.sleep(delay / 1000) 
        for i in range(rep):
            print("Running file:" + snip + str(i))
            crc.trigger('A')
            time.sleep((pulse + 5)/ 1000) 

    crc = tdt.DSPCircuit('C:/Users/InVivo/Desktop/RZ6_Python/empty.rcx', "RZ6", interface = 'GB', device_id = 1, start = True)

    print("Looming protocol done")
    return wav

    
    

 #%%
"""
Overtone mix
"""


def mix_overtone_shuff(rep):
    binary = [0,1]
    combinations = [(a,b) for a in binary for b in binary]
    combinations = np.array(combinations)
    index = np.array(range(len(combinations) * rep))
    combinations2 = combinations
    for i in range(rep-1):
        combinations2 = np.append(combinations2, combinations, axis = 0)
    combinations = np.concatenate((combinations2, index.reshape(len(index),1)), axis = 1)
    
    np.random.seed(42)
    combinations = np.random.permutation(combinations)
    return combinations

   

 #%%
"""
Overtone mix - short adaptation
"""
def Expose_overtone_adaptation(local_params):
    
    rep = local_params['repeats']
    pulse = local_params['pulse']
    delay = local_params['delay']
    f0 = local_params['f0']
    
    x = mix_overtone_shuff(rep)
    print("Running overtone shuffle")
    crc = tdt.DSPCircuit('C:/Users/InVivo/Desktop/RZ6_Python/overtone shuffle.rcx', "RZ6", interface = 'GB', device_id = 1, start = True)
    
    
    for i in tqdm(x):
        crc.set_tag('f0', i[1] * f0 * 1)
        crc.set_tag('h1', i[1] * f0 * 2)
        crc.set_tag('h2', i[1] * f0 * 3)
        crc.set_tag('h3', i[1] * f0 * 4)
        crc.set_tag('s1', i[0] * f0 * 1.5)
        crc.set_tag('s2', i[0] * f0 * 2.5)
        crc.set_tag('s3', i[0] * f0 * 3.5)
        crc.set_tag('s4', i[0] * f0 * 4.5)
        crc.set_tag('pulse [ms]', pulse)
        time.sleep(delay/ 1000)
        crc.trigger('A')
        time.sleep((pulse + 5)/ 1000)
    
    print("mix_overtone_shuff done")
    return x


 #%%

""" 
Overtone shuffle:
    
"""

def Expose_overtone_shuff(local_params):
    
    rep = local_params['repeats']
    pulse = local_params['pulse']
    delay = local_params['delay']
    f0 = local_params['f0']
    
    x = mix_overtone_shuff(rep)
    print("Running overtone shuffle")
    crc = tdt.DSPCircuit('C:/Users/InVivo/Desktop/RZ6_Python/overtone shuffle.rcx', "RZ6", interface = 'GB', device_id = 1, start = True)
    
    for i in tqdm(x):
        crc.set_tag('f0', i[1] * f0 * 1)
        crc.set_tag('h1', i[1] * f0 * 2)
        crc.set_tag('h2', i[1] * f0 * 3)
        crc.set_tag('h3', i[1] * f0 * 4)
        crc.set_tag('s1', i[0] * f0 * 1.5)
        crc.set_tag('s2', i[0] * f0 * 2.5)
        crc.set_tag('s3', i[0] * f0 * 3.5)
        crc.set_tag('s4', i[0] * f0 * 4.5)
        
        crc.set_tag('pulse [ms]', pulse)
        time.sleep(delay/ 1000)
        crc.trigger('A')
        time.sleep((pulse + 5)/ 1000)
    
    print("mix_overtone_shuff done")
    return x

 #%%
#needs some work 
""" 
This function exposes the overtone step:
    
"""

def Expose_overtone_step(local_params):
    
    rep = local_params['repeats']
    pulse = local_params['pulse']
    delay = local_params['delay']
    f0 = local_params['f0']
    
    x = mix_overtone_shuff(rep)
    print("Running overtone step")
    crc = tdt.DSPCircuit('C:/Users/InVivo/Desktop/RZ6_Python/overtone step.rcx', "RZ6", interface = 'GB', device_id = 1, start = True)
    
    for i in tqdm(x):
        crc.set_tag('f0', i[1] * f0 * 1)
        crc.set_tag('h1', i[1] * f0 * 2)
        crc.set_tag('h2', i[1] * f0 * 3)
        crc.set_tag('h3', i[1] * f0 * 4)
        crc.set_tag('s1', i[0] * f0 * 1.5)
        crc.set_tag('s2', i[0] * f0 * 2.5)
        crc.set_tag('s3', i[0] * f0 * 3.5)
        crc.set_tag('s4', i[0] * f0 * 4.5)
        time.sleep(delay / 1000)
        crc.trigger('A')
        time.sleep((pulse*2 )/ 1000)
    
    print("mix_overtone_step done")
    return x


 #%%

# modulated sin wave


def Produce_sin_protocol(shift, rep, modulation, max_freq):

    freq = np.arange(start = shift, stop = max_freq, step = shift)
    stim = np.zeros((1,2))
    modulation = np.array(modulation)

    for i in range(len(freq)):
        temp = np.array([modulation, np.full(len(modulation), freq[i])])
        stim = np.concatenate((stim, temp.T), axis = 0)
    
    stim = np.delete(stim, 0 ,0)
    
    if rep == 1:
        stim2 = stim
    elif rep > 1:
        stim2 = np.append(stim,stim, axis = 0)
        for i in range(rep-2):
            stim2 = np.append(stim2, stim, axis = 0)
        
    index = np.array(range(len(freq)*len(modulation)*rep))
    index = index.reshape(len(index), 1)
    stim3 = np.concatenate((stim2, index), axis = 1)
    np.random.seed(42)
    stim3 = np.random.permutation(stim3)
    return stim3
 
 #%%
""" 
This script exposes sin wave protocol
""" 
 
def Expose_sin_protocol(local_params):
    
    shift       = local_params['shift']
    pulse       = local_params['pulse']
    delay       = local_params['delay']
    max_freq    = local_params['max_freq'] 
    rep         = local_params['rep']
    modulation  = local_params['modulation'] 
    
    x = Produce_sin_protocol(shift, rep, modulation, max_freq)
    crc = tdt.DSPCircuit('C:/Users/InVivo/Desktop/RZ6_Python/sine_modulation.rcx', "RZ6", interface = 'GB', device_id = 1, start = True)
    
    for i in tqdm(x):
        crc.set_tag('Shift', shift)
        crc.set_tag('Modulation', i[0])
        crc.set_tag('Shift', i[1])
        crc.set_tag('pulse', pulse)
        time.sleep(delay / 1000)
        crc.trigger('A')
        time.sleep((pulse + 5)/ 1000)
    
    print("Expose_sin_protocol done")
    return x

 #%%
 
# modulated sin wave with phase shift


def Produce_sin_protocol_2(freq, rep, phase):

    freq = np.array(freq)
    stim = np.zeros((1,2))
    phase = np.array(phase)

    for i in range(len(freq)):
        temp = np.array([phase, np.full(len(phase), freq[i])])
        stim = np.concatenate((stim, temp.T), axis = 0)
    
    stim = np.delete(stim, 0 ,0)
    
    if rep == 1:
        stim2 = stim
    elif rep > 1:
        stim2 = np.append(stim,stim, axis = 0)
        for i in range(rep-2):
            stim2 = np.append(stim2, stim, axis = 0)
        
    index = np.array(range(len(freq)*len(phase)*rep))
    index = index.reshape(len(index), 1)
    stim3 = np.concatenate((stim2, index), axis = 1)
    np.random.seed(42)
    stim3 = np.random.permutation(stim3)
    return stim3
    

 #%%
""" 
This script exposes sin wave protocol
""" 
 
def Expose_sin_protocol_2(local_params):
    
    pulse       = local_params['pulse']
    delay       = local_params['delay']
    freq        = local_params['freq'] 
    rep         = local_params['rep']
    phase       = local_params['phase'] 
    modulation  = local_params['modulation']
    bandwidth   = local_params['bandwidth']
    
    x = Produce_sin_protocol_2(freq, rep, phase)
    crc = tdt.DSPCircuit('C:/Users/InVivo/Desktop/RZ6_Python/sine_modulation2.rcx', "RZ6", interface = 'GB', device_id = 1, start = True)
    
    for i in tqdm(x):
        crc.set_tag('Modulation', modulation)
        crc.set_tag('Bandwidth', bandwidth)  
        crc.set_tag('Phase', i[0])
        crc.set_tag('Shift', i[1])
        crc.set_tag('pulse', pulse)
        time.sleep((delay + 0) / 1000)
        crc.trigger('A')
        time.sleep((pulse + 5) / 1000)
    
    print("Expose_sin_protocol done")
    return x

 #%%
 
 
# modulated ramp wave


def Produce_ramp_protocol(shift, rep, slope, min_freq):

    freq = np.arange(start = 0, stop = max_freq, step = shift)
    stim = np.zeros((1,2))
    modulation = np.array(modulation)


    for i in range(len(freq)):
        temp = np.array([modulation, np.full(len(modulation), freq[i])])
        stim = np.concatenate((stim, temp.T), axis = 0)
    
    stim = np.delete(stim, 0 ,0)
    
    if rep == 1:
        stim2 = stim
    elif rep > 1:
        stim2 = np.append(stim,stim, axis = 0)
        for i in range(rep-2):
            stim2 = np.append(stim2, stim, axis = 0)
        
    index = np.array(range(len(freq)*len(modulation)*rep))
    index = index.reshape(len(index), 1)
    stim3 = np.concatenate((stim2, index), axis = 1)
    np.random.seed(42)
    stim3 = np.random.permutation(stim3)
    return stim3


 
 
""" 
This script exposes ramp protocol
""" 
 
def Expose_ramp_protocol(local_params):
    
    shift       = local_params['shift']
    pulse       = local_params['pulse']
    delay       = local_params['delay']
    min_freq    = local_params['min_freq'] 
    rep         = local_params['rep']
    slope       = local_params['slope'] 
    
    x = Produce_sin_protocol(shift, rep, slope, min_freq)
    crc = tdt.DSPCircuit('C:/Users/InVivo/Desktop/RZ6_Python/sine_modulation.rcx', "RZ6", interface = 'GB', device_id = 1, start = True)
    
    for i in tqdm(x):
        crc.set_tag('Shift', shift)
        crc.set_tag('Modulation', i[0])
        crc.set_tag('Shift', i[1])
        time.sleep(delay/ 1000)
        crc.trigger('A')
        time.sleep(pulse / 1000)
    
    print("Expose_sin_protocol done")
    

 #%%
 

# Split call (frequency step)

def produce_tone_split_protocol(freq, rep):

    freq = freq*rep
    freq = np.array(freq)
    index = np.array(range(len(freq)))
    stim = np.vstack((freq, index))
    stim = stim.T
    np.random.seed(42)
    stim = np.random.permutation(stim)
    return stim


 #%%

def Expose_tone_split(local_params):
     
    freq         = local_params['freq']
    rep          = local_params['rep']
    delay       = local_params['delay']
    pulse       = local_params['pulse']
    
    x = produce_tone_split_protocol(freq, rep)
    crc = tdt.DSPCircuit('C:/Users/InVivo/Desktop/RZ6_Python/tone split.rcx', "RZ6", interface = 'GB', device_id = 1, start = True)
    
    for i in tqdm(x):
        time.sleep(1)
        crc.set_tag('freq [Hz]', i[0])
        crc.set_tag('freq_low [Hz]', i[0] / 1.5)
        crc.set_tag('freq_high [Hz]', (i[0] / 1.5) *2)
        time.sleep(delay/ 1000)
        crc.trigger('A')
        time.sleep(pulse / 1000)
    
    print("Expose_sin_protocol done")


 #%%


"""
tone split components mix
"""


def produce_tone_split_mix(rep):
    binary = [0,1]
    combinations = [(a,b,c,d) for a in binary for b in binary for c in binary for d in binary]
    combinations = np.array(combinations)
    index = np.array(range(len(combinations) * rep))
    combinations2 = combinations
    for i in range(rep-1):
        combinations2 = np.append(combinations2, combinations, axis = 0)
    combinations = np.concatenate((combinations2, index.reshape(len(index),1)), axis = 1)
    np.random.seed(42)
    combinations = np.random.permutation(combinations)
    return combinations


 #%%

def Expose_tone_split_individual_components(local_params):
     
    freq         = local_params['freq']
    rep          = local_params['rep']
    delay        = local_params['delay']
    pulse        = local_params['pulse']
    
    freq_1 = freq
    freq_2 = freq / 1.5
    freq_3 = freq_2 * 2
    freq_4 = freq_1
    
    x = produce_tone_split_mix(rep)
    crc = tdt.DSPCircuit('C:/Users/InVivo/Desktop/RZ6_Python/tone split individual components.rcx', "RZ6", interface = 'GB', device_id = 1, start = True)
     
    for i in tqdm(x):
        time.sleep(1)
        crc.set_tag('freq_1 [Hz]', freq_1 * i[0])
        crc.set_tag('freq_2 [Hz]', freq_2 * i[1])
        crc.set_tag('freq_3 [Hz]', freq_3 * i[2])
        crc.set_tag('freq_4 [Hz]', freq_4 * i[3])
        time.sleep(delay/ 1000)
        crc.trigger('A')
        time.sleep(pulse / 1000)
    
    print("Expose_sin_protocol done")


 #%%
 
# modulated sin wave with phase shift and noise


def Produce_sin_protocol_3(freq, rep, noise):

    freq = np.array(freq)
    stim = np.zeros((1,2))
    noise = np.array(noise)

    for i in range(len(freq)):
        temp = np.array([noise, np.full(len(noise), freq[i])])
        stim = np.concatenate((stim, temp.T), axis = 0)
    
    stim = np.delete(stim, 0 ,0)
    
    if rep == 1:
        stim2 = stim
    elif rep > 1:
        stim2 = np.append(stim,stim, axis = 0)
        for i in range(rep-2):
            stim2 = np.append(stim2, stim, axis = 0)
        
    index = np.array(range(len(freq)*len(noise)*rep))
    index = index.reshape(len(index), 1)
    stim3 = np.concatenate((stim2, index), axis = 1)
    np.random.seed(42)
    stim3 = np.random.permutation(stim3)
    return stim3
    

 #%%
""" 
This script exposes sin wave protocol
""" 
 
def Expose_sin_protocol_3(local_params):
    
    pulse       = local_params['pulse']
    delay       = local_params['delay']
    freq        = local_params['freq'] 
    rep         = local_params['rep']
    noise       = local_params['noise'] 
    modulation  = local_params['modulation']
    bandwidth   = local_params['bandwidth']
    
    x = Produce_sin_protocol_2(freq, rep, noise)
    crc = tdt.DSPCircuit('C:/Users/InVivo/Desktop/RZ6_Python/call with noise.rcx', "RZ6", interface = 'GB', device_id = 1, start = True)
    
    for i in tqdm(x):
        crc.set_tag('Modulation', modulation)
        crc.set_tag('Bandwidth', bandwidth)  
        crc.set_tag('noise', i[0])
        crc.set_tag('Shift', i[1])
        crc.set_tag('pulse', pulse)
        time.sleep((delay + 0) / 1000)
        crc.trigger('A')
        time.sleep((pulse + 5) / 1000)
    
    print("Expose_sin_protocol with noise done")
    return x









