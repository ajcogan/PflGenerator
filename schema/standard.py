
class PFLCreator():

    def selRtuCard(rtu, card):
        ## Selects and active RTU and Card (to then add points to)
        return [['3000'], [rtu], ['3103'], [card]]

    def addComment(comment):
        ## Adds a comment to PFL script
        return [['999'],[comment]]

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

if __name__ == "__main__":

    pass
