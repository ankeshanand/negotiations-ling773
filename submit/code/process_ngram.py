#!/usr/bin/python
################################################################
# Name : process_ngram.py
# Desc : convert n-gram feature into sparse arff format for weka
################################################################
import csv
import os
from global_variable import *

########################################################
# Global Variables
########################################################
# input:
all_fv_file = '../results/dialog_all_ngrams'
meta_fv = meta_info_file
# output:
word_fv_file = '../results/word_fv'

# groc_fv_file = '../results/dialog_grocery_ngrams'
# wine_fv_file = '../results/dialog_wine_ngrams'

num_unigram = 2498
num_bigram = 2648
num_trigram = 608

# find valid ID

meta_file = open(meta_fv,'r')
meta_csv = csv.reader(meta_file,delimiter='\t')
meta = [w for w in meta_csv]
meta_file.close()
ID = [int(w[0]) for w in meta[1:]] # list of ID

########################################################
# Data conversion
########################################################

# compute mapping from n-gram ID to feature index

uni_id_str = ["%d-%04d"%(1,ii) for ii in range(1,num_unigram+1)]
bi_id_str = ["%d-%04d"%(2,ii) for ii in range(1,num_bigram+1)]
tri_id_str = ["%d-%04d"%(3,ii) for ii in range(1,num_trigram+1)]

fv_name = uni_id_str+bi_id_str+tri_id_str

# load n-gram feature file and convert it to sparse arff format

def ngram_csv2arff(file_name):
    f = open(file_name+'.csv','r')
    f_reader = csv.reader(f,delimiter = '\n')
    data = [w for w in f_reader]
    f.close()
    fv = [w[0].split(',')[1:] for w in data]        # feature vectors
    fv_id = [int(w[0].split(',')[0]) for w in data] # ID associated with fv
    # feature vector = [1-gram, 2-gram, 3-gram]
    index = [i for i in range(len(fv_id)) if fv_id[i] in ID]
    fv = [fv[i] for i in range(len(fv)) if i in index]
    fv_csv = []
    for row in fv:
        fv_temp = [0]*len(fv_name)
        for w in row:
            id = w[:6]
            count = w[7:]
            idx = fv_name.index(id)
            fv_temp[idx] = int(count)
            
        fv_csv.append(fv_temp)
    
    # write to a .csv file
    f = open(word_fv_file+'.csv','w')
    f_writer = csv.writer(f)
    fv_csv = [fv_name] + fv_csv
    # add joint profit to the last column of extracted feature
    meta_reader = csv.reader(open(meta_fv),delimiter = '\t')
    meta_data = [w for w in meta_reader]
    for i in range(len(fv_csv)):
        fv_csv[i] = fv_csv[i]+[meta_data[i][-1]]

    f_writer.writerows(fv_csv)
    f.close()
    
    # convert to arff file
    weka_cmd1 = 'java -cp weka.jar weka.core.converters.CSVLoader %s > %s' % (word_fv_file+'.csv', file_name+'_d.arff')
    # convert dense arff file to sparse arff
    weka_cmd2 = 'java -cp weka.jar weka.filters.unsupervised.instance.NonSparseToSparse -i %s -o %s' % (file_name+'_d.arff', word_fv_file+'.arff')
    os.system(weka_cmd1)
    os.system(weka_cmd2)
    
ngram_csv2arff(all_fv_file)
# ngram_csv2arff(groc_fv_file)
# ngram_csv2arff(wine_fv_file)


# cmd = 'cp %s > %s' % (all_fv_file+'_new.csv', word_fv_file+'.csv')
# os.system(cmd)    

