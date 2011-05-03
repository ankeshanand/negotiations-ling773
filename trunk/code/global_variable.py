# global variables
# input: negotiation corpus and meta information
corpus_file = "../resources/fields_speaker.txt"
meta_info_file = "../resources/meta_fv.csv"

# features

# 1. meta information based feature
meta_fv_file = '../results/meta_fv'
meta_fv_file_s = '../results/meta_fv_s.arff'

# 2. code-based features
code_fv_file = '../results/code_fv'
code_fv_file_s = '../results/code_fv_s.arff'

# 3. word-based feature
all_fv_file = '../results/dialog_all_ngrams'
groc_fv_file = '../results/dialog_grocery_ngrams'
wine_fv_file = '../results/dialog_wine_ngrams'

all_fv_file_s = '../results/dialog_all_ngrams_s.arff'
groc_fv_file_s = '../results/dialog_grocery_ngrams_s.arff'
wine_fv_file_s = '../results/dialog_wine_ngrams_s.arff'



import os
# merge meta and word-based feature
meta_word_fv = '../results/meta_word_fv.arff'
cmd1 = 'java -cp weka.jar weka.core.Instances merge %s %s > %s' % (meta_fv_file_s, all_fv_file_s, meta_word_fv)
os.system(cmd1)

meta_code_fv = '../results/meta_code_fv.arff'
cmd2 = 'java -cp weka.jar weka.core.Instances merge %s %s > %s' % (meta_fv_file_s, code_fv_file_s, meta_code_fv)
os.system(cmd2)
