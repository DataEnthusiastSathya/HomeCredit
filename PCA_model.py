# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 20:14:54 2018

@author: SK056042
"""

import pandas as pd
from pandas import read_csv 
import os
import math
import numpy as np
import statistics
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import seaborn as sns
sns.set()
plt.rcParams["figure.figsize"] = [16,9]
  

os.chdir("C:/Users/SK056042/Desktop/Kaggle/Home Credit")

data_train=read_csv("application_train.csv")

data_test=read_csv("application_test.csv")
bureau=read_csv("bureau.csv")
bureau_balance=read_csv("bureau_balance.csv")
install_pay=read_csv("installments_payments.csv")
POS=read_csv("POS_CASH_balance.csv")
previous=read_csv("previous_application.csv")

previous[previous['SK_ID_PREV']==1071426]
install_pay[install_pay['SK_ID_PREV']==1071426].to_csv("1461079.csv")


install_pay.head()
previous.head()
inst=install_pay[['SK_ID_CURR','SK_ID_PREV','NUM_INSTALMENT_NUMBER']]
#(13605401, 3)

inst1=inst.drop_duplicates()
#(12861994, 3)

inst2=install_pay[['SK_ID_CURR','SK_ID_PREV','NUM_INSTALMENT_NUMBER','AMT_INSTALMENT']]
inst3=inst2.drop_duplicates()


AMT_INS=install_pay[['SK_ID_CURR','SK_ID_PREV','NUM_INSTALMENT_NUMBER','AMT_INSTALMENT']]
AMT_INS=AMT_INS.sort_values(['SK_ID_CURR','SK_ID_PREV','NUM_INSTALMENT_NUMBER'])
AMT_INS=AMT_INS.drop_duplicates()
AMT_INS=AMT_INS.groupby(['SK_ID_CURR','SK_ID_PREV','NUM_INSTALMENT_NUMBER']).agg('sum')
AMT_INS.shape
AMT_INS=AMT_INS.reset_index()
AMT_PAY=install_pay[['SK_ID_CURR','SK_ID_PREV','NUM_INSTALMENT_NUMBER','AMT_PAYMENT']]
AMT_PAY=AMT_PAY.sort_values(['SK_ID_CURR','SK_ID_PREV','NUM_INSTALMENT_NUMBER'])
AMT_PAY=AMT_PAY.drop_duplicates()
AMT_PAY=AMT_PAY.groupby(['SK_ID_CURR','SK_ID_PREV','NUM_INSTALMENT_NUMBER']).agg('sum')
AMT_PAY.shape
AMT_PAY=AMT_PAY.reset_index()

Merged=AMT_PAY.merge(AMT_INS,how='left',on=['SK_ID_CURR','SK_ID_PREV','NUM_INSTALMENT_NUMBER'])
Merged['Remaining']=Merged['AMT_INSTALMENT']-Merged['AMT_PAYMENT']
len(Merged[Merged['Remaining']>0])#72592../78839
len(Merged[Merged['Remaining']>2])#5127

len(Merged[Merged['Remaining']<0])#158422../72715
len(Merged[Merged['Remaining']<-2])#243
len(Merged[Merged['Remaining']<-10])#243

len(Merged[Merged['Remaining']==0])#12628090../12707550
####Inspect into the above 2 out of three categories)
Merged['Remaining'].min()
Merged['Remaining'].max()

Rem=Merged[Merged['Remaining'].notnull()==True].Remaining
Rem=Rem.sort_values(ascending=True)

Rem1=Merged[(Merged['Remaining'].notnull()==True) & (Merged['Remaining']!=0)].Remaining
#Rem2-Only non zero values, not close to zero also
Rem2=Merged[(Merged['Remaining'].notnull()==True) & (Merged['Remaining']!=0) & ((Merged['Remaining']<-1) | (Merged['Remaining'] >1))].Remaining

#Rem1=Merged[(Merged['Remaining'].notnull()==True) & (Merged['Remaining']!=0)].Remaining
# values=-41434.29 is an error and should be zero, SK_ID_PREV=2311125
#Merged1=Merged

Merged.iloc[Merged[Merged['Remaining']<-2].index,5]=0

Rem.head(20)
Out[237]: 
11366232   -818842.50   2060229 # this guy paid in the first installment
634655     -125640.00
5291769     -41434.29
5291806     -41434.29
5291807     -41434.29
5291774     -41434.29
5291764     -41434.29
5291808     -41434.29
5291778     -41434.29
5291768     -41434.29
5291792     -41434.29
5291767     -41434.29
5291766     -41434.29
5291791     -41434.29
5291790     -41434.29
5291789     -41434.29
5291788     -41434.29
5291770     -41434.29
5291787     -41434.29
5291786     -41434.29

Rem.tail(20)
Out[238]: 
6616822      59284.575
6211475      59436.855
10630806     60071.805
861596       60098.895
10645335     60180.930
6740892      63736.290
2302031      65913.975
8662802      67534.920
7235451      70378.875
1196960      70975.215
4045742      74198.880
9209793      81494.820
10637181     85158.000
99193        89566.920
7242983      92547.720
1576939      94087.620
2817133      94150.260
4443352      96734.070
5270549     101790.000
8301561     128824.425


# Features to be extracted:
1. Number of Previous loans
2. Number of Installments
3. Number of Installments pending
4. Total amount loan taken- Mean,median
5. Total amount paid back-Mean,median
6. Remaining Amount-sum, average
7. Remaning amount/ number of installments

1. Calculate the rate of interest from the previous data: (CNT_PAYMENT*AMT_ANNUITY - AMT_CREDIT)/AMT_CREDIT

In line 266, there are 243 people who have payed more than 2 dollars extra..kindly introspect.
Replace all the extra payments with zero. No one paid extra(apart from 262837
). Data cleaning.
-------------------------------------
# Installment Dates study

1. Number of Late Payments
2. Total number of days, where payment was late




DATE_INS=install_pay[['SK_ID_CURR','SK_ID_PREV','NUM_INSTALMENT_NUMBER','DAYS_INSTALMENT','DAYS_ENTRY_PAYMENT']]
DATE_INS=DATE_INS.sort_values(['SK_ID_CURR','SK_ID_PREV','NUM_INSTALMENT_NUMBER'],ascending=True)

DATE_INS['DAYS_INSTALMENT']=DATE_INS['DAYS_INSTALMENT']*-1
DATE_INS['DAYS_ENTRY_PAYMENT']=DATE_INS['DAYS_ENTRY_PAYMENT']*-1

DATE_INS['DAYS_PAID_BEFORE']=DATE_INS['DAYS_ENTRY_PAYMENT']-DATE_INS['DAYS_INSTALMENT']
DATE_INS['PAID_BEFORE_FLAG']=DATE_INS['DAYS_PAID_BEFORE'].apply(lambda x: "Yes" if x >= 0 else "No")
------------------------------------------------------
#Aggregating
NUM_PREV=DATE_INS[['SK_ID_CURR','SK_ID_PREV']]
NUM_PREV=NUM_PREV.groupby('SK_ID_CURR').agg('count')
NUM_PREV=NUM_PREV.reset_index() #NUM_PREV.shape-339587

NUM_INS=DATE_INS[['SK_ID_CURR','NUM_INSTALMENT_NUMBER']]
NUM_INS=NUM_INS.groupby('SK_ID_CURR').agg('count')
NUM_INS=NUM_INS.reset_index() #NUM_PREV.shape-339587

LAST_INS=DATE_INS[['SK_ID_CURR','DAYS_INSTALMENT']]
LAST_INS=LAST_INS.groupby('SK_ID_CURR').agg('min')
LAST_INS=LAST_INS.reset_index() #NUM_PREV.shape-339587

LAST_PAID=DATE_INS[['SK_ID_CURR','DAYS_ENTRY_PAYMENT']]
LAST_PAID=LAST_PAID.groupby('SK_ID_CURR').agg('min')
LAST_PAID=LAST_PAID.reset_index() #NUM_PREV.shape-339587


---------------------------------------------------------------------------

TOTAL_INS=Merged[['SK_ID_CURR','AMT_INSTALMENT']]
TOTAL_INS=TOTAL_INS.groupby('SK_ID_CURR').agg('sum')
TOTAL_INS=TOTAL_INS.reset_index() #NUM_PREV.shape-339587

TOTAL_PAID=Merged[['SK_ID_CURR','AMT_PAYMENT']]
TOTAL_PAID=TOTAL_PAID.groupby('SK_ID_CURR').agg('sum')
TOTAL_PAID=TOTAL_PAID.reset_index() #NUM_PREV.shape-339587

--------------------------------------------------------------------------

insta=install_pay.sort_values(['SK_ID_CURR','SK_ID_PREV','NUM_INSTALMENT_NUMBER'],ascending=True)


inst=insta[['SK_ID_CURR','SK_ID_PREV','NUM_INSTALMENT_VERSION']]
inst1=inst.groupby(['SK_ID_CURR','SK_ID_PREV']).agg('nunique')
inst1=inst1['NUM_INSTALMENT_VERSION']
inst1=inst1.reset_index()
inst1=inst1[['SK_ID_CURR','NUM_INSTALMENT_VERSION']]
inst1=inst1.groupby('SK_ID_CURR').agg('sum')
inst1=inst1.reset_index()
------------------------------------------------------

FINAL_AGG=NUM_PREV.merge(NUM_INS, on='SK_ID_CURR')
FINAL_AGG=FINAL_AGG.merge(LAST_INS,on='SK_ID_CURR')
FINAL_AGG=FINAL_AGG.merge(LAST_PAID,on='SK_ID_CURR')
FINAL_AGG=FINAL_AGG.merge(TOTAL_INS,on='SK_ID_CURR')
FINAL_AGG=FINAL_AGG.merge(TOTAL_PAID,on='SK_ID_CURR')
FINAL_AGG=FINAL_AGG.merge(inst1,on='SK_ID_CURR')

FINAL_AGG['AVG_PAY']=FINAL_AGG['AMT_PAYMENT'] / FINAL_AGG['NUM_INSTALMENT_NUMBER']
FINAL_AGG['AVG_INS']=FINAL_AGG['AMT_INSTALMENT'] / FINAL_AGG['NUM_INSTALMENT_NUMBER']

FINAL_AGG.isnull().sum()
FINAL_AGG=FINAL_AGG.fillna(0)

data_train1=data_train.merge(FINAL_AGG,how='left',on='SK_ID_CURR')
#columns=['SK_ID_CURR', 'SK_ID_PREV', 'NUM_INSTALMENT_NUMBER', 'DAYS_INSTALMENT',
 #      'DAYS_ENTRY_PAYMENT', 'AMT_INSTALMENT', 'AMT_PAYMENT', 'AVG_PAY',
  #     'AVG_INS', 'NUM_INSTALMENT_VERSION'],

data_train[~data_train['SK_ID_CURR'].isin(FINAL_AGG['SK_ID_CURR'])].SK_ID_CURR.nunique()
#15868
There are 15 k records with no previous installment records, hence converting NAN to zero

data_train1.iloc[:,122:131]=data_train1.iloc[:,122:131].fillna(0)


data_train2=pd.get_dummies(data_train1)
data_train2=data_train2.fillna(0)

Target=data_train2['TARGET']
Train=data_train2.drop('TARGET', axis=1)

train_features, test_features, train_labels, test_labels = train_test_split(Train, Target, test_size = 0.25, random_state = 42)

print('Training Features Shape:', train_features.shape)
print('Training Labels Shape:', train_labels.shape)
print('Testing Features Shape:', test_features.shape)
print('Testing Labels Shape:', test_labels.shape)


feature=train_features
feature_list = list(Train.columns)
feature=np.array(train_features)

# Convert to numpy array
#features = np.array(features)


from sklearn.ensemble import RandomForestClassifier
# Instantiate model with 1000 decision trees
rf = RandomForestClassifier(n_estimators = 1000,verbose=1, random_state = 42)
# Train the model on training data
rf.fit(train_features, train_labels);

predictions_train = rf.predict(train_features)

predictions = rf.predict(test_features)

--------------------


importances = list(rf.feature_importances_)
# List of tuples with variable and importance
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
# Print out the feature and importances 
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];


------------------



errors = abs(predictions - test_labels)
mape = 100 * (errors / test_labels)
# Calculate and display accuracy
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')

sklearn.metrics.confusion_matrix(y_true, y_pred, labels=None, sample_weight=None)

confusion_matrix(train_labels,predictions_train)
confusion_matrix(test_labels,predictions)

#classical case of overfitting

rf1 = RandomForestClassifier(n_estimators = 1500,verbose=1, random_state = 42,min_samples_split=20)
rf1.fit(train_features, train_labels);

predictions_train = rf1.predict(train_features)

predictions = rf1.predict(test_features)

errors = abs(predictions - test_labels)
mape = 100 * (errors / test_labels)
# Calculate and display accuracy
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')

sklearn.metrics.confusion_matrix(y_true, y_pred, labels=None, sample_weight=None)

confusion_matrix(train_labels,predictions_train)
confusion_matrix(test_labels,predictions)
#Overall accuracy is good with Random forest , but precision is not good
-----------------------------------------------------------

from xgboost import XGBClassifier
import xgboost as xgb
from sklearn.metrics import accuracy_score

xgbmodel = XGBClassifier(n_estimators=500,learning_rate=0.01, max_depth=5)
xgbmodel.fit(train_features, train_labels)

pred_train = xgbmodel.predict(train_features)

pred1 = xgbmodel.predict(test_features)

confusion_matrix(train_labels,pred_train)
confusion_matrix(test_labels,pred1)


parameters = {'nthread':[4], #when use hyperthread, xgboost may become slower
              'objective':['binary:logistic'],
              'learning_rate': [0.05], #so called `eta` value
              'max_depth': [6],
              'min_child_weight': [11],
              'silent': [1],
              'subsample': [0.8],
              'colsample_bytree': [0.7],
              'n_estimators': [500], #number of trees, change it to 1000 for better results
              'missing':[-999],
              'seed': [1337]}

grid = GridSearchCV(xgbmodel, parameters, n_jobs=5, 
                   scoring='roc_auc',
                   verbose=2, refit=True)

grid_result = grid.fit(train_features, train_labels)



data_train2.head()
data_train2.columns

--------------------------------------------------------
#PCA approach
from sklearn.preprocessing import StandardScaler
x = data_train2.values

x = StandardScaler().fit_transform(x)

from sklearn.decomposition import PCA
pca = PCA(n_components=254)
principalComponents = pca.fit_transform(x)
var= pca.explained_variance_ratio_

#Cumulative Variance explains
var1=np.cumsum(np.round(pca.explained_variance_ratio_, decimals=4)*100)

plt.plot(var1)

# consider the top 150 components as it cross >80% vriance
-----------------------------------------------------

from imblearn.over_sampling import SMOTE
from sklearn.pipeline import make_pipeline
from imblearn.pipeline import make_pipeline as make_pipeline_imb
classifier = RandomForestClassifier

smote_pipeline = make_pipeline_imb(SMOTE(random_state=4), classifier(min_samples_split=25,n_estimators=700,random_state=42))
smote_model = smote_pipeline.fit(train_features, train_labels)
smote_prediction = smote_model.predict(test_features)
confusion_matrix(test_labels,smote_prediction)



#oversampler=SMOTE(random_state=0)
#os_features,os_labels=oversampler.fit_sample(features_train,labels_train)