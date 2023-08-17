
# -*- coding: utf-8 -*-

#here we import the tool for sounds
import numpy as np
import os
import time
import tdt
from tqdm import tqdm
import TDT_toolboxes_mw as OurTDT
from datetime import date

#here we import for visual stim
import Toolboxes_multisensory as OurSetup
# import matplotlib.pyplot as plt
#the next ones are extra script just for visual
import ImageStimulus
import MovingGratingStimulus
import MovingBarStimulus
import LoomingStimulus

#%%# This part is for the date and saving parameters of stimuli

type_of_reco = 'test'

date = date.today()
protocol_index = 0
save_params = dict()
headers = dict()
headers['date'] = date
headers['type_of_reco'] = type_of_reco
header['electrode'] = 'Neuropixel'
header['penetrationtype'] = 'Mouse_vertical'
folder_save_params = 'C:/Users/InVivo/Desktop/RZ6_Python/TDT_RZ6_and_visual_params/'
os.mkdir(folder_save_params + str(date))

header['folder_tmp'] = folder_save_params
header['folder_save'] = folder_save_params

monitor = {}
monitor['distance'] = 10
monitor['background'] = [0.,0.,0.]
monitor['refreshrate'] = 120.
monitor['type'] =  'Dell' #   'Dell'  #     
# position of the stimulus
position = np.array([0.,0.]) # negative: right and up, positive: left and down 
monitor['position'] =  position
#### WARNING for the dome it is inverted! poisitve: right and up, negative: left and down 
# stimulus params
stimulus = {}
stimulus['onset_adaptation_time_sec'] = 1.

#%% we open a window for all stimuli. then we might have to set the backgorund
win,trigger = OurSetup.OpenScreen(monitor['background'],monitor['distance'],monitor['type'])
#this should already have made the stimulus screen on

save_params['monitor'] = monitor
save_params['headers'] = headers

#%%# these are the desired protocols list

p0   = 'online'                         
p1   = 'FRA_log2_implement' 
p1_5 = 'FRA_high_freq'
p2   = 'harmonic_shuffle_3500'           
p3   =  'ILD_different_tone'
p4   =  'Looming_left'
p5   =  'Looming_right'
p6   =  'Looming_left_right'

protocols_to_be_run = ['FRA_log2_implement','FRA_high_freq']

protocols_to_be_run =   ['mb']#,'sl36x22_3','sd36x22_3','chi','mg','csd','mp'] #['slquick']
protocols_to_be_run = ['online_pure_tone']

#%%# This part actually runs the protocols
start = time()
for protocol in protocols_to_be_run:
    
    elif protocol == 'online_pure_tone':
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
    
    elif stimulus_type == 'slquick':
        # load the stimulus file
        #        filename = 'locally_light_sparse_noise_45_25_target_size_3_targets_per_frame_2_trials_10_background_-1.0_20181020.npy' 
        filename = 'locally_light_sparse_noise_36_22_target_size_3_targets_per_frame_2_trials_10_background_-1.0_20181120.npy'
        stimulus['filename'] = filename
        stimulus_tmp = np.load('stimuli/'+filename).item()
        stimulus_frames = stimulus_tmp['frames']
        background = stimulus_tmp['background']
        
        params['monitor']['background'] =[background,background,background]# [1.,1.,1.]#
        stimulus['trials'] = 1
        stimulus['scale'] = 5. # scale is now in the units of deg, i.e. scale = 1 means that one noise pixel has the size of 1x1 deg
        stimulus['stimulus_duration_in_frames'] = 6
        stimulus['position'] = position# in deg    
        
        analysis['type'] = 'STA'
        
        params['stimulus'] = stimulus
        params['analysis'] = analysis
        # run
        ImageStimulus.present_images(stimulus_frames,params,setup)
        print "Time passed %d" %(time()-start) + ' seconds'
        
      
    elif stimulus_type == 'sl36x22_3':
        # load the stimulus file
        filename = 'locally_light_sparse_noise_36_22_target_size_3_targets_per_frame_2_trials_10_background_-1.0_20181120.npy'#
                    
        stimulus['filename'] = filename
        stimulus_tmp = np.load('stimuli/'+filename).item()
        stimulus_frames = stimulus_tmp['frames']
        background = stimulus_tmp['background']
        
        params['monitor']['background'] = [background,background,background]
        stimulus['trials'] = 1
        stimulus['scale'] = 5. # scale is now in the units of deg, i.e. scale = 1 means that one noise pixel has the size of 1x1 deg
        stimulus['stimulus_duration_in_frames'] = 12
        stimulus['position'] = position# in deg    
        
        analysis['type'] = 'STA'
        
        params['stimulus'] = stimulus
        params['analysis'] = analysis
        # run
        ImageStimulus.present_images(stimulus_frames,params,setup)
        
    elif stimulus_type == 'sd36x22_3':
        # load the stimulus file
        filename = 'locally_dark_sparse_noise_36_22_target_size_3_targets_per_frame_2_trials_10_background_1.0_20181120.npy'
        stimulus['filename'] = filename
        stimulus_tmp = np.load('stimuli/'+filename).item()
        stimulus_frames = stimulus_tmp['frames']
        background = stimulus_tmp['background']
        
        params['monitor']['background'] = [background,background,background]
        stimulus['trials'] = 1
        stimulus['scale'] = 5. # scale is now in the units of deg, i.e. scale = 1 means that one noise pixel has the size of 1x1 deg
        stimulus['stimulus_duration_in_frames'] = 12
        stimulus['position'] = position# in deg    
        
        analysis['type'] = 'STA'
        
        params['stimulus'] = stimulus
        params['analysis'] = analysis
        # run
        ImageStimulus.present_images(stimulus_frames,params,setup)

    elif stimulus_type == 'mg':
        stimulus['local_type'] = 'do nothing'
        stimulus['trials'] = 5
        stimulus['temporalfrequencies'] = np.array([2.])#,2.,3.]) # in Hz, maybe here going to 2 would save time? # for LGN: 2,3,4 Hz
        stimulus['spatialfrequencies'] = np.array([0.02,0.08]) #np.array([0.01,0.02,0.04,0.08,0.16]) # np.array([0.01,0.02,0.04,0.08,0.16])
        stimulus['orientations'] = np.linspace(0.,360.-(360/12.),12) # np.array([270.]) #  np.linspace(0.,360.-(360/12.),12) #np.linspace(0.,360.-(360/12.),12) #np.linspace(0.,360.-(360/12.),12)  # np.array([210.])
        stimulus['size'] = ([400.,400.]) # np.array([50.,50.]) # ([400.,400.]) # to change in order to reduce the mask size
        stimulus['phase'] = 0.0
        stimulus['duration'] = 1.5
        stimulus['pause'] = 0.5
        stimulus['position'] = position
        params['monitor']['background'] = [0.,0.,0.]
        
        analysis['type'] = 'TuningPolar'
        analysis['parameters'] = ['orientations'] 
        analysis['psth_duration'] = stimulus['duration']
        
        params['stimulus'] = stimulus
        params['analysis'] = analysis
        # run
        MovingGratingStimulus.run_stimulus(params,setup)    
        print "Time passed %d" %(time()-start) + ' seconds'    
        
    elif stimulus_type == 'mb': #mooving bar white or black on gray background
        stimulus['trials'] = 10
        stimulus['orientations'] = np.linspace(0.,360.-(360./12.),12) # np.array([270.])#np.linspace(0.,360.-(360./12.),12)#np.linspace(0.,360.-(360./12.),12)#np.array([120.])
        stimulus['widths'] = np.array([10.])
        stimulus['length'] = 400. # 50. #400
        stimulus['speeds'] = np.array([150.])#np.array([150.]) #degree per seconds
        stimulus['luminances'] = np.array([1.]) # 1 = light, -1 dark, 0 gray  np.array([-1.,1.])
        stimulus['radius_circle'] =  120. #30. #
        params['monitor']['background'] = [-1.,-1.,-1.]
        
        analysis['type'] = 'TuningPolar'
        analysis['parameters'] = ['orientations'] 
        analysis['psth_duration'] = 1.5
        
        params['stimulus'] = stimulus
        params['analysis'] = analysis
        MovingBarStimulus.run_stimulus(params,setup)
        print "Time passed %d" %(time()-start) + ' seconds'
        
    elif stimulus_type == 'mp': #moving point
        stimulus['trials'] = 10
        stimulus['orientations'] = np.linspace(0.,360.-(360./12.),12) #np.array([330.])#np.linspace(0.,360.-(360/12.),12)#np.linspace(0.,360.-(360/12.),12)#np.array([120.])
        stimulus['widths'] = np.array([5.])
        stimulus['length'] = 5.
        stimulus['speeds'] = np.array([150.]) #degree per seconds
        stimulus['luminances'] = np.array([1.]) # 1 = light, -1 dark, 0 gray
        stimulus['radius_circle'] =  90.#  30. #
        params['monitor']['background'] = [-1.,-1.,-1.]
        
        analysis['type'] = 'TuningPolar'
        analysis['parameters'] = ['orientations'] 
        analysis['psth_duration'] = 2.
        
        params['stimulus'] = stimulus
        params['analysis'] = analysis
        MovingBarStimulus.run_stimulus(params,setup)
        print "Time passed %d" %(time()-start) + ' seconds'
        
    elif stimulus_type == 'chi':
        # load the stimulus file
        filename = 'chirp_stimulus_20181011.npy'
        stimulus['filename'] = filename
        stimulus_frames = np.load('stimuli/'+filename)
        # parameters
        params['monitor']['background'] = [0.,0.,0.]
        stimulus['trials'] = 10
        stimulus['scale'] = 350. # scale is now in the units of deg, i.e. scale = 1 means that one noise pixel has the size of 1x1 deg
        stimulus['stimulus_duration_in_frames'] = 1
        stimulus['position'] = position# in deg
        stimulus['duration'] = 35.
                           
        analysis['type'] = 'PSTH' #'TunningLinear'# #'TunningLinear'
        analysis['parameters'] = ['speeds']         
        analysis['psth_duration'] = stimulus['duration']
                
        params['stimulus'] = stimulus
        params['analysis'] = analysis
        # run
        ImageStimulus.present_images_with_first_frame_trigger(stimulus_frames,params,setup)
        print "Time passed %d" %(time()-start) + ' seconds'
        
    elif stimulus_type == 'lo':
        params['monitor']['background'] = [1.,1.,1.]
        stimulus['trials'] = 20
        stimulus['speeds'] = np.array([10.,50.,100.,200.])
        stimulus['max_size'] = 100. # this is the size when the disc is at its largest size
        stimulus['luminances'] = np.array([-1.])
        stimulus['position'] = position #np.array([0.,15.]) 
        stimulus['duration'] = 3.
        
        analysis['type'] = 'TunningLinear'# 'PSTH'#'TunningLinear'
        analysis['parameters'] = ['speeds'] 
        analysis['psth_duration'] = stimulus['duration']
                
        params['stimulus'] = stimulus
        params['analysis'] = analysis
        
        LoomingStimulus.run_stimulus(params,setup)
        print "Time passed %d" %(time()-start) + ' seconds'
        
    elif stimulus_type == 'csd': #
        # load the stimulus fil
        background = 0.
        params['monitor']['background'] = [background,background,background]# [1.,1.,1.]#

        stimulus['trials'] = 200
        stimulus['scale'] = 10. # scale is now in the units of deg, i.e. scale = 1 means that one noise pixel has the size of 1x1 deg
        stimulus['stimulus_duration_in_frames'] = 120 # 1 sec
        stimulus['position'] = position# in deg        
#        analysis['type'] = 'STA'        
        params['stimulus'] = stimulus
        params['analysis'] = analysis

        # run
        CSDStimulus.present_images(params,setup)
