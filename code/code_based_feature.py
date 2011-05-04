#!/usr/bin/python
##########################################################
# Name : code_based_feature.py
# Desc : extract code based unigram and bigram feature
##########################################################

import csv
import math
import os
from global_variable import *

########################################################
# Load data
########################################################
# input:
# corpus_file and meta_info_file is defined in global_variable.py
meta_fv = meta_info_file
data_file = open(corpus_file,'r')
meta_file = open(meta_fv,'r')
# output: 
fv_file = code_fv_file

data_csv = csv.reader(data_file,delimiter='\t')
meta_csv = csv.reader(meta_file,delimiter='\t')
data = [w for w in data_csv]
meta = [w for w in meta_csv]
data_file.close()
meta_file.close()

ID = [w[0] for w in meta[1:]] # list of ID
code_seq = [w[4] for w in data] # sequence of code
code_unigram = list(set(code_seq)) # list of thought unit code
code_bigram = list(set([(code_seq[i],code_seq[i+1]) for i in range(0,len(code_seq)-1)]))

########################################################
# Functions
########################################################

def JS_divergence(P,Q):
    if len(P)!=len(Q):
        print 'Error! \n'
        return -1
    else:
        s = 0
        for i in range(len(P)):
            if P[i]!=0 and Q[i]!=0:
                s+=P[i]*math.log10(P[i]/float(Q[i]))+Q[i]*math.log10(Q[i]/float(P[i]))
        
        return s/2

########################################################
# Feature extraction
# features: number of thought unit, percentage of wine thought unit, percentage of grocery thought unit
# percentage of each code in entire dyad, in wine part, in grocery part
########################################################
fv_name = ['number-of-thought-unit','percentage-of-thought-unit-wine','percentage-of-thought-unit-grocery','wine-is-East-Asian']
# unigram feature
fv_name += ['percentage-of-(%s)-overall' % w for w in code_unigram]
fv_name += ['percentage-of-(%s)-wine' % w for w in code_unigram]
fv_name += ['percentage-of-(%s)-grocery' % w for w in code_unigram]

fv_name += ['number-of-(%s)-overall' % w for w in code_unigram]
fv_name += ['number-of-(%s)-wine' % w for w in code_unigram]
fv_name += ['number-of-(%s)-grocery' % w for w in code_unigram]

fv_name += ['unigram-JS-divergence-wine-vs-grocery']

# bigram feature
fv_name += ['number of turns']
fv_name += ['percentage-of-(%s-%s)-overall' % (w[0],w[1]) for w in code_bigram]
fv_name += ['percentage-of-(%s-%s)-wine' % (w[0],w[1]) for w in code_bigram]
fv_name += ['percentage-of-(%s-%s)-grocery' % (w[0],w[1]) for w in code_bigram]
fv_name += ['percentage-of-(%s-%s)-turns' % (w[0],w[1]) for w in code_bigram]

fv_name += ['number-of-(%s-%s)-overall' % (w[0],w[1]) for w in code_bigram]
fv_name += ['number-of-(%s-%s)-wine' % (w[0],w[1]) for w in code_bigram]
fv_name += ['number-of-(%s-%s)-grocery' % (w[0],w[1]) for w in code_bigram]
fv_name += ['number-of-(%s-%s)-turns' % (w[0],w[1]) for w in code_bigram]

fv_name += ['bigram-JS-divergence-wine-vs-grocery']
fv =[]


for key in ID:
    dyad = [w for w in data if w[0]==key]
    tu_list = [w[4] for w in dyad]
    tu_list_wine = [w[4] for w in dyad if w[2]=='Wine']
    tu_list_grocery = [w[4] for w in dyad if w[2]=='Grocery']
    bi_tu_list = [(tu_list[i],tu_list[i+1]) for i in range(0,len(tu_list)-1)]
    bi_tu_list_wine = [(tu_list_wine[i],tu_list_wine[i+1]) for i in range(0,len(tu_list_wine)-1)]
    bi_tu_list_grocery = [(tu_list_grocery[i],tu_list_grocery[i+1]) for i in range(0,len(tu_list_grocery)-1)]
    
    tu_turns = [dyad[i][4] for i in range(len(dyad)-1) if dyad[i][2]!=dyad[i+1][2]] # extract the turning point in the dyad
    bi_tu_list_turns = [(tu_turns[i],tu_turns[i+1]) for i in range(0,len(tu_turns)-1)]
    
    fv_c = [len(tu_list), len(tu_list_wine)/float(len(tu_list)), len(tu_list_grocery)/float(len(tu_list)),  'East Asian' in [w[3] for w in dyad if w[2]=='Wine']]
    # ------------Unigram feature------------
    # overall percentage
    fv_c += [len([a for a in tu_list if a==w])/float(len(tu_list)) if len([a for a in tu_list if a==w])!=0 else 0 for w in code_unigram]
    # wine dyad percentage
    wine_code_dist = [len([a for a in tu_list_wine if a==w])/float(len(tu_list_wine)) if len([a for a in tu_list if a==w])!=0 else 0 for w in code_unigram]
    fv_c += wine_code_dist
    # grocery dyad percentage
    groc_code_dist = [len([a for a in tu_list_grocery if a==w])/float(len(tu_list_grocery)) if len([a for a in tu_list if a==w])!=0 else 0 for w in code_unigram]
    fv_c += groc_code_dist
    # overall count
    fv_c += [len([a for a in tu_list if a==w]) if len([a for a in tu_list if a==w])!=0 else 0 for w in code_unigram]
    # wine dyad count
    wine_code_dist = [len([a for a in tu_list_wine if a==w]) if len([a for a in tu_list if a==w])!=0 else 0 for w in code_unigram]
    fv_c += wine_code_dist
    # grocery dyad count
    groc_code_dist = [len([a for a in tu_list_grocery if a==w]) if len([a for a in tu_list if a==w])!=0 else 0 for w in code_unigram]
    fv_c += groc_code_dist
    # JS divergence between grocery code distribution and wine code distribution
    fv_c +=[JS_divergence(wine_code_dist,groc_code_dist)]
    
    # ------------Bigram feature------------
    # number of turns
    fv_c += [len(tu_turns)]
    # overall percentage
    fv_c += [len([a for a in bi_tu_list if a==w])/float(len(bi_tu_list)) if len([a for a in bi_tu_list if a==w])!=0 else 0 for w in code_bigram]
    # wine dyad percentage
    wine_bicode_dist = [len([a for a in bi_tu_list_wine if a==w])/float(len(bi_tu_list_wine)) if len([a for a in bi_tu_list_wine if a==w])!=0 else 0 for w in code_bigram]
    fv_c += wine_bicode_dist
    # grocery dyad percentage
    groc_bicode_dist = [len([a for a in bi_tu_list_grocery if a==w])/float(len(bi_tu_list_grocery)) if len([a for a in bi_tu_list_grocery if a==w])!=0 else 0 for w in code_bigram]
    fv_c += groc_bicode_dist
    # turns percentage
    fv_c += [len([a for a in bi_tu_list_turns if a==w])/float(len(bi_tu_list_turns)) if len([a for a in bi_tu_list_turns if a==w])!=0 else 0 for w in code_bigram]
    
    # overall count
    fv_c += [len([a for a in bi_tu_list if a==w]) if len([a for a in bi_tu_list if a==w])!=0 else 0 for w in code_bigram]
    # wine dyad count
    fv_c += [len([a for a in bi_tu_list_wine if a==w]) if len([a for a in bi_tu_list_wine if a==w])!=0 else 0 for w in code_bigram]
    # grocery dyad count
    fv_c += [len([a for a in bi_tu_list_grocery if a==w]) if len([a for a in bi_tu_list_grocery if a==w])!=0 else 0 for w in code_bigram]
    # turns count
    fv_c += [len([a for a in bi_tu_list_turns if a==w]) if len([a for a in bi_tu_list_turns if a==w])!=0 else 0 for w in code_bigram]
    # JS divergence between grocery bigram distribution and wine bigram distribution
    fv_c +=[JS_divergence(wine_bicode_dist,groc_bicode_dist)]
    fv.append(fv_c)

########################################################
# Save feature vectors
########################################################
csv_file = open(fv_file+'.csv','w')
fv_file_writer = csv.writer(csv_file)
fv = [fv_name] + fv
# add joint-profit to the last element of the feature vector
meta_reader = csv.reader(open(meta_fv),delimiter = '\t')
meta_data = [w for w in meta_reader]
for i in range(len(fv)):
    fv[i] = fv[i]+[meta_data[i][-1]]

fv_file_writer.writerows(fv)
csv_file.close()

########################################################
# Data format conversion:
# convert .csv file to sparse arff format for weka
########################################################
# convert csv file to dense arff file



weka_cmd1 = 'java -cp weka.jar weka.core.converters.CSVLoader %s > %s' % (fv_file+'.csv', fv_file+'_d.arff')
# convert dense arff file to sparse arff
weka_cmd2 = 'java -cp weka.jar weka.filters.unsupervised.instance.NonSparseToSparse -i %s -o %s' % (fv_file+'_d.arff', fv_file+'.arff')
os.system(weka_cmd1)
os.system(weka_cmd2)









