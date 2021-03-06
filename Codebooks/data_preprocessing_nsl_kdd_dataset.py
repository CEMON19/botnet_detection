# -*- coding: utf-8 -*-
"""Data Preprocessing NSL-KDD dataset

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aFs84KCw2C60pMAUp-ZsuxKS_ss8giZI
"""
import numpy as np
import pandas as pd
import matplotlib
import seaborn as sb
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier as xgb
from matplotlib import pyplot as plt
from sklearn import svm
from sklearn.cluster import KMeans
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score

columns=[
        'duration',
'protocol_type', 
'service' , 
'flag' ,
 'src_bytes' ,
 'dst_bytes',
'land',
'wrong_fragment',
 'urgent' ,
'hot',
'num_failed_logins',
 'logged_in',
 'num_compromised',
 'root_shell' ,
 'su_attempted' ,
 'num_root' ,
 'num_file_creations' ,
 'num_shells' ,
 'num_access_files',
'num_outbound_cmds' ,
 'is_host_login',
 'is_guest_login',
 'count',
 'srv_count' ,
 'serror_rate' ,
 'srv_serror_rate' ,
 'rerror_rate' ,
 'srv_rerror_rate' ,
 'same_srv_rate' ,
 'diff_srv_rate' ,
 'srv_diff_host_rate',
 'dst_host_count',
 'dst_host_srv_count' ,
 'dst_host_same_srv_rate' ,
 'dst_host_diff_srv_rate' ,
 'dst_host_same_src_port_rate' ,
 'dst_host_srv_diff_host_rate' ,
 'dst_host_serror_rate' ,
 'dst_host_srv_serror_rate' ,
 'dst_host_rerror_rate',
 'dst_host_srv_rerror_rate' ,
 'class'
]

print(len(columns))

def Standardization(X_original):
  
  scaler1 = StandardScaler().fit(X)
  X_original=scaler1.transform(X)
  return X_original

data=pd.read_csv(".\data\KDD Train+ Unwanted removed.txt")

data.columns=columns

print(data.head())

print(data.tail())

print(data['duration'].count())

print(data['class'].value_counts())

print(data.describe())

for i in columns:
  if type(data[i][0])==type(data['protocol_type'][0]):
    print(i+" column has "+str(data[i].nunique())+" unique features")



cat_col=['protocol_type','service','flag','class']
new_categorical_columns=data[cat_col]
print(new_categorical_columns.head())

new_cat_encoded=new_categorical_columns.apply(LabelEncoder().fit_transform)

print(new_cat_encoded.head())

data=data.drop(['flag','protocol_type','service'],axis=1)

data=data.drop('class',axis=1)

data=data.join(new_cat_encoded)

data = data.reindex(columns, axis=1)
print(data.head())

X = data.drop('class',1)
Y = data['class']

print(X)

"""Data Standardization for Feature Selection"""

#Standardizing X for the purpose of FEATURE SELECTION
X_original=Standardization(X)

Y_original=Y.values

print(Y_original)

"""Feature Scaling is a technique to standardize the independent features present in the data in a fixed range. It is performed during the data pre-processing to handle highly varying magnitudes or values or units. If feature scaling is not done, then a machine learning algorithm tends to weigh greater values, higher and consider smaller values as the lower values, regardless of the unit of the values.

Example: If an algorithm is not using the feature scaling method then it can consider the value 3000 meters to be greater than 5 km but that???s actually not true and in this case, the algorithm will give wrong predictions. So, we use Feature Scaling to bring all values to the same magnitudes and thus, tackle this issue.

Techniques to perform Feature Scaling
Consider the two most important ones:

Min-Max Normalization: This technique re-scales a feature or observation value with distribution value between 0 and 1.
X_{\text {new }}=\frac{X_{i}-\min (X)}{\max (x)-\min (X)}

Standardization: It is a very effective technique which re-scales a feature value so that it has distribution with 0 mean value and variance equals to 1.

X_{\text {new }}=\frac{X_{i}-X_{\text {mean }}}{\text { Standard Deviation }}

PLOTTING TO SEE HOW MANY NORMAL AND ANAMOLY TRAFFIC EXISTS, NORMAL 1,ANAMOLY 0
"""

# for i in columns[0:41]:
  # print(i)
  # print(sb.boxplot(data[i]))
  # plt.show()

print(sb.histplot(Y_original))



fig, ax = plt.subplots(figsize=(20,20))         # Sample figsize in inches
print(sb.heatmap(data.corr(),ax=ax))

print(data.corr())

"""Feature Selection process:
How to carryout feature selection:

Feature Selector Wrapper Method:

Default forward

if Forward=False the backward wrapper works


Using XG Boost for Feature Selection
"""


rf=xgb()
rf.fit(X_original,Y_original)

importances=rf.feature_importances_
importances_with_feature=pd.Series(importances,index=columns[:-1])
print(importances_with_feature)

fix,ax=plt.subplots(figsize=(22,22))
importances_with_feature.plot.bar(ax=ax)
print(plt.show())


y_true=rf.predict(X_original)
print(accuracy_score(y_true, Y_original))



model = LogisticRegression(max_iter=30)
# fit the model
model.fit(X_original,Y_original)
importance = model.coef_[0]

# summarize feature importance
for i,v in enumerate(importance):
	print(columns[i]+"  importance = "+str(v))
# plot feature importance
plt.bar([x for x in range(len(importance))], importance)
plt.show()

importance=pd.Series(importance)
print(importance)

y_true=model.predict(X_original)
print(accuracy_score(y_true, Y_original))

features_names = columns[:-1]
svm = svm.SVC(kernel='linear',max_iter=300)
svm.fit(X_original, Y_original)

result=pd.Series(svm.coef_[0])
print(result)

fig,ax2=plt.subplots(figsize=(20,20))
result.plot.bar(ax=ax2)
print(plt.show())

y_true=svm.predict(X_original)
print(accuracy_score(y_true, Y_original))

"""Since the Accuracy of the XGBoost model is good we shall choose features based on XGBOOST model.

Removing feature numbers:

6=land

8	urgent

10	num_failed_logins

13	root_shell	
14	su_attempted	
15	num_root

7	num_shells	
18	num_access_files	
19	num_outbound_cmds	
20	is_host_login	
24	serror_rate

27	srv_rerror_rate

Final Removal of the above features and standardising the Independent variables
"""

print(X)

X = data.drop(['land','urgent','num_failed_logins','root_shell','su_attempted','num_root' ,'num_shells',
'num_access_files','num_outbound_cmds','is_host_login','serror_rate','srv_rerror_rate'],1)

print(len(X.columns))

X_original=Standardization(X)

"""Y_original is the true Y to be predicted

Clustering and Relabelling Process using KMeans
"""


wcss=[]
for i in range(1,7):
    kmeans = KMeans(n_clusters=i, init='k-means++', n_init=10, max_iter=300, random_state=0)
    kmeans.fit(X_original)
    wcss.append(kmeans.inertia_)
plt.plot(range(1,7), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of Clusters')
plt.ylabel('wcss')
print(plt.show())

kmeans = KMeans(n_clusters=4, random_state=0).fit(X_original)

Y_new_orig=kmeans.predict(X_original)

count_0,count_1,count_2,count_3=0,0,0,0
for i in Y_new_orig:
  if i==0:
    count_0+=1
  elif i == 1:
    count_1+=1
  elif i==2:
    count_2+=1
  else:
    count_3+=1
print("Count of class 0 is "+str(count_0))
print("Count of class 1 is "+str(count_1))
print("Count of class 2 is "+str(count_2))
print("Count of class 3 is "+str(count_3))

"""Indirectly upon correlating with the original data class 1 of new data belongs to normal traffic with slight amount of anamoly as well

XGBOOST Model after Kmeans clustering
"""

xgb_multi=xgb(n_estimators=200,max_depth=5)
xgb_multi.fit(X_original,Y_new_orig)

y_true_xgb=xgb_multi.predict(X_original)
print(accuracy_score(y_true_xgb, Y_new_orig))

fpr, tpr, _ = roc_curve(y_true_xgb,Y_new_orig,pos_label=1)
plt.plot(fpr,tpr)
plt.title('XGBoost')
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()
import pickle
pickle.dump(kmeans, open("/content/kmeans_cluster.pkl", "wb"))

import pickle
pickle.dump(xgb_multi, open("/content/xgboost_kmeans.pkl", "wb"))

"""Logistic Regression Classifier"""

LR_multi = LogisticRegression(max_iter=100)
# fit the model
LR_multi.fit(X_original,Y_new_orig)

y_true_log=xgb_multi.predict(X_original)
print(accuracy_score(y_true_log, Y_new_orig))

fpr, tpr, _ = roc_curve(y_true_log,Y_new_orig,pos_label=1)
plt.plot(fpr,tpr)
plt.title('Logistic Regression')
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()

pickle.dump(LR_multi, open("/content/LR_kmeans.pkl", "wb"))

"""SVM Classifier"""

svm_multi = svm.SVC(kernel='linear',max_iter=300)
svm_multi.fit(X_original, Y_new_orig)

y_true_svm=svm_multi.predict(X_original)
print(accuracy_score(y_true_svm, Y_new_orig))

fpr, tpr, _ = roc_curve(y_true_svm,Y_new_orig,pos_label=1)
plt.plot(fpr,tpr)
plt.title('SVM')
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()
pickle.dump(svm_multi, open("/content/svm_kmeans.pkl", "wb"))

print("exiting..")