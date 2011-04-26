#!/usr/bin/python
########################################################
# Name : tokenizer.py
# Desc : tokenizing for n-gram
#        make tokenized dialogs of Grocery, Wine, and Both 
########################################################
import csv
import re
import os

########################################################
# Global Variables
########################################################
fields_data = ''
dyID_List = []
res_dirname = "../results/"
dest_dirname = "../results/ngrams/"
dialog_allname = dest_dirname+"dialog_all.txt" 
unigram_ids = {}
bigram_ids = {}
trigram_ids = {}

########################################################
# Functions
########################################################
def initialize():
    global dest_dirname
    print "initialize"
    dst_dir = os.path.dirname(dest_dirname)
    if not os.path.exists(dst_dir) :
        print "create ngram directory"
        os.makedirs(dst_dir)
    else : 
        print "reset ngram directory"
        os.system('rm -rf '+dest_dirname+"*")


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
    ret = re.sub('\? \.  $', " ?  ",
          re.sub('\.*\s*$', " .  ", 
          re.sub('\s*\?\s*', " ?  ", 

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
          re.sub('^\,*\s*', "", 
          re.sub('["\x85\x91\x92\x93\x94\x96\xad\xe9]', subst_non_ascii,
          re.sub(r'\?[a-z]{1,2}', subst_question_mark, 
                  _str.lower())))))))))))))))))
    return ret

# load raw data and create tokenized dialog for creating ID of ngrams
def make_whole_dialogs() :
    global fields_data

    #data_file = open("../negotiation_corpus/merged_turns.csv",'r')
    #data_csv = csv.reader(data_file,delimiter=',')
    data_file = open("../resources/fields_speaker.txt",'r')
    data_csv = csv.reader(data_file,delimiter='\t')
    fields_data = [w for w in data_csv]
    data_file.close()

    # Make each dialog files for making n-grams
    # open output files
    dialog_grocery  = open('../results/ngrams/dialog_grocery.txt','w')
    dialog_wine     = open('../results/ngrams/dialog_wine.txt','w')
    dialog_all      = open(dialog_allname, 'w')

    # data [ dyID, ThUnit, Shop, Race, ANNO, Dialog ] 
    for w in fields_data :
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

    return

# create each dyID files
def make_dyid_dialogs() :
    global fields_data, dyID_List
    dyID = -1; 

    for w in fields_data :
        cl_str = tokenize(w[5])
        if int(w[0]) != dyID : 
            # close previous dyID file
            if dyID != -1 : dyid_grocery.close(); dyid_wine.close(); dyid_all.close()

            dyID = int(w[0]) # new start
            dyID_List.append(dyID)
            # open new dyID file
            dyid_grocery = open('../results/ngrams/%02d_grocery.txt'%(dyID), "w")
            dyid_wine    = open('../results/ngrams/%02d_wine.txt'%(dyID), "w")
            dyid_all     = open('../results/ngrams/%02d_all.txt'%(dyID), "w")

        if re.search('\(even if two sbrs\)', cl_str) : continue
        elif w[2] == "Grocery" : dyid_grocery.write(cl_str)
        elif w[2] == "Wine" : dyid_wine.write(cl_str)
        else : print ">>>>ERROR:", w[2]
        #print cl_str # for debug
        dyid_all.write(cl_str)
    
    dyid_grocery.close(); dyid_wine.close(); dyid_all.close()
    return

def count_ngrams():
    global dyID_List

    # create ngram with all dialog 
    for i in range(1,4):
        print "Create %d-gram for Whole dialogs"%i
        cmd_ngram = "count.pl --ngram %d --stop stop-word.txt "%i+ \
                    dialog_allname+".%d"%i+" "+dialog_allname
        #print cmd_ngram
        os.system(cmd_ngram)

    # count ngrams with each dyads
    for i in range(1,4):
        print "Create %d-gram for each dialog"%i
        for dyID in dyID_List :
            cmd_ngram = "count.pl --ngram %d --stop stop-word.txt "%i \
                       +dest_dirname+"%02d_all.txt.%d "%(dyID,i) \
                       +dest_dirname+"%02d_all.txt"%(dyID)
            #print cmd_ngram
            os.system(cmd_ngram)

            cmd_ngram = "count.pl --ngram %d --stop stop-word.txt "%i \
                       +dest_dirname+"%02d_wine.txt.%d "%(dyID,i) \
                       +dest_dirname+"%02d_wine.txt"%(dyID)
            #print cmd_ngram
            os.system(cmd_ngram)

            cmd_ngram = "count.pl --ngram %d --stop stop-word.txt "%i \
                       +dest_dirname+"%02d_grocery.txt.%d "%(dyID,i) \
                       +dest_dirname+"%02d_grocery.txt"%(dyID)
            #print cmd_ngram
            os.system(cmd_ngram)
    return

def create_ngram_files() :
    create_ngram_file_catetory("all")
    create_ngram_file_catetory("wine")
    create_ngram_file_catetory("grocery")
    return

def create_ngram_file_catetory( category ) :
    global dyID_List
    
    outfilename = res_dirname+"dialog_"+category+"_ngrams.cvs"
    outfd = open( outfilename, "w")

    for dyID in dyID_List:
        outfd.write("%02d"%dyID)
        for i in range(1,4):
            ngram_filename = dest_dirname+"%02d_%s.txt.%d"%(dyID,category,i)
            infd = open(ngram_filename,'r')
            allLines = infd.readlines()
            infd.close();
            #print ngram_filename

            for oneLine in allLines :
                m = re.match("^(.*<>)+(\d+)",oneLine)
                if m :
                    if i == 1 : 
                        #print unigram_ids[m.group(1)] +":"+m.group(2)
                        outfd.write(','+ unigram_ids[m.group(1)] +":"+m.group(2))
                    elif i == 2 :
                        #print bigram_ids[m.group(1)] +":"+m.group(2)
                        outfd.write(','+ bigram_ids[m.group(1)] +":"+m.group(2))
                    elif i == 3 :
                        #print trigram_ids[m.group(1)] +":"+m.group(2)
                        outfd.write(','+ trigram_ids[m.group(1)] +":"+m.group(2))
        outfd.write("\n")
    outfd.close()

def create_ngram_ids():
    global unigram_ids, bigram_ids, trigram_ids

    #load ngram files and make id dictionary
    for i in range(1,4):
        fdin = open(dialog_allname+".%d"%i,'r')
        allLines = fdin.readlines()
        fdin.close()

        fdout = open(res_dirname+"%d_gram_ids.txt"%i,'w')

        ii = 0; id_str = ''
        for oneLine in allLines :
            m = re.match("^(.*<>)+(\d+)",oneLine)
            if m :
                #print  m.group(1), m.group(2)
                ii+=1; id_str = "%d-%04d"%(i,ii)
                if i == 1 : unigram_ids[m.group(1)] = id_str
                elif i == 2 : bigram_ids[m.group(1)] = id_str 
                elif i == 3 : trigram_ids[m.group(1)] = id_str
                fdout.write(id_str+" "+re.sub('<>', ' ', m.group(1))+"\n")
            #else : print "error", oneLine

        # write id contents
        fdout.close()

########################################################
# Main Proceduer
########################################################
initialize()
make_whole_dialogs()
make_dyid_dialogs()
count_ngrams()
create_ngram_ids()
create_ngram_files()

exit(0)

