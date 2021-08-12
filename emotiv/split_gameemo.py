# %%
# Imports
from os import listdir
from os.path import join

import pandas as pd
import numpy as np
#from utils.split import split_features_and_labels

# Things associated with the GAMEEMO dataset
# The sampling rate is supposed to be 128 Hz and time time of recording 5 mins/trial, but this doesn't add up entirely correctly. I'll assume 128 Hz is correct, though.
# https://www.sciencedirect.com/science/article/pii/S1746809420301075?casa_token=5iie8DmkwPYAAAAA:6yrlBkC7QzpMnwWZV-f_lENHTpUmJKD_lSng13wureo_mzS3gwd2bEyP4NkU9IqhQRdznep4VCk
top_level = 'GAMEEMO'
electrodes = 'AF3 AF4 F3 F4 F7 F8 FC5 FC6 O1 O2 P7 P8 T7 T8'.split(' ')
sample_rate = 128

# %%
# Iterate through all of the raw EEG data and create a numpy array (a multidimensional matrix) out of the data
# There are both features and labels

all_feature_data = []
all_label_data = []

for folder in listdir(top_level):
    this_subject = []
    target = join(top_level, folder, 'Raw EEG Data')
    for subfolder in sorted(listdir(join(target, '.csv format'))):
        print(subfolder)
        data = pd.read_csv(join(target, '.csv format', subfolder)).dropna(axis='columns', how='all')

        assert list(data.columns) == electrodes
        data.insert(loc=0, column = 'ID', value=subfolder[:subfolder.find('All')])

        this_subject.append(data)
    all_feature_data.append(np.stack(this_subject))

    target = join(top_level, folder, 'SAM Ratings/labels.txt')
    data = pd.read_csv(target)
    data['Episode'] = [folder[1:-1]+x for x in data['Episode']]
    data['Subject'] = [int(x[1:3]) for x in data['Episode']]
    data['Trial'] = [int(x[4:5]) for x in data['Episode']]
    data=data.rename(columns={'Episode':'ID'})

    all_label_data.append(data)
all_feature_data = np.stack(all_feature_data)
all_label_data = np.stack(all_label_data)
# by here, the data is in the dimensionality (n_subjects x n_trials x eeg length x n_channels+1), with 14 channels + 1 trial number
print(all_feature_data.shape)
# n_subjects x n_trials x (2+1)), with the last dimension being trial number, valence, arousal
print(all_label_data.shape)

# %%
# Collapse the first two dimensions of the previous matrix, getting the number of total trials.
# Reshaped to dimensionality (n_total_trials x eeg length x (ID+n_channels))
reshaped_feature_data = np.reshape(all_feature_data, [all_feature_data.shape[0]* all_feature_data.shape[1], all_feature_data.shape[2], all_feature_data.shape[3]])
# Reshaped to dimensionality (n_total_trials x (ID, valence, arousal, subject, trial))
reshaped_label_data = np.reshape(all_label_data, [all_label_data.shape[0]*all_label_data.shape[1], all_label_data.shape[2]])

# reshaped to dimensionality (n_total_trials x n_channels x n_times)
reshaped_feature_data = np.transpose(reshaped_feature_data, [0, 2, 1])

print(reshaped_feature_data.shape)
print(reshaped_label_data.shape)

# %%
# Check to see if the features and labels correspond to the same trials (I had an issue with that before)
# and then save all the data, after removing the trial number columns.
assert(np.all(reshaped_feature_data[:, 0, 0]==reshaped_label_data[:, 0]))
#reshaped_feature_data, reshaped_label_data = split_features_and_labels(reshaped_feature_data, reshaped_feature_data, sample_rate, 5)
np.save('gameemo_features.npy', reshaped_feature_data[:, 1:].astype('float32'))
np.save('gameemo_labels.npy', reshaped_label_data[:, 1:].astype('float32'))


# %%
# Drop any labels that have negative valence/arousal (invalid)
#drop_locs = np.any(reshaped_label_data[:, 1:] <0, axis=-1)

#reshaped_feature_data = reshaped_feature_data[np.logical_not(drop_locs)]
#reshaped_label_data = reshaped_label_data[np.logical_not(drop_locs)]

# %%


