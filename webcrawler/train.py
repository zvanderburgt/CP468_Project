from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition, ensemble
from sklearn import metrics

import pandas, xgboost, numpy, textblob, string

import os
from datetime import datetime
import json

def train_model(classifier, feature_vector_train, label, feature_vector_valid, is_neural_net=False):
    # fit the training dataset on the classifier
    classifier.fit(feature_vector_train, label)
    
    # predict the labels on validation dataset
    predictions = classifier.predict(feature_vector_valid)
    
    if is_neural_net:
        predictions = predictions.argmax(axis=-1)
    
    return metrics.accuracy_score(predictions, valid_y)

#load the dataset 
here = os.path.dirname(os.path.realpath(__file__))
dir = os.path.join(here, "Dataset")
keywords = ["self+driving+cars", "quantum+computing", "artificial+intelligence"]

labels, texts = [], []

for folder in keywords:
    print("-----"+folder+"-----")
    c = 0
    subDir = os.path.join(here, dir, folder)
    for file in os.listdir(subDir):
        labels.append(folder)
        filepath = os.path.join(here, dir, subDir, file)
        try:
            print("Reading: " + file)
            f = open(filepath, 'r',encoding='utf8', errors="ignore")
            r = f.read()
            texts.append(r)
            f.close()
            print("Done!")
            c+=1
        except:
            print("Unable to read: " + file)
    print("Able to read: " + str(c) + " files")


dir = os.path.join(here, "Features")
# if there isn't already a subdirectory called Dataset in the same directory as the python file
if not os.path.exists(dir):
    # make a new direcotry
    os.makedirs(dir)

# create a dataframe using texts and lables
trainDF = pandas.DataFrame()
trainDF['text'] = texts
trainDF['label'] = labels

# split the dataset into training and validation datasets 
train_x, valid_x, train_y, valid_y = model_selection.train_test_split(trainDF['text'], trainDF['label'])

# label encode the target variable 
encoder = preprocessing.LabelEncoder()
train_y = encoder.fit_transform(train_y)
valid_y = encoder.fit_transform(valid_y)

# word level tf-idf
tfidf_vect = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', max_features=5000)
tfidf_vect.fit(trainDF['text'])
xtrain_tfidf =  tfidf_vect.transform(train_x)
xvalid_tfidf =  tfidf_vect.transform(valid_x)
# same as above but for the dataset subdirecories based on keywords
subDir = os.path.join(here, dir, "Word Level")
if not os.path.exists(subDir):
    os.makedirs(subDir)
filepath = os.path.join(here, dir, subDir, str(datetime.date(datetime.now()))+".txt")
outFile = open(filepath, "w+")
outFile.write("Vocabulary: " + json.dumps(tfidf_vect.vocabulary_)+'\n'+'*'*10+'\n')
print("\nIDF: ",file=outFile)
print(tfidf_vect.idf_,file=outFile)
print('\n'+'*'*10+'\n',file=outFile)
print("Train Shape: ",file=outFile)
print(xtrain_tfidf.shape,file=outFile)
print('\n'+'*'*10+'\n',file=outFile)
print("Train Array: ",file=outFile)
print(xtrain_tfidf.toarray(),file=outFile)
print('\n'+'*'*10+'\n',file=outFile)
print("Valid Shape: ",file=outFile)
print(xvalid_tfidf.shape,file=outFile)
print('\n'+'*'*10+'\n',file=outFile)
print("Valid Array: " ,file=outFile)
print(xvalid_tfidf.toarray(),file=outFile)
print('\n'+'*'*10+'\n',file=outFile)
outFile.close()

# ngram level tf-idf 
tfidf_vect_ngram = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', ngram_range=(2,3), max_features=5000)
tfidf_vect_ngram.fit(trainDF['text'])
xtrain_tfidf_ngram =  tfidf_vect_ngram.transform(train_x)
xvalid_tfidf_ngram =  tfidf_vect_ngram.transform(valid_x)
subDir = os.path.join(here, dir, "Ngram Level")
if not os.path.exists(subDir):
    os.makedirs(subDir)
filepath = os.path.join(here, dir, subDir, str(datetime.date(datetime.now()))+".txt")
outFile = open(filepath, "w+")
outFile.write("Vocabulary: " + json.dumps(tfidf_vect_ngram.vocabulary_)+'\n'+'*'*10+'\n')
print("\nIDF: ",file=outFile)
print(tfidf_vect_ngram.idf_,file=outFile)
print('\n'+'*'*10+'\n',file=outFile)
print("Train Shape: ",file=outFile)
print(xtrain_tfidf_ngram.shape,file=outFile)
print('\n'+'*'*10+'\n',file=outFile)
print("Train Array: ",file=outFile)
print(xtrain_tfidf_ngram.toarray(),file=outFile)
print('\n'+'*'*10+'\n',file=outFile)
print("Valid Shape: ",file=outFile)
print(xvalid_tfidf_ngram.shape,file=outFile)
print('\n'+'*'*10+'\n',file=outFile)
print("Valid Array: " ,file=outFile)
print(xvalid_tfidf_ngram.toarray(),file=outFile)
print('\n'+'*'*10+'\n',file=outFile)
outFile.close()

# characters level tf-idf
tfidf_vect_ngram_chars = TfidfVectorizer(analyzer='char', token_pattern=r'\w{1,}', ngram_range=(2,3), max_features=5000)
tfidf_vect_ngram_chars.fit(trainDF['text'])
xtrain_tfidf_ngram_chars =  tfidf_vect_ngram_chars.transform(train_x) 
xvalid_tfidf_ngram_chars =  tfidf_vect_ngram_chars.transform(valid_x) 
subDir = os.path.join(here, dir, "Character Level")
if not os.path.exists(subDir):
    os.makedirs(subDir)
filepath = os.path.join(here, dir, subDir, str(datetime.date(datetime.now()))+".txt")
outFile = open(filepath, "w+")
outFile.write("Vocabulary: " + json.dumps(tfidf_vect_ngram_chars.vocabulary_)+'\n'+'*'*10+'\n')
print("\nIDF: ",file=outFile)
print(tfidf_vect_ngram_chars.idf_,file=outFile)
print('\n'+'*'*10+'\n',file=outFile)
print("Train Shape: ",file=outFile)
print(xtrain_tfidf_ngram_chars.shape,file=outFile)
print('\n'+'*'*10+'\n',file=outFile)
print("Train Array: ",file=outFile)
print(xtrain_tfidf_ngram_chars.toarray(),file=outFile)
print('\n'+'*'*10+'\n',file=outFile)
print("Valid Shape: ",file=outFile)
print(xvalid_tfidf_ngram_chars.shape,file=outFile)
print('\n'+'*'*10+'\n',file=outFile)
print("Valid Array: " ,file=outFile)
print(xvalid_tfidf_ngram_chars.toarray(),file=outFile)
print('\n'+'*'*10+'\n',file=outFile)
outFile.close()


subDir = os.path.join(here, dir, "Accuracy")
if not os.path.exists(subDir):
    os.makedirs(subDir)
filepath = os.path.join(here, dir, subDir, str(datetime.date(datetime.now()))+".txt")
outFile = open(filepath, "w+")
# Naive Bayes on Word Level TF IDF Vectors
accuracy = train_model(naive_bayes.MultinomialNB(), xtrain_tfidf, train_y, xvalid_tfidf)
print("NB, WordLevel TF-IDF: ", accuracy,file=outFile)

# Naive Bayes on Ngram Level TF IDF Vectors
accuracy = train_model(naive_bayes.MultinomialNB(), xtrain_tfidf_ngram, train_y, xvalid_tfidf_ngram)
print("NB, N-Gram Vectors: ", accuracy,file=outFile)

# Naive Bayes on Character Level TF IDF Vectors
accuracy = train_model(naive_bayes.MultinomialNB(), xtrain_tfidf_ngram_chars, train_y, xvalid_tfidf_ngram_chars)
print("NB, CharLevel Vectors: ", accuracy,file=outFile)
outFile.close()

