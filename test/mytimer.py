#encoding:utf-8
'''
用于记时的脚本
'''

import time
reps=1000
replist=range(reps)

def timer(func,*pargs,**kargs):
    start=time.clock()
    for i in replist:
        ret=func(*pargs,**kargs)
    elapsed=time.clock()-start
    return (elapsed,ret)
