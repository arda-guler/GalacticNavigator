# reads star data from HYG catalog file
import csv
from star import *

def read_data(filename):
    filename = "data/" + filename

    file = open(filename, "r")
    csvFile = csv.reader(file)

    data = []

    # the first line is just the headers, not a star
    i = 0
    for line in csvFile:
        if i > 0:
            new_star = star(*line)
            data.append(new_star)
        i += 1

##    spectrals = []
##    for stara in data:
##        if stara.spect and not stara.spect[0] in spectrals:
##            spectrals.append(stara.spect[0])
##
##    print(spectrals)

    return data
