##
##      PFL and SCADAPack Config Generation
##
##      Ashley Cogan 26/04/18
##      Revision 2.0
##      Python 3.9
##
##      1.0 - Basic Concept
##      1.1 - Additional Layer of Abstraction
##      1.2 - Cleaned Up Functions
##      1.3 - Added scaling adjustment
##      1.4 - Added automatic file collating functions
##          - Made script work for multiple import files
##      1.5 - Time Stamping excecution of script
##          - Takes email as parameter for log file
##          - Take inverted status for Binary Inputs
##	    1.6 - Added Binary Counters Points to the CreatePoints function
##      1.7 - Modified ScadaPackParse() to also create link<AI/BI/CI> templates from RTU file
##          - Modified createMain() to produce new .sh files for seperating points creation and linking
##      1.8 - Added functionality to create cards along with points for new RTUs
##      2.0 - Refractored for Python3
##
##      Instructions:
##
##      -Place any file that creates points in root directory. Complete header information. Data must be of format <Index, Description> (see template for more info).
##          File must be labelled create%AI%.csv for analogue points and create%BI%.csv for binary points
##
##      -Place any file that breaks scan links in root directory. Complete header information. Data must be of format <Description, RowID, Component, Analog Raw Scan, ICCP Associated Value> (see template for more info).
##          File must be labelled break%AI%.csv for analogue points and break%BI%.csv for binary points
##
##      -Place any file that creates scan links in root directory. Complete header information. Data must be of format <Description, Component, Analog Raw Scan, ICCP Associated Value> (see template for more info).
##          File must be labelled link%AI%.csv for analogue points and link%BI%.csv for binary points
##
##      -Place any file that modifies component attributes. Complete header information (header info must match name of component attribute). Data must be of format <Description, Component, Old Param1, Old Param2, New Param1, New Param2> (see template for more info).
##          File must be labelled link%AI%.csv for analogue points and link%BI%.csv for binary points

import csv
import os
import datetime
# from os import path.basename as basename
# from easygui import msgbox
import sys

def indexConversion(index):
    return index/32, index%32

def cleaner(x):
    ## Takes a list of strings and returns the same list with all
    ## white space carriage return and new line characters removed
    y = []
    for i in x:
        y.append(i.strip())
    return y

def dataSeperator(data):
    ## Takes list of lines and returns as list of lists,
    ## data in usable format
    a = []
    for x in data:
        a.append(cleaner(x.split(',')))
    return a

def importData(fileName):
    ## Import and clean the RTU data from a csv file
    ## Input: fileName, Returns: A list of lines
    rawData = []
    dat = open(fileName,'r')
    for x in dat:
        rawData.append(x.strip('\n'))
    dat.close()
    return rawData

def printToCSV(data,svFile):
    ## General writer to CSV file
    with open(svFile, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                        quoting=csv.QUOTE_MINIMAL)
        for x in data:
            writer.writerow(x)
    csvfile.close()

def generalFileOut(data,svFile):
    ## Function for generally writing to output files
    with open(svFile, 'w') as the_file:
        for line in data:
            the_file.write(line[0] + "\n")
    the_file.close()

def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file

def cleanup(files,directory):
    ## Moves all files into specified directory after execution
    for file in files:
        os.rename("./"+file,"./"+directory+"/"+file)
        print(file)

def returnDT():
    ## Returns date and time in different formats
    now = datetime.datetime.now()
    date_string = now.strftime('%y%m%d_%H%M')
    date_sql = now.strftime('%Y-%m-%d %H:%M:%S')
    date_readable = now.strftime('%A, %d %B %Y @ %H:%M:%S')
    return date_string,date_sql,date_readable

def searchFor(part, whole):
    ## Searches if a string is contatained within another
    if part in whole:
        return True
    else:
        return False

def addRTUCard(rtu, cardType):
    ## Add new card based on cardType into selected RTU
    if cardType == 'AI':
        return [['3000'], [rtu], ['3100'], [0, 2, 'sDNP3 Anlogue Input']]
    elif cardType == 'BI':
        return [['3000'], [rtu], ['3100'], [0, 2, 'sDNP3 Digitial Input']]
    elif cardType == 'BO':
        return [['3000'], [rtu], ['3100'], [1, 2, 'sDNP3 Digitial Output']]
    elif cardType == 'CI':
        return [['3000'], [rtu], ['3100'], [0, 2, 'sDNP3 Binary Counter']]
    else:
        pass

def addAnalogueInput(index, description):
    ## PFL addition of Analogue Input (Card must be selected)
    return [['3201'], [30,0,0,index,0,0,32,0,description,description,'DNP Analog Input']]

def addBinaryInput(index, description):
    ## PFL addition of Binary Input (Card must be selected)
    j,k = indexConversion(int(index))
    return [['3201'], [1,0,0,j,0,0,1,k,description, description, 'DNP Digital Input']]

def addBinaryCounter(index, description):
    ## PFL addition of Binary Counter (Card must be selected)
    return [['3201'], [20,0,0,index,0,0,32,0,description,description,'DNP Analog Input']]

def addBinaryOutput(index, description):
    ## PFL addition of Binary Output (Card must be selected)
    return [['3300'], [12,1,0,index,0,0,description,'sDNP3 Control Plant']]

def addComment(comment):
    ## Adds a comment to PFL script
    return [['999'],[comment]]

def selRtuCard(rtu, card):
    ## Selects and active RTU and Card (to then add points to)
    return [['3000'], [rtu], ['3103'], [card]]

def endScript():
    ## Identifier for end of script
    return [['0'], ['ENDSEC']]

def delScanLink_RID(rowID, component, attribute,*associated):
    ## Delete a scan link base on row ID (Card must be selected)
    return [['3203'], [rowID], ['3501'], [component, attribute]+list(associated)]

def delScanLink_NAME(name, component, attribute, *associated):
     ## Delete a scan link base on link name (Card must be selected and name defined by user)
    return [['3202'], [name], ['3501'], [component, attribute]+list(associated)]

def newScanLink_RID(rowID, component, attribute, *associated):
    ## Add a scan link base on row ID (Card must be selected)
    return [['3203'],[rowID],['3500'],[component,attribute]+list(associated)]

def newScanLink_NAME(name, component, attribute, *associated):
    ## Add a scan link base on link name (Card must be selected and name defined by user)
    return [['3202'], [name], ['3500'], [component,attribute]+ list(associated)]

def updateAttribute(component,attribute,value):
    ## Modify the value of selected attribute of a component
    return [['1101'],[component],['2'],[attribute],['6'],[value]]

def updateProperty(name, propertyID, component, attribute):
    ## Modify the value of selected property of a scan link
    return [['3400'],[propertyID],['3202'],[name],['3402'],[component, attribute]]


def createPoints(createList):
##
##  Create Points
##

    output = []
    dataCorrect = True

    for fileName in createList:

        raw = dataSeperator(importData(fileName))
        header = raw[1]
        data = raw[4:]

        if header[0] == '': ## or header[1] == '':
            msgbox(msg='Please add RTU parameters to "' + fileName + '" before proceeding.', title='Import Error - Incomplete Data')
            dataCorrect = False
            break
        else:

            if searchFor('AI',fileName):
            ##  Addition Of Analogue Input Points
                output.extend(addComment('Addition Of Analogue Input Points from ' + fileName))
                output.extend(addRTUCard(header[0],'AI'))
                for point in data:
                    output.extend(addAnalogueInput(point[0],point[1]))
            elif searchFor('BI',fileName):
            ##  Addition Of Binary Input Points
                output.extend(addComment('Addition Of Binary Input Points from ' + fileName))
                output.extend(addRTUCard(header[0],'BI'))
                for point in data:
                    output.extend(addBinaryInput(point[0],point[1]))
                    try:
                        if point[2]=='y' or point[2]=='Y':
                            output.extend(updateProperty(point[1],'-8','scan config','WP_TELE_2STATE10'))
                        else:
                            pass
                    except IndexError:
                        pass
            elif searchFor('BO',fileName):
            ##  Addition Of Binary Output Points
                output.extend(addComment('Addition Of Binary Output Points from ' + fileName))
                output.extend(addRTUCard(header[0],'BO'))
                for point in data:
                    output.extend(addBinaryOutput(point[0],point[1]))
            elif searchFor('CI',fileName):
            ##  Addition Of Binary Counter Points
                output.extend(addComment('Addition Of Binary Counter Points from ' + fileName))
                output.extend(addRTUCard(header[0],'CI'))
                for point in data:
                    output.extend(addBinaryCounter(point[0],point[1]))

            else:
                pass

    if dataCorrect:
    ##  End of Script
        output.extend(addComment('End of Script'))
        output.extend(endScript())

        printToCSV(output,"pflFiles/main/createPoints.pfl")
    else:
        pass


def createLinker(breakList,linkList):
##
##  Break / Creating Links
##

    output = []
    dataCorrect = True

##  Breaking Links

    for fileName in breakList:

        raw = dataSeperator(importData(fileName))
        header = raw[1]
        data = raw[4:]

        if header[0] == '' or header[1] == '':
            msgbox(msg='Please add RTU and Card parameters to "' + fileName + '" before proceeding.', title='Import Error - Incomplete Data')
            dataCorrect = False
            break
        else:

            if searchFor('AI',fileName):
                output.extend(addComment('Breaking Links Analogue Inputs from ' + fileName))
                output.extend(selRtuCard(header[0],header[1]))
                for point in data:
                    try:
                        output.extend(delScanLink_RID(point[1],point[2],point[3],point[4]))
                    except IndexError:
                        output.extend(delScanLink_RID(point[1],point[2],point[3]))
            elif searchFor('BI',fileName):
                output.extend(addComment('Breaking Links Binary Inputs from ' + fileName))
                output.extend(selRtuCard(header[0],header[1]))
                for point in data:
                    try:
                        output.extend(delScanLink_RID(point[1],point[2],point[3],point[4]))
                    except IndexError:
                        output.extend(delScanLink_RID(point[1],point[2],point[3]))
            elif searchFor('CI',fileName):
                output.extend(addComment('Breaking Links Counter Inputs from ' + fileName))
                output.extend(selRtuCard(header[0],header[1]))
                for point in data:
                    try:
                        output.extend(delScanLink_RID(point[1],point[2],point[3],point[4]))
                    except IndexError:
                        output.extend(delScanLink_RID(point[1],point[2],point[3]))
            else:
                pass


##  Recreating Links

    for fileName in linkList:

        raw = dataSeperator(importData(fileName))
        header = raw[1]
        data = raw[4:]

        if header[0] == '' or header[1] == '':
            msgbox(msg='Please add RTU and Card parameters to "' + fileName + '" before proceeding.', title='Import Error - Incomplete Data')
            dataCorrect = False
            break
        else:

            if searchFor('AI',fileName):
                output.extend(addComment('Creating Links Analogue Inputs from ' + fileName))
                output.extend(selRtuCard(header[0],header[1]))
                for point in data:
                    try:
                        output.extend(newScanLink_NAME(point[0],point[1],point[2],point[3]))
                    except IndexError:
                        output.extend(newScanLink_NAME(point[0],point[1],point[2]))
            elif searchFor('BI',fileName):
                output.extend(addComment('Creating Links Binary Inputs from ' + fileName))
                output.extend(selRtuCard(header[0],header[1]))
                for point in data:
                    try:
                        output.extend(newScanLink_NAME(point[0],point[1],point[2],point[3]))
                    except IndexError:
                        output.extend(newScanLink_NAME(point[0],point[1],point[2]))
            elif searchFor('CI',fileName):
                output.extend(addComment('Creating Links Counter Inputs from ' + fileName))
                output.extend(selRtuCard(header[0],header[1]))
                for point in data:
                    try:
                        output.extend(newScanLink_NAME(point[0],point[1],point[2],point[3]))
                    except IndexError:
                        output.extend(newScanLink_NAME(point[0],point[1],point[2]))
            else:
                pass

    if dataCorrect:
    ##  End of Script
        output.extend(addComment('End of Script'))
        output.extend(endScript())

        printToCSV(output,"pflFiles/main/linker.pfl")
    else:
        pass

def createRollback(breakList,linkList):
##
##  Break / Creating Links (Revert/Backup)
##

    backup = []
    dataCorrect = True


##  Breaking Links
    for fileName in linkList:

        raw = dataSeperator(importData(fileName))
        header = raw[1]
        data = raw[4:]

        if header[0] == '' or header[1] == '':
            msgbox(msg='Please add RTU and Card parameters to "' + fileName + '" before proceeding.', title='Import Error - Incomplete Data')
            dataCorrect = False
            break
        else:

            if searchFor('AI',fileName):
                backup.extend(addComment('Breaking Links Analogue Inputs ' + fileName))
                backup.extend(selRtuCard(header[0],header[1]))
                for point in data:
                    try:
                        backup.extend(delScanLink_NAME(point[0],point[1],point[2],point[3]))
                    except IndexError:
                        backup.extend(delScanLink_NAME(point[0],point[1],point[2]))
            elif searchFor('BI',fileName):
                backup.extend(addComment('Breaking Links Binary Inputs ' + fileName))
                backup.extend(selRtuCard(header[0],header[1]))
                for point in data:
                    try:
                        backup.extend(delScanLink_NAME(point[0],point[1],point[2],point[3]))
                    except IndexError:
                        backup.extend(delScanLink_NAME(point[0],point[1],point[2]))
            elif searchFor('CI',fileName):
                backup.extend(addComment('Breaking Links Counter Inputs ' + fileName))
                backup.extend(selRtuCard(header[0],header[1]))
                for point in data:
                    try:
                        backup.extend(delScanLink_NAME(point[0],point[1],point[2],point[3]))
                    except IndexError:
                        backup.extend(delScanLink_NAME(point[0],point[1],point[2]))
            else:
                pass

##  Recreating Links
    for fileName in breakList:

        raw = dataSeperator(importData(fileName))
        header = raw[1]
        data = raw[4:]

        if header[0] == '' or header[1] == '':
            msgbox(msg='Please add RTU and Card parameters to "' + fileName + '" before proceeding.', title='Import Error - Incomplete Data')
            dataCorrect = False
            break
        else:

            if searchFor('AI',fileName):
                backup.extend(addComment('Creating Links Analoge Inputs ' + fileName))
                backup.extend(selRtuCard(header[0],header[1]))
                for point in data:
                    try:
                        backup.extend(newScanLink_RID(point[1],point[2],point[3],point[4]))
                    except IndexError:
                        backup.extend(newScanLink_RID(point[1],point[2],point[3]))
            elif searchFor('BI',fileName):
                backup.extend(addComment('Creating Links Binary Inputs ' + fileName))
                backup.extend(selRtuCard(header[0],header[1]))
                for point in data:
                    try:
                        backup.extend(newScanLink_RID(point[1],point[2],point[3],point[4]))
                    except IndexError:
                        backup.extend(newScanLink_RID(point[1],point[2],point[3]))
            elif searchFor('CI',fileName):
                backup.extend(addComment('Creating Links Counter Inputs ' + fileName))
                backup.extend(selRtuCard(header[0],header[1]))
                for point in data:
                    try:
                        backup.extend(newScanLink_RID(point[1],point[2],point[3],point[4]))
                    except IndexError:
                        backup.extend(newScanLink_RID(point[1],point[2],point[3]))
            else:
                pass

    if dataCorrect:
    ##  End of Script
        backup.extend(addComment('End of Script'))
        backup.extend(endScript())

        printToCSV(backup,"pflFiles/rollback/linker-rollback.pfl")
    else:
        pass


def attributeModifier(attributeModList):
##
##  Modifying component attributes
##

    output = []
    backup = []
    dataCorrect = True

    for fileName in attributeModList:

        raw = dataSeperator(importData(fileName))
        header = raw[0]
        data = raw[1:]

        output.extend(addComment('Modifying component attributes from ' + fileName))
        backup.extend(addComment('Modifying component attributes from ' + fileName))

        for comp in data:
            output.extend(updateAttribute(comp[1],comp[2],comp[4]))
            backup.extend(updateAttribute(comp[1],comp[2],comp[3]))

    if dataCorrect:
    ##  End of Script
        output.extend(addComment('End of Script'))
        output.extend(endScript())
        backup.extend(addComment('End of Script'))
        backup.extend(endScript())

        printToCSV(output,"pflFiles/main/attributeMod.pfl")
        printToCSV(backup,"pflFiles/rollback/attributeMod-rollback.pfl")
    else:
        pass

def createMain(emailAddr):
    ##
    ## Creates main.sh execution scripts that runs all the other scripts and generates log files
    ##
    createPts = [['#!/bin/bash'],['runTime="$(date +%d/%m/%Y%tat%t%H:%M:%S)"'],['load_plant_file -o3 createPoints.pfl 2>&1 | tee createPoints.log'],['cat *.log* | mail -s "$runTime PFL Script Log" ' +emailAddr]]

    linker = [['#!/bin/bash'],['runTime="$(date +%d/%m/%Y%tat%t%H:%M:%S)"'],['load_plant_file -o3 linker.pfl 2>&1 | tee linker.log'],['cat *.log* | mail -s "$runTime PFL Script Log" ' +emailAddr]]

    attribMod = [['#!/bin/bash'],['runTime="$(date +%d/%m/%Y%tat%t%H:%M:%S)"'],['load_plant_file -o3 attributeMod.pfl 2>&1 | tee attributeMod.log'],['cat *.log* | mail -s "$runTime PFL Script Log" ' +emailAddr]]

    output = [['#!/bin/bash'],['runTime="$(date +%d/%m/%Y%tat%t%H:%M:%S)"'],['load_plant_file -o3 createPoints.pfl 2>&1 | tee createPoints.log'],
              ['load_plant_file -o3 linker.pfl 2>&1 | tee linker.log'],['load_plant_file -o3 attributeMod.pfl 2>&1 | tee attributeMod.log'],['cat *.log* | mail -s "$runTime PFL Script Log" ' +emailAddr]]

    backup = [['#!/bin/bash'],['runTime="$(date +%d/%m/%Y%tat%t%H:%M:%S)"'],['load_plant_file -o3 linker-rollback.pfl 2>&1 | tee linker-rollback.log'],
              ['load_plant_file -o3 attributeMod-rollback.pfl 2>&1 | tee attributeMod-rollback.log'],['cat *.log* | mail -s "$runTime PFL Script Log" ' + emailAddr]]

    generalFileOut(createPts,"pflFiles/main/createPoints.sh")
    generalFileOut(linker,"pflFiles/main/linker.sh")
    generalFileOut(attribMod,"pflFiles/main/attribMod.sh")
    generalFileOut(output,"pflFiles/main/main.sh")
    generalFileOut(backup,"pflFiles/rollback/main-rollback.sh")

def generateLogFile():
    ##
    ## Generates log files
    ##
    output = []

    output.append(['PFL generated on ' + returnDT()[2] + ' using PFL generator script'])

    generalFileOut(output,"pflFiles/pflGenerator.log")
    generalFileOut(output,"dataFiles/pflGenerator.log")

def SCADAPackParse(deviceName, rtuAlias, aiCardID, biCardID, ciCardID):
    ##
    ## Pulls point data from SCADAPack RTU configuration file to form createList and linkList
    ##
    output = []

    raw = dataSeperator(importData(deviceName))
    header = raw[0:2]
    data = raw[3:]
    processing = [[]]
    pointer = 0

    cAI = [['RTU', 'CARD'],[rtuAlias,aiCardID],['',''],['Index', 'Description']]
    cBI = [['RTU', 'CARD'],[rtuAlias,biCardID],['',''],['Index', 'Description']]
    cCI = [['RTU', 'CARD'],[rtuAlias,ciCardID],['',''],['Index', 'Description']]
    cBO = [['RTU', 'CARD'],[rtuAlias,''],['',''],['Index', 'Description']]

    lAI = [['RTU', 'CARD'],[rtuAlias,aiCardID],['',''],['Description','Component','Attribute','Associated']]
    lBI = [['RTU', 'CARD'],[rtuAlias,biCardID],['',''],['Description','Component','Attribute','Associated']]
    lCI = [['RTU', 'CARD'],[rtuAlias,ciCardID],['',''],['Description','Component','Attribute','Associated']]
    lBO = [['RTU', 'CARD'],[rtuAlias,''],['',''],['Description','Component','Attribute','Associated']]

    for line in data:
        if line[0] == 'TE':
            processing.append([])
            pointer += 1
        else:
            if searchFor('PC',line[0]):
                processing[pointer].append(cleaner([line[0][:2],line[0][2:-2],line[0][-2:]]))
            else:
                processing[pointer].append([line[0]])

    for point in processing:

        try:
            point[0][0]

        except IndexError:
            pass
        else:
            print(point)
            if point[0][0] == 'PC' and point[0][1]!= '':
                if point[0][2] == 'AI':
                    cAI.append([point[1][0].split(" ")[1],point[0][1].strip('"')])
                    lAI.append([point[0][1].strip('"'),"",'Analog Raw Scan',""])
                elif point[0][2] == 'DI' and point[0][1].split("_")[2]!="SPARE":
                    cBI.append([point[1][0].split(" ")[1],point[0][1].strip('"')])
                    lBI.append([point[0][1].strip('"'),"",'Digital Scanned Value','Associated Scanned Value'])
                elif point[0][2] == 'CI':
                    cCI.append([point[1][0].split(" ")[1],point[0][1].strip('"')])
                    lCI.append([point[0][1].strip('"'),"",'Analog Raw Scan',""])
                elif point[0][2] == 'DO':
                    cBO.append([point[1][0].split(" ")[1],point[0][1].strip('"')])
                    lBO.append([point[0][1].strip('"'),"",'Digital Scanned Value','Associated Scanned Value'])
                else:
                    pass
            else:
                pass

    printToCSV(cAI,"createAI.csv")
    printToCSV(cBI,"createBI.csv")
    printToCSV(cCI,"createCI.csv")
##   printToCSV(cBO,"createBO.csv") ##Commented out as it is not required for IPP project

    printToCSV(lAI,"linkAI.csv")
    printToCSV(lBI,"linkBI.csv")
    printToCSV(lCI,"linkCI.csv")
##    printToCSV(lBO,"linkBO.csv") ##Commented out as it is not required for IPP project


def fileSorter():
##
##  File Sorter
##

    createList = []
    breakList = []
    linkList = []
    attributeModList = []
    csvList = []
    miscList = []

    fileNames = files('.')

    for name in fileNames:
        if searchFor('create',name) and searchFor('.csv',name):
            createList.append(name)
            csvList.append(name)
        elif searchFor('break',name) and searchFor('.csv',name):
            breakList.append(name)
            csvList.append(name)
        elif searchFor('link',name) and searchFor('.csv',name):
            linkList.append(name)
            csvList.append(name)
        elif searchFor('attributeMod',name) and searchFor('.csv',name):
            attributeModList.append(name)
            csvList.append(name)
        else:
            miscList.append(name)

    return createList,breakList,linkList,attributeModList,csvList,miscList


if __name__ == '__main__':
##
##      MAIN FUNCTION
##

    argList = sys.argv
    createList,breakList,linkList,attributeModList,csvList,miscList = fileSorter()

    if len(argList) == 1:
        print("\nUseage for PFLGenerator.py; \n\n \
    --scadaPackParse <filename> : Generate POF import tables from ScadaPack.rtu file \n \
    --generatePFL <email@address.com> : Generate PFL files from table information \n\n ")

    elif argList[1] == '--scadaPackParse':
        SCADAPackParse(argList[2],argList[3], argList[4], argList[5], argList[6])
        print("\n\nSCADAPack Parse Successful!!\n\n")

    elif argList[1] == '--genCreate':
        os.makedirs("pflFiles")
        os.makedirs("pflFiles/main")
        os.makedirs("pflFiles/rollback")
        os.makedirs("dataFiles")

        createPoints(createList)

        createMain(argList[2])

        cleanup(csvList,"dataFiles")

        generateLogFile()

        print("\n\nPFL Generaton Successful!!\n\n")

    elif argList[1] == '--genAll':
        os.makedirs("pflFiles")
        os.makedirs("pflFiles/main")
        os.makedirs("pflFiles/rollback")
        os.makedirs("dataFiles")


        createPoints(createList)
        createLinker(breakList,linkList)
        createRollback(breakList,linkList)
        attributeModifier(attributeModList)

        createMain(argList[2])

        cleanup(csvList,"dataFiles")

        generateLogFile()

        print("\n\nPFL Generaton Successful!!\n\n")
    else:
        print("\nUseage for PflGenerator.py; \n\n \
    --scadaPackParse <filename> : Generate POF import tables from ScadaPack.rtu file \n \
    --generatePFL <email@address.com> : Generate PFL files from table information \n\n ")
