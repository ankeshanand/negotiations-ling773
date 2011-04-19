#!/bin/bash
# This script uses "count.pl" in the Ted Pedersen's Ngram Statistics Package.
# So, it should be installed before running this script
# In addition, "bin" direcotry of the package should be added in "PATH"
# environment variable
# This script need to be run in the directory containing dialog_all.txt, 
# dialog_grocery.txt, and dialog_wine.txt, which are the result of tokenizer.py script

# Creating n-grams for whole dialogs
count.pl --ngram 1 --stop stop-word.txt dialog_all.uni dialog_all.txt
count.pl --ngram 2 --stop stop-word.txt dialog_all.bi dialog_all.txt
count.pl --ngram 3 --stop stop-word.txt dialog_all.tri dialog_all.txt

# Creating n-grams for grocery dialogs
count.pl --ngram 1 --stop stop-word.txt dialog_grocery.uni dialog_grocery.txt
count.pl --ngram 2 --stop stop-word.txt dialog_grocery.bi dialog_grocery.txt
count.pl --ngram 3 --stop stop-word.txt dialog_grocery.tri dialog_grocery.txt

# Creating n-grams for wine dialogs
count.pl --ngram 1 --stop stop-word.txt dialog_wine.uni dialog_wine.txt
count.pl --ngram 2 --stop stop-word.txt dialog_wine.bi dialog_wine.txt
count.pl --ngram 3 --stop stop-word.txt dialog_wine.tri dialog_wine.txt

