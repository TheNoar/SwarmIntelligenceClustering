import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

class test:
	summatrix = []
	count =0
	listmatix = []
	



f = open("semeion.data")
count = 0
for line in f:
	name = 'test'+str(count)+'.png'
	data = line.rstrip('\r\n').split(' ')
	data = map(float,data[0:256])
	plt.imsave(name,np.array(data).reshape(16,16), cmap=cm.gray)
	count+=1