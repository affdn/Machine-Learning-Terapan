# -*- coding: utf-8 -*-
"""Predictive Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1N4fbgPPfagVKxVC5EQdG6ub5iaswin7r

**IMPORT LIBRARY DAN DATASET**
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# %matplotlib inline
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import mean_squared_error
from xgboost import XGBClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

# install kaggle package
!pip install -q kaggle

# upload kaggle.json
from google.colab import files
files.upload()

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json
!ls ~/.kaggle

# Download dataset
!kaggle competitions download -c titanic

# unzip
!mkdir data
!unzip -qq titanic.zip -d data
!ls data

"""Pada cell dibawah ini dilakukan import dataset """

data_train = pd.read_csv("data/train.csv")
data_test = pd.read_csv("data/test.csv")
data_train.head()

"""Cell dibawah ini untuk melihat rangkuman dataset"""

data_train.describe()

"""Cell dibawah ini digunakan untuk melakukan cek pada NaN values di dalam dataset"""

sns.heatmap(data_train.isnull(),yticklabels=False,cbar=False,cmap='viridis')

"""Pada cell dibawah berfungsi untuk menghapus data cabin karena banyak NaN values dan pada kolom age terdapat NaN values dengan nilai median."""

data_train.drop(['Cabin'],axis=1,inplace=True)
data_train['Age'] = data_train['Age'].fillna((data_train['Age'].median()))

"""Cell dibawah digunakan untuk mengecek apakah masih terdapat NaN values."""

sns.heatmap(data_train.isnull(),yticklabels=False,cbar=False,cmap='viridis')

"""Pada cell dibawah berfungsi untuk menghilangkan value-value yang terlalu jauh."""

Q1 = data_train.quantile(0.25)
Q3 = data_train.quantile(0.75)
IQR=Q3-Q1
data_train=data_train[~((data_train<(Q1-1.5*IQR))|(data_train>(Q3+1.5*IQR))).any(axis=1)]

"""**Univariate Analysis**

Cell code dibawah ini digunakan sebagai num dengan object kolom
"""

train_num = ['Age','SibSp','Fare']
train_cat = ['Survived','Pclass','Sex','Ticket','Embarked']

"""Pada cell code dibawah dilakukan Univariate EDA pada kolom-kolom object"""

for i in range(len(train_cat)):
    feature = train_cat[i]
    count = data_train[feature].value_counts()
    percent = 100*data_train[feature].value_counts(normalize=True)
    df = pd.DataFrame({'jumlah sampel':count, 'persentase':percent.round(1)})
    print(df)
    count.plot(kind='bar', title=feature)
    plt.show()

"""**Multivariate Analysis**

Pada cell code di bawah berfungsi untuk mengecek pada Multivariate EDA dengan heatmap
"""

plt.figure(figsize=(10, 8))
correlation_matrix = data_train.corr().round(2)

sns.heatmap(data=correlation_matrix, annot=True,linewidths=0.5 )
plt.title("Correlation Matrix", size=20)

"""Cell code di bawah berfungsi menghapus Pclass dan Parch karena memiliki korelasi yang rendah terhadap suvivability"""

data_train.drop(['Pclass','Parch'],axis=1,inplace=True)
data_train.head()

"""**Data Preparation**

Cell code dibawah dilakukan get_dummies pada kolom sex dan embark
"""

sex = pd.get_dummies(data_train['Sex'])
embark = pd.get_dummies(data_train['Embarked'])

"""Pada cell code dibawah, dilakukan drop/menghapus kolom yang tidak relevan dan meng-concat get_dummies dari sex dan embarked sebelumnya"""

data_train.drop(['PassengerId','Sex','Embarked','Name','Ticket'],axis=1,inplace=True)
data_train = pd.concat([data_train,sex,embark],axis=1)
data_train.head()

"""Cell code dibawah berfungsi untuk men-split data train."""

from sklearn.model_selection import train_test_split
 
X = data_train.drop(["Survived"],axis =1)
y = data_train["Survived"]
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size = 0.2, random_state = 0)

"""Pada cell code di bawah dilakukan standardscaler pada x train dan x valid"""

from sklearn.preprocessing import StandardScaler
train_num = ['Age','SibSp','Fare']
scaler = StandardScaler()
scaler.fit(X_train[train_num])
scaler.fit(X_valid[train_num])
X_train[train_num] = scaler.transform(X_train.loc[:, train_num])
X_valid[train_num] = scaler.transform(X_valid.loc[:, train_num])
X_train.head()

"""**Model Development**

**XGBClassifier**

Pada cell code di bawah digunakan untuk mendefinisikan paramater XGBClassifier
"""

model_XGBClassifier = XGBClassifier()
model_XGBClassifier.fit(X_train, y_train,
          verbose=False)

preds_XGBClassifier = model_XGBClassifier.predict(X_valid)

"""Cell code di bawah untuk menghitung akurasi, presisi, recall, dan F1 score model XGBClassifier"""

accuracy_XGBClassifier=accuracy_score(y_valid,preds_XGBClassifier)
print("XGBClassifier accuracy value: {:.2f}".format(accuracy_XGBClassifier))
print('XGBClassifier Precision: %.3f' % precision_score(y_valid,preds_XGBClassifier))
print('XGBClassifier Recall: %.3f' % recall_score(y_valid,preds_XGBClassifier))
print('XGBClassifier F1 Score: %.3f' % f1_score(y_valid,preds_XGBClassifier))



"""**Preprocessing Test Data**

Pada cell di bawah dilakukan drop pada kolom yang telah didrop pada data train
"""

X_test=data_test.drop(['Cabin','Parch','PassengerId','Name','Ticket','Pclass'],axis =1)
test_num = ['Age','SibSp','Fare']
scaler = StandardScaler()
scaler.fit(X_test[train_num])
X_test[train_num] = scaler.transform(X_test.loc[:, test_num])

"""Pada cell code dibawah dilakukan get_dummies pada kolom sex dan embark dan dilakukan juga concat pada dataframe test"""

sex = pd.get_dummies(X_test['Sex'])
embark = pd.get_dummies(X_test['Embarked'])
X_test=X_test.drop(['Sex','Embarked'],axis =1)
X_test = pd.concat([X_test,sex,embark],axis=1)

X_test.head()

"""Pada cell code di bawah dilakukan prediksi dari dataset test menggunakan model XGBClassifier"""

predictions=model_XGBClassifier.predict(X_test)

output = pd.DataFrame({'PassengerId': data_test.PassengerId,
                       'Survived': predictions})
output.to_csv('submission.csv', index=False)
output.head()