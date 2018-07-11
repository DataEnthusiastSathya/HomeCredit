# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 14:39:14 2018

@author: SK056042
"""

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


pdf=previous.isnull().sum()
pdf=pdf.apply(lambda x: round(x/1670214*100))

#---------------------------------------------------
previous.columns

#'SK_ID_PREV', 'SK_ID_CURR', 'NAME_CONTRACT_TYPE', 'AMT_ANNUITY',
 #      'AMT_APPLICATION', 'AMT_CREDIT', 'AMT_DOWN_PAYMENT', 'AMT_GOODS_PRICE',
  #     'WEEKDAY_APPR_PROCESS_START', 'HOUR_APPR_PROCESS_START',
   #    'FLAG_LAST_APPL_PER_CONTRACT', 'NFLAG_LAST_APPL_IN_DAY',
    #   'RATE_DOWN_PAYMENT', 'RATE_INTEREST_PRIMARY',
     #  'RATE_INTEREST_PRIVILEGED', 'NAME_CASH_LOAN_PURPOSE',
      # 'NAME_CONTRACT_STATUS', 'DAYS_DECISION', 'NAME_PAYMENT_TYPE',
       #'CODE_REJECT_REASON', 'NAME_TYPE_SUITE', 'NAME_CLIENT_TYPE',
       #'NAME_GOODS_CATEGORY', 'NAME_PORTFOLIO', 'NAME_PRODUCT_TYPE',
 #      'CHANNEL_TYPE', 'SELLERPLACE_AREA', 'NAME_SELLER_INDUSTRY',
#       'CNT_PAYMENT', 'NAME_YIELD_GROUP', 'PRODUCT_COMBINATION',
  #     'DAYS_FIRST_DRAWING', 'DAYS_FIRST_DUE', 'DAYS_LAST_DUE_1ST_VERSION',
   #    'DAYS_LAST_DUE', 'DAYS_TERMINATION', 'NFLAG_INSURED_ON_APPROVAL']
   
previous.shape
# (1670214, 37)

previous.SK_ID_PREV.nunique()
#1670214

previous.SK_ID_CURR.nunique()
# 338857
PSK=previous.SK_ID_CURR.unique()

len(data_train[data_train['SK_ID_CURR'].isin(PSK)].SK_ID_CURR)
#291057
#307511-291057=16454, 16k ids do not have previous data
------------------------------------------------------------
plt.hist(previous.NAME_CONTRACT_TYPE)
previous[previous['NAME_CONTRACT_TYPE']=='XNA']# 346 rows
#these 346 rows have all crucial info as NaN, hence removing
previous[previous['NAME_CONTRACT_TYPE']=='XNA'].index

previous=previous.drop(previous[previous['NAME_CONTRACT_TYPE']=='XNA'].index,axis=0)
previous.shape
# (1669868, 37)

------------------------------------------------------------
plt.hist(previous.AMT_ANNUITY.fillna(0))

------------------------------------
plt.hist(previous.AMT_APPLICATION.fillna(0))

previous.AMT_APPLICATION.max()#6905160
previous.AMT_APPLICATION.min()#6905160

previous.AMT_APPLICATION.sort_values(ascending=True).tail(15)

AmtApp=previous.drop(previous[previous['AMT_APPLICATION']==0].index,axis=0)
AmtApp=previous[previous['AMT_APPLICATION']<=1000000]

plt.hist(AmtApp.AMT_APPLICATION)
----------------------------------------

plt.hist(previous.AMT_CREDIT)


--------------------------------
##Aggregation

PrevSK=previous[['SK_ID_PREV','SK_ID_CURR']]
PrevCount = PrevSK.groupby('SK_ID_CURR').agg(['count'])
PrevCount.shape

AmtCred=previous[['SK_ID_CURR','AMT_CREDIT','AMT_APPLICATION']]
AmtCredagg = AmtCred.groupby('SK_ID_CURR').agg(['mean','sum','median'])
AmtCredagg.shape

AmtCred=previous[['SK_ID_CURR','AMT_CREDIT']]
AmtCredagg = AmtCred.groupby('SK_ID_CURR').agg(['mean','sum','median'])
AmtCredagg.shape

prevdays=previous[['SK_ID_CURR','DAYS_FIRST_DRAWING', 'DAYS_FIRST_DUE', 'DAYS_LAST_DUE_1ST_VERSION','DAYS_LAST_DUE', 'DAYS_TERMINATION']]
prevdays[prevdays['SK_ID_CURR']==100001]

------------------------------------------------
#installments study 1251047



install_paid1=install_pay[['SK_ID_CURR','SK_ID_PREV','NUM_INSTALMENT_NUMBER','AMT_INSTALMENT']]
install_paid1.shape
install_paid1=install_paid1.drop_duplicates()
install_paid1.shape# (12951891, 4)

install_paid=install_pay[['SK_ID_CURR','SK_ID_PREV','NUM_INSTALMENT_NUMBER','AMT_PAYMENT']]
#install_paid=install_paid.drop_duplicates()
install_paid = install_paid.groupby(['SK_ID_CURR','SK_ID_PREV','NUM_INSTALMENT_NUMBER']).agg(['sum'])

install_paid.reset_index(inplace=True)
install_paid.shape# (12861994, 4)

installmerged=install_paid.merge(install_paid1,  on=(["SK_ID_CURR","SK_ID_PREV","NUM_INSTALMENT_NUMBER"]))
installmerged1=installmerged.iloc[:,[0,1,6,7]]



installmergednew1=installmerged1.groupby(['SK_ID_CURR','SK_ID_PREV']).agg('sum')
installmergednew1=installmergednew1.reset_index()
installmergednew1['AMT_PAYMENT']=installmergednew1.iloc[:,2]

installmergednew1['Remaining']=installmergednew1['AMT_INSTALMENT']-installmergednew1['AMT_PAYMENT']
installmergednew2=installmergednew1.fillna(0)
plt.hist(installmergednew2['Remaining'])
#len(installmergednew1[installmergednew1['Remaining'].isnull()==True])
len(installmergednew1[installmergednew1['Remaining']>0]) #8623
len(installmergednew1[installmergednew1['Remaining']<0]) #56764

len(installmergednew1[installmergednew1['Remaining']>0].SK_ID_CURR.unique())#8342
len(installmergednew1[installmergednew1['Remaining']<0].SK_ID_CURR.unique())#49328
