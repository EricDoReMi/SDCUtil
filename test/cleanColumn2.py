#encoding:utf-8

'''
增对大文件的读写
'''

try:
    f=open("C:\\Users\\Eric m shi\\Desktop\\666\\JE.txt",'rt',encoding='utf-8',errors='replace')
    f1=open("C:\\Users\\Eric m shi\\Desktop\\666\\JE_back.txt","at+",encoding='utf-8',errors='replace')
    l_decs=[]

    num=0
    lineList=[]
    lineList.append("Company\tglICUT\tglICU\tglDCT\tglDOC\tglKCO\tglCO\tglDGJ\tglMCU\tglOBJ\tglSUb\tamount\tglLT\tglJELN\tglPN\tglTORG\tglUSER\tglDICJ\tgmR022\tglEXA\tglEXR\n")
    for line in f:
        l_orc=line.split('\t')
        if 'glICUT' not in l_orc[1]:
            l_pro=l_orc[19:]
            str_tmp=(''.join(l_pro)).replace('\t','')
            l_replace=[]
            l_replace.append(str_tmp)
            l_dec=l_orc[:19]+l_replace[::]
            del l_replace
            str_dec='\t'.join(l_dec)
             
            lineList.append(str_dec)
            
            if num%500000==0:
                if num!=0:
                    f1.writelines(lineList)
                    lineList.clear()  
        num+=1
        
    f1.writelines(lineList)
except Exception as e:
    print(num)
    raise(e)
finally:
    f1.close()
    f.close()

    
    

