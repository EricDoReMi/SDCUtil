# -*- coding: utf-8 -*-
import re
import fileinput

'''
Created on 3 Mar 2017

@author: Eric M Shi
'''

#匹配[]
myReg=re.compile(r'\[(.+?)\]')

#定义作用域
mySpace={}

def replacement(match):
    code=match.group(1)
    try:
        return str(eval(code,mySpace))
    except Exception as e:
        exec(code,mySpace)
        return ''

if __name__ == '__main__':
    myLine=""
    for line in fileinput.input(openhook=fileinput.hook_encoded("utf-8")):
        myLine+=line
   
    try:    
        print(myReg.sub(replacement,myLine).strip())
    except Exception as e:
        print("main"+str(e))
    