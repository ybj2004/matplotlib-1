import sys, time, os
from helpers import rand_val, rand_point, rand_bbox, rand_transform

def report_memory(i):
    pid = os.getpid()
    a2 = os.popen('ps -p %d -o rss,sz' % pid).readlines()
    print i, '  ', a2[1],
    return int(a2[1].split()[0])

N = 200
for i in range(N):
    v1, v2, v3, v4, v5 = rand_val(5)
    b1 = v1 + v2
    b2 = v3 -v4
    b3 = v1*v2*b2 - b1
    

    p1 = rand_point()
    box1 = rand_bbox()
    t = rand_transform()
    val = report_memory(i)
    if i==1: start = val

end = val
print 'Average memory consumed per loop: %1.4f\n' % ((end-start)/float(N))

