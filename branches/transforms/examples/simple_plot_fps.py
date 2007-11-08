#!/usr/bin/env python
"""
Example: simple line plot.
Show how to make and save a simple line plot with labels, title and grid
"""
from pylab import *

ion()

t = arange(0.0, 1.0+0.001, 0.001)
s = cos(2*2*pi*t)
plot(t, s, '-', lw=2)

xlabel('time (s)')
ylabel('voltage (mV)')
title('About as simple as it gets, folks')
grid(True)

#savefig('simple_plot.png')
#savefig('simple_plot')

import time

frames = 100.0
t = time.time()
for i in xrange(int(frames)):
    part = i / frames
    axis([0.0, 1.0 - part, -1.0 + part, 1.0 - part])
print "fps:", frames / (time.time() - t)
