#!/usr/bin/python

import sys

# Clean up data

def usage():
    print "Usage:"
    print "   python "+sys.argv[0]+" [-ht] [-f featurelist]"
    print "      -h  (--help) Display this help and exit."
    print "      -t  (--tokenize) Tokenize data."
    print "      -f  (--features=) List of features to test."
    print "      -o  (--output=) Directory to put intermediate output in."
    print "          Final results will be in ../results."
    print "      -c  (--config=) Configuration file to use."


try:
    opts, args = getopt.getopt(sys.argv[1:],
                               "hf:to:",
                               ["help",
                                "features=",
                                "tokenize",
                                "output="])
except getopt.GetoptError:
    usage()
    sys.exit(2)

tokenize = False
features = []

for opt, arg in opts:
    if opt in ("-h", "--help"):
        usage()
        sys.exit()
    elif opt == '-t':
        tokenize = True
    elif opt in ("-f", "--features"):
        features = arg

# Extract features



# Run classification models


# Run regression models
