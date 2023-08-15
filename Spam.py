#!/usr/bin/env python
# coding: utf-8

# In[12]:


#importing Modules
import os
import re
import pandas
import math


# In[13]:


#Pre-processing
def contract(phrase):
    line=re.sub(r"\'d", " would", phrase)
    phrase =line
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    return phrase


# In[14]:


def preprocessFile(filename):
	temp=0
	words = []
	with open(filename, "r", errors="ignore") as file:
		filedata = file.readlines()
		for line in filedata:
			ans=0
			sent = contract(line) # calling contract function
			sent = sent.replace('\\n', ' ')
			sent = sent.replace('\\r', ' ')
			sent = sent.replace('\\"', ' ')
			sent = re.sub('[^A-Za-z0-9]+', ' ', sent)
			sent = ' '.join(e.lower() for e in sent.split())
			ans=sent.strip().split()
			words += list(ans)
	return words


# In[15]:


def creatingFromWords(words):
	lis=[]
	frequencies = [words.count(word) for word in words]
	return dict(list(zip(words, frequencies)))


# In[16]:


def savingToCSV(dic, filename):
	lis=[]
	with open(filename, "w+") as file:
		res=0
		for word in dic.keys():
			file.write("%s %d\n" % (word, dic[word]))


# In[17]:


def readCSV(filename, datatype="float"):
	temp=[]
	dic = {}
	with open(filename, "r") as file:
		filedata = file.readlines()
		for line in filedata:
			res=0
			word, frequency = line.split(" ")
			if(datatype == "float"):
				dic[str(word)] = float(frequency)
				res=1
			elif(datatype == "int"):
				dic[str(word)] = int(frequency)
				res=0
			else:
				dic[str(word)] = frequency
				res=1
	return dic


# In[18]:


#Test

vocabulary = readCSV("vocabulary.csv")
spam = readCSV("spam.csv")
nonspam = readCSV("non-spam.csv")

Prob_spamprior = 0.5
Prob_nonspamprior = 0.5
NonSpamCount = len(nonspam)
TotalWords = len(vocabulary)
SpamCount = len(spam)


# In[19]:


def predict(filename):
	lis1=[]
	lis2=[]
	testDict = creatingFromWords(preprocessFile(filename))

	testSpamProb = Prob_spamprior
	testnonspamProb = Prob_nonspamprior

	for word in testDict.keys():
		flag=1
		denom1=(SpamCount + TotalWords)
		denom2=(NonSpamCount + TotalWords)
		if word in spam.keys():
			wordSpamProb = (spam[word] + 1.0) / denom1
			flag=0
		else:
			flag=1
			wordSpamProb = (0.0 + 1.0) / denom1
		testSpamProb += math.log(wordSpamProb)
	
		if word in nonspam.keys():
			flag=0
			wordnonspamProb = (nonspam[word] + 1.0) / denom2
            
		else:
			wordnonspamProb = (0.0 + 1.0) / denom2
		testnonspamProb += math.log(wordnonspamProb)
	if(testSpamProb > testnonspamProb):
		lis1.append(testSpamProb)
		print("Spam!")
		return 1
	else:
		lis2.append(testnonspamProb)
		print("Non-spam!")
		return 0


# In[21]:


#prediction
print("Predicting the emails of test file:")
path = "C:/Users/ravis/Documents/PRML 3/test/"   ## test data path , Please change it accordingly
c=0
n=0
for file in os.listdir(path):
    c+=predict(path + file)
    n+=1
print("Accuracy%="+str((c/n)*100))


# In[ ]:




