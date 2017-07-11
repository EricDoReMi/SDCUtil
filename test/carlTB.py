#encoding:utf-8
import re

def numLine():
    with open(r'C:\Users\Eric m shi\Desktop\aaa\1002010100_qucuohang.txt','r',encoding='gb2312',errors='ignore') as f:
        lines=f.readlines()
        num=0
        myRegLine=re.compile(r'^\s{2}(\d{2}\-\d{2}).*?([借|贷])$')#每条具体记录的正则表达式
        for line in lines:
            if myRegLine.match(line):
                num+=1
        print(num)

def combineLine():
    f=open(r'C:\Users\Eric m shi\Desktop\aaa\1002010100.txt','r',encoding='gb2312',errors='replace')
    
    f1=open(r'C:\Users\Eric m shi\Desktop\aaa\1002010100_qucuohang.txt','w',encoding='gb2312',errors='ignore')
    try:
        lines=f.readlines()
        
        myRegCuoHang=re.compile(r'^\s{2}\d{2}\-\d{2}?[^借贷]*$')
        
        ############去错行#################
        for line in lines:
            if myRegCuoHang.match(line):
                line=line.rstrip()
            f1.write(line)
    except Exception as e:
        print('combineLine:%s' % e)
    finally:
        f.close()
        f1.close()


if __name__ == '__main__':
      
    combineLine()
      
    #############生成标准文件############
    myRegLine=re.compile(r'^\s{2}(\d{2}\-\d{2})\s+([\d|未过帐]+).*?([借|贷])$')#每条具体记录的正则表达式
      
    bianbaodanweiReg=re.compile(r'^\s{2}编报单位(.*)?$')
      
    kuaijikemuBizongReg=re.compile(r'^\s{2}会计科目(.*)?币种(.*)?$')
      
    danweiReg=re.compile(r'^\s*单位(.*)?$')
      
  
   
    title_data={'编报单位':'','会计科目':'','币种':'','单位':''}#存储title行信息
    f=open(r'C:\Users\Eric m shi\Desktop\aaa\1002010100_qucuohang.txt','r',encoding='gb2312',errors='ignore')
    f1=open(r'C:\Users\Eric m shi\Desktop\aaa\1002010100_back.txt','w',encoding='gb2312',errors='ignore')
      
    try:
        f1.write('日期|凭证号|摘要|借方金额|贷方金额|余额|借贷|编报单位|会计科目|币种|单位\n')#用于添加表头
        lines=f.readlines()
          
        for index,line in enumerate(lines):
            if bianbaodanweiReg.match(line):
                title_data['编报单位']=bianbaodanweiReg.match(line).group(1)[1:].strip()
          
            if kuaijikemuBizongReg.match(line):
                title_data['会计科目']=kuaijikemuBizongReg.match(line).group(1)[1:].strip()
                title_data['币种']=kuaijikemuBizongReg.match(line).group(2)[1:].strip()
              
            if danweiReg.match(line):
                title_data['单位']=danweiReg.match(line).group(1)[1:].strip()
              
            if myRegLine.match(line):
                des_line=[]
                line=line.replace('"','').replace('|','')
                des_line.append("2016"+myRegLine.match(line).group(1)[:2]+myRegLine.match(line).group(1)[-2:])#日期
                des_line.append(myRegLine.match(line).group(2))#凭证号
                if len(re.split(r'\s{2,}',line))<7:
                        des_line.append(' ')#摘要 
                        des_line.append(re.split(r'\s{2,}',line)[3].strip().replace(',',''))#借方金额
                        des_line.append(re.split(r'\s{2,}',line)[4].strip().replace(',',''))#贷方金额
                        des_line.append(re.split(r'\s{2,}',line)[5].strip()[:-2].replace(',',''))#余额
                else:
                        des_line.append(re.split(r'\s{2,}',line)[3].strip())#摘要
                        des_line.append(re.split(r'\s{2,}',line)[4].strip().replace(',',''))#借方金额
                        des_line.append(re.split(r'\s{2,}',line)[5].strip().replace(',',''))#贷方金额
                        des_line.append(re.split(r'\s{2,}',line)[6].strip()[:-2].replace(',',''))#余额
                des_line.append(myRegLine.match(line).group(3))#借贷
                des_line.append(title_data['编报单位'])
                des_line.append(title_data['会计科目'])
                des_line.append(title_data['币种'])
                des_line.append(title_data['单位'])
                f1.write('|'.join(des_line)+'\n')
                del des_line
              
                  
    except Exception as e:
        print('mainException:%s' % index)
        raise e
    finally:
        f.close()
        f1.close()
            
# if __name__ == '__main__':
#     numLine()
#         

 
