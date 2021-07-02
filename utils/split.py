from pickle import FALSE
import numpy as np

def split_features_and_labels(features, labels, sample_rate, n):
    npoints_5s = sample_rate*n
    slice_amt = int(np.floor(features.shape[2]/npoints_5s))

    splitted_feature_data = np.split(features[:, :, :slice_amt *npoints_5s], slice_amt, axis=-1)
    splitted_feature_data = np.asarray(splitted_feature_data)
    splitted_feature_data = np.reshape(splitted_feature_data, [splitted_feature_data.shape[0]*splitted_feature_data.shape[1], splitted_feature_data.shape[2], splitted_feature_data.shape[3]])

    concatenated = np.concatenate([labels for _ in range(slice_amt)])

    return splitted_feature_data, concatenated

