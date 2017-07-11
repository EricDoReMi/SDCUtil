#encoding:utf-8
import os
import codecs
 
 
 
 
def copy_data(filePath,fileName):
    fileNamePath=os.path.join(filePath,fileName)
    l_decs=[]
    f=codecs.open(fileNamePath,'r','utf-8')
     
     
    lines=f.readlines()
     
     
     
    for l in lines:
        l_orc=l.split('\t')
        l_pro=l_orc[18:]
        str_tmp=(''.join(l_pro)).replace('\t','')
        l_replace=[]
        l_replace.append(str_tmp)
        l_dec=l_orc[:18]+l_replace[::]
        del l_replace
        str_dec='\t'.join(l_dec)+'\n'
         
        l_decs.append(str_dec)
     
    f.close()
     
    f1=open(fileNamePath+"_back.txt",'w+')
         
    for j in l_decs:
        f1.writelines(j)
     
    f1.close()
 
if __name__ == '__main__':
    
    #路径需修改，\用\\代替   
    rootdir="C:\\Users\\Eric m shi\\Desktop\\data"
 
    list=os.listdir(rootdir)
     
    for i in range(0,len(list)):
        path=os.path.join(rootdir,list[i])
        if os.path.isfile(path):
            copy_data(rootdir,path)