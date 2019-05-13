import loadData as loader
import matplotlib.pyplot as plot
import numpy as np
from multiprocessing import Process

def calculateE(tempList, dCList):
    resultList = []
    resultList.append((tempList[1]-tempList[0])*(dCList[0]+dCList[1])/2)

    for x in range (1,len(tempList)-1):
        resultList.append(resultList[x-1] + \
            (tempList[x+1]-tempList[x]) * \
            (dCList[x]+dCList[x+1])/2)
    
    resultList.append(resultList[len(resultList)-1])
    #print(resultList)

    return(resultList)

def interpolate(dataList):
    tempRange = range(int(dataList[0][0]),int(dataList[0][len(dataList[0])-1]))
    dCInterp = np.interp( \
        tempRange, \
        dataList[0],dataList[1])

    dataList[0] = tempRange
    dataList[1] = dCInterp
    return dataList

def drawPlot(x,y):
    plot.xlabel("Temp")
    plot.ylabel("Entalphy")
    plot.plot(x,y)
    plot.show()

if(__name__ == "__main__"):
    filename = "dane.txt"
    dataFolderPath = "resources/"
    path = dataFolderPath + filename
    
    dataList = loader.load(path)

    dataList = interpolate(dataList)

    resultList = calculateE(dataList[0],dataList[1])

    p = Process(target=drawPlot, args=(dataList[0],resultList))
    p.start()
    for x in range(len(dataList[0])): 
        print("Temp: {}\tdC: {}\t Result: {}".format(dataList[0][x],dataList[1][x],resultList[x]))
    p.join()
    