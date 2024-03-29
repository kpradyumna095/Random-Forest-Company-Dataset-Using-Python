# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 14:35:44 2019

@author: Hello
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

company = pd.read_csv("C:\\Users\\Hello\\Desktop\\Data science\\data science\\assignments\\RF\\datasets\\Company_Data(1).csv")

##Looking into unique value 
company["Sales"].unique()

##Preforming how many times each number is repeated
company["Sales"].value_counts()

##Looking into median to check the median-- middle value, which can help us in Stratified sampling
np.median(company["Sales"])
##middle value is 7.49

company["sales"]="<=7.49"
company.loc[company["Sales"]>=7.49,"sales"]=">=7.49"

company.drop(["Sales"],axis=1,inplace=True)

##Encoding the data as model.fit doesnt convert string data to float
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
for column_names in company.columns:
    if company[column_names].dtype == object:
        company[column_names]= le.fit_transform(company[column_names])
    else:
        pass
    
##Splitting the data into input and output
featues = company.iloc[:,0:10]
labels = company.iloc[:,10]

##Splitting the data into train and test by using stratify sampling
from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test = train_test_split(featues,labels,test_size = 0.3,stratify = labels) 

##Looking into the class variable split
y_train.value_counts()

y_test.value_counts()

##Building the model
from sklearn.ensemble import RandomForestClassifier as RF

model =RF(n_jobs=4,n_estimators = 150, oob_score =True,criterion ='entropy') 
model.fit(x_train,y_train)
model.oob_score_
#76.42%

##Predicting on training data
pred_train = model.predict(x_train)
##Accuracy on training data
from sklearn.metrics import accuracy_score
accuracy_train = accuracy_score(y_train,pred_train)
##100%
##Confusion matrix
from sklearn.metrics import confusion_matrix
con_train = confusion_matrix(y_train,pred_train)

##Prediction on test data
pred_test = model.predict(x_test)

##Accuracy on test data
accuracy_test = accuracy_score(y_test,pred_test)
#82.5
np.mean(y_test==pred_test)
# 82.5
##Confusion matrix
con_test = confusion_matrix(y_test,pred_test)

##Visualizing the one decision tree in random forest
from sklearn.tree import export_graphviz 
from sklearn.externals.six import StringIO
import pydotplus
colnames = list(company.columns)
predictors = colnames[0:10]
target = colnames[10]
tree1 = model.estimators_[20]
dot_data = StringIO()
export_graphviz(tree1,out_file = dot_data, feature_names =predictors, class_names = target, filled =True,rounded=True,impurity =False,proportion=False,precision =2)

graph = pydotplus.graph_from_dot_data(dot_data.getvalue())

##Creating pdf file
graph.write_pdf('companyrf.pdf')

##Creating png file
graph.write_png('companyrf.png')
