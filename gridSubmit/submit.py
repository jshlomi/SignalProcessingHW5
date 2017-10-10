import sys
import numpy as np
import os


nJobsPerGarble = 19 # 19 jobs, each one of length 40, gives us 760 points, each of 1000 letters
nTestsPerJobs = 40
seqLength = 1000

garbleProbs = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99]

for gProb in garbleProbs:
	if not os.path.exists('gProb'+str(gProb)):
		os.mkdir('gProb'+str(gProb))
	for i in range(nJobsPerGarble):
		startingPoint = i*nTestsPerJobs*seqLength
		print 'startingPoint ', startingPoint

