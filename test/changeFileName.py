#encoding:utf-8
import os
import codecs
import sys



if __name__ == '__main__':
    
    #路径需修改，\用\\代替   
    rootdir=r"C:\Users\Eric m shi\Desktop\111"
 
    filenames=os.listdir(rootdir)
    
    for a in range(len(filenames)):
        os.rename(rootdir+os.sep+filenames[a],rootdir+os.sep+filenames[a].replace(r".txt_back.txt",r".txt")) 
