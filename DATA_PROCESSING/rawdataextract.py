import os
import csv
import re

def extract(): ##match left eye, right eye positions with correct humphry values in a dictionary, such that a csv
                ## file can be made with the index representing position and the humphry value in the cell.
    extractedData = [] ## stores list of lists containing final humphry values in correct positions
    values = [] 
    rightPositions = [22,6,7,12,13,14,20,21,23,29,30,31,32,33,25,8,9,15,
16,17,24,26,27,34,35,36,37,55,44,45,46,47,54,56,57,63,64,65,70,71,
52,39,40,41,42,43,50,51,53,60,61,62,68,69]
    leftPositions = [25,9,8,17,16,15,27,26,24,38,37,36,35,34,22,7,6,14,
13,12,23,22,20,33,32,31,30,52,43,42,41,40,53,51,50,62,61,60,69,
68,55,48,47,46,45,44,57,56,54,65,64,63,70,71]
    with open(r"C:\Users\Not You\Desktop\projectdata.csv") as csvfile:  
        readCSV = csv.reader(csvfile, delimiter=',')
        count = 0
        for row in readCSV:
            count+=1
            raw = row[79]
            n = 2
            raw = str(raw)
            values = re.findall('..', raw) ## converts raw values into a list of double digit numbers (as strings temporarily)
            for i in range(0,len(values)):
                values[i] = int(values[i]) ##converts all values back to integer from string
            if(int(row[3])): ##is right eye
                mapping = dict(zip(rightPositions, values))
            else: ##is left eye
                mapping = dict(zip(leftPositions, values))
            templist = []
            for i in range (0, 77):
                templist.append(mapping.get(i, "-")) ##creates list of humphry values in its corresponding position as the
                                                    ##index of the list, if there is no value in the index position, -
            extractedData.append(templist)
        csvfile.close()
        return(extractedData)
def main(): ## simply run main() and change the filepaths, to the filepaths on your machine.
            ##Make sure to create an output.csv and copy the location into the below write command below this.
    with open(r'C:\Users\Not You\Desktop\output.csv', 'w', newline="") as writeFile: 
        writer = csv.writer(writeFile, lineterminator = '\n')
        rows = extract()
        writer.writerows(rows)
    writeFile.close()
                

                    
                
                
                
            
