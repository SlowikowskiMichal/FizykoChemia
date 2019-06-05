from random import randint
from random import randrange
from sympy import symbols, Eq, solve, sympify
import operator

class Range:
	def __init__(self, min, max, start, end, formula, thermalEffect, name = "", methodId = 0):

		if end < start:
			self.start = end
			self.end = start
		else:
			self.start = start
			self.end = end

		if end == start:
			raise ValueError('Start and end of the range cannot be equal')
		
		if start < min or max < end:
			raise AssertionError('Start and end of the range cannot be equal')


		self.thermalEffect = thermalEffect
		self.formula = formula
		self.name = name
		self.methodId = methodId


def InsertNewRange(listOfRanges, newRange):
	isInserted = False
	index = 0

	if len(listOfRanges) == 0:
		listOfRanges.append(newRange)
		isInserted = True;
		index = 0;
	elif newRange.end <= listOfRanges[0].start:
		listOfRanges = [newRange] + listOfRanges
		index = 0;
	elif newRange.start >= listOfRanges[-1].end:
		listOfRanges += [newRange]
		isInserted = True;
		index = len(listOfRanges) - 1;
	else:
		for i in range(0, len(listOfRanges) - 1):
			if newRange.start >= listOfRanges[i].end and newRange.end <= listOfRanges[i + 1].start:
				listOfRanges[i+1:i+1] = [newRange]
				isInserted = True;
				index = i;
				break
	if isInserted == False:
		raise AssertionError('Given range overlaps with previously defined ranges')
	return listOfRanges, index

def RemoveRange(listOfRanges, rangeID):
    if(len(listOfRanges) > 1 and rangeID < len(listOfRanges)):
        del listOfRanges[rangeID]
    return listOfRanges

def SortRanges(listOfRanges):
    sortedListOfRanges = sorted(listOfRanges, KeyboardInterrupt=operator.attrgetter('start'))

def InsertThermalEffect(listOfPairs, rangeObject):
	placement = rangeObject.methodId
	if placement == 0:
		listOfPairs.append([rangeObject.start, rangeObject.thermalEffect])
	elif placement == 1:
		listOfPairs.append([rangeObject.end, rangeObject.thermalEffect])
	elif placement == 2:
		listOfPairs.append([round((rangeObject.end - rangeObject.start) * 0.5), rangeObject.thermalEffect])
	elif placement == 3:
		listOfPairs.append([rangeObject.start, rangeObject.thermalEffect * 0.5])
		listOfPairs.append([rangeObject.end, rangeObject.thermalEffect * 0.5])
	elif placement == 4:
		listOfPairs.append([rangeObject.start, rangeObject.thermalEffect / 3.0])
		listOfPairs.append([round((rangeObject.end + rangeObject.start) * 0.5), rangeObject.thermalEffect / 3.0])
		listOfPairs.append([rangeObject.end, rangeObject.thermalEffect / 3.0])
	elif placement == 5:
		sum = 0
		functionValuesList = []
		for i in range(int(rangeObject.end) - int(rangeObject.start)):
			#i = x - int(rangeObject.end)
			eq = sympify(rangeObject.formula.replace("x", str(i)))
			functionValuesList.append(eq)
			sum += eq
			print("X: {} = : {}".format(i,eq))        
		scale = rangeObject.thermalEffect / sum
		if abs(scale) < 0.00001:
		    raise Exception('Wrong equation')
		print("SUM: {},SCALE: {}".format(sum,scale))
		for i in range(int(rangeObject.end) - int(rangeObject.start)):
			listOfPairs.append([rangeObject.start + i, functionValuesList[i] * scale])
			
		
	#elif placement.lower() == 'random':
	#	iter = randrange(1, rangeObject.end - rangeObject.start + 1, 1)
	#	tempThermalEffect = rangeObject.thermalEffect/iter
	#	for x in range(0, iter, 1):
	#		randTemp = randrange(rangeObject.start, rangeObject.end + 1, 1)
	#		isFound = False
	#		if(x > 0):
	#			search = randTemp
	#			for sublist in listOfPairs:
	#				if sublist[0] == search:
	#					searchIndex = listOfPairs.index(sublist)
	#					listOfPairs[searchIndex][0] += tempThermalEffect
	#					isFound = True
	#					break
	#			if isFound == False:
	#				listOfPairs.append([randTemp, tempThermalEffect])
	#		else:
	#			listOfPairs.append([randTemp, tempThermalEffect])
	else:
		raise Exception('specified placement cannot be identified')
	return listOfPairs

def calculateFinalEntalphy(listOfTemp, listOfEntalphy, listOfPairs):
	toupleIndex = 0
	if listOfPairs:
	    print("JESTEM")
	    entalphyIndex = listOfTemp.index(listOfPairs[toupleIndex][0])
	    thermalEffectSum = 0
	    for i in range(entalphyIndex, len(listOfTemp)):
	    	if(toupleIndex < len(listOfPairs)):
	    		if listOfTemp[i] == listOfPairs[toupleIndex][0]:
	    			thermalEffectSum += listOfPairs[toupleIndex][1]
	    			listOfEntalphy[i] += thermalEffectSum
	    			toupleIndex += 1
	    		else:
	    			listOfEntalphy[i] += thermalEffectSum
	    	else:
	    		listOfEntalphy[i] += thermalEffectSum
	return listOfEntalphy

if __name__ == "__main__":
	r1 = Range(10, 20, "x+1", 20)
	r2 = Range(30, 33, "x+1", 300)
	r3 = Range(61, 67, "x+1", 155.4)
	
	listOfRanges = [r1, r2, r3]
	listOfRanges = InsertNewRange(listOfRanges, Range(100, 111, "x+1", 4.5))
	
	listOfTemp = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 29, 30, 31, 32, 33, 60, 61, 62, 63, 64, 65, 66, 67, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112]
	listOfEntl = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
	listOfPair = []
	for rangeItem in listOfRanges:
		listOfPair = InsertThermalEffect(listOfPair, rangeItem, 'equation')
	
	print('Temperature List')
	print(listOfTemp)
	print('Pair List')
	print(listOfPair)
	print('Entalphy List')
	print(listOfEntl)
	listOfEntl = calculateFinalEntalphy(listOfTemp, listOfEntl, listOfPair)
	print('New Entalphy')
	print(listOfEntl)
	
