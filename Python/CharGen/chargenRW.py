from dataclasses import replace
import re


def chargen(instr):
    numsList = []
    outputList = []
    count = 0


    getValuesRE = re.compile('{[^}]+}')
    valuesInstr = getValuesRE.findall(instr)
    for value in valuesInstr:
        x = "," in str(value)
        if x == True:
            print("Comming Soon..")
        else:
            getNumRE = re.compile('[0-9]+')
            nums = getNumRE.findall(value)
            for num in nums:
                numsList.append(int(num))
        
            count = numsList[0]
            while count <= numsList[1]:
                stringt = str(count)

                output = re.sub('{[^}]+}', stringt, instr, 1)
                outputList.append(output)
                count = count + 1

        #print(outputList)    
        #print(numsList)
    for x in range(len(outputList)):
        print(outputList[x])
    
    
    
    #print(p1.search('{[^}]+}', instr))
    #print(instr)