import random
import math


def getLength( inValue ):
	if inValue > 0:
		div = int(math.log10(inValue))+1
	elif inValue == 0:
		div = 1
	else:
		div = int(math.log10(-inValue))+2
	return int(div);	

def getFactor( inValue ):

	factorList = createList(inValue);
	index = int(getIndex(inValue));
	#print(index)
	res =factorList[index]
	return int(res);


def createList( inValue, adujst = 1 ):
	digits = getLength(inValue);
	#print(digits)
	linRange = 1- digits / 10.0

	print(str(linRange))
	percXrange = (linRange * inValue) / adujst;

	swit = linRange * 100;
	if swit > 0:
		slope = percXrange  /swit;
	else:
		slope = 1;
	a = ((inValue - percXrange) / (math.pow((100-swit),digits)))

	print(slope)
	factorList = []
	for i in range(0, 100):
		if i <= swit:
			y = i * slope;
		else:
			y = a* math.pow((i-swit),digits) + percXrange;
		
		deviation = random.normalvariate(0, 0.4) / 100

		y = y + deviation*y
		factorList.append(y);

	print(factorList)
	return factorList;	



def getIndex (inValue):
	#Get Lambda for triangular distributions
	lmbda = getLength(inValue) / 10.0
	
	#Keep Lambda in Range of 1 & 0
	if lmbda < 0:
		lmbda = 1;
	elif lmbda > 1:
		lmbda = 1;


	index = random.triangular(0,1, lmbda)
	index = random.randrange(0,99,1) 
	return float(index);

#inValue = 10000;
#factor = getFactor(inValue)
#print (factor)