import numpy as np
from pyeeg import bin_power

import matplotlib.pyplot as plt
from xgboost import XGBClassifier

from sklearn.model_selection import KFold
from sklearn.metrics import classification_report, f1_score
import pandas as pd
import pickle
import os
from IPython import display

from sys import path
path.append('../')
from utils.average_classifier import *
from utils.split_features_and_labels import split_features_and_labels_interfaces

channels = "Fp1,Fp2,Fz,Cz,T3,T4,Pz,Oz".split(',')
channels_to_use = 'Fp1,Fp2,T3,T4'.split(',') 
electrodes_idx = np.asarray([channels.index(e) for e in channels_to_use])
channels = channels_to_use

sampling_rate = 250
seconds_to_predict = 5

EEG = np.load('INTERFACES/EEG_ICA.npy')
label_arousal = np.load('INTERFACES/label/arousal.npy')
label_valence = np.load('INTERFACES/label/valence.npy')

bands = ['3-7','8-13','14-29','30-47']
feature_names = np.asarray([[str(bands[x]) + '|' + e for x in range(len(bands))] for e in channels], dtype='object')
feature_names = np.ravel(feature_names)
print(feature_names)

importance_dfs = []

use_last_npy = False
feature_dump_file = 'interfaces_features_4.npy'
EEG = EEG[:, electrodes_idx]

splitted_features, splitted_labels_arousal = split_features_and_labels_interfaces(EEG, label_arousal, sampling_rate, seconds_to_predict)
splitted_features, splitted_labels_valence = split_features_and_labels_interfaces(EEG, label_valence, sampling_rate, seconds_to_predict)

if use_last_npy and os.path.exists(feature_dump_file):
    final_features = np.load(feature_dump_file)
else:
    temp_reshaped = np.reshape(splitted_features, [splitted_features.shape[0]*splitted_features.shape[1]*splitted_features.shape[2], splitted_features.shape[3]])
    powers = []
    for i, sample in enumerate(temp_reshaped):
        if i % 3000 == 0:
            print('Progress: %s' % (str(np.round(i/len(temp_reshaped), 2))))
        powers.append(bin_power(sample, [0, 999999], Fs=sampling_rate))

    powers = np.asarray(powers)
    powers = np.reshape(powers[:, 0, :], splitted_features.shape[:3])
    powers = np.reshape(powers, [powers.shape[0], powers.shape[1] * powers.shape[2]])
    final_features = powers

    final_features.dump(feature_dump_file)


importance_dfs = []
for classification_type in ['valence', 'arousal']:
    print('-------------------------------------------------------------------------')
    print(classification_type)
    final_features = powers
    if classification_type == 'valence':
        labels=splitted_labels_valence
    elif classification_type == 'arousal':
        labels=splitted_labels_arousal
    kf = KFold(n_splits=10, shuffle=True)
    i = 0
    regressors = []
    importances =[]
    all_predictions_arousal = np.zeros((final_features.shape[0], ))
    for train_index, test_index in kf.split(final_features):
        x_train = final_features[train_index]
        y_train = labels[train_index]
        x_test = final_features[test_index]
        y_test = labels[test_index]

        xgb =  XGBClassifier(eval_metric='mlogloss')
        xgb.fit(x_train, y_train)
        

        print('Fold number ' + str(i))
        y_pred = xgb.predict(x_train)
        print('Train F1: ' + str(f1_score(y_train, y_pred)))
        y_pred = xgb.predict(x_test)
        print('Test F1: ' + str(f1_score(y_test, y_pred)))
        importances.append(xgb.feature_importances_)
        all_predictions_arousal[test_index] = y_pred
        regressors.append(xgb)
        i += 1
    print(classification_report(labels,all_predictions_arousal))


    df = pd.DataFrame()
    df['feature_name'] = feature_names
    df['mean_importances'] = np.sum(np.asarray(importances), axis=0)
    df['electrode'] = [x.split('|')[1] for x in df['feature_name']]
    importance_dfs.append(df)

    average_predictor = AverageXGBClassifier(regressors, feature_names)
    print('This score should be high because of overfitting, but not low')
    print(average_predictor.predict(final_features).shape)

    print(f1_score(labels, average_predictor.predict(final_features)))
    pickle.dump(average_predictor,open('average_classifier_%s.pkl' % (classification_type), 'wb'))


importance_dfs[0].sort_values('mean_importances', ascending = False)
importance_dfs[1].sort_values('mean_importances', ascending = False)