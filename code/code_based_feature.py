#!/usr/bin/python
##########################################################
# Name : code_based_feature.py
# Desc : extract code based unigram and bigram feature
##########################################################

import csv
import math
import os

########################################################
# Load data
########################################################
data_file = open("../resources/fields_speaker.txt",'r')
meta_file = open("../resources/meta_fv.csv",'r')

data_csv = csv.reader(data_file,delimiter='\t')
meta_csv = csv.reader(meta_file,delimiter='\t')
data = [w for w in data_csv]
meta = [w for w in meta_csv]
data_file.close()
meta_file.close()

ID = [w[0] for w in meta[1:]] # list of ID
code_set = list(set([w[4] for w in data])) # list of thought unit code

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
fv_name += ['percentage-of-(%s)-overall' % w for w in code_set]
fv_name += ['percentage-of-(%s)-wine' % w for w in code_set]
fv_name += ['percentage-of-(%s)-grocery' % w for w in code_set]
fv_name += ['JS-divergence']

fv =[]

for key in ID:
    dyad = [w for w in data if w[0]==key]
    tu_list = [w[4] for w in dyad]
    tu_list_wine = [w[4] for w in dyad if w[2]=='Wine']
    tu_list_grocery = [w[4] for w in dyad if w[2]=='Grocery']
    fv_c = [len(tu_list), len(tu_list_wine)/float(len(tu_list)), len(tu_list_grocery)/float(len(tu_list)),  'East Asian' in [w[3] for w in dyad if w[2]=='Wine']]
    # overall percentage
    fv_c += [len([a for a in tu_list if a==w])/float(len(tu_list)) if len([a for a in tu_list if a==w])!=0 else 0 for w in code_set]
    # wine dyad percentage
    wine_code_dist = [len([a for a in tu_list_wine if a==w])/float(len(tu_list_wine)) if len([a for a in tu_list if a==w])!=0 else 0 for w in code_set]
    fv_c += wine_code_dist
    # grocery dyad percentage
    groc_code_dist = [len([a for a in tu_list_grocery if a==w])/float(len(tu_list_grocery)) if len([a for a in tu_list if a==w])!=0 else 0 for w in code_set]
    fv_c += groc_code_dist
    # JS divergence between grocery code distribution and wine code distribution
    fv_c +=[JS_divergence(wine_code_dist,groc_code_dist)]
    fv.append(fv_c)

########################################################
# Save feature vectors
########################################################
fv_file = '../results/unigram_code_fv'

csv_file = open(fv_file+'.csv','w')
fv_file_writer = csv.writer(csv_file)
fv_file_writer.writerow(fv_name)
fv_file_writer.writerows(fv)
csv_file.close()

########################################################
# Data format conversion:
# convert .csv file to sparse arff format for weka
########################################################
# convert csv file to dense arff file

weka_cmd1 = 'java -cp weka.jar weka.core.converters.CSVLoader %s > %s' % (fv_file+'.csv', fv_file+'_d.arff')
# convert dense arff file to sparse arff
weka_cmd2 = 'java -cp weka.jar weka.filters.unsupervised.instance.NonSparseToSparse -i %s -o %s' % (fv_file+'_d.arff', fv_file+'_s.arff')
os.system(weka_cmd1)
os.system(weka_cmd2)


