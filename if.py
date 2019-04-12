import time
max=0
while (true):
	old=time.time()
	if time.time()-old>max:
		max=time.time()-old
	print max