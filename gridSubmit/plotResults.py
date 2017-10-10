import sys
import numpy as np
import glob


#filelist = glob.glob('gProb0.5/*.npy')

filelist = glob.glob('gProbSize100_0.6/*.npy')

testSetGarbPofH1 = []
bkgSetPofH1 = []

for filename in filelist:

	results = np.load(filename)
	testSetGarbPofH1.extend(results[0])
	bkgSetPofH1.extend(results[1])


import matplotlib.pyplot as plt

n, bins, patches = plt.hist(testSetGarbPofH1,50, normed=True, alpha=0.3)
n2, bins2, patches2 = plt.hist(bkgSetPofH1,50, normed=True,alpha=0.3)

from scipy.stats import norm
from scipy import stats
import matplotlib.mlab as mlab

(mu, sigma) = norm.fit(testSetGarbPofH1)
(mu2, sigma2) = norm.fit(bkgSetPofH1)

y = mlab.normpdf( bins, mu, sigma)
l = plt.plot(bins, y, 'r--', linewidth=2)

y2 = mlab.normpdf( bins2, mu2, sigma2)
l2 = plt.plot(bins2, y2, 'b--', linewidth=2)

cutPoint = np.percentile()

#plt.yscale('log')
#plt.xlim(-3500,-3200)
plt.xlim(-500,-200)
plt.ylim(0,0.2)
plt.show()