# baseline
import csv
import os

# load data
data_file = open("../resources/fields_speaker.txt",'r')
meta_file = open("../resources/meta_fv.txt",'r')

data_csv = csv.reader(data_file,delimiter='\t')
meta_csv = csv.reader(meta_file,delimiter='\t')

data = [w for w in data_csv]
meta = [w for w in meta_csv]
 
data_file.close()
meta_file.close()

# replace 'NA' with '?'
meta_new = []
for row in meta[1:]:
    row_new = [w if w!='NA' else '?' for w in row]
    meta_new.append(row_new)

# extract meta feature and write to a .csv file
csv_file = open('../results/meta_fv.csv','w')
head = meta[0] 
fv_file_writer = csv.writer(csv_file,delimiter = '\t', quoting=csv.QUOTE_NONE)
fv_file_writer.writerow(head) 
fv_file_writer.writerows(meta_new)
csv_file.close()

# Feature extraction
ID = [w[0] for w in meta[1:] if w[0] in [d[0] for d in data]]  # list of ID
code_set = list(set([w[4] for w in data])) # list of thought unit code
# -------Features based on meta data----------------
fv_dict = {}
head = meta[0] 
for key in ID:
    w = [w for w in meta_new if w[0]==key][0]
    fv_dict[w[0]] = {}
    for i in range(len(head)):
        fv_dict[w[0]][head[i]] = w[i]
    
# -------Features based on thought unit--------------
for key in ID:
    dyad = [w for w in data if w[0]==key]
    tu_list = [w[4] for w in dyad]
    tu_list_wine = [w[4] for w in dyad if w[2]=='Wine']
    tu_list_grocery = [w[4] for w in dyad if w[2]=='Grocery']
    # Feature: number of thought unit for each code
    fv_dict[key].update(dict([('number-of-(%s)-overall' % w, len([a for a in tu_list if a==w])) for w in code_set]))
    fv_dict[key].update(dict([('number-of-(%s)-wine' % w, len([a for a in tu_list_wine if a==w])) for w in code_set]))
    fv_dict[key].update(dict([('number-of-(%s)-grocery' % w, len([a for a in tu_list_grocery if a==w])) for w in code_set]))
    # Feature: number of thought unit
    fv_dict[key]['number-of-thought-unit'] = len(tu_list)
    fv_dict[key]['number-of-thought-unit-wine'] = len(tu_list_wine)
    fv_dict[key]['number-of-thought-unit-grocery'] = len(tu_list_grocery)
    # Feature: Is the Wine speaker East Asian?
    fv_dict[key]['wine-is-East-Asian'] = 'East Asian' in [w[3] for w in dyad if w[2]=='Wine']
    # Feature: percentage of thought unit for each code
    fv_dict[key].update(dict([('percentage-of-(%s)-overall' % w, len([a for a in tu_list if a==w])/float(len(tu_list))) for w in code_set]))
    fv_dict[key].update(dict([('percentage-of-(%s)-wine' % w, len([a for a in tu_list_wine if a==w])/float(len(tu_list_wine))) for w in code_set]))
    fv_dict[key].update(dict([('percentage-of-(%s)-grocery' % w, len([a for a in tu_list_grocery if a==w])/float(len(tu_list_grocery))) for w in code_set]))

csv_file = open('../results/baseline_fv.csv','w')
head = fv_dict[ID[0]].keys()
fv_file_writer = csv.writer(csv_file,delimiter = '\t', quoting=csv.QUOTE_NONE)
fv_file_writer.writerow(head)
for key in ID:
    fv_file_writer.writerow(fv_dict[key].values())
    
csv_file.close()


weka_cmd1 = 'java -cp weka.jar weka.core.converters.CSVLoader %s > %s' % ('../results/baseline_fv.csv', '../results/baseline_fv_d.arff')
# convert dense arff file to sparse arff
weka_cmd2 = 'java -cp weka.jar weka.filters.unsupervised.instance.NonSparseToSparse -i %s -o %s' % ('../results/baseline_fv_d.arff', '../results/baseline_fv.arff')
os.system(weka_cmd1)
os.system(weka_cmd2)
