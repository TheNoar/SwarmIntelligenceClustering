import numpy as np
import random as rand
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation

# constants?
kd = 0.9
kp = 0.7

threshold = 20
counterthing = 0
class pile:
	sumvector = []
	count =0
	vectorlist = []
	def __init__(self):
		self.sumvector = np.zeros(256)
		count = 0
		vectorlist = []

	def add(self, vector):
		self.sumvector += vector
		self.vectorlist.append(vector)
		self.count += 1

	def remove(self, index):
		self.sumvector -= self.vectorlist[index]
		v = self.vectorlist.pop(index)
		self.count -= 1
		return v


def f1(pile, xV):
	pnorm = np.linalg.norm(pile.sumvector)
	xnorm = np.linalg.norm(pile.sumvector)
	
	if((xnorm == 0.0) or (pnorm == 0.0)):
		return 0.0

	v1 = pile.sumvector/pnorm
	v2 = xV/xnorm

	dot = np.dot(v1,v2)
	
	return abs(dot)

def f2(pile,xV):
	Va = pile.sumvector/pile.count

	dot = np.dot(Va,xV)
	
	return abs(dot)/sum(xV)

def f3(pile,xV):
	if pile.count == 0:
		return 1
	difsum = np.linalg.norm(xV - pile.sumvector/pile.count)
	# print str(difsum) + ":" + str(pile.count)

	return 1.0 - (difsum/16.0)

def f4(pile,xV):

	for v in pile.vectorlist:
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
	vec = pile.vectorlist[index]
	fx = func(pile, vec)

	choice = rand.random()

	prob = (kp/(kp+fx))**2

	if choice < prob:
		vec = pile.remove(index)
		return vec, True
	else:
		return 0, False

piles = [pile(),pile(),pile(),pile(),pile(),pile(),pile(),pile(),pile(),pile()]

im = 0
im2 = 0
imar = 0

def main():
	global piles, im, im2, imar, counterthing
	f = open("semeion.data")

	func = f3

	count = 0
    # piles = [pile() for i in xrange(10)]

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

	
	# while(running):
	print "here"
	fig = plt.figure()
	imar = np.zeros((32,80))
	im = plt.imshow(imar, cmap=cm.gray, animated=True)

	def init_test(*args):
		global piles, im, im2, imar
		count = 0
		for p in piles:			
			data = p.sumvector/p.count
			row = (count/5)*16
			col = (count*16)%80
			imar[row:(row+16),col:(col+16)] = data.reshape(16,16)
			count += 1
		im = plt.imshow(imar, cmap=cm.gray, animated=True)

		return im,


	def test(*args):
		global piles, im, im2, imar, counterthing
		running = True
		holding = False
		hands = 0
		for q in xrange(1000):
			counterthing += 1
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
		count = 0
		for p in piles:			
			data = p.sumvector/p.count
			row = (count/5)*16
			col = (count*16)%80
			imar[row:(row+16),col:(col+16)] = data.reshape(16,16)
			count += 1
		im = plt.imshow(imar, cmap=cm.gray, animated=True)
		# im.set_data(imar)
		return im,
			# if(done):
			# 	holding = True
				# if(piles[indexp].count == 0):
				# 	piles.pop(indexp)
				# 	count -= 1

		# if(count < threshold):
		# 	running = False

	ani = animation.FuncAnimation(fig, test, init_func=init_test, interval=50, blit=True)
	plt.show()

	print "almost done"
	print counterthing
	for p in piles:
		avr = 0
		if p.count == 0:
			continue
		for v in p.vectorlist:
			avr += func(p,v)
		print(avr/p.count)

	# c = 0
	# for p in piles:
	# 	if p.count == 0:
	# 		continue
	# 	name = 'test'+str(c)+'.png'
	# 	# data = map(lambda x: 1 if x>0.4 else 0, p.sumvector/p.count)
	# 	data = p.sumvector/p.count
	# 	im = plt.imshow(data.reshape(16,16),cmap=cm.gray, animated=True)
	# 	c+=1
	# 	plt.show()


main()