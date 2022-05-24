##
##      A Simple tool for generating PFL file to import to POF
##      from a CSV dump of a SMP slave table from the RTU
##
##      Benjamin Ng 31/05/2018
##      Revision 0.1
##      Python 2.7
##      RTU Dump Version 7.1r2 or 7.1r3
##      
##
##      0.1 - Taken from Ashley Cohen's Version
##          - Added functionality to enter slave names
##          - Use PFL to create cards using RTU Alias

import csv
import sys
import os
from os.path import basename
from easygui import msgbox

def indexConversion(index):
    return index/32, index%32

def importRtu(fileName):

    ## Import and clean the RTU data from a csv file
    ## Input: fileName, Returns: A list of lines
    ## rawData[Line1,Line2, .....]

    rawData = []
    
    dat = file(fileName,'r')

    for x in dat:
        
        rawData.append(x.strip('\n'))

    return rawData

def dataSeperator(data):

    ## Takes list of lines and returns as list of lists,
    ## data in usable format
    ## a[Line1Word1,Line1Word2, .... ]

    a = []

    for x in data:
        a.append(x.split(','))

    return a

def createListFromStringMatch(file1, file2, slaveName, slaveDataType):

    ## Searches for the 

    with open(file1) as rtuConfig:
        with open(file2, "w") as slaveTable:
            for line in rtuConfig:
                if len(line.split(',')) > 1:
                    if slaveName in line.split(',', 2)[1]:
                        if slaveDataType in line.split(',', 1)[0]:
                            print line
                            slaveTable.write(line)
                    ##else:
                    ##    print slaveName
                    ##    msgbox(msg= slaveName + ' not found in ' + file1, title='List Create Error - No Slave Found')
                
def printToCSV(data,svFile):

    ## General writer to CSV file

    with open(svFile, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for x in data:
            spamwriter.writerow(x)


def addPfl(rtuAlias,dnpType,data,output):

    ## Adds binary outputs to the PFL file (data)
    rtuToSelect = '<Enter RTU Alias Here>'
    cardToSelect = '<Enter Card ID Here>'

    separatedData = dataSeperator(importRtu(data))                           
    if dnpType == 'BI' or dnpType == 'BO':
        pointList = [i[3] for i in separatedData]
        indexList = [i[6] for i in separatedData]
    elif dnpType == 'AI':
        pointList = [i[3] for i in separatedData]
        indexList = [i[8] for i in separatedData]
    
    output.append(['3000'])
    output.append([rtuAlias])
    	
    for i in range(len(pointList)):
        if dnpType == 'BI':
            if i==0:   	
                output.append(['3100'])
                output.append([0, 2, 'sDNP3 Digital Input'])

            j,k = indexConversion(int(indexList[i]))
            output.append(['3200'])
            output.append([1,0,0,j,0,0,1,k,pointList[i],'DNP Binary Input'])
            
        elif dnpType == 'BO':
            if i==0:   	
                output.append(['3100'])
                output.append([1, 2, 'sDNP3 Digital Output'])
                
            output.append(['3300'])
            output.append([12,1,0,indexList[i],0,0,pointList[i],'sDNP3 Control Plant'])
            
        elif dnpType == 'AI':
            #print (i)
            if i==0:   	
                output.append(['3100'])
                output.append([0, 2, 'sDNP3 Analog Input'])
            
            output.append(['3200'])
            output.append([30,0,0,indexList[i],0,0,32,0,pointList[i],'DNP Analog Input'])           

    output.append(['0'])
    output.append(['ENDSEC'])
    

##
##      MAIN FUNCTION
##
      
if __name__ == '__main__':

    ## Split the file into BI, BO and AI
	
    global indexlist
    indexlist = []
    argList = sys.argv

    if len(argList) == 1:
        print "\nUseage for pflGen.py; \n\n \
    --createPOF <RTU Name> <Slave Name> : Generate POF import tables from SMP RTU csv file \n\n "
    ## --generatePFL <email@address.com> : Generate PFL files from table information \n\n "

    elif argList[1] == '--createPOF':
        createListFromStringMatch('slaveTable.csv','BI.csv',argList[3],'SDNP3PFBI')
        createListFromStringMatch('slaveTable.csv','BO.csv',argList[3],'SDNP3PFBO')
        createListFromStringMatch('slaveTable.csv','AI.csv',argList[3],'SDNP3PFAI')

        BIdata = []
        BOdata = []
        AIdata = []
        
        addPfl(argList[2],'BI','BI.csv',BIdata)
        addPfl(argList[2],'BO','BO.csv',BOdata)
        addPfl(argList[2],'AI','AI.csv',AIdata)
    
        printToCSV(BIdata,'createBI.pfl')
        printToCSV(BOdata,'createBO.pfl')
        printToCSV(AIdata,'createAI.pfl')
    
    else:
        print "\nUseage for pflGen.py; \n\n \
    --createPOF <RTU Name> <Slave Name> : Generate POF import tables from SMP RTU csv file \n\n "
    ## --generatePFL <email@address.com> : Generate PFL files from table information \n\n "



