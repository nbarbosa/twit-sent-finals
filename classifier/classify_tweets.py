from __future__ import print_function
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
import pandas as pd
from sklearn import linear_model, decomposition, datasets
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from time import time
from selectors import ItemSelector
from sklearn.linear_model import LogisticRegression
from tokenizers import tweet_tokenize

script_dir = os.path.dirname(__file__) 
rel_file_path = "all.csv"
abs_file_path = os.path.join(script_dir, rel_file_path)

stop_words = open(os.path.join(script_dir, 'stopwords_twitter.txt')).read().splitlines()

pipeline = Pipeline([
    ('features', FeatureUnion(
        transformer_list=[
            ('content', Pipeline([
                ('selector', ItemSelector(key='text')),
                ('tfidf', TfidfVectorizer(tokenizer=tweet_tokenize, stop_words=stop_words, ngram_range=(1,2), min_df=5))
            ]))
        ],
       
    )),

    # Use a SVC classifier on the combined features
    ('clf', LogisticRegression()),
])


df = pd.read_csv(abs_file_path, encoding='utf-8')

dfy = df['sentiment']
dfx = df
del dfx['sentiment']

predicted = cross_val_predict(pipeline, dfx, dfy, cv=10)

print('\n**** Classification Report:')
print(classification_report(dfy, predicted))

print('\n**** Confusion Matrix:')
print(confusion_matrix(dfy, predicted))
