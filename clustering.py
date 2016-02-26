import numpy as np
import random as rand
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# constants?
kd = 0.9
kp = 0.6

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


def f1(pile, xV):
	pnorm = np.linalg.norm(pile.sumvecter)
	xnorm = np.linalg.norm(pile.sumvecter)
	
	if((xnorm == 0.0) or (pnorm == 0.0)):
		return 0.0

	v1 = pile.sumvecter/pnorm
	v2 = xV/xnorm

	dot = np.dot(v1,v2)
	
	return abs(dot)

def f2(pile,xV):
	Va = pile.sumvecter/pile.count

	dot = np.dot(Va,xV)
	
	return abs(dot)/sum(xV)

def f3(pile,xV):
	if pile.count == 0:
		return 1
	difsum = np.linalg.norm(xV - pile.sumvecter/pile.count)
	# print str(difsum) + ":" + str(pile.count)

	return 1.0 - (difsum/16.0)

def f4(pile,xV):

	for v in pile.vecterlist:
		dif = abs(v - xV)
		difsum += sum(dif)
	avrdif = difsum/pile.count

	return avrdif

def drop(pile, vector, func):
	fx = func(pile, vector)
	
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


def pickup(pile, index, func):
	vec = pile.vecterlist[index]
	fx = func(pile, vec)

	choice = rand.random()

	prob = (kp/(kp+fx))**2

	if choice < prob:
		vec = pile.remove(index)
		return vec, True
	else:
		return 0, False


def main():
	f = open("semeion.data")

	func = f3

	count = 0
    # piles = [pile() for i in xrange(10)]
	piles = [pile(),pile(),pile(),pile(),pile(),pile(),pile(),pile(),pile(),pile()]

	for line in f:
		data = line.rstrip('\r\n').split(' ')
		data = map(float,data[0:256])
		vec = np.array(data)
		index = rand.randint(0,9)
		piles[index].add(vec)
		# p = pile()
		# p.add(vec)
		count+=1

	# for testing
	# threshold = count/2

	# print count

	running = True
	holding = False
	hands = 0
	# while(running):
	print "here"
	for q in xrange(5000000):
		indexp = rand.randint(0,9)
		# print q
		# if(holding):
		done = drop(piles[indexp],hands, func)
		
		if(done):
			holding = False
			while not holding: 
		# else:
				indexv = 0
				if(piles[indexp].count>1):
					indexv = rand.randint(0,piles[indexp].count-1)
				else:
					continue
				hands, holding = pickup(piles[indexp],indexv,func)

			# if(done):
			# 	holding = True
				# if(piles[indexp].count == 0):
				# 	piles.pop(indexp)
				# 	count -= 1

		# if(count < threshold):
		# 	running = False

	print "almost done"

	for p in piles:
		avr = 0
		if p.count == 0:
			continue
		for v in p.vecterlist:
			avr += func(p,v)
		print(avr/p.count)

	c = 0
	for p in piles:
		if p.count == 0:
			continue
		name = 'test'+str(c)+'.png'
		# data = map(lambda x: 1 if x>0.4 else 0, p.sumvecter/p.count)
		data = p.sumvecter/p.count
		plt.imsave(name,np.array(data).reshape(16,16),cmap=cm.gray)
		c+=1



main()