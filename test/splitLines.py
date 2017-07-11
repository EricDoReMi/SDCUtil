#encoding:utf-8

'''
增对大文件的读写
'''
from _ast import Num
try:
    f=open("C:\\Users\\Eric m shi\\Desktop\\111\\JE_quan.txt",'rt',encoding='utf-8',errors='replace')

    

    num=0
    numFile=1
    f1=None
    lineList=[]
    for line in f:
        
        if num%5000000==0:
            if num!=0:
                f1.writelines(lineList)
                f1.close()
                lineList.clear()
            f1=open("C:\\Users\\Eric m shi\\Desktop\\111\\"+"JE_quan"+str(numFile)+".txt","w+")
            numFile+=1
        
        lineList.append(line)    
        num=num+1
    
except Exception as e:
    print(num)
    raise(e)
finally:
    f1.close()
    f.close()

    
    