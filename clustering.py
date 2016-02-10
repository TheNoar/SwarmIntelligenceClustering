import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

class pile:
	sumvecter = []
	count =0
	vecterlist = []
	def __init__(self):
		self.sumvecter = np.array
		

	def add(self, vector):

	def remove(self, index):

	

	
def drop(pile, vector):


def pickup(pile, index):


def main():
	f = open("semeion.data")
	count = 0
	for line in f:
		name = 'test'+str(count)+'.png'
		data = line.rstrip('\r\n').split(' ')
		data = map(float,data[0:256])
		count+=1