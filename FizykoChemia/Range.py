from random import randint
from random import randrange

class Range:
	def __init__(self, start, end, formula, thermalEffect):
		if end < start:
			self.start = end
			self.end = start
		elif end == start:
			raise Exception('start and end of the range cannot be equal')
		else:
			self.start = start
			self.end = end
		self.thermalEffect = thermalEffect
		self.formula = formula
	
def InsertNewRange(listOfRanges, newRange):
	isInserted = False
	if len(listOfRanges) == 0:
		listOfRanges.append(newRange)
		isInserted = True;
	elif newRange.end <= listOfRanges[0].start:
		listOfRanges = [newRange] + listOfRanges
		isInserted = True;
	elif newRange.start >= listOfRanges[len(listOfRanges) - 1].end:
		listOfRanges += [newRange]
		isInserted = True;
	else:
		for i in range(0, len(listOfRanges) - 1):
			if newRange.start >= listOfRanges[i].end and newRange.end <= listOfRanges[i + 1].start:
				listOfRanges[i+1:i+1] = [newRange]
				isInserted = True;
				break
	if isInserted == False:
		raise Exception('given range overlaps with previously defined ranges')
	return listOfRanges

def InsertThermalEffect(listOfPairs, rangeObject, placement):
	if placement.lower() == 'start':
		listOfPairs.append((rangeObject.start, rangeObject.thermalEffect))
	elif placement.lower() == 'end':
		listOfPairs.append((rangeObject.end, rangeObject.thermalEffect))
	elif placement.lower() == 'middle':
		listOfPairs.append((round((rangeObject.end - rangeObject.start)*0.5), rangeObject.thermalEffect))
	elif placement.lower() == 'both':
		listOfPairs.append((rangeObject.start, rangeObject.thermalEffect * 0.5))
		listOfPairs.append((rangeObject.end, rangeObject.thermalEffect * 0.5))
	elif placement.lower() == 'triple':
		listOfPairs.append((rangeObject.start, rangeObject.thermalEffect/3.0))
		listOfPairs.append((round((rangeObject.end - rangeObject.start)*0.5), rangeObject.thermalEffect/3.0))
		listOfPairs.append((rangeObject.end, rangeObject.thermalEffect/3.0))
	elif placement.lower() == 'random':
		iter = randrange(1, rangeObject.end - rangeObject.start + 1, 1)
		tempThermalEffect = rangeObject.thermalEffect/iter
		for x in range(0, iter, 1):
			listOfPairs.append((rangeObject.start, rangeObject.end + 1, 1), tempThermalEffect)
	else:
		raise Exception('specified placement cannot be identified')
	return listOfPairs

def calculateFinalEntalphy(listOfTemp, listOfEntalphy, listOfPairs):
	toupleIndex = 0
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
	r1 = Range(10, 20, "x*2", 20)
	r2 = Range(30, 33, "x*2", 300)
	r3 = Range(61, 67, "x*2", 155.4)
	
	listOfRanges = [r1, r2, r3]
	listOfRanges = InsertNewRange(listOfRanges, Range(100, 111, "x", 4.5))
	
	listOfTemp = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 29, 30, 31, 32, 33, 60, 61, 62, 63, 64, 65, 66, 67, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112]
	listOfEntl = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
	listOfPair = []
	for rangeItem in listOfRanges:
		listOfPair = InsertThermalEffect(listOfPair, rangeItem, 'end')
	
	#print(listOfPair)
	print('Temperature List')
	print(listOfTemp)
	print('Pair List')
	print(listOfPair)
	print('Entalphy List')
	print(listOfEntl)
	listOfEntl = calculateFinalEntalphy(listOfTemp, listOfEntl, listOfPair)
	print('New Entalphy')
	print(listOfEntl)
	
