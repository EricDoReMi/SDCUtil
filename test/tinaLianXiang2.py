#encoding:utf-8
import os
import xlwt
import time
import sys
import importlib
import codecs


 
def copy_data(fileName,filePath,rootdir,mysheet):
    

  
    f=codecs.open(filePath,'r','utf-8')
    lines=f.readlines()
    l_desc=[]
    l_desc.append(['CoCd', 'G/L acct', 'Short Text', 'Crcy', 'BusA', 'Balance Carryforward','Balance,prev.periods','Debit rept.period','Credit report per','Accumulated balance'])
    num=1
    for line in lines[6:]:
        
        
        if (num%2 and line[1:2]!='*'):
            l_orc=[]
            
            l_orc.append(line[2:6])
            l_orc.append(line[6:18].strip())
            l_orc.append(line[18:39])
            l_orc.append(line[39:45])
            l_orc.append(line[45:53])
            #这几个是数值
            l_orc.append(line[53:77].strip().replace('.','').replace(',','.'))
            l_orc.append(line[77:104].strip().replace('.','').replace(',','.'))
            l_orc.append(line[104:127].strip().replace('.','').replace(',','.'))
            l_orc.append(line[127:150].strip().replace('.','').replace(',','.'))
            l_orc.append(line[150:169].strip().replace('.','').replace(',','.'))
            m=5
            while m<10:
                if(l_orc[m].find("-")>0):
                    l_orc[m]='-'+(l_orc[m].replace("-",""))
                m=m+1     
            l_desc.append(l_orc)
            
             
            
#         l_orc=line.split('|')
#         l_orc=l_orc[1:6]
#         str_head=l_orc[0][0:8]
#         l_orc.insert(0,str_head)
#         for i in range(len(l_orc[2:6])):
#             
#             l_orc[2+i]=(l_orc[2+i].strip()).replace('.',"").replace(",",".")
#             if(l_orc[2+i].find('-')>0):
#                 l_orc[2+i]=l_orc[2+i].replace("-",'')
#                 l_orc[2+i]='-'+l_orc[2+i]
#        
#         
#         l_desc.append(l_orc)
        
        num=num+1
        for j in range(len(l_desc)):
            for k in range(len(l_desc[j])):
                mysheet.write(j,k,l_desc[j][k])
#               
    f.close()
  
    
if __name__ == '__main__':
   
    
    #获取当前时间
    my_year_month=time.strftime("%Y-%D")
    my_year_month=my_year_month[0:4]+"_"+my_year_month[5:7]+"_"+my_year_month[8:10]
     
 
       
    #路径需修改，\用\\代替   
    rootdir="C:\\Users\\Eric m shi\\Desktop\\111"
    
    listDir=os.listdir(rootdir)
    for m in range(len(listDir)):
        wb = xlwt.Workbook() #新建一张excel表用于保存数据
        wbPath=rootdir+"\\"+listDir[m]#工作表存放的目录
        list=os.listdir(wbPath)#每个工作表中的txt文件
           
              
        for i in range(len(list)):
            path=os.path.join(wbPath,list[i])
            fileName=os.path.basename(path)
               
            mysheet=wb.add_sheet(fileName.split('_')[-1].split('.')[-2],cell_overwrite_ok=True)
            if os.path.isfile(path):
                copy_data(fileName,path,rootdir,mysheet)
        wb.save(wbPath+"\\"+listDir[m]+"_"+my_year_month+".xls")

