from matplotlib import rcParams
rcParams['text.fontname'] = 'cmr10'
from pylab import *


mu, sigma = 100, 15
x = mu + sigma*randn(10000)

# the histogram of the data
n, bins, patches = hist(x, 100, normed=1)

# add a 'best fit' line
y = normpdf( bins, mu, sigma)
l = plot(bins, y, 'r--')
set(l, 'linewidth', 2)
xlim(40, 160)

xlabel('Smarts')
ylabel('P')
title(r'$\rm{IQ:}\/ \mu=100,\/ \sigma=15$')

show()
