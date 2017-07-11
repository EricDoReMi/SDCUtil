#encoding:utf-8

#根据accountNo把所有的列表搜索出来，存储到相应的文件中
def search_Account_List(accountNo):
    flag=False
    try:
        f=open(r'C:\Users\Eric m shi\Desktop\test\JE.txt','r',encoding='gb2312',errors='replace')
        f1=open("C:\\Users\\Eric m shi\\Desktop\\test\\" + accountNo+r".txt",'w',encoding='gb2312',errors='replace')
        for num,line in enumerate(f):
            if accountNo in line:
                flag=True
            if '\f' in line:
                flag=False
            if flag:
                f1.write(line)
    except Exception as e:
        print('lineNum:'+str(num)+"---"+e)
    finally:
        f.close()
        f1.close()
        
if __name__ == '__main__':
    unbalance_Account_List=('1002010100','1132030000','1132040000','1211000000','1214010100','1215010000','1216010000','1501010101','1501020101','1503010101','1503020101','1503030101','1604000000','1811000000','2211080000','2221990000','2241990000','2901000000','3001020100','3001020101','3001020200','3001020201','3001030000','3001030001','3001040100','3001040101','3001050100','3001050101','3001050200','3001050201','3001990000','3001990001','4002020400','6111020102','6111030102','6201020100','6204010000','6205010000','6301020000','6404020100','6601110500','6801020000')
    for accNo in unbalance_Account_List:
        search_Account_List(accNo)    