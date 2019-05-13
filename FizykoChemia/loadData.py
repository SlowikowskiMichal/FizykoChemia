from bisect import bisect
import numpy as np

def insert(list, n, index):
	list.insert(index, n)
	return list
	
def check_temp(temperature_array, changes_num):
	for i in range(changes_num):
		a = float(input("Poczatek przedzialu: "))
		b = float(input("Koniec przedzialu: "))
		
		if a in temperature_array:
			index_a = temperature_array.index(a)
			if b in temperature_array:
				raise Exception("Podane temperatury sa juz zdefiniowane")
			else:
				index_b = bisect(temperature_array, b)
				if index_b - index_a != 1:
					raise Exception("Podany przedzial pokrywa sie ze zdefiniowanymi juz temperaturami")
				else:
					insert(temperature_array, b, index_b)
		else:
			index_a = bisect(temperature_array, a)
			if b in temperature_array:
				index_b = temperature_array.index(b)
				if index_b - index_a != 0:
					raise Exception("Podany przedzial pokrywa sie ze zdefiniowanymi juz temperaturami")
				else:
					insert(temperature_array, a, index_a)
			else:
				index_b = bisect(temperature_array, b)
				if index_b - index_a != 0:
					raise Exception("Podany przedzial pokrywa sie ze zdefiniowanymi juz temperaturami")
				else:
					insert(temperature_array, a, index_a)
					insert(temperature_array, b, index_a + 1)
	return temperature_array

temperature_array = []
specific_heat_array = []

def load(filePath = "resources/dane.txt"):
    file = open(filePath, 'r').read()
    lines = file.split('\n')
    listToReturn = [[],[]]
    for line in lines:
    	data = line.split()
    	listToReturn[0].append(float(data[0]))
    	listToReturn[1].append(float(data[1]))
    return listToReturn


#index = bisect(temperature_array, 125.0)

if(__name__ == "__main__"):
    changes_num = int(input("Ile przemian chcesz dodac?: "))
    temperature_array = check_temp(temperature_array, changes_num)
    print(temperature_array)
