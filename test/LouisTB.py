#encoding:utf-8
import re

#若有非英文字符，将字符改为'你 '
def cleanColumnFun(columnStr):
    ds=''
    for l in columnStr:
        try:
            l.encode('ascii')
            
        except Exception as e:
            l=l+' '
        ds=ds+l    
    return ds 


if __name__ == '__main__':
       
       
    #############生成标准文件############
    myRegLine=re.compile(r'^\s{5}\d{4}\.\d{3}\.\d{6}\.\d{5}\.\d{3}.*$')#每条具体记录的正则表达式
       
    TitleReg=re.compile(r'^\s{2}Doc Seq Num:\s*(\d*?)\s*GL Date:\s*(\d{2}\-[A-Z]{3}\-\d{2}).*$')
       
    
    title_data={'Doc Seq Num':'','GL Date':''}#存储title行信息
    f=open(r'C:\Users\Eric m shi\Desktop\111\gl.txt','r',encoding='utf-8',errors='ignore')
    f1=open(r'C:\Users\Eric m shi\Desktop\111\glBackup.txt','w',encoding='utf-8',errors='ignore')
       
    try:
        f1.write('Doc Seq Num|GL Date|Accounting Flexfield|Source Date|Description|User|Date|VAT Code|Acct Debits|Acct Credits|Entered Debits|Entered Credits\n')#用于添加表头
        lines=f.readlines()
           
        for index,line in enumerate(lines):
            line=line.replace('\n','')
            line=(cleanColumnFun(line)) 
            if TitleReg.match(line):
                title_data['Doc Seq Num']=TitleReg.match(line).group(1).strip()
           
            if TitleReg.match(line):
                title_data['GL Date']=TitleReg.match(line).group(2).strip()
               
               
            if myRegLine.match(line):
                
                des_line=[]
                des_line.append(title_data['Doc Seq Num'])
                des_line.append(title_data['GL Date'])
                des_line.append(line[5:32])
                des_line.append(line[32:45])
                des_line.append(line[45:72])
                des_line.append(line[72:83])
                des_line.append(line[83:96])
                des_line.append(line[96:106])
                des_line.append(line[106:124])
                des_line.append(line[124:142])
                des_line.append(line[142:160])
                des_line.append(line[160:])
             
                 
                f1.write('|'.join(des_line)+'\n')
                del des_line
               
                   
    except Exception as e:
        print('mainException:%s' % index)
        raise e
    finally:
        f.close()
        f1.close()
            
# if __name__ == '__main__':
#     print(cleanColumnFun('你好aaa'))
#         

 
