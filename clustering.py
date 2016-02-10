import numpy as np
import random as rand
# import matplotlib.pyplot as plt
# import matplotlib.cm as cm

# constants?
kd = 0.5
kp = 0.5

threshold = 20

class pile:
	sumvecter = []
	count =0
	vecterlist = []
	def __init__(self):
		self.sumvecter = np.zeros(256)
		count = 0
		vecterlist = []

	def add(self, vector):
		self.sumvecter += vector
		self.vecterlist.append(vector)
		self.count += 1

	def remove(self, index):
		self.sumvecter -= self.vecterlist[index]
		v = self.vecterlist.pop(index)
		self.count -= 1
		return v


def f(pileV, xV):
	pnorm = np.linalg.norm(pileV)
	xnorm = np.linalg.norm(pileV)
	
	if((xnorm == 0.0) or (pnorm == 0.0)):
		return 0.0

	v1 = pileV/pnorm
	v2 = xV/xnorm

	dot = np.dot(v1,v2)
	
	return abs(dot)

def drop(pile, vector):
	fx = f(pile.sumvecter, vector)
	choice = rand.random()
	if fx < kd:
		if 2*fx > choice:
			pile.add(vector)
			return True
		else:
			return False
	else:
		pile.add(vector)
		return True


def pickup(pile, index):
	vec = pile.vecterlist[index]
	fx = f(pile.sumvecter - vec, vec)
	choice = rand.random()

	prob = (kp/(kp+fx))**2

	if choice < prob:
		vec = pile.remove(index)
		return vec, True
	else:
		return 0, False


def main():
	f = open("semeion.data")
	count = 0

	piles = []

	for line in f:
		data = line.rstrip('\r\n').split(' ')
		data = map(float,data[0:256])
		vec = np.array(data)
		p = pile()
		p.add(vec)
		piles.append(p)
		count+=1

	# for testing
	# threshold = count/2

	running = True
	holding = False
	hands = 0
	while(running):
		indexp = rand.randint(0,count-1)

		if(holding):
			done = drop(piles[indexp],hands)
			if(done):
				holding = False

		else:
			indexv = rand.randint(0,piles[indexp].count)

			hands, done = pickup(piles[indexp],indexv)

			if(done):
				holding = True
				if(piles[indexp].count == 0):
					piles.pop(indexp)
					count -= 1

		if(count < threshold):
			running = False

	

main()