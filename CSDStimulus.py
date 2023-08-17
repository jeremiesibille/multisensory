# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 08:28:24 2018

@author: AGKremkow
"""
# %%
from psychopy import visual
import numpy as np
import time
import OurSetup 

# %%
def present_images(params,setup):
     # %% we create some filenames, the tmp is used for the communication with the stimulus pc. the save for saving ... haha 
    filename_save = OurSetup.generate_filename_and_make_folders(params)
    # %% Create window
    win = setup['win']
    trigger = setup['trigger']
    background_color = params['monitor']['background']
    background_color
    win.setRGB(background_color)
    win.flip()
    #win,trigger = OurSetup.OpenScreen(background_color,monitor_distance)
    trigger.Stimulus_Start()
     # we present background for few second such that the retina can adapt
    onset_adaptation_time_sec = params['stimulus']['onset_adaptation_time_sec']
    onset_adaptation_time_frames = int(np.round(onset_adaptation_time_sec * 120))
    OurSetup.present_pause(onset_adaptation_time_frames,win)
    # %% generate images
    scale = params['stimulus']['scale']
    position = params['stimulus']['position']
    position = position*-1. # because ofthe funcky flipping of the axis
    stimulus_duration_in_frames = params['stimulus']['stimulus_duration_in_frames']
    # %%
    np.random.seed(1675)
    
    xn = 40
    yn = 40
    
    checker = np.random.randint(2,size=(xn,yn)).astype(float)
    checker *= 2.
    checker -= 1.
    
    checker_inverse = checker*-1.
    # %%
    #n_frames = stimulus_frames.shape[2]
    stim_size = np.array([xn,yn]).astype('float')
    #images = {}
    image_checker = visual.ImageStim(win,checker,size=stim_size*scale,pos=position)
    image_checker_inverse = visual.ImageStim(win,checker_inverse,size=stim_size*scale,pos=position)
    # %%   
    
    # we save the params
    if not params['test']:
        # we save the params in the folder, always needed. Just in test maybe not
        np.save(filename_save,params)
        # we wait for the online analysis
        if params['closed_loop_with_analysis']:
            OurSetup.write_current_params_and_wait_for_go(params)
    
    # we present some text outside the screen to get the system up and running
    OurSetup.present_pause(120,win,trigger)# in frames    
    
    for trial in range(int(params['stimulus']['trials'])):
        # on even trials we present checker, on odds checker inverse
        if np.mod(trial,2) == 0: # even 
            image = image_checker
        else:
            image = image_checker_inverse
                
        # present images
        for flipN in range(stimulus_duration_in_frames):
            image.draw()
            win.flip()
            #raw_input()
            if flipN == 0:
                trigger.FrameTime()
#            trigger.EyeCamera()
    # done
    # we flip one more time to make the screen gray
    win.flip()
    OurSetup.present_pause(360,win,trigger)# in frames
    
    # %%
    #OurSetup.present_pause(240,win)# in frames
    
    trigger.Stimulus_Stop()
    #win.close()



def present_images_with_first_frame_trigger(stimulus_frames,params,setup):
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
     # we present background for few second such that the retina can adapt
    onset_adaptation_time_sec = params['stimulus']['onset_adaptation_time_sec']
    onset_adaptation_time_frames = int(np.round(onset_adaptation_time_sec * 120))
    OurSetup.present_pause(onset_adaptation_time_frames,win)
    # %% generate images
    scale = params['stimulus']['scale']
    position = params['stimulus']['position']
    stimulus_duration_in_frames = params['stimulus']['stimulus_duration_in_frames']
    n_frames = stimulus_frames.shape[2]
    stim_size = np.array([stimulus_frames.shape[1],stimulus_frames.shape[0]]).astype('float')
    images = {}
    for frameN in range(n_frames):
        images[str(frameN)]=visual.ImageStim(win,stimulus_frames[:,:,frameN],size=stim_size*scale,pos=position)
    # %%
    
    # we save the params
    if not params['test']:
        # we save the params in the folder, always needed. Just in test maybe not
        np.save(filename_save,params)
        # we wait for the online analysis
        if params['closed_loop_with_analysis']:
            OurSetup.write_current_params_and_wait_for_go(params)
            
    
    for trial in range(params['stimulus']['trials']):
        # we present some text outside the screen to get the system up and running
        OurSetup.present_pause(120,win)# in frames
        # present images
        for frameN in range(n_frames):
            for flipN in range(stimulus_duration_in_frames):
                images[str(frameN)].draw()
                win.flip()
                if frameN == 0:
                    trigger.FrameTime()
        # we flip one more time to make the screen gray
        win.flip()
        OurSetup.present_pause(360,win)# in frames
    
    # %%
    #OurSetup.present_pause(240,win)# in frames
    
    trigger.Stimulus_Stop()



def present_images_with_delay(stimulus_frames,scale,frame_durations,delay_duration,position,background_color,n_protocol,monitor_distance):
    # open screen
    win,trigger = OurSetup.OpenScreen(background_color,monitor_distance)
    trigger.Stimulus_Start()
    
    # %% generate images
    n_frames = stimulus_frames.shape[2]
    stim_size = np.array([stimulus_frames.shape[1],stimulus_frames.shape[0]]).astype('float')
    images = {}
    for frameN in range(n_frames):
        images[str(frameN)]=visual.ImageStim(win,stimulus_frames[:,:,frameN],size=stim_size*scale,pos=position)
    
    
    # protocol
    for k in range(n_protocol):
        trigger.triggger_protocol()
        time.sleep(0.1)
       
    n_trials = 1
    
    stim=visual.TextStim(win)
    countdown = 20*2
    for i in range(countdown):
        stim.text = str(countdown-i)
        stim.pos = [0,0]
        stim.draw()
        win.flip()
    
    # present images
    for ti in range(n_trials):
        for stim_n in range(len(frame_durations)):
            frame_duration = frame_durations[stim_n]
            for flipN in range(frame_duration):
                images[str(frameN)].draw()
                win.flip()
                if flipN == 0:
                    trigger.FrameTime()
        # after we have presented the stimulus we will wait a for the duration o delay. we have to present something for reliable frames
        for i in range(delay_duration):
            stim.text = 'delay'
            stim.pos = [-2000,0] # should not be visible
            stim.draw()
            win.flip()
    
    # we flip one more time to make the screen gray
    win.flip()
    
    # %%
    trigger.Stimulus_Stop()
    #win.close()



def present_images_with_delay_lr(stimulus_frames,scale,frame_duration,position,background_color,n_protocol,delay_duration,monitor_distance):
    # open screen
    win,trigger = OurSetup.OpenScreen(background_color,monitor_distance)
    trigger.Stimulus_Start()
    
    # %% generate images
    n_frames = stimulus_frames.shape[2]
    stim_size = np.array([stimulus_frames.shape[1],stimulus_frames.shape[0]]).astype('float')
    images = {}
    for frameN in range(n_frames):
        images[str(frameN)]=visual.ImageStim(win,stimulus_frames[:,:,frameN],size=stim_size*scale,pos=position)
    
    
    # protocol
    for k in range(n_protocol):
        trigger.triggger_protocol()
        time.sleep(0.1)
       
    n_trials = 1
    
    stim=visual.TextStim(win)
    countdown = 20*2
    for i in range(countdown):
        stim.text = str(countdown-i)
        stim.pos = [0,0]
        stim.draw()
        win.flip()
    
    # present images
    for ti in range(n_trials):
        for frameN in range(n_frames):
            
            for flipN in range(frame_duration):
                images[str(frameN)].draw()
                win.flip()
                if flipN == 0:
                    trigger.FrameTime()
            # after we have presented the stimulus we will wait a for the duration o delay. we have to present something for reliable frames
            for i in range(delay_duration):
                stim.text = 'delay'
                stim.pos = [-2000,0] # should not be visible
                stim.draw()
                win.flip()
    # we flip one more time to make the screen gray
    win.flip()
    stop_duration = 500
    for i in range(stop_duration):
                stim.text = 'delay'
                stim.pos = [-2000,0] # should not be visible
                stim.draw()
                win.flip()
    
    # %%
    trigger.Stimulus_Stop()
    #win.close()