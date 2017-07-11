#encoding:utf-8
import os,chardet
import codecs


f=codecs.open("C:\\Users\\Eric m shi\\Desktop\\111\\JE_quan.txt",'r','utf-8')



lines=f.readlines()

num=0
f1=None
for line in lines:
    
    if num%5000000==0:
        if num!=0:
            f1.close()
        f1=open("C:\\Users\\Eric m shi\\Desktop\\111\\"+"JE_quan"+str((num+1))+".txt","w+")
    
    f1.writelines(line)    
    num=num+1
    

f1.close()
f.close()
    
    