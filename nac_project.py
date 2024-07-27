# -*- coding: utf-8 -*-
"""NAC_project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1w8U-t9-mpkQ0F0HXeGuASndwC-4njfI-
"""

import nltk

import pandas as pd

nltk.download('punkt')

from google.colab import drive
drive.mount('/content/drive')

real = pd.read_csv('/content/drive/MyDrive/NAC_datasets/True.csv')
fake = pd.read_csv('/content/drive/MyDrive/NAC_datasets/Fake.csv')

fake

real

real["correctness"] = 1
fake["correctness"] = 0

real

data = pd.concat([fake,real],axis=0)
data

data = data.reset_index(drop=True)
data = data.drop(['title','subject','date'], axis = 1)
data

from nltk.tokenize import word_tokenize
data['text'] = data['text'].apply(word_tokenize)

from nltk.stem.snowball import SnowballStemmer
sb = SnowballStemmer("english",ignore_stopwords=False)

def stem_it(text):
  return [sb.stem(word) for word in text]

data['text'] = data['text'].apply(stem_it)

def stopword_remover(text):
  return [word for word in text if len(word)>>2]

data['text'] = data['text'].apply(' '.join)

data

import sklearn
from sklearn import model_selection
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(data['text'],data['correctness'],test_size=0.25)

x_train

from sklearn import feature_extraction
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer( max_df= 0.7)

tfidf_train = tfidf.fit_transform(x_train)
tfidf_test  = tfidf.transform(x_test)

from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
LR = LogisticRegression( max_iter = 900)
LR.fit(tfidf_train, y_train)

pred1 = LR.predict(tfidf_test)
pred1

y_test

from sklearn import metrics
from sklearn.metrics import accuracy_score
score1 = accuracy_score(y_test, pred1)
score1

from sklearn.linear_model import PassiveAggressiveClassifier
PAC = PassiveAggressiveClassifier( max_iter = 100)
PAC.fit(tfidf_train,y_train)

pred2 = PAC.predict(tfidf_test)
pred2

y_test

score2 = accuracy_score(y_test,pred2)
score2