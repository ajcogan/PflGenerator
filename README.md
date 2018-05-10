# PflGenerator
This script generates PFL files for loading into PowerOn Fusion

##
##      PFL and SCADAPack Config Generation
##
##      Ashley Cogan 26/04/18
##      Python 2.7
##
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
