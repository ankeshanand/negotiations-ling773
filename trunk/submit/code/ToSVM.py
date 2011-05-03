# Convert .csv file to SVMlight (or libSVM) input file format 
import csv
import os


def CSV2SVMInput(csv_data, svm_file, fv_Index, target_Index, mapping):
    # csv_data: a list of list consisting of rows in .csv file to be converted to the format for SVM input
    # svm_file: svm input data file
    # fv_Index: the index of features that would be used for classification or regression
    # target_Index: the index of attribute that is class label or regression target
    # mapping: svm_file has float valued data, but in .csv file there may exists some nominal feature
    #          mapping is a dictionary that maps nominal value to corresponding float value
    svm_writer = csv.writer(svm_file,delimiter = ' ')
    numFv = len(fv_Index) # number of features
    # in csv_file '?' represents a missing attribute, but the SVM we use cannot handle missing value,
    # thus here we will remove samples with missing values
    for data in csv_data:
        data = [data[target_Index]]+[data[i] for i in fv_Index] # data =[target, fv1, fv2, ... fvn]
        if '?' in data: # if missing attributes exist
            continue
        
        if mapping!=[]:
            data = [w if w not in mapping.keys() else mapping[w] for w in data]
        
        data = [data[0]]+["%s:%s" % (x,data[x]) for x in range(1,len(data)) if float(data[x])!=0]
        svm_writer.writerow(data)


# read .csv file data
csv_file = open('../results/baseline_fv.csv','rb')
csv_reader = csv.reader(csv_file,delimiter = '\t')
csv_data = [w for w in csv_reader]
csv_file.close()
head = csv_data[0]
csv_data = csv_data[1:]

# information for preprocessing
target_Index = head.index('profit.joint')
fv_Index = [i for i in range(len(head)) if i not in [head.index('profit.diff'),head.index('ID'),head.index('profit.joint')]]
mapping = {'Graduate':1,'Undergraduate':-1,'yes':1,'no':-1,'True':1,'False':-1}

# create a .dat file as input for SVM
svm_file = open('../results/baseline_fv.dat','wb')
CSV2SVMInput(csv_data, svm_file, fv_Index, target_Index, mapping)
svm_file.close()

# using SVMlight
# '-x 1': leave one out cross-validation
# '-z r': regression
svm_cmd = 'svm_learn -x 1 -z r ../results/baseline_fv.dat ../results/baseline_svmlight_model'
os.system(svm_cmd)

# using libSVM
os.system('svm-scale -l -1 -u 1 -s range1 ../results/baseline_fv.dat > ../results/baseline_fv_scale.dat');
# -s    3 -- epsilon-SVR
#	4 -- nu-SVR
# -v 10 -- 10-fold cross-validation
os.system('svm-train -v 10 -s 3 ../results/baseline_fv_scale.dat')
