import os
import csv
import re

def extract(): 
     ##row 1 is test id
     ## row 2 is defect key
     ## row 3 is defect value
    with open(r"C:\Users\Not You\Desktop\projectdata.csv") as csvfile:
        ##Altitudinal defect 58
        ##hemifield defect - not included (not in 1 , 0 format. in 0.00)
        ##arcuatedefect upper 60
        ##temporalwedgedefect 62
        ##paracentraldefect 63
        ##peripherarimdefect 64
        ##partialperiopheralrimdefect 65
        ##BlindSpotDefect 67
        ##NasalStepDefect 72
        ##ArcuateDefectLower 82
        ##CentrealDefect  83
        ##Altitudinaldefectsuperior 85
        ## NasalStepDefectSuperior 88
        ## NasalStepDefectInferior 89
        ## VerticalStepNasalDefect 90
        ##VerticalstepTemporaldefect 91
        ## SupernasalDefect 92
        ##InferonasalDefect93
        ##SuperotemporalDefect 94
        ##InferotemporalDefect 95
        ##622 combinations of defects from 45000 patients - could possibly be 524288
        defectCount = 0;
        extractedData = []
        defectDic = {}
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            tempdata = []
            tempdata.append(row[0])
            result = str(row[58]) + str(row[60]) + str(row[62]) + str(row[63]) + str(row[64]) + str(row[65]) + str(row[67]) + str(row[72]) + str(row[82]) + str(row[83]) + str(row[85]) + str(row[88]) + str(row[89]) + str(row[90]) + str(row[91]) + str(row[92]) + str(row[93]) + str(row[94]) + str(row[95])
            if result in defectDic:
                tempdata.append(defectDic.get(result))
                tempdata.append(result)
            else:
                defectDic[result] = defectCount
                tempdata.append(defectCount)
                tempdata.append(result)
                defectCount+=1
            extractedData.append(tempdata)
        csvfile.close()
        return(extractedData)
def main(): 
    with open(r'C:\Users\Not You\Desktop\defects.csv', 'w', newline="") as writeFile: 
        writer = csv.writer(writeFile, delimiter = ',')
        rows = extract()
        writer.writerows(rows)
    writeFile.close()
                

                    
                
                
                
            

