#encoding:utf-8
import os
import codecs
import sys

 
 
 
 
def copy_data(filePath,fileName):
    
    fileNamePath=os.path.join(filePath,fileName)
    l_decs=[]
    f=codecs.open(fileNamePath,'r','utf-8')
    try: 
     
        lines=f.readlines()
         
        for l in lines:
            l_orc=l.split('\t')
            if len(l_orc)>=13:
                l_pro=l_orc[0:14]
                
                str_dec='\t'.join(l_pro)+'\n'
                 
                l_decs.append(str_dec)
         
        f.close()
         
        f1=codecs.open(fileNamePath.replace('.txt','')+"_back.txt",'w+','utf-8')
             
        for j in l_decs:
            f1.writelines(j)
         
        f1.close()
    except Exception as e:
        print(e)
        print(fileNamePath)
 
if __name__ == '__main__':
    
    #路径需修改，\用\\代替   
    rootdir="C:\\Users\\Eric m shi\\Desktop\\1"
 
    list=os.listdir(rootdir)
     
    for i in range(0,len(list)):
        path=os.path.join(rootdir,list[i])
        if os.path.isfile(path):
            copy_data(rootdir,path)