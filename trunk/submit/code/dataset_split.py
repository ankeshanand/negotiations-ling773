# split all samples into training and testing set

import csv
import os
from global_variable import *
from operator import itemgetter, attrgetter


# combine all extracted feature into one file and split into training and testing part
# 1. code based feature
f1  = '../results/code_fv.csv'
f1_train = '../results/code_fv_train.csv'
f1_test = '../results/code_fv_test.csv'
# 2. word based feature
f2 = '../results/word_fv.csv'
f2_train = '../results/word_fv_train.csv'
f2_test = '../results/word_fv_test.csv'

# 3. meta info based feature
f3 = '../resources/meta_fv.csv'
f3_train = '../results/meta_fv_train.csv'
f3_test = '../results/meta_fv_test.csv'


# Split f1 and f2 into training and testing set
f1_reader = csv.reader(open(f1))
f2_reader = csv.reader(open(f2))
f3_reader = csv.reader(open(f3),delimiter = '\t')

data1 = [w for w in f1_reader]
data2 = [w for w in f2_reader]
data3 = [w for w in f3_reader]
h1 = data1[0]
h2 = data2[0]
h3 = data3[0]
data1_v = data1[1:]
data2_v = data2[1:]
data3_v = data3[1:]

data1_v = sorted(data1_v,key=itemgetter(-1))
data2_v = sorted(data2_v,key=itemgetter(-1))
data3_v = sorted(data3_v,key=itemgetter(-1))
# uniformly downsampling the sorted data to form a test set
idx = [1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53, 57]
data1_train = [data1_v[i] for i in range(61) if i not in idx]
data1_test = [data1_v[i] for i in range(61) if i in idx]
data2_train = [data2_v[i] for i in range(61) if i not in idx]
data2_test = [data2_v[i] for i in range(61) if i in idx]
data3_train = [data3_v[i] for i in range(61) if i not in idx]
data3_test = [data3_v[i] for i in range(61) if i in idx]

f = open(f1_train,'w')
f_w = csv.writer(f)
f_w.writerow(h1)
f_w.writerows(data1_train)
f.close()

f = open(f1_test,'w')
f_w = csv.writer(f)
f_w.writerow(h1)
f_w.writerows(data1_test)
f.close()


f = open(f2_train,'w')
f_w = csv.writer(f)
f_w.writerow(h2)
f_w.writerows(data2_train)
f.close()

f = open(f2_test,'w')
f_w = csv.writer(f)
f_w.writerow(h2)
f_w.writerows(data2_test)
f.close()

f = open(f3_train,'w')
f_w = csv.writer(f)
f_w.writerow(h3)
f_w.writerows(data3_train)
f.close()

f = open(f3_test,'w')
f_w = csv.writer(f)
f_w.writerow(h3)
f_w.writerows(data3_test)
f.close()

def csv2arff(f):
    # convert .csv file to .arff file
    weka_cmd1 = 'java -cp weka.jar weka.core.converters.CSVLoader %s > %s' % (f, f[:-4]+'_d.arff')
    # convert dense arff file to sparse arff
    weka_cmd2 = 'java -cp weka.jar weka.filters.unsupervised.instance.NonSparseToSparse -i %s -o %s' % (f[:-4]+'_d.arff', f[:-4]+'.arff')
    os.system(weka_cmd1)
    os.system(weka_cmd2)

csv2arff(f1_train)
csv2arff(f1_test)
csv2arff(f2_train)
csv2arff(f2_test)

csv2arff(f3_train)
csv2arff(f3_test)

