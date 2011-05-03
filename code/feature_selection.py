# feature selection
# and split data into training and testing set
import csv
import re
import os
from global_variable import *
from operator import itemgetter, attrgetter

# combine all extracted feature into one file and split into training and testing part
# 1. code based feature
f1  = '../results/code_fv.csv'
# 2. word based feature
f2 = '../results/word_fv.csv'
# 3. meta feature
f3 = '../results/meta.csv'
# Feature selection result from weka
meta_word_fv_f = '../results/fv_best_first_search_meta_ngramall.txt'
meta_code_fv_f = '../results/fv_best_first_search_meta_codefv.txt'


f1_reader = csv.reader(open(f1))
f2_reader = csv.reader(open(f2))
f3_reader = csv.reader(open(f3),delimiter = '\t')

data1 = [w for w in f1_reader]
data2 = [w for w in f2_reader]
data3 = [w for w in f3_reader]



def printbestfv(file,N):
    f = open(file,'r')
    f_reader = csv.reader(f)
    data = [w for w in f_reader]
    data = [d[0] for d in data if len(d)!=0 and d[0][0]!='#']
    fv_weight = [(data[i].split(' ')[-1],int(re.search('[0-9]+.%',data[i]).group(0)[:-1])) for i in range(len(data))]
    fv_weight = sorted(fv_weight,key=itemgetter(1),reverse=True)
    fv_name = []
    for i in range(N):
        fv_name.append(fv_weight[i][0])
        print fv_weight[i][0], ' \n'
    
    f.close()
    return fv_name

fv_name_1 = printbestfv(meta_code_fv_f,30)
fv_name_2 = printbestfv(meta_word_fv_f,30)

# combine the best features from two differernt set
h1 = data1[0]
h2 = data2[0]

idx1 = [i for i in range(len(h1)) if h1[i] in fv_name_1]
idx2 = [i for i in range(len(h2)) if h2[i] in fv_name_2]

data1_s = [[w[j] for j in idx1] for w in data1]
data2_s = [[w[j] for j in idx2] for w in data2]

# load meta data



fv_all = [[]]*len(data3)

for i in range(len(data3)):
    print i
    fv_all[i] = data1_s[i]+ data2_s[i]+ data3[i]
    
all_fv_f = '../results/all_fv_N30'
f = open(all_fv_f+'.csv','w')
f_writer = csv.writer(f)
f_writer.writerows(fv_all)
f.close()

weka_cmd = 'java -cp weka.jar weka.core.converters.CSVLoader %s > %s' % (all_fv_f+'.csv', all_fv_f+'.arff')
os.system(weka_cmd)

