import os
import csv
import re


def main():
    stack = []
    values = []
    rightPositions = [22,6,7,12,13,14,20,21,23,29,30,31,32,33,25,8,9,15,
16,17,24,26,27,34,35,36,37,55,44,45,46,47,54,56,57,63,64,65,70,71,
52,39,40,41,42,43,50,51,53,60,61,62,68,69]
    leftPositions = [25,9,8,17,16,15,27,26,24,38,37,36,35,34,22,7,6,14,
13,12,23,22,20,33,32,31,30,52,43,42,41,40,53,51,50,62,61,60,69,
68,55,48,47,46,45,44,57,56,54,65,64,63,70,71]
    with open(r"C:\Users\frazz\OneDrive\Documents\projectdata.csv") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        count = 0
        for row in readCSV:
            if(count != 2):
                count+=1
                raw = row[79]
                n = 2
                raw = str(raw)
                values = re.findall('..', raw)
                if(int(row[3])):
                    mapping = dict(zip(rightPositions, values))
                    print(mapping)
                    row[79] = mapping
                else:
                    mapping = dict(zip(leftPositions, values))
                    print(mapping)
                    row[79] = mapping
                writer = csv.writer(open(r"C:\Users\frazz\OneDrive\Documents\output.csv", 'w'))
                writer.writerows(row)

def check():
    with open(r"C:\Users\frazz\OneDrive\Documents\output.csv") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        count = 0
        for row in readCSV:
            if(count != 2):
                count+=1
                raw = row[0]
                

                    
                
                
                
            
