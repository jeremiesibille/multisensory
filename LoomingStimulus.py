# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 07:17:58 2018

@author: AGKremkow
"""

# this code presents a looming stimulus
# %%
import numpy as np
from psychopy import visual, monitors
import OurSetup

# %%
def run_stimulus(params,setup):
     # %% we create some filenames, the tmp is used for the communication with the stimulus pc. the save for saving ... haha 
    filename_save = OurSetup.generate_filename_and_make_folders(params)
    # %% Create window
    win = setup['win']
    trigger = setup['trigger']
    background_color = params['monitor']['background']
    win.setRGB(background_color)
    win.flip()
    #win,trigger = OurSetup.OpenScreen(background_color,monitor_distance)
    trigger.Stimulus_Start()
    
    refreshrate = params['monitor']['refreshrate']
     # we present background for few second such that the retina can adapt
    onset_adaptation_time_sec = params['stimulus']['onset_adaptation_time_sec']
    onset_adaptation_time_frames = int(np.round(onset_adaptation_time_sec * refreshrate))
    OurSetup.present_pause(onset_adaptation_time_frames,win)
    # %%
    stimulus_speed = params['stimulus']['speeds']
    stimulus_luminance = params['stimulus']['luminances']
    n_trials = params['stimulus']['trials']
    
    [all_speeds,all_luminances] = np.meshgrid(stimulus_speed,stimulus_luminance)
    
    all_speeds = all_speeds.flatten()
    all_luminances = all_luminances.flatten()
    
    
    
    # %% we randomize the sequenze
    np.random.seed(1675) # this is to have always the same random sequence. However, we need to save the sequence to a file because when we change the parameters the sequences changes
    
    speed_sequence = []
    luminance_sequence = []
    
    for t in range(n_trials):
        rand_ind = np.random.permutation(len(all_speeds))
        tmp_speed = all_speeds[rand_ind]
        tmp_luminance = all_luminances[rand_ind]
    
        speed_sequence = np.concatenate((speed_sequence,tmp_speed),axis=0)
        luminance_sequence = np.concatenate((luminance_sequence,tmp_luminance),axis=0)
        
        
    sequence = {}
    sequence['speeds'] = speed_sequence
    sequence['luminances'] = luminance_sequence
    params['stimulus']['sequence'] = sequence
    
#    #local save for PSTH analysis
#    path_to_save =  'D:/Neuropixel-Stim-computer-20190509/Visual-Stimuli-Neuropixel/VisualStimuli/stimuli/'
#    np.save(path_to_save + 'loooming_80trials.npy',params)
    # params['stimulus']['speed_sequence'] = speed_sequence
    # params['stimulus']['luminance_sequence'] = luminance_sequence
    
    # we save the params
    if not params['test']:
        # we save the params in the folder, always needed. Just in test maybe not
        np.save(filename_save,params)
        # we wait for the online analysis
        if params['closed_loop_with_analysis']:
            OurSetup.write_current_params_and_wait_for_go(params)
    
    # %%
    duration_sec = 0.5
    duration_frames = int(np.round(duration_sec*refreshrate))
    
    
    # %% looping to plot the stimulis    
    triggercount = 0
    
    # %%
    for i in range(len(speed_sequence)):
#        line=visual.Circle(win, radius=5, edges=32)#np.ones((1,1))*lum_ori,size=(width_ori,length),ori=tmp_orientations[indxcondition]*360./(np.pi*2),pos=(local_center_x,local_center_y))
        # print(indxcondition)
        # trigger.FrameTime()
        #win.flip() 
        #factor=1
        #time.sleep(1.)
        #if speed_sequence[i] == 2:
        #    factor = 10
        #if speed_sequence[i] == 10:
        #    factor = 2
        #if speed_sequence[i] == 20:
         #   factor = 1
        tmp_speed = speed_sequence[i] # this is in deg / sec
        d_speed_frame = tmp_speed/refreshrate
        
        tmp_luminance = luminance_sequence[i]
        
        max_size = params['stimulus']['max_size']
        duration_frames = int(np.round(max_size/d_speed_frame))
        
        OurSetup.present_pause(240,win)
        circle = visual.Circle(win, radius=0., edges=64, lineColor=[tmp_luminance,tmp_luminance,tmp_luminance], fillColor=tmp_luminance, units='deg') #
        for frameN in range(duration_frames): 
            circle.radius = circle.radius + d_speed_frame
            circle.draw()
            win.flip()
            # you have to send the trigger after a monitor flip!!!
            if frameN == 0:
                trigger.FrameTime()
                triggercount += 1
                print(triggercount)
                
        OurSetup.present_pause(240,win)
    # %%
    trigger.Stimulus_Stop()
    #win.close()