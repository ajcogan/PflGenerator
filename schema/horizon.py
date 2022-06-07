from standard import PFLCreator

class PFLCreator(PFLCreator):

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

if __name__ == "__main__":

    a = PFLCreator

    print(a.endScript())
