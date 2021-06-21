# %%
from os import listdir
from os.path import join

import pandas as pd
import numpy as np
top_level = 'GAMEEMO'


electrodes = 'AF3 AF4 F3 F4 F7 F8 FC5 FC6 O1 O2 P7 P8 T7 T8'.split(' ')
sample_rate = 128
all_train_data = []
all_test_data = []

for folder in listdir(top_level):
    this_subject = []
    target = join(top_level, folder, 'Raw EEG Data')
    for subfolder in sorted(listdir(join(target, '.csv format'))):
        print(subfolder)
        data = pd.read_csv(join(target, '.csv format', subfolder)).dropna(axis='columns', how='all')

        assert list(data.columns) == electrodes
        data['ID'] = subfolder[:subfolder.find('All')]
        this_subject.append(data)
    all_train_data.append(np.stack(this_subject))

    target = join(top_level, folder, 'SAM Ratings/labels.txt')
    data = pd.read_csv(target)
    data['Episode'] = [folder[1:-1]+x for x in data['Episode']]
    data=data.rename(columns={'Episode':'ID'})

    all_test_data.append(data)
all_train_data = np.stack(all_train_data)
all_test_data = np.stack(all_test_data)

# The sampling rate is supposed to be 128 Hz and time time of recording 5 mins/trial, but this doesn't add up entirely correctly. I'll assume 128 Hz is correct, though.
# https://www.sciencedirect.com/science/article/pii/S1746809420301075?casa_token=5iie8DmkwPYAAAAA:6yrlBkC7QzpMnwWZV-f_lENHTpUmJKD_lSng13wureo_mzS3gwd2bEyP4NkU9IqhQRdznep4VCk
# by here, the data is in the dimensionality (n_subjects x n_trials x eeg length x n_channels)
print(all_train_data.shape)
# n_subjects x n_trials x (trial number, valence, arousal)
print(all_test_data.shape)

# The sampling rate is supposed to be 128 Hz and time time of recording 5 mins/trial, but this doesn't add up entirely correctly. I'll assume 128 Hz is correct, though.
# https://www.sciencedirect.com/science/article/pii/S1746809420301075?casa_token=5iie8DmkwPYAAAAA:6yrlBkC7QzpMnwWZV-f_lENHTpUmJKD_lSng13wureo_mzS3gwd2bEyP4NkU9IqhQRdznep4VCk
# by here, the data is in the dimensionality (n_subjects x n_trials x eeg length x n_channels)
print(all_train_data.shape)
# n_subjects x n_trials x (trial number, valence, arousal)
print(all_test_data.shape)
# %%
# Reshaped to dimensionality (n_total_trials x eeg length x n_channels)
reshaped_train_data = np.reshape(all_train_data, [all_train_data.shape[0]* all_train_data.shape[1], all_train_data.shape[2], all_train_data.shape[3]])
# Reshaped to dimensionality (n_total_trials x 2(valence, arousal))
reshaped_test_data = np.reshape(all_test_data, [all_test_data.shape[0]*all_test_data.shape[1], all_test_data.shape[2]])

# reshaped to dimensionality (n_total_trials x n_channels x n_times)
reshaped_train_data = np.transpose(reshaped_train_data, [0, 2, 1])

print(reshaped_train_data.shape)
print(reshaped_test_data.shape)


# %%
drop_locs = np.any(reshaped_test_data[:, 1:] <0, axis=-1)

reshaped_train_data = reshaped_train_data[np.logical_not(drop_locs)]
reshaped_test_data = reshaped_test_data[np.logical_not(drop_locs)]

npoints_5s = sample_rate*10
slice_amt = int(np.floor(reshaped_train_data.shape[2]/npoints_5s))

splitted_train_data = np.split(reshaped_train_data[:, :, :slice_amt *npoints_5s], slice_amt, axis=-1)
splitted_train_data = np.asarray(splitted_train_data)
splitted_train_data = np.reshape(splitted_train_data, [splitted_train_data.shape[0]*splitted_train_data.shape[1], splitted_train_data.shape[2], splitted_train_data.shape[3]])
print(splitted_train_data.shape)

#repeated_test_data = np.repeat(reshaped_test_data, slice_amt, axis=0)
#print(repeated_test_data.shape)



# %%
#print(splitted_train_data[:, -1, 0].tolist())
concatenated = np.concatenate([reshaped_test_data for _ in range(slice_amt)])

assert(np.all(concatenated[:, 0]==splitted_train_data[:, -1, 0]))
np.save('eeg_splitted_features.npy', splitted_train_data[:, :-1].astype('float32'))
np.save('eeg_splitted_labels.npy', concatenated[:, 1:].astype('float32'))

# %%
