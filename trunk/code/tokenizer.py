#!/usr/bin/python
########################################################
# Name : tokenizer.py
# Desc : tokenizing for n-gram
#        make tokenized dialogs of Grocery, Wine, and Both 
########################################################
import csv
import re

########################################################
# Functions
########################################################
def subst_question_mark(match):
    s = match.group()
    if s[1:] in ["s", "t", "d", "re", "ll", "ve"]:
        return "'" + s[1:]
    else:
        return "? " + s[1:]

def subst_non_ascii(match):
    s = match.group()
    if s == '\x92':
        return "'"
    elif s == '\x85':
        return ' '
    else:
        return ''

# tokenize string
def tokenize( _str ) :
    # in the following substitituion, the sequence is important.
    ret = re.sub('\s*\?\s*', " ?  ", 

          re.sub('\-', " ...  ", 
          re.sub('\. ', " .  ", 
          re.sub('\s*\.\s*$', ". ", 
          re.sub('\.\.\.', "-", 

          re.sub('i\'m', "i 'm",
          re.sub(r'\bim\b', "i 'm",
          re.sub(r'i\? m', "i 'm", 
          re.sub('\'t', " 't", 
          re.sub('\'s', " 's", 
          re.sub('\'d', " 'd", 

          re.sub('\,\s*', " , ", 
          re.sub('\,$', "", 
          re.sub('^\,*\s*', "", 
          re.sub('["\x85\x91\x92\x93\x94\x96\xad\xe9]', subst_non_ascii,
          re.sub(r'\?[a-z]{1,2}', subst_question_mark, 
                  _str.lower()))))))))))))))))
    return ret

########################################################
# Main Proceduer
########################################################
# load data - using raw data
#data_file = open("../negotiation_corpus/merged_turns.csv",'r')
#data_csv = csv.reader(data_file,delimiter=',')
# load data - using cleaned data by Peng
data_file = open("../resources/fields_speaker.txt",'r')
data_csv = csv.reader(data_file,delimiter='\t')
data = [w for w in data_csv]
data_file.close()

# Make each dialog files for making n-grams
# open output files
dialog_grocery  = open('../results/dialog_grocery.txt','w')
dialog_wine     = open('../results/dialog_wine.txt','w')
dialog_all      = open('../results/dialog_all.txt','w')

# data [ dyID, ThUnit, Shop, Race, ANNO, Dialog ] 
for w in data :
    cl_str = tokenize(w[5])
    if re.search('\(even if two sbrs\)', cl_str) : continue
    elif w[2] == "Grocery" : dialog_grocery.write(cl_str)
    elif w[2] == "Wine" : dialog_wine.write(cl_str)
    else : print ">>>>ERROR:", w[2]
    #print cl_str # for debug
    dialog_all.write(cl_str)

dialog_grocery.close();
dialog_wine.close();
dialog_all.close();

exit(0)

