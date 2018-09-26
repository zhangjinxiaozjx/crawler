#! python2
import urllib.request
import sys
import threading
from bs4 import BeautifulSoup
from selenium import webdriver
from xlrd import open_workbook
from xlutils.copy import copy

workplace = "C:/Users/user/Desktop/schoolline.xls"
threadnum = 10
sheet = 0
weburl = "https://gkcx.eol.cn/soudaxue/queryProvinceScore.html?&page="
row_each_page = 10
all_page = 12951
adv_school = 1
list = 8


page = 1
def getpage():
    global page
    return page
def setpage():
    global page
    page +=1


def getthreadnum():
    global threadnum
    return threadnum

finish = 0
def getfinish():
    global finish
    return finish
def setfinish():
    global finish
    finish +=1

rb = open_workbook(workplace)
rs = rb.sheet_by_index(sheet)
wb = copy(rb)
ws = wb.get_sheet(sheet)



class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print ("开启线程： " + self.name)

        global all_page
        while(getpage()<=all_page):
            # 获取锁
            threadLock.acquire()
            thispage = getpage()
            setpage()
            # 释放锁
            threadLock.release()
            doit(thispage)

        print("结束线程： " + self.name)
        setfinish()
        if(getfinish() == threadnum):
            global workplace
            wb.save(workplace)
            print("全部结束")




threadLock = threading.Lock()

def doit(thispage):
        #12951   第一页1所广告大学
        print("打印第"+str(thispage)+"页")

        global weburl
        url = weburl+str(thispage)
        driver = webdriver.PhantomJS(executable_path='C:/Python27/Scripts/phantomjs-2.1.1-windows/bin/phantomjs.exe')
        driver.get(url)
        html = driver.page_source
        #print (driver.page_source)

        #response = urllib.request.urlopen("https://gkcx.eol.cn/soudaxue/queryschool.html?&page=1")
        #soup = BeautifulSoup(response, "html.parser")

        soup = BeautifulSoup(html, "html.parser")
        #print(soup)

        table = soup.find('table',id='seachtab',width='750',class_='lin-sechple-table')

        tbody = table.find('tbody')

        alltr = tbody.find_all('tr')

        #table = []
        global row_each_page
        row = (thispage-1)*row_each_page

        index = 0
        for n in alltr:
            global adv_school
            if (not ((thispage == 1) and (index < adv_school))):
                alltd = n.find_all('td')
                count = 0
                global list
                while count<list:
                    ws.write(row, count, alltd[count].text)
                    count+=1
                row = row + 1
            index = index + 1

        if thispage%100==0:
            global workplace
            wb.save(workplace)

threads = []

# 创建新线程
count = 0
while count<getthreadnum():
    thread1 = myThread(1, "Thread-"+str(count), 1)
    thread1.start()
    threads.append(thread1)
    count +=1


# 等待所有线程完成
for t in threads:
    t.join()
print ("退出主线程")

