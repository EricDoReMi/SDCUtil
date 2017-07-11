#encoding:utf-8
import string
'''
Created on 19 Feb 2017

@author: Eric M Shi

 去除字符串中的不可打印字符
'''

def cleanColumnFun(columnStr):
    table=str.maketrans(chr(0)+ chr(1)+ chr(2)+ chr(3)+ chr(4)+ chr(5)+ chr(6)+ 
                        chr(7)+ chr(8)+ chr(9)+ chr(10)+ chr(11)+ chr(12)+ chr(13)+ chr(14)+ chr(15)+ chr(16)+ chr(17)+
                        chr(18)+ chr(19)+ chr(20)+ chr(21)+ chr(22)+ chr(23)+ chr(24)+ chr(25)+ chr(26)+ chr(27)+ chr(28)+ 
                        chr(29)+ chr(30)+ chr(31),' '*32)
    columnStr=columnStr.translate(table).replace(' ','')
    return columnStr 
    
if __name__ == '__main__':
    MyStrTest='''aaa    
                jkl'''
    MyStrTest=cleanColumnFun(MyStrTest)
    print(MyStrTest)