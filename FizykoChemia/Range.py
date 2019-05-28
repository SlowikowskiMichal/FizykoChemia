class Range:
	def __init__(self, start, end, formula):
		if end < start:
			self.start = end
			self.end = start
			self.formula = formula
		elif end == start:
			raise Exception('start and end of the range cannot be equal')
		else:
			self.start = start
			self.end = end
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
		
if __name__ == "__main__":
	r1 = Range(10, 20, "x*2")
	r2 = Range(30, 40, "x*2")
	r3 = Range(60, 100, "x*2")
	
	listOfRanges = [r1, r2, r3]
	listOfRanges = InsertNewRange(listOfRanges, Range(100, 200, "x"))
	
	for x in listOfRanges:
		print(x.start, x.end)
	
	
