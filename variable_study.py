# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 02:27:21 2018

@author: SK056042
"""

###Variable study- Home Credit
import pandas as pd
from pandas import read_csv 
import os
import math
import numpy as np
import statistics
import matplotlib.pyplot as plt 
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

#Target: 8% 1, 92%-0s
plt.hist(data_train.TARGET)

#Name contract type,: Cash loans: 278232, revolving: 29279
#9% cash loans and 91% revolving loans
plt.hist(data_train.NAME_CONTRACT_TYPE)

##Code gender- M:105059, F=202448, XNA=4
##M:34%, F=66%
plt.hist(data_train.CODE_GENDER)
#__Remove XNA rows___#

###34% has car, and 66 % has no car
plt.hist(data_train.FLAG_OWN_CAR)

-----------------------------
##70% people have realty, 30% doesnt
# the irony is people with own house had 
plt.hist(data_train.FLAG_OWN_REALTY)
housedpop=data_train[data_train['FLAG_OWN_REALTY']=='Y']
housedpop.shape
housedata=housedpop.iloc[:,44:91]
#housedata.shape= 213312, 47
houseddatamissing=pd.DataFrame(housedata.isnull().sum())
houseddatamissing=houseddatamissing.apply(lambda x: x/213312*100)

nohousedpop=data_train[data_train['FLAG_OWN_REALTY']=='N']
#nohousedpop.shape: 94199, 122
nohousedata=nohousedpop.iloc[:,44:91]
#housedata.shape= 213312, 47
nohouseddatamissing=pd.DataFrame(nohousedata.isnull().sum())
nohouseddatamissing=nohouseddatamissing.apply(lambda x: x/213312*100)

#data_train.columns[90], is 'EMERGENCYSTATE_MODE",,, data_train.columns[44] 'APARTMENTS_AVG'

data_train[data_train['FLAG_OWN_REALTY']=='Y'].NAME_HOUSING_TYPE.unique()

#array(['House / apartment', 'Rented apartment', 'With parents',
 #      'Municipal apartment', 'Co-op apartment', 'Office apartment'],
  #    dtype=object)
#People despite having own house, can stay rented
------------------------------------------------------
#Children count: range(1-14)
plt.hist(data_train.CNT_CHILDREN)
data_train.CNT_CHILDREN.unique()


# Amt_Credit

c=data_train.AMT_CREDIT.unique()
c=pd.DataFrame(c)
plt.hist(c,bins=15)
c['count']=c.iloc[:,0].apply(lambda x: len(data_train[data_train['AMT_CREDIT']== x]))
plt.scatter(c.iloc[:,0],c['count'])

#Make a bin of Amt credit value
bins=np.linspace(45000,4050000,15)

from scipy.stats import binned_statistic

bin_means = binned_statistic(c, c, bins=10, range=(45000, 4050000))[0]
###__outliers has to be removed

#---------------------------
#Amt Annuity
data_train[data_train[']]

#---------------------------
#Amt Income
i=data_train['AMT_INCOME_TOTAL'].sort_values(ascending=True)
i.tail()
i=i[0:307500]
ih=np.histogram(i,bins=10)
plt.hist(ih)
#---------
#Study of income, credit and annuity
inc_cred=data_train[['AMT_INCOME_TOTAL','AMT_CREDIT','AMT_ANNUITY']]
inc_cred.to_csv("inc_cred_ann.csv")

-------------------
#Days birth
db=data_train.DAYS_BIRTH
db.max() #69.12 years
db.min()#21.5 years
db=db.apply(lambda x: x*-1/365)
plt.hist(db)
#Close to a normal dist with max pop in 30-45 years
#no outliers
-------
de=data_train.DAYS_EMPLOYED
delog=de.apply(lambda x: math.log(x))
de.max() #365243
de.min()#-17912
plt.hist(math.log(de))
#lot of wrong values, needs correction, 55K records have same value i.e. 365243
len(data_train[data_train['DAYS_EMPLOYED']>0])# 55374
len(data_train[data_train['DAYS_EMPLOYED']==365243])
data_train['DAYS_EMPLOYED']=data_train['DAYS_EMPLOYED'].replace(365243,0)
-------------------

g=data_train['AMT_GOODS_PRICE']

gs=gs.apply(lambda x: math.log10(x))
plt.hist(math.log(gs))


--------
#Edu type

plt.hist(data_train.NAME_EDUCATION_TYPE)
---------------------

#Study of previous loans
#Remove the applications which had zero while asking, reduces from 16lakh to 12lakh
previouskey=previous[['SK_ID_CURR','SK_ID_PREV','AMT_ANNUITY','AMT_APPLICATION','AMT_CREDIT','AMT_GOODS_PRICE','AMT_DOWN_PAYMENT',]]
previouskey=previouskey[previouskey['AMT_APPLICATION']>=0]
previouskeyprint=previouskey.iloc[0:100000,:]
previouskeyprint.to_csv("previouskey.csv")
