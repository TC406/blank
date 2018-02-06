#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 10:43:27 2018

@author: di
"""

import scipy.signal as sig
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile as wav

def events_time(max_val, freq, time, spect, ref_spectrum=None):
    """
    This function is detects events. Event maybe begin, or end of the signal.
    Algorythm based on spectrum comparison 
    in each window. It takes spectrum fromm first window as reference. Then if
    it detect difference in spectrum bigger than max_val, it record it to 
    events_time and current spectrum becomes reference.
    
    Parameters:
        
        max_val: float. sensivity of detection. It measure in parrots.
        
        freq: array of frequencies. It is output from 
              scipy.signal.spectrogramm.
        
        time: time array of windows. It is output from 
              scipy.signal.spectrogram.
        
        spect: Spectrogramm two dimensional array. It is output from 
               scipy.signal.spectrogram.
        
        ref_spectrum: array with same shape as freq. It is amplitude spectrum
                      that will be set up as reference.
    
    Returns:
        
        events_time: array with time, in which event started.
        
        ref spectrum: array with same dimension as freq array. It contains
                      last event reference  spectrum.
    
    
    """
    events_time=[]
    sz=time.shape[0]
    fshape=freq.shape[0]
    curr_ind=1
    if ref_spectrum is None:
        events_time.append(0)
        ref_spectrum=spect[:,0].reshape([fshape,1])
    
    iter_count=0
    while(curr_ind<sz-2):
        sub_arr=ref_spectrum.reshape([fshape,1]) * np.ones( [fshape, sz-curr_ind] )
        next_ind=np.argmax( np.sum(abs(spect[:,curr_ind:] - sub_arr),
                                   axis=0)>max_val )
        if next_ind<3 :
            next_ind=1
            if (np.sum(abs(spect[:,curr_ind:] - sub_arr)) < max_val/100):
                break
        else:
            events_time.append(time[curr_ind + next_ind ])
        curr_ind+=np.copy(next_ind)
        #print(iter_count, curr_ind, next_ind, np.sum(abs(ref_spectrum - spect[:,curr_ind-1])))
        #if next_ind>1:
            #print (time[curr_ind])
        iter_count+=1
        ref_spectrum=np.copy(spect[:,curr_ind])
    return events_time, ref_spectrum


test_long='test_long.wav'
test_knock='test.wav'
hlopki1='1.wav'
hlopki2='2.wav'
hlopki3='3.wav'
test_name=hlopki3


sampl_freq, data = wav.read(test_name)

