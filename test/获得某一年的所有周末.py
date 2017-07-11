#encoding:utf-8
'''
Created on 23 Feb 2017

@author: Eric M Shi
'''
import calendar

def getWeekend(myYear):
    myYearStr=str(myYear)
    
    #用于放周末的日期字符串列表
    weekendsStrList=[]
    c=calendar.TextCalendar()
    
    
    monStr=""#用来给月份加0
    for mon in range(1,13):
        #monthdayscalendar()方法可以获得每个星期的日期编码的list
        if mon<10:
            monStr="0"+str(mon)
        else:
            monStr=str(mon)
            
        for week in c.monthdayscalendar(myYear, mon):
            for i in range(5,7):#5,7是周六和周日
                if week[i]!=0:
                    if week[i]<10:
                        weekendsStrList.append(myYearStr+monStr+"0"+str(week[i]))
                    else:
                        weekendsStrList.append(myYearStr+monStr+str(week[i]))
    
    return weekendsStrList
  

if __name__ == '__main__':
    f1=open('./weekends.txt','w')
    
    weekends=getWeekend(2017)
    
    for line in weekends:
        f1.writelines(line+"\n")
        
    f1.close()

