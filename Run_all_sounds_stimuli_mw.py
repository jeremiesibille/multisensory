# -*- coding: utf-8 -*-


import numpy as np
import os
import time
import tdt
from tqdm import tqdm
import TDT_toolboxes_mw as OurTDT
from datetime import date


#%%# This part is for the date and saving parameters of stimuli


type_of_reco = 'test'

date = date.today()
protocol_index = 0
save_params = dict()
headers = dict()
headers['date'] = date
headers['type_of_reco'] = type_of_reco
save_params['headers'] = headers
folder_save_params = 'C:/Users/InVivo/Desktop/RZ6_Python/TDT_RZ6_params/'
os.mkdir(folder_save_params + str(date))

#%%# 

p0   = 'online'                         
p1   = 'FRA_log2_implement' 
p1_5 = 'FRA_high_freq'
p2   = 'harmonic_shuffle_3500'           
p3   = 'USV'
#p4  = 'harmonic_steps'                    
p5   = 'mix_overtone_shuff'               
p6   = 'mix_overtone_step'                
p7   = 'sin_wave'                         
p8   = 'sine_phase_modulation'
p8_5 = 'sine_phase_modulation_37500'
p9   = 'tone_split'  
p11  = 'interval_1'
p12  = 'interval_2'
p13  = "call_with_noise"

protocols_to_be_run = ['FRA_log2_implement','FRA_high_freq','harmonic_shuffle_3500', 'mix_overtone_shuff' ,'mix_overtone_step','sin_wave','sine_phase_modulation','sine_phase_modulation_37500','USV','tone_split','interval_1','interval_2',"call_with_noise"]

protocols_to_be_run = ['online']


#%%# This part actually runs the protocols

for protocol in protocols_to_be_run:
       

    
    if protocol == 'FRA_log2_implement':
        
        print('Running ' + protocol)
        # 10 attenuations x 30 steps x 10 repeats x 0.6s 
        # 30 minutes in total
        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
    
        full = [0, 10, 20, 30, 40, 50, 60, 70, 80]
        local_params = dict()
        local_params['min_freq'] = 1000
        local_params['max_freq'] = 80000
        local_params['n_steps']  = 30
        local_params['attenuation'] = full
        local_params['repeats'] = 10
        local_params['pulse'] = 100
        local_params['delay'] = 500
        local_params['randomize'] = 1
        
        Combinatory_mat = OurTDT.Expose_FRA_log(local_params)
        local_params['Combinatory_matrice'] = Combinatory_mat
        save_params['local_params'] = local_params
        protocol_index += 1
        save_name = folder_save_params + str(date) + '/' + str(protocol) + '_' + str(protocol_index) + '.npy'
        np.save(save_name,save_params)
        
        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
        
    elif protocol == 'FRA_high_freq':
        
        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
        print('Running ' + protocol)    
        
        local_params = dict()
        local_params['min_freq'] = 50000
        local_params['max_freq'] = 88000
        local_params['n_steps'] = 15
        local_params['randomize'] = 1
        local_params['attenuation'] = [0,5,10,15,20,25,30]
        local_params['repeats'] = 10
        local_params['pulse'] = 100
        local_params['delay'] = 500
    
        Combinatory_mat = OurTDT.Expose_FRA_lin(local_params)
        local_params['Combinatory_matrice'] = Combinatory_mat
        save_params['local_params'] = local_params
        protocol_index += 1
        save_name = folder_save_params + str(date) + '/' + str(protocol) + '_' + str(protocol_index) + '.npy'
        np.save(save_name, save_params)
            
        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
    
    elif protocol == 'online':
        print('Running ' + protocol)    
        # 10 steps x 3 att x 3 rep x 0.6 s
        # Gives 55 s
        
        local_params = dict()
        local_params['min_freq'] = 3000
        local_params['max_freq'] = 80000
        local_params['n_steps'] = 10
        local_params['randomize'] = 0
        local_params['attenuation'] = [0, 20, 40, 60, 80]
        local_params['repeats'] = 3
        local_params['pulse'] = 100
        local_params['delay'] = 200
    
        Combinatory_mat = OurTDT.Expose_FRA_log(local_params)
        local_params['Combinatory_matrice'] = Combinatory_mat
        save_params['local_params'] = local_params
        protocol_index += 1
        save_name = folder_save_params + str(date) + '/' + str(protocol) + '_' + str(protocol_index) + '.npy'
        np.save(save_name, save_params)
            
      #  OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
        
      
     
        
    elif protocol == 'harmonic_shuffle_3500':
        print('Running ' + protocol)   
        # 10 rep x 2**5 x 0.6s = 3.2 min
        # one protocol @3500 Hz
        
        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
        
        local_params = dict()
        local_params['f0'] = 3500
        local_params['repeats'] = 20
        local_params['pulse'] = 100
        local_params['delay'] = 500
        
        Combinatory_mat = OurTDT.Expose_harm_shuff(local_params)
        local_params['Combinatory_matrice'] = Combinatory_mat
        protocol_index += 1
        save_params['local_params'] = local_params
        save_name = folder_save_params + str(date) + '/' + str(protocol) + '_' + str(protocol_index) + '.npy'
        np.save(save_name,save_params)
        
        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
        
            
    elif protocol == 'harmonic_steps':
        
        # 10 steps x 15 reps x 0.6s =  1 min
        # one protocol @3500 Hz
        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
        print('Running ' + protocol)
        local_params = dict()
        local_params['harm'] = 10
        local_params['f0'] = 3500
        local_params['repeats'] = 20
        local_params['pulse'] = 100 
        local_params['delay'] = 500
        local_params['attenuation'] = 0
        
        Combinatory_mat = OurTDT.Expose_harm_steps(local_params)
        local_params['Combinatory_matrice'] = Combinatory_mat
        protocol_index += 1
        save_params['local_params'] = local_params
        save_name = folder_save_params + str(date) + '/' + str(protocol) + '_' + str(protocol_index) +'.npy'
        np.save(save_name,save_params)
           
        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
           
    elif protocol == 'USV':
        
        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
        print('Running ' + protocol)
        local_params = dict()
        local_params['repeats'] = 15
        local_params['delay'] = 800
        Combinatory_mat = OurTDT.Expose_squeaks(local_params)
        local_params['Combinatory_matrice'] = Combinatory_mat
        protocol_index += 1
        save_params['local_params'] = local_params
        save_name = folder_save_params + str(date) + '/' + str(protocol) + '_' + str(protocol_index) +'.npy'
        np.save(save_name,save_params)
            
        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
       
    
        
    
    elif protocol == "interval_1":
        print('Running ' + protocol)        
        OurTDT.Between_protocols_TTL()
        
        local_params = dict()
        local_params['repeats'] = 15
        local_params['delays'] = np.linspace(start = 50, stop = 1000, num = 10)    # get distribution of delays
        
        Combinatory_mat = OurTDT.Expose_interval(local_params)
        
        local_params['Combinatory_matrice'] = Combinatory_mat
        protocol_index += 1
        save_params['local_params'] = local_params
        save_name = folder_save_params + str(date) + '/' + str(protocol) + '_' + str(protocol_index) +'.npy'
        np.save(save_name,save_params)
            
        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
            
   
    elif protocol == "interval_2":
        print('Running ' + protocol)        
        OurTDT.Between_protocols_TTL()
        
        local_params = dict()
        local_params['repeats'] = 15
        local_params['delays'] = np.linspace(start = 50, stop = 1000, num = 10)    # get distribution of delays
        
        Combinatory_mat = OurTDT.Expose_interval2(local_params)
        
        local_params['Combinatory_matrice'] = Combinatory_mat
        protocol_index += 1
        save_params['local_params'] = local_params
        save_name = folder_save_params + str(date) + '/' + str(protocol) + '_' + str(protocol_index) +'.npy'
        np.save(save_name,save_params)
            
        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
            
              
    elif protocol == 'mix_overtone_shuff': 
        print('Running ' + protocol)      
        # 10 repeats 100ms pulse + 500ms delay == 24s  
        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
        
        local_params = dict()
        local_params['repeats'] = 20
        local_params['pulse']   = 100
        local_params['delay']   = 500
        local_params['f0']      = 3500
        Combinatory_mat = OurTDT.Expose_overtone_shuff(local_params)
        local_params['Combinatory_matrice'] = Combinatory_mat
        protocol_index += 1
        save_params['local_params'] = local_params
        save_name = folder_save_params + str(date) + '/' + str(protocol) +'_' + str(protocol_index) + '.npy'
        np.save(save_name,save_params)        
        
        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
         
    elif protocol == 'mix_overtone_step': 
        print('Running ' + protocol)        
        # 10 reps * 100+500 ms == 24 s
        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
        
        local_params = dict()
        local_params['repeats'] = 20
        local_params['pulse']   = 100
        local_params['delay']   = 500
        local_params['f0']      = 3500
        Combinatory_mat = OurTDT.Expose_overtone_step(local_params)
        local_params['Combinatory_matrice'] = Combinatory_mat
        protocol_index += 1
        save_params['local_params'] = local_params
        save_name = folder_save_params + str(date) + '/' + str(protocol) +'_' + str(protocol_index) + '.npy'
        np.save(save_name,save_params)

        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
        
   
    elif protocol == 'sin_wave':
        print('Running ' + protocol)
        # 500ms + 500ms * shift 10kHz * max_freq 90kHz * 10 rep * 7 modulations
        # 10 minutes
        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
        
        local_params = dict()
        
        local_params['pulse']      = 500
        local_params['delay']      = 1000
        local_params['shift']      = 10000
        local_params['max_freq']   = 90000
        local_params['rep']        = 15
        
        local_params['modulation'] = [0, 3.125, 6.25, 12.5, 25, 50, 100, 200]
    
        Combinatory_mat = OurTDT.Expose_sin_protocol(local_params)
        local_params['Combinatory_matrice'] = Combinatory_mat
        save_params['local_params'] = local_params
        protocol_index += 1
        save_name = folder_save_params + str(date) + '/' + str(protocol) + '_' + str(protocol_index) + '.npy'
        np.save(save_name,save_params)    

        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
            

    elif protocol == 'sine_phase_modulation':
        print('Running ' + protocol)
        # This produces complex to chevron to antiphase complex to inverted chevron to complex
        
        # modulation = sine wave modulation in Hz
        # delay = between pulses
        # freq = middle frequency
        # bandwidth = amplitude of sin wave
        # phase = phase shift of sin wave
        
        # proposed values for replication of natural call
        # freq       = 67.5kHz
        # bandwidth  = 7.5 kHz
        # modulation = 8.3 Hz 
        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
        
        local_params = dict()
        modulation = 8.3                                          
    
        local_params['pulse']      = (1/modulation)*1000
        local_params['phase']      = np.linspace(-179, 179, num = 9)
        local_params['freq']       = [67500]  # middle frequency
        local_params['bandwidth']  = 7500 
        local_params['modulation'] = modulation
        
        local_params['rep']        = 15
        local_params['delay']      = 1000
        
        
        Combinatory_mat = OurTDT.Expose_sin_protocol_2(local_params)
        local_params['Combinatory_matrice'] = Combinatory_mat
        save_params['local_params'] = local_params
        protocol_index += 1
        save_name = folder_save_params + str(date) + '/' + str(protocol) + '_' + str(protocol_index) + '.npy'
        np.save(save_name,save_params)    

        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
        
        
    elif protocol == 'sine_phase_modulation_37500':
        print('Running ' + protocol)
        # This produces complex to chevron to antiphase complex to inverted chevron to complex
        
        # modulation = sine wave modulation in Hz
        # delay = between pulses
        # freq = middle frequency
        # bandwidth = amplitude of sin wave
        # phase = phase shift of sin wave
        
        # proposed values for replication of natural call
        # freq       = 67.5kHz
        # bandwidth  = 7.5 kHz
        # modulation = 8.3 Hz 
        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
        
        local_params = dict()
        modulation = 8.3                                          
    
        local_params['pulse']      = (1/modulation)*1000
        local_params['phase']      = np.linspace(-179, 179, num = 9)
        local_params['freq']       = [37500]  # middle frequency
        local_params['bandwidth']  = 7500 
        local_params['modulation'] = modulation
        
        local_params['rep']        = 15
        local_params['delay']      = 1000
        
        
        Combinatory_mat = OurTDT.Expose_sin_protocol_2(local_params)
        local_params['Combinatory_matrice'] = Combinatory_mat
        save_params['local_params'] = local_params
        protocol_index += 1
        save_name = folder_save_params + str(date) + '/' + str(protocol) + '_' + str(protocol_index) + '.npy'
        np.save(save_name,save_params)    

        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
        
        
    elif protocol == 'tone_split':
        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
        print('Running ' + protocol)       
        local_params = dict()
        local_params['freq']       = [60000, 50000]
        local_params['rep']        = 10
        local_params['delay']      = 500
        local_params['pulse']      = 500
        
        Combinatory_mat = OurTDT.Expose_tone_split(local_params)
        local_params['Combinatory_matrice'] = Combinatory_mat
        save_params['local_params'] = local_params
        protocol_index += 1
        save_name = folder_save_params + str(date) + '/' + str(protocol) + '_' + str(protocol_index) + '.npy'
        np.save(save_name,save_params)    
        
        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
        
    elif protocol == 'tone_split_individual_components':
        print('Running ' + protocol)
        # freq = 65000
        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
        local_params = dict()
        local_params['freq']       = 65000
        local_params['rep']        = 10
        local_params['delay']      = 500
        local_params['pulse']      = 130
        
        Combinatory_mat = OurTDT.Expose_tone_split_individual_components(local_params)
        local_params['Combinatory_matrice'] = Combinatory_mat
        save_params['local_params'] = local_params
        protocol_index += 1
        save_name = folder_save_params + str(date) + '/' + str(protocol) + '_' + str(protocol_index) + '.npy'
        np.save(save_name,save_params)    
        
        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
        
        
    elif protocol == 'call_with_noise':
        
        print('Running ' + protocol)
        # This produces complex to chevron to antiphase complex to inverted chevron to complex
        
        # modulation = sine wave modulation in Hz
        # delay = between pulses
        # freq = middle frequency
        # bandwidth = amplitude of sin wave
        # phase = phase shift of sin wave
        
        # proposed values for replication of natural call
        # freq       = 67.5kHz
        # bandwidth  = 7.5 kHz
        # modulation = 8.3 Hz 
        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols
        
        local_params = dict()
        modulation = 8.3                                          
    
        local_params['pulse']      = (1/modulation)*1000
        local_params['noise']      = np.linspace(0, 0.5, 9)
        local_params['freq']       = [67500]  # middle frequency
        local_params['bandwidth']  = 7500 
        local_params['modulation'] = modulation
        local_params['rep']        = 10
        local_params['delay']      = 1000
        
        
        Combinatory_mat = OurTDT.Expose_sin_protocol_3(local_params)
        local_params['Combinatory_matrice'] = Combinatory_mat
        save_params['local_params'] = local_params
        protocol_index += 1
        save_name = folder_save_params + str(date) + '/' + str(protocol) + '_' + str(protocol_index) + '.npy'
        np.save(save_name,save_params)    

        OurTDT.Between_protocols_TTL()  #TTL sequence between protocols 
        