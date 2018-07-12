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







