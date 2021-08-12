import numpy as np
class AverageXGBClassifier(object):
    def __init__(self, classifiers, features_used):
        self.classifiers = classifiers
        self.features_used = features_used
    def predict_proba(self, x):
        predictions = np.mean([xgb.predict_proba(x)[:, 1] for xgb in self.classifiers], axis=0)
        return predictions
    def predict(self, x):
        return np.round(self.predict_proba(x)).astype(np.int32)