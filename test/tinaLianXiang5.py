#encoding:utf-8
import os
import codecs


def copy_data(filePath,fileName):
    
    fileNamePath=os.path.join(filePath,fileName)
    l_decs=[]
    f=codecs.open(fileNamePath,'r','utf-8',errors='ignore')
    f1=codecs.open(fileNamePath.replace('.txt','')+"_back.txt",'w+','utf-8')
#     f1.write('G/L Account\tDocument Number\tDebitOrCredit\tAmount in LC\n')
    try:  
        for l in f:
            l_orc=l.split('\t')
         
#             if len(l_orc)>11:
            l_pro=l_orc[0:10]
                
            str_dec='\t'.join(l_pro)+'\n'
            f1.write(str_dec) 
                
         
        f.close()
        f1.close()
    except Exception as e:
        print(e)
        print(fileNamePath)
 
if __name__ == '__main__':
    
    #路径需修改，\用\\代替   
    rootdir="C:\\Users\\Eric m shi\\Desktop\\222"
 
    list=os.listdir(rootdir)
     
    for i in range(0,len(list)):
        path=os.path.join(rootdir,list[i])
        if os.path.isfile(path):
            copy_data(rootdir,path)