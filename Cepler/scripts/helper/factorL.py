import math
import random
import stddev

def getLength( inValue ):
	if inValue > 0:
		div = int(math.log10(inValue))+1
	elif inValue == 0:
		div = 1
	else:
		div = int(math.log10(-inValue))+2
	return div;	


def getFactor( inValue):
	factor = int(inValue)
	factor2 = int(inValue)
	facorList = []
	
	div = getLength(factor)
	#print(str(div))
	divH = int(div/2);
	while(factor >= 1):
		if(div == 0 & divH ==0):
			div = 1;
			divH = 1;
		factor = int (factor / div)
		factor2 = int (factor2 /divH)
		if factor != 0:
			facorList.append(factor)
		if factor2 != 0:
			facorList.append(factor2)
			
	if inValue >= 100:
		percentage = 1 / div;
		n = int(inValue *percentage);
	else:
		n = int(inValue)		
	for i in range(1,n, div):
		facorList.append(int(i))
		
	return sorted(facorList)

def getFactor2 (inValue):
	factor = 1
	facorList = []
	facorList.append(factor)
	multLimit = getLength(int(inValue)) -1

	mult = 1;
	if multLimit == 1:
		multLimit = 2;	
	while (factor <= inValue):
		factor = factor * mult;

		fuzz = random.randrange(1, 20, 1)/100;

		sign = random.randrange(0,1,1)
		if sign == 1:
			factor = factor+ fuzz*factor
		else:	
			factor = factor- fuzz*factor
		if(factor <= inValue):
			facorList.append(factor)
		if mult <= multLimit:
			mult = mult +1; 	
	return facorList;		

def getFactor3( inValue , resultListLen =100 ):
	n = resultListLen
	factorList = []
	a = inValue / math.pow(n, 4);

	for i in range(1,n+1):
		factor = math.ceil(a * math.pow(i, 4));
		factorList.append(factor)
	return factorList;	

def getFinalFactor(inValue):
	factorList = getFactor3(inValue)
	index = stddev.getIndex(len(factorList), getLength(inValue))
	factor = factorList[index];
	#print(str(factorList))
	return int(factor);