#!/usr/bin/python
import os
  
print "Run ./create_ngram.py"
e = os.system("python ./create_ngram.py");

print "Run ./process_ngram.py"
e = os.system("python ./process_ngram.py >& prg_log ");

print "Run ./code_based_feature.py"
e = os.system("python ./code_based_feature.py >& prg_log ");

print "Run ./dataset_split.py"
e = os.system("python ./dataset_split.py >& prg_log ");

