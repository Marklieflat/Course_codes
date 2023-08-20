#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 13:04:11 2023

@author: rnd
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from imblearn.over_sampling import SMOTE
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

def addfeature(df):
    if df['feature_4'] <= 30:
        df['feature_5'] = 0
    else:
        df['feature_5'] = 1
    return df

train = pd.read_csv('train.csv')
train = train.apply(addfeature, axis = 1)
train = train[['feature_1','feature_2','feature_3','feature_4','feature_5','label','example_id']]
test = pd.read_csv('test.csv')

X = train.iloc[:, :5].to_numpy()
y = train.iloc[:, 5].to_numpy()

smo = SMOTE(random_state=2023, k_neighbors=5, n_jobs = -1)
X_res, y_res = smo.fit_resample(X, y)

#%%
params = {'base_estimator__max_depth': [5,6,7,8,9,10], 'base_estimator__min_samples_split': [2,3,4,5,6,7],
          'n_estimators': [50,60,70,80,90,100], 'learning_rate':[0.5,0.7,0.8,1]}
weakclf = DecisionTreeClassifier()
ada = AdaBoostClassifier(base_estimator = weakclf)
grid = GridSearchCV(ada, params, cv = 5, n_jobs = -1)
grid.fit(X_res, y_res)
print(grid.best_score_)
print(grid.best_params_)
print(grid.best_estimator_)

weakclf = DecisionTreeClassifier(max_depth = 5, min_samples_split = 2)
ada = AdaBoostClassifier(base_estimator = weakclf, n_estimators=50, learning_rate = 1)
ada.fit(X_res, y_res)

#Testing on additional dataset
add_test = pd.read_csv('augmented_test.csv')
add_test = add_test.apply(addfeature, axis = 1)
add_test = add_test[['feature_1','feature_2','feature_3','feature_4','feature_5','example_id']]
add_X_test = add_test.iloc[:, :5].to_numpy()
add_y_pred = ada.predict(add_X_test)
add_df_y_pred = pd.DataFrame(add_y_pred, columns = ['prediction'])
add_test_new = pd.concat([add_test, add_df_y_pred], axis = 1)
add_test_final = add_test_new.iloc[:, 5:]
add_test_final.to_csv('addition_120090651.csv',  index = False)

#%%
X_res = X_res[:, :4]
params = {'base_estimator__C': [1,2,3,4,5], 'base_estimator__kernel': ['linear', 'poly', 'rbf', 'sigmoid'], 
          'base_estimator__gamma' : [0.1, 0.5, 1, 1.5, 2,2.5,3]}
weakclf = SVC()
ada = AdaBoostClassifier(base_estimator = weakclf, algorithm='SAMME')
grid = GridSearchCV(ada, params, cv = 5, n_jobs = -1)
grid.fit(X_res, y_res)
print(grid.best_score_)
print(grid.best_params_)
print(grid.best_estimator_)

X_res = np.log(X_res)
scaler = StandardScaler()
scaler.fit(X_res)
X_res = scaler.transform(X_res)

X_test = test.iloc[:, :4].to_numpy()
X_test = np.log(X_test)
scaler = StandardScaler()
scaler.fit(X_test)
X_test = scaler.transform(X_test)

weakclf = SVC(C=5, gamma=2.5, kernel='poly')
ada = AdaBoostClassifier(base_estimator = weakclf, algorithm='SAMME', n_estimators=100, learning_rate = 0.1)
ada.fit(X_res, y_res)
# Testing on Kaggle testset
y_pred = ada.predict(X_test)
df_y_pred = pd.DataFrame(y_pred, columns = ['prediction'])
test_new = pd.concat([test, df_y_pred], axis = 1)
test_final = test_new.iloc[:, 4:]
test_final.to_csv('prediction.csv',  index = False)




