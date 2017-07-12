#encoding:utf-8
import os
import codecs
import openpyxl
import re 
import chardet

'''
用于JE数据的处理了
''' 

#用于清洗数据
def clean_data(filePath):
    
    l_decs=[]
    with codecs.open(filePath,'r','utf-8',errors='ignore') as f: 
         
        for l in f:
            if l.startswith("Company Code"):
                l_decs.append(l)
            
        
    with codecs.open(filePath.replace('.txt','')+"_back.txt",'w+','utf-8') as f1:     
        for j in l_decs:
            f1.writelines(j)

#去表头         
def clean_data2(filePath):
    
    l_decs=[]
    with codecs.open(filePath,'r','utf-8',errors='ignore') as f: 
         
        for index,l in enumerate(f):
            if l.startswith("Company Code") and index>0:
                continue
            l_decs.append(l)
            
        
    with codecs.open(filePath.replace('.txt','')+"_back.txt",'w+','utf-8') as f1:     
        for j in l_decs:
            f1.writelines(j)



#生成workspace
def createWorkSpace(filePath,sep):
    """
    filePath:acl生成的统计字数的脚本
    sep:分隔符
    """
    l_desc=[]
    index=0
    f=re.split('\r\n|\n|\r',_getFileEncoding(filePath)[1])
    for line in f:
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
#单纯的复制文件了
def copy_lines(filePath):
    f1=codecs.open(filePath.replace('.txt','')+"_back.txt",'w+','utf-8',errors='ignore') 
    with codecs.open(filePath,'r','utf-8',errors='ignore') as f:
        for line in f:
            line='\t'.join(line.split('\t')[:7])+'\n'    
            f1.writelines(line)
                    
    f1.close()        
                     
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
    with codecs.open(filePath,'r','utf-8',errors='ignore') as f:
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
            
def clean_1(filePath):
    line_des=[]
    with codecs.open(filePath,'r','utf-8',errors='replace') as f:
                lines=f.readlines()
                for line in lines:
                    line_des.append(line.replace('\n','\r\n'))
    with codecs.open(filePath+'back.txt','w','utf-8',errors='replace') as f:
                for j in line_des:
                    f.writelines(j) 
            
def clean_2(filePath):
    f1=codecs.open(filePath+"back.txt",'w','utf-8',errors='ignore')
    with codecs.open(filePath,'r','utf-8',errors='ignore') as f:
        for line in f:
            if line.count("|")==7 or line.count("|")==0:
                line=line.replace("\r","")
                line=line.replace("\n","")
            f1.write(line)
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
                
if __name__ == '__main__':
    
    #路径需修改，\用\\代替   
    rootdir=r"C:\Users\Eric m shi\Desktop\555\output.TXT"
    
    #分析分隔符数量
#     list_file(get_separator_exception_lines, rootdir,'|','utf-8','utf-8')
    
    #去错行
#     list_file(clean_2, rootdir)
    
    #加表头
#     list_file(add_title,rootdir)

    #清数据
#     copy_lines(rootdir)
    
#     clean_data(rootdir)
    
#     clean_data2(rootdir)

    createWorkSpace(rootdir,sep="|")
#     print(_getFileEncoding(rootdir)[1])
#     splitWorkSpace(rootdir)
    
