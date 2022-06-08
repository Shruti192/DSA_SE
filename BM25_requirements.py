########################  Preparation for similarity Calculation By BM25  #############################################
#########  Here we will try to calculate all the paramereters required for similarity calculation that we could calculate w/o using query sting
########  Reference to Maths of BM25: https://kmwllc.com/index.php/2020/03/20/understanding-tf-idf-and-bm-25/

# Import all  require libraries
from copy import copy
import re
import os
import math
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize,word_tokenize
from num2words import num2words
from nltk.stem import PorterStemmer
ps = PorterStemmer()
from spellchecker import SpellChecker
spell = SpellChecker()
import json

#################################   Formation of Keyword arrays    ##################################################################
#########    Get the stopwords
from nltk.corpus import stopwords
nltk.download('stopwords')
stopwrds = stopwords.words('english')
stopwrds.append('any')
stopwrds.append('?')
stopwrds.append('¶')
stopwrds.append('a')
stopwrds.append('i')
stopwrds.extend(("<","n","(", ")","()", "[", "]", "[]", "[", "]", "{}", "{", "}", ".", ",", "'", '"', "_", ":", "-", "NaN","=",">",":","?","!","%","&","@","#","$","^","*","<",">","+",";","|","b","a","p","q"))

#########    Get All_Keyword Array and Keyword_per_doc arrays {training over problem content as well as title}
all_keywords = []    ###### array of keywords through out the corpus
keywords_per_doc = []   #######  list of keyword ith row of which will represent key_word array of ith document
doc_len = []           ######  array containing length of each document   doc_len[i] = length of ith document
doc_lenstr = []         ## same as above just for writing all_doc_len.txt purposes
avg_dl = 0              ### avg_document length over the corpus
d = dict()  ### Creating global dictionary
mypath = r"C:\Users\shrut\PycharmProjects\Scraping\Problem_Set_reduced"

########  Running loop to calculate above arrays
for i in range(1,N+1):
    ######  we are reading both problem content and problem title as we want to train our data on both
    file_content = open("C:/Users/shrut/PycharmProjects/Scraping/Problem_Set_1000/Problem_Content/problem_"+str(i)+".txt",'r').read()
    file_title = open(
        "C:/Users/shrut/PycharmProjects/Scraping/Problem_Set_1000/Problem_titles/problem_title_" + str(i) + ".txt", 'r').read()
    ######    Remove the symbols, digits, \n,
    f_content = file_content.replace("\\n", "\n")
    f_content = re.sub(r'[^\w]', ' ', f_content)
    f_content = re.sub(" \d+", " ", f_content)
    tokens1 = f_content.split()
    f_title = file_content.replace("\\n", "\n")
    f_title = re.sub(r'[^\w]', ' ', f_title)
    f_title = re.sub(" \d+", " ", f_title)
    tokens1 = f_content.split()   #word array from problem content
    tokens2 = f_title.split()     #word array from problem title
    #########   Remove the stopwords and get the keywords
    keywords = []   # for storing of keyword of this specific doc
    d1 = dict()  ### creating an empty dictionary for this doc
    count = 0
    for word in tokens1:
        if word not in stopwrds:
            count+=1
            word = word.lower()
            word = spell.correction(word)
            word = ps.stem(word)
            if word in d1:
                d1[word] += 1
            else:
                d1[word] = 1
            if word in d:
                d[word] += 1
            else:
                d[word] = 1
            if word  not in keywords:
                keywords.append(word)
                if (word not in all_keywords):
                    all_keywords.append(word)
    for word in tokens2:
        if word not in stopwrds:
            count += 1

    #########  Calculating doc_len  and avd_dword = word.lower()
            word = spell.correction(word)
            word = ps.stem(word)
            if word in d1:
                d1[word] += 1
            else:
                d1[word] = 1
            if word in d:
                d[word] += 1
            else:
                d[word] = 1
            if word not in keywords:
                keywords.append(word)
                if (word not in all_keywords):
                    all_keywords.append(word)
    keywords_per_doc.append(keywords)
    with open('Problem_Set_1000\Problem_dict\dict_'+str(i)+'.txt', 'w') as convert_file:
        convert_file.write(json.dumps(d1))
    with open("Problem_Set_1000\Problem_keywords\kewords_" + str(i) + ".txt", "w+") as f:
        f.write('\n'.join(keywords))
        print("keywords collected for document number: "+str(i))
    doc_len.append(count)
    doc_lenstr.append(str(count))
    avg_dl += count

with open('Problem_Set_1000\global_dict_.txt', 'w') as convert_file:
    convert_file.write(json.dumps(d))
with open("Problem_Set_1000/All_Keywords.txt", "w+") as f:
	f.write('\n'.join(all_keywords))
avg_dl /= 1000
print("avg document length is: "+str(avg_dl))
# print("average length of doc over corpus = "+str(avg_dl)+"\n")
with open("Problem_Set_1000/All_doc_len.txt", "w+") as f:
        f.write('\n'.join(doc_lenstr))

#####################  Emergency all keywords making###########
# for i in range(1,1001):
#     with open(r"C:\Users\shrut\PycharmProjects\Scraping\Problem_Set_reduced\Problem_dict\dict_"+str(i)+".txt") as f:
#         data = f.read()
#     d_doc = json.loads(data)
#     for k in  d_doc:
#         if k not in all_keywords:
#             all_keywords.append(k)
# # with open("Problem_Set_1000/All_Keywords.txt", "w+") as f:
# # 	f.write('\n'.join(all_keywords))
# print("Number of all_keywords = "+str(len(all_keywords)))

# ######################################  Get the freq matrix  i.e f(q,D)   ###########################################################
# freq_matrix = []
# tfstr = []
# # all_keywords = open(r"C:\Users\shrut\PycharmProjects\Scraping\Problem_Set_1000\All_Keywords.txt",'r').read().split()
# i = 0
# for i in range(1,1001):
#     data = open(r"C:\Users\shrut\PycharmProjects\Scraping\Problem_Set_reduced\Problem_dict\dict_"+str(i)+".txt")
#     doc = json.load(data)
#     row_matrix = []
#     tyum = []
#     for keyword in all_keywords:
#         cnt = 0.0
#         for k, v in doc.items():
#             if k == keyword:
#                 cnt += v
#         row_matrix.append(cnt)
#         tyum.append(str(cnt))
#     copypath=r"C:\Users\shrut\PycharmProjects\Scraping\Problem_Set_reduced\Problem_freqrows\freq_row_"+str(i)+".txt"
#     with open(copypath, "w+") as f:
#         f.write('\n'.join(tyum))
#     freq_matrix.append(row_matrix)
#     tfstr.append(str(row_matrix))
#     print("freq row done for document no: "+str(i))
#     i+=1
# copypath=r"C:\Users\shrut\PycharmProjects\Scraping\Problem_Set_reduced\freq_matrix.txt"
# with open(copypath, "w+") as f:
#     f.write('\n'.join(tfstr))
###################################################  n(qi) = document frequency for each keyword   Calculation i.e df[j]= document frequency
copypath = "C:/Users/shrut/PycharmProjects/Scraping/Problem_Set_1000/All_Keywords.txt"
keywords = open(copypath,'r').readlines()

df1=[]  #  df1[i]= number of document in corpus containing ith keyword        length of array  = length of  all_keywords
dfstr1=[]
l=0
for keyword in keywords:
    l+=1
    count1 = 0
    for i in range(1,1001):
        content1 = open(r"C:/Users/shrut/PycharmProjects/Scraping/Problem_Set_1000/Problem_keywords/kewords_" + str(i) + ".txt",'r').read()
        if keyword in content1:
            count1+=1
    df1.append(count1)
    dfstr1.append(str(count1))
    print("loop ran successfully for keyword number = "+str(l)+"  and count1 is "+str(count1)+"\n")
with open("Problem_Set_1000/df_row.txt", "w+") as f:
    f.write('\n'.join(dfstr1))

#####################################################
###### With this code we were able to obtain :-
#####  1) All_Keywords.txt  containing all keyword through out the corpus
#####  2) All_doc_len.txt  containing  length of all doc
#####  3) df_row.txt  containing document frequency of each keyword from all_keywords
#####  4) Problem_dict folder ith file of which contains dictionary for ith problem content i.e contains total no. of different word with it's frequency
#####  5) Problem_Keyword folder ith file of which contains keyword array of ith problem

################### Now if have read BM25's Mathematics we will realize we will need to copy paste these folders to VS_code for further purposes:
# folders: Problem_Content, Problem_titles, Problem_urls, Problem_dict, Problem_keywords
# file: All_doc_len.txt, df_row.txt
# So put all these in one folder Problem_Set_1000 and pass it to VS Code