#encoding:utf-8
import os
import codecs
import openpyxl
import re 
import chardet

'''
用于JE数据的处理了
''' 
#复制文件的逻辑，需根据每个case的要求来写
def copy_lines(filePath):
    f1=codecs.open(filePath.replace('.txt','')+"_back.txt",'w+','utf-8',errors='ignore')
    with codecs.open(filePath,'r','utf-8',errors='ignore') as f:
        for line in f:
            if '"' in line:
                line=line.replace('"','“')
            f1.write(line.strip()+'\n')
    f1.close()  



#生成workspace
def createWorkSpace(filePath,sep):
    """
    filePath:acl生成的统计字数的脚本
    sep:分隔符
    """
    l_desc=[]
    index=0
    with codecs.open(filePath,'r','UTF-16-LE') as f:
        for i,line in enumerate(f):
            if i==0:
                line=line[1:]#去bom
            if line.strip().startswith("Field"):
                l_desc.append("F"+str(index+1).zfill(3)+"_"+line.split(":")[1].strip()+" computed\r\n")
            if line.strip().startswith("Highest"):
                l_desc.append("substr( alltrim( split( Full_Record , chr(" +str(ord(sep))+"), "+str(index+1).zfill(3)+" , chr( 34 ) ) ) , 1 , "+line.split(":")[1].strip().split(' ')[0]+" )\r\n")
                index+=1
    
    with codecs.open(filePath.replace('.txt','')+"_back.txt",'w+','utf-8') as f1:     
        for j in l_desc:
            f1.writelines(j)    
            
 

#检查每个文件分隔符的数量
#sep:分隔符
#num_sep:分隔符数量
#srcCode:源文件编码
#descCode:目标文件编码
def get_separator_exception_lines(filePath,sep,srcCode,descCode):
    num_sep=0
    l_decs=[]

    with codecs.open(filePath,'r',srcCode,errors='ignore') as f:
        for lineNum,line in enumerate(f):
            if lineNum==0:
                num_sep=line.count(sep)
            if line.count(sep)!=num_sep:
                l_decs.append(str(lineNum+1)+":"+str(line.count(sep))+":"+line)
                    
        if len(l_decs)>0:        
            with codecs.open(filePath.replace('.txt','')+"_split.txt",'w+',descCode,errors='ignore') as f1:     
                for j in l_decs:
                    f1.writelines(j)
                    
#检查每个文件分隔符的数量，需要自定义分隔符数量
#sep:分隔符
#num_sep:分隔符数量
#srcCode:源文件编码
#descCode:目标文件编码
#num_sep:分隔符数量
def get_separator_exception_lines_NumSep(filePath,sep,srcCode,descCode,num_sep):
    l_decs=[]

    with codecs.open(filePath,'r',srcCode,errors='ignore') as f:
        for lineNum,line in enumerate(f):
            if line.count(sep)!=num_sep:
                l_decs.append(str(lineNum+1)+":"+str(line.count(sep))+":"+line)
                    
        if len(l_decs)>0:        
            with codecs.open(filePath.replace('.txt','')+"_split.txt",'w+',descCode,errors='ignore') as f1:     
                for j in l_decs:
                    f1.writelines(j)
                          
                     
#给文件加表头
def add_title(filePath):
    headstr='G/L Account\tDocument Number\tDebit/Credit\tAmount in LC\tClient\tCompany Code\tFiscal Year\tLine Item\tLine item ID\tPosting Key\tAccount Type\tAmount\tG/L Amount\tText\tCost Centre\tG/L Account No\tG/L Currency\tTransaction Type\tBilling Doc\tSales Doc\tCustomer\tVendor\tBalance Sheet Acct\tP&L State.Acct\r\n'
    with codecs.open(filePath,'r+','utf-8',errors='ignore') as f:
                lines=f.readlines()
                lines.insert(0,headstr)
                with codecs.open(filePath+'back.txt','w','utf-8',errors='ignore') as f1:
                    for j in lines:
                        f1.writelines(j)
                        
#将workspace的computed中的内容抽离出来，导入excel
def splitWorkSpace(filePath):
    with codecs.open(filePath,'r','UTF-16LE',errors='ignore') as f:
        thedatas=f.read()
        l_desc=list(map(lambda s:re.split(r"computed\r\n",s),re.split(r'\r\n\r\n',thedatas)))
        _fillExcel(l_desc,filePath)

#file_fun 遍历完文件后需要调用的函数      
def list_file(file_fun,rootdir,*args):
    list=os.listdir(rootdir)
     
    for i in range(0,len(list)):
        path=os.path.join(rootdir,list[i])
        if os.path.isfile(path):
            file_fun(path,*args)

#去除不可打印字符            
def clean_UnprintChar(filePath,encode):
    f1=codecs.open(filePath.replace('.txt','')+"_back.txt",'w','utf-8',errors='ignore')
    with codecs.open(filePath,'r',encode,errors='ignore') as f:
        for line in f:
            f1.write(cleanColumnFun(line))
    f.close()
    f1.close()

#将tupleList写入到excel中
def _fillExcel(listTuple,filePath):
    wb = openpyxl.Workbook()
    sht=wb.active
    for j in range(len(listTuple)):
            for k in range(len(listTuple[j])):
                sht.cell(row=j+1,column=k+1).value=listTuple[j][k]
    wb.save(filePath.replace('txt','xlsx'))

#判断文件编码格式
#return:编码,去掉bom之后的read文本
def _getFileEncoding(filePath):
    with open(filePath,'rb') as f:
        f_read=f.read()
    
        #四位BOM
        if f_read[:4] in [codecs.BOM64_BE,codecs.BOM64_LE,codecs.BOM_UTF32,codecs.BOM_UTF32_BE,codecs.BOM_UTF32_LE]:
            f_read=f_read[4:]
        #三位BOM
        elif f_read[:3] in [codecs.BOM_UTF8]:
            f_read=f_read[3:]
        #两位BOM    
        elif f_read[:2] in [codecs.BOM,codecs.BOM32_BE,codecs.BOM_BE,codecs.BOM_LE,codecs.BOM_UTF16,codecs.BOM_UTF16_BE,codecs.BOM_UTF16_LE]:
            f_read=f_read[2:]
        f_charInfo=chardet.detect(f_read)   
    return f_charInfo['encoding'],f_read.decode(f_charInfo['encoding'].replace(chr(0),''))

#去Bom
def removeBom(filePath,encode):
    with open(filePath,'rb') as f:
        f_read=f.read()
    
        #四位BOM
        if f_read[:4] in [codecs.BOM64_BE,codecs.BOM64_LE,codecs.BOM_UTF32,codecs.BOM_UTF32_BE,codecs.BOM_UTF32_LE]:
            f_read=f_read[4:]
        #三位BOM
        elif f_read[:3] in [codecs.BOM_UTF8]:
            f_read=f_read[3:]
        #两位BOM    
        elif f_read[:2] in [codecs.BOM,codecs.BOM32_BE,codecs.BOM_BE,codecs.BOM_LE,codecs.BOM_UTF16,codecs.BOM_UTF16_BE,codecs.BOM_UTF16_LE]:
            f_read=f_read[2:]
        with  codecs.open(filePath.replace('.txt','')+"_back.txt",'w','utf-8',errors='ignore') as f1:
            f1.write(f_read.decode(encode))

#检查各个文件表头是否一样
def checkHead(filePath,encode):
    checkHead.headlist=None
    listLine=[]
    
    
    def list_file(rootdir):
        list=os.listdir(rootdir)
     
        for i in range(0,len(list)):
            path=os.path.join(rootdir,list[i])
            if os.path.isfile(path):
                _checkHead(path,list[i])
                
    def _checkHead(filePath,filename):
        
        with codecs.open(filePath,'r',encode,errors='ignore') as f:
            flist=[line for line in f]
            if checkHead.headlist:
                if flist[0]!=checkHead.headlist:
                    listLine.append(filename+':'+flist[0]+'\n')
            else: 
                checkHead.headlist=flist[0]
                 
    list_file(filePath) 
    with codecs.open(os.path.join(rootdir,"report.txt"),'w','utf-8',errors='ignore') as f1:
        for line in listLine:
            f1.write(line)            

#去除不可打印字符
def cleanColumnFun(columnStr):
    table=str.maketrans(chr(0)+ chr(1)+ chr(2)+ chr(3)+ chr(4)+ chr(5)+ chr(6)+ chr(7)+ chr(8)+ chr(11)+ chr(12)+ chr(14)+ chr(15)+ chr(16)+ chr(17)+
                        chr(18)+ chr(19)+ chr(20)+ chr(21)+ chr(22)+ chr(23)+ chr(24)+ chr(25)+ chr(26)+ chr(27)+ chr(28)+ 
                        chr(29)+ chr(30)+ chr(31),' '*29)
    columnStr=columnStr.translate(table).replace(' ','')
    return columnStr

#lineNum:开始错行的列数了
#encode:文件的编码方式
#sep:分隔符
def combineLine(filePath,encode,sep,*lineNum):
    with codecs.open(filePath.replace('.txt','')+"_back.txt",'w','utf-8',errors='ignore') as f1:
        with codecs.open(filePath,'r',encode,errors='ignore') as f:
            for line in f:
                if line.count(sep) in list(lineNum):
                    line=line.replace("\r","")
                    line=line.replace("\n","")
                f1.write(line)

#清理摘要中的分隔符
#sep:分隔符
#abstractNum:摘要所在的列
#sepNum:分隔符的正常数量
def clearAbstract(filePath,encode,sep,abstractNum,sepNum):
    with codecs.open(filePath.replace('.txt','')+"_back.txt",'w','utf-8',errors='ignore') as f1: 
        with codecs.open(filePath,'r',encode,errors='ignore') as f:
            for line in f:
                if line.count(sep)>sepNum:
                    l=line.split(sep)
                    clearL=sep.join(l[abstractNum-1:abstractNum-sepNum-1]).replace(sep,'')
                    l=l[:abstractNum-1]+clearL.split(sep)+l[abstractNum-sepNum-1:]
                    line=sep.join(l)
                f1.write(line)

    
                
#修改文件名称            
def changeFileName(rootdir):
 
    filenames=os.listdir(rootdir)
    
    for a in range(len(filenames)):
        os.rename(rootdir+os.sep+filenames[a],rootdir+os.sep+filenames[a].replace(r"_back.txt",r".txt"))

#删除原文件
def deleteSourceFile(rootdir):
 
    filenames=os.listdir(rootdir)
    
    for a in range(len(filenames)):
        if not filenames[a].endswith(r'_back.txt'):
            os.remove(rootdir+os.sep+filenames[a])  

def delete01(filePath):
    with codecs.open(filePath.replace('.txt','')+"_back.txt",'w','utf-8',errors='ignore') as f1: 
        with codecs.open(filePath,'r','utf-8',errors='ignore') as f:
            for line in f:
                if line.split('|')[4] in ('1700001191', '1700001194', '1700001196', '1700001179', '1700001178', '1700001189', '1700001195', '1700001190', '1700001175', '1700001192', '1700001180', '1700001186', '1700001182', '1700001183', '1700001187', '1700001193', '1700001173', '1700001174', '1700001181', '1700001184', '1700001176', '1700001177', '1700001188'):
                    f1.write(line)
                
    
                  
if __name__ == '__main__':
    
    #路径需修改，\用\\代替   
    rootdir=r"C:\Users\Eric M Shi\Desktop\111"
    
    #检查表头是否相同
#     checkHead(rootdir,'utf-8')
    
    #分析分隔符数量
#     list_file(get_separator_exception_lines, rootdir,';','utf-8','utf-8')
    
    #分析分隔符数量,自定义分隔符数量
#     list_file(get_separator_exception_lines_NumSep, rootdir,'|','utf-8','utf-8',33)
    
    
    #去除不可打印字符
#     list_file(clean_UnprintChar,rootdir,'utf-8')
    
    #去Bom
#     list_file(removeBom,rootdir,'UTF-16-LE')
    
    #去错行
#     list_file(combineLine, rootdir,'utf-8','|',7)

    #删除原文件
#     deleteSourceFile(rootdir)
        
    #改文件名称
#     changeFileName(rootdir)
    
    #加表头
#     list_file(add_title,rootdir)

    #清除摘要中的多余分隔符
#     list_file(clearAbstract,rootdir,'utf-8','|',31,33)

    #清数据
#     list_file(copy_lines,rootdir)

    #生成workspace
    list_file(createWorkSpace,rootdir,";")

    #workspace生成excel
#     list_file(splitWorkSpace,rootdir)

#     list_file(delete01,rootdir)
    
