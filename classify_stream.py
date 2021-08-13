def classify(last_eeg_mp, valence_mp, arousal_mp, eeg_setup_phase, currently_running, n_samples, n_rows, sampling_rate, channel_names, eeg_channel_idx, use_synthetic=False):
   import time
   import numpy as np
   from pickle import load
   from utils.average_classifier import AverageXGBClassifier
   from pyeeg import bin_power
   import mne
   import pandas as pd

   mne.set_log_level(verbose='WARNING')
   bands = [(3,7), (8,13), (14, 29), (30, 47)]

   info = mne.create_info(ch_names=channel_names, sfreq=sampling_rate, ch_types='eeg')

   with open('openbci/average_classifier_valence.pkl', 'rb') as valence:
      valence_classifier = load(valence)
   with open('openbci/average_classifier_arousal.pkl', 'rb') as arousal:
      arousal_classifier = load(arousal)

   print('Starting process - waiting for EEG!')
   while True:
      with eeg_setup_phase.get_lock():
         if not eeg_setup_phase.value:
            break
      time.sleep(0.25)
   print('Done waiting for EEG!')

   while True:
      last_value = np.frombuffer(last_eeg_mp)
      last_value = np.reshape(last_value, [n_rows, n_samples])
      # last_value is in shape 14 x 1000 or so
      last_value = last_value[eeg_channel_idx]
      # last_value is in shape 4 x 1000 or so

      # old processing pipeline
      eeg_channels = last_value#[1:(len(channel_names)+1), :]
      data_channels = np.ravel([[bin_power(channel, band, Fs=sampling_rate)[0] for band in bands] for channel in eeg_channels])

      # new processing pipeline
      # cannot use automatic ICA because we don't have an EOG channel
    #  current_arr = mne.io.RawArray(last_value*1e6, info=info) # *1e6 because units of Ganglion are in micro-volts
      # Low-pass filter to remove slow drifts
      # current_arr = current_arr.filter(l_freq=1, h_freq=None, verbose='WARNING') 
      # Notch filter to remove power-line
      # current_arr = current_arr.notch_filter(freqs=50, verbose='WARNING') # 50 Hz power signal in Canada

      #eeg_data = []
      #fnames = []
      #for band in bands:
      #   this_band = current_arr.copy()
      #   this_band = this_band.filter(band[0], band[1]).to_data_frame()[channel_names]#/1e6 #undo the *1e6
      #   # this_band is in shape 4 (n channels) x 1000
      #   power = [bin_power(this_band[channel], [0, 100], Fs=sampling_rate)[0] for channel in this_band.columns]
      #   # power is in shape 4 (n channels)
      #   eeg_data.append(power)
      #   these_fnames = [str(band[0])+'-'+str(band[1])+'|' +channel for channel in this_band.columns]
      #   fnames.append(these_fnames)
   #   # eeg_data is in shape 4 (n bands) x 4 (n channels)
     # eeg_data = np.transpose(eeg_data)
      # eeg_data is in shape 4 (n channels) x 4 (n bands)

      # eeg_data is in shape 16 (n_channels x n_bands)
     # data_channels = np.ravel(eeg_data)
      # same with fnames
    #  fnames = np.ravel(np.transpose(np.asarray(fnames, dtype='object')))

      # these assert statements technically should only be run once, a bit inefficient
    #  assert np.all(valence_classifier.features_used == fnames)
    #  assert np.all(arousal_classifier.features_used == fnames)
    
      with valence_mp.get_lock():
         valence_mp.value = valence_classifier.predict_proba(np.expand_dims(data_channels, axis=0))[0]
         print('Valence: '+str(valence_mp.value))
      with arousal_mp.get_lock():
         arousal_mp.value = arousal_classifier.predict_proba(np.expand_dims(data_channels, axis=0))[0]
         print('Arousal: ' + str(arousal_mp.value))
      with currently_running.get_lock():
         if not currently_running.value:
            print('Session terminated.')
            break
      time.sleep(0.25)
