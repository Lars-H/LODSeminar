import math
import random


def getIndex(listLength, numOfDigits):
	#index = random.normalvariate(listLength/2, 3)
	index = random.weibullvariate(listLength/2, numOfDigits*0.5);
	index = math.ceil(index)
	if index > listLength -1:
		index = listLength - 1
	if index < 0:
		index = 0;	
	return int(index);