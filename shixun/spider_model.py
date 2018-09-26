
# coding: utf-8

# In[1]:


import requests
import re
from lxml import etree
from collections import OrderedDict
from queue import Queue
import json
import threading
from jsonpath_rw import jsonpath,parse


# In[2]:


URL_JFK = 'localhost:8080'


# In[3]:


#查询模板信息
def getdata():
    #从数据库中取数据,解析json返回字典对象
    URL_HERE = '/findAll'
    url = URL_JFK+URL_HERE
    #print(url)
    data_res = requests.post(url,data=None)
    
    print("data_res:",data_res,"来自getdata()方法")
    
    #data_json = str(data_res)
    #print(data_json)
    
    data = data_res.json()
    #print(data)
    
    return data


# In[4]:


#test cell
#ini_url = 'www'
#currentLevel = 1

#一会儿加个循环，对每个模板都爬
#data = getdata()[1]
#print("data:  ",data)


# In[32]:


#向表2里插数据
def saveToTable2(startUrl,currentLevel,urllist):
    #将数据整理成合适的形式，json传输到数据库，存到表2中
    URL_HERE = '/addUrlInfo'
    url = URL_JFK+URL_HERE

    #ret = []
    for i in range(len(urllist)):
        item = OrderedDict()
        item.clear()
        
        item['url'] = urllist[i]
        item['startUrl'] = startUrl
        item['currentLevel'] = currentLevel
        
        #ret.append(item)
        ret_json = json.dumps(item,ensure_ascii=False)
        print("来自向表2存数据，存入的数据：",ret_json)
        
        headers = {'Content-Type':'application/json'}
        #r = requests.post(url,data=ret_json.encode('utf-8'))
        r = requests.post(url,data=ret_json.encode('utf-8'),headers=headers)
        
        res=r.json()
    
    
    
    return res


# In[ ]:


#测试cell
#ini_url = 'www'
#currentLevel = 1

#data = getdata()
#print("data:  ",data)



#urllist = ['url1:dfajskld','url2:dfas3432432','url3:adfaasdf']
#r1 = saveToTable2(ini_url,currentLevel,urllist)
#print("r1往表2里存的结果",r1)


# In[48]:


#查表2，只返回url的list
def getdata2(startUrl,currentLevel):
    URL_HERE = '/findNextUrl'
    url = URL_JFK+URL_HERE
    
    item = OrderedDict()
    item.clear()
    
    item['startUrl'] = startUrl
    item['currentLevel'] = currentLevel
    
    sendjson = json.dumps(item,ensure_ascii=False)
    
    headers = {'Content-Type':'application/json'}
    res_json = requests.post(url,data=sendjson.encode('utf-8'),headers=headers)
    
    #解析获得的json
    #res = json.loads(res_json)
    res = res_json.json()
    print("来自getData2方法：从表二中取到了:",res)
    return res


# In[ ]:


#test cell
#ini_url = 'www'
#currentLevel = 1

#data2 = getdata2(ini_url,currentLevel)
#print("data2:    ",data2)


# In[7]:


#向表3中添加数据
def saveToTable3(url_table3,data):
    
    URL_HERE = '/addParameters'
    url = URL_JFK+URL_HERE
    
    
    #ret = []
    for i in range(len(data)):
        dict = data[i]
        rank = dict['rank']
        name = dict['name']
        value = dict['value']
        
        item = OrderedDict()
        item.clear()
    
        item['url'] = url_table3
        item['rank'] = rank
        item['name'] = name 
        item['value'] = value
        
        #ret.append(item)
        
        
        headers = {'Content-Type':'application/json'}
        ret_json = json.dumps(item,ensure_ascii=False)
        print("来自向表3存，数据为：",ret_json)
        
        r_re = requests.post(url,data=ret_json.encode('utf-8'),headers=headers)
    
    
        r = r_re.json()
    
    return r
   


# In[ ]:


#test cell
#ini_url = 'www'
#currentLevel = 1


#table3data=[{'rank':'0','name':'n1','value':None},{'rank':'1','name':'n2','value':32},{'rank':'2','name':'n3','value':None}]
#r2 = saveToTable3(ini_url,table3data)
#print("r2往表3里存的结果：  ",r2)


# In[8]:


def getdata3(url_table3):
    URL_HERE = '/findParameters'
    url = URL_JFK+URL_HERE
    
    item = OrderedDict()
    item.clear()
    
    item['url'] = url_table3
    sendjson = json.dumps(item,ensure_ascii=False)
    headers = {'Content-Type':'application/json'}
    res_json = requests.post(url,data=sendjson.encode('utf-8'),headers=headers)
    #print(res_json)
    #解析获得的json
    #res = json.loads(res_josn)
    res = res_json.json()
    #print(res)
    
    return res 
    


# In[22]:


#test cell
#ini_url = 'www'
#currentLevel = 1


#data3 = getdata3(ini_url)
#print("data3:  ",data3)


# In[9]:


def getdata4(startUrl,currentLevel):
    URL_HERE = '/findMatchInfo'
    url = URL_JFK+URL_HERE
    
    item = OrderedDict()
    item.clear()
    
    item['startUrl'] = startUrl
    item['currentLevel'] = currentLevel
    
    headers = {'Content-Type':'application/json'}
    
    sendjson = json.dumps(item,ensure_ascii=False)
    
    res_json = requests.post(url,data=sendjson.encode('utf-8'),headers=headers)
    
    #解析获得的json
    #res = json.loads(res_json)
    res = res_json.json()[0]
    
    return res 
    


# In[80]:


#test cell
#ini_url = 'https://data-gkcx.eol.cn/soudaxue/querySpecialtyScore.html?messtype=jsonp&callback=jQuery183011759433663494101_1532413675802&provinceforschool=&schooltype=&page=1&size=10&keyWord=&schoolproperty=&schoolflag=&province=&fstype=&zhaoshengpici=&fsyear=&zytype=&_=1532413676106'
#currentLevel = 0


#与数据库中数据相匹配才行
#data4= getdata4(ini_url,currentLevel)
#print("data4:   ",data4)


# In[10]:


'''
向表3中添加数据
添加一条参数信息：
url:	/addParameters
parameters:	String url, int rank, String name, String value
response:	{flag:true}

在表3种查询数据，返回
查找某url的参数信息：
url:	/findParameters
parameters: String url
response:	List<Parameter>

在表4中查数据
查找某url某一层的匹配信息：
url:	/findMatchInfo
parameters:String startUrl, int currentLevel
response: List<MatchView>
			{ [ {token, pattern, wherePagenumber, whereSize, total}, … ] }

'''


# In[25]:


def getPage(url,isStatic,headers):
    if isStatic:
        #静态网页请求方法
        print("来着getpage方法：url：",url)
        r = requests.get(url)
        html = r.text
        s = etree.HTML(html)
    else:
        #动态网页请求方法
        r = requests.get(url,headers=headers)
        html = r.text
        s = html

    return s


# In[11]:


#用截取方式获得想要的字符串
#regex为正则表达式，s为被匹配的字符串，total是正则表达式获取的数据条数
def getByRegex(regex,s,total):
    #print("From method getByRegex(),regex:",regex)
    #print("From method getByRegex(),str:",s)
    #print("From method getByRegex(),total:",total)
    matchObj = re.match(r''+(regex),s,re.S)
    Content = []
    for i in range(1,total+1):
        #print("From method getByRegex(),No.%s round"%i)
        con = matchObj.group(i)
        Content.append(con)
    return Content

#matchOBJ = re.match(r''+(regex), ini_url, re.S)


# In[12]:


#用xpath的方式获得想要的字符串
#xpath为xpath的表达式，s为待匹配的内容
def getByXpath(xpath,s):
    content = s.xpath(xpath)
    return content


# In[13]:


#用json方式获得想要的元素
def getByJpath(jpath,s1):
    s = json.loads(s1)
    #print(s,"from getbyjpath")
    #print(type(s),"from method getByJpath,type(s)")
    jpath_real = parse(jpath)
    content_tem = jpath_real.find(s)
    content = [match.value for match in jpath_real.find(s)]
    print(content,"from method getByJpath,content")
    
    return content


# In[64]:


def getXpathData1(xpath,s):
    xpathset = xpath.split(',')
    
    xpath0 = xpathset[0]
    provincePath = xpathset[1]
    yearPath = xpathset[2]
    subjectPath = xpathset[3]
    piciPath = xpathset[4]
    scorePath = xpathset[5]
    
    count_xpath = xpath0+provincePath
    for_count = s.xpath(count_xpath)
    count = len(for_count)
    
    ret=[]
    
    for j in range(count):
        lstu_province = s.xpath(xpath0+'['+str(j+2)+']'+provincePath)
        if len(lstu_province)!=0:
            stu_province = lstu_province[0]
        else:
            stu_province = None
        
        
        lyear = s.xpath(xpath0+'['+str(j+2)+']'+yearPath)
        if len(lyear)!=0:
            year = lyear[0]
        else:
            year = None
        
        
        
        lsubject = s.xpath(xpath0+'['+str(j+2)+']'+subjectPath)
        if len(lsubject)!=0:
            subject = lsubject[0]
        else:
            subject = None
                
        
        lpici = s.xpath(xpath0+'['+str(j+2)+']'+piciPath)
        if len(lpici)!=0:
            pici = lpici[0]
        else:
            pici = None
            
        
        lscore = s.xpath(xpath0+'['+str(j+2)+']'+scorePath)
        if len(lscore)!=0:
            score = lscore[0]
        else:
            score = None
            
            
        item = OrderedDict()
        item.clear()
        
        item['province'] = stu_province
        item['year'] = year
        item['category'] = subject
        item['batch'] = pici
        item['grade'] = score
        
        ret.append(item)
    
    #data = {}
    return ret

                
        
    


# In[15]:


def getXpathData(xpath,s):
    xpathset = xpath.split(',')
    
    xpath0 = xpathset[0]
    majorPath = xpathset[1]
    schoolPath = xpathset[2]
    avscorePath = xpathset[3]
    hiscorePath = xpathset[4]
    provincePath = xpathset[5]
    subjectPath = xpathset[6]
    yearPath = xpathset[7]
    piciPath = xpathset[8]
    
    
    #输入样例：xpath = "//*[@id="wrapper"]/div[4]/table/tr,/td[1]//text(),/td[2]//text(),/td[3]//text(),/td[4]//text(),/td[5]//text(),/td[6]//text(),/td[7]//text(),/td[8]//text()"
    #按照专业、学校、平均分、最高分、省份、文理科、年份、批次、最低分的顺序输入
    
    count_xpath= xpath0+yearPath
    for_count = s.xpath(count_xpath)
    count = len(for_count)
    
    for j in range(count):
        lmajor = s.xpath(xpath0+'['+str(j+2)+']'+majorPath)
        if len(lmajor)!=0:
            major = lmajor[0]
        else:
            major = None
                
        lschool = s.xpath(xpath0+'['+str(j+2)+']'+schoolPath)
        if len(lschool)!=0:
            school = lschool[0]
        else:
            school = None
                
        lav_score = s.xpath(xpath0+'['+str(j+2)+']'+avscorePath)
        if len(lav_score)!=0:
            av_score = lav_score[0]
        else:
            av_score = None
                
        lhi_score = s.xpath(xpath0+'['+str(j+2)+']'+hiscorePath)
        if len(lhi_score)!=0:
            hi_score = lhi_score[0]
        else:
            hi_score = None
                
        lstu_province = s.xpath(xpath0+'['+str(j+2)+']'+provincePath)
        if len(lstu_province)!=0:
            stu_province = lstu_province[0]
        else:
            stu_province = None
                
        lsubject = s.xpath(xpath0+'['+str(j+2)+']'+subjectPath)
        if len(lsubject)!=0:
            subject = lsubject[0]
        else:
            subject = None
                
        lyear = s.xpath(xpath0+'['+str(j+2)+']'+yearPath)
        if len(lyear)!=0:
            year = lyear[0]
        else:
            year = None
                
        lpici = s.xpath(xpath0+'['+str(j+2)+']'+piciPath)
        if len(lpici)!=0:
            pici = lpici[0]
        else:
            pici = None
            
            
        #print(major)
        #print(school)
            
        item = OrderedDict()
        item.clear()
            
            
            
        if school=="--" or school=="------" or school=='':
            school = None
            item['schoolName'] = school
        else:
            item['schoolName'] = school
             
            
        if stu_province=="--" or stu_province=="------" or stu_province=='':
            stu_province = None
            item['province'] = stu_province
        else:
            item['province'] = stu_province   
            
            
        if year=="--" or year=="------" or year=='':
            year = None
            item['year'] = year
        else:
            item['year'] = year
                
            
        if subject=="--" or subject=="------" or subject=='':
            subject = None
            item['category'] = subject
        else:
            item['category'] = subject
                
            
        if major=="--" or major=="------" or major=='':
            major = None
            item['major'] = major
        else:
            item['major'] = major
                
                
        if pici=="--" or pici=="------" or pici=='' or pici==None or pici=='-----':
            pici = None
            item['batch'] = pici
        else:
            item['batch'] = pici[1:]
            
            
        if av_score=="--" or av_score=="------" or av_score=='':
            av_score = None
            item['avegrade'] = av_score
        else:
            item['avegrade'] = av_score
                
            
        if hi_score=="--" or hi_score=="------" or hi_score=='':
            hi_score = None
            item['maxgrade'] = hi_score
        else:
            item['maxgrade'] = hi_score
                
            
            
            
        #item['school_name'] = school
        #item['province'] = stu_province
        #item['year'] = year
        #item['category'] = subject
        #item['major'] = major
        #item['batch'] = pici
        #item['avegrade'] = av_score
        #item['maxgrade'] = hi_score
            
        item['mingrade'] = None
            
            
        ret.append(item)
        
    return ret
    
    
    
    
    
    


# In[16]:


#用jsonpath的方式获得想要的字符串
#Jpath为jsonpath的表达式，s为待匹配的json内容,字符串类型
def getJpathData(Jpath,s,size):
    #解析json获取内容时所用的的方法
    
    
    #把jsonpath表达式，按“，”截开
    JpathSet = Jpath.split(',')
    
    #输入样例：
    #顺序：学校，省份，年份，文理科，专业，批次，平均分，最高分，最低分
    
    #jsonobj =json.loads(s)
    jsonobj = s
    
    ret = []
    
    for i in range(size):
        item = OrderedDict()
        item.clear()
        
        jpath_sn = parse(JpathSet[0])
        json_schoolname = jpath_sn.find(jsonobj)
        sn = [match.value for match in jpath_sn.find(jsonobj)][i-1]
        #schoolname = json.dumps(sn,indent=4,ensure_ascii=False)
        if sn=="--":
            sn = None
            item['schoolName'] = sn
        else:
            item['schoolName'] = sn
            
        
        
        jpath_pv = parse(JpathSet[1])
        json_province = jpath_pv.find(jsonobj)
        pv = [match.value for match in jpath_pv.find(jsonobj)][i-1]
        #province = json.dumps(pv,indent=4,ensure_ascii=False)
        if pv=="--":
            pv = None
            item['province'] = pv
        else:
            item['province'] = pv
            
    
    
        jpath_year = parse(JpathSet[2])
        json_year = jpath_year.find(jsonobj)
        yr = [match.value for match in jpath_year.find(jsonobj)][i-1]
        #year = json.dumps(yr,indent=4,ensure_ascii=False)
        if yr=="--":
            yr = None
            item['year'] = yr
        else:
            item['year'] = yr
            
    
        jpath_st = parse(JpathSet[3])
        json_st = jpath_st.find(jsonobj)
        st = [match.value for match in jpath_st.find(jsonobj)][i-1]
        #studenttype = json.dumps(st,indent=4,ensure_ascii=False)
        if st=="--":
            st = None
            item['category'] = st
        else:
            item['category'] = st
            
            
            
    
    
        jpath_major = parse(JpathSet[4])
        json_major = jpath_major.find(jsonobj)
        mj = [match.value for match in jpath_major.find(jsonobj)][i-1]
        #major = json.dumps(mj,indent=4,ensure_ascii=False)
        if mj=="--":
            mj = None
            item['major'] = mj
        else:
            item['major'] = mj
            
            
            
        
        
        jpath_pici = parse(JpathSet[5])
        json_pici = jpath_pici.find(jsonobj)
        pc = [match.value for match in jpath_pici.find(jsonobj)][i-1]
        #pici = json.dumps(pc,indent=4,ensure_ascii=False)
        if pc=="--":
            pc = None
            item['batch'] = pc
        else:
            item['batch'] = pc
            
    
    
    
        jpath_var = parse(JpathSet[6])
        json_var = jpath_var.find(jsonobj)
        ave = [match.value for match in jpath_var.find(jsonobj)][i-1]
        #var = json.dumps(ave,indent=4,ensure_ascii=False)
        if ave=="--":
            ave = None
            item['avegrade'] = ave
        else:
            item['avegrade'] = ave
            
    
    
    
        jpath_max = parse(JpathSet[7])
        json_max = jpath_max.find(jsonobj)
        ma = [match.value for match in jpath_max.find(jsonobj)][i-1]
        #maxscore = json.dumps(ma,indent=4,ensure_ascii=False)
        if ma=="--":
            ma = None
            item['maxgrade'] = ma
        else:
            item['maxgrade'] = ma
            
        
    
    
        jpath_min = parse(JpathSet[8])
        json_min = jpath_min.find(jsonobj)
        mi = [match.value for match in jpath_min.find(jsonobj)][i-1]
        #minscore = json.dumps(mi,indent=4,ensure_ascii=False)
        if mi=="--":
            mi = None
            item['mingrade'] = mi
        else:
            item['mingrade'] = mi
            
            
        
        
        ret.append(item)
    
    
    
    return ret


# In[17]:


#处理headers的方法
def handleHeaders(headers_str):
    headersset = headers_str.split('\'')
    item = {}

    count = int((len(headersset)-1)/4)
    print(count,"输出自handleHeaders()方法，表示headers中字段数")
    for i in range(count):
    #print(i)
    #print((4*i+1))
    #print(4*i+3)
    
        key = headersset[(4*i+1)]
        value = headersset[4*i+3]
    
        item[key] = value
    
    #print(key,value)
    #item[headersset[key]=value

    #print(item)
    
    
    return item
    


# In[98]:


#ini_url = "https://data-gkcx.eol.cn/soudaxue/querySpecialtyScore.html?messtype=jsonp&callback=jQuery183014377195846113588_1531220188434&provinceforschool=&schooltype=&page=15701&size=50&keyWord=&schoolproperty=&schoolflag=&province=&fstype=&zhaoshengpici=&fsyear=&zytype=&_=1531220188657"
#headers_in = "{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36', 'Cookie': 'tool_ipuse=211.87.236.7; tool_ipprovince=37; tool_iparea=3', 'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Connection': 'keep-alive', 'Host': 'data-gkcx.eol.cn', 'Referer': 'https://gkcx.eol.cn/soudaxue/querySpecialtyScore.html'}"

#isStatic = False
#level = 4



# In[65]:


#获得pagenum和url_model的各部分
#可以再将两层拆开为两个封装好的方法，进行调用
def getUrlStr(ini_url,headers_in,isStatic,level,URL_DATABASE):
#def getUrlStr(ini_url,headers_in,isStatic,level):
    
    print("from line 6,ini_url?:",ini_url)
    headers = handleHeaders(headers_in)
    
    if isStatic:
        #静态网页的处理
        currentLevel = 0
        currentUrl = ini_url 
        size = ''
        urllisttem = []
        urllisttem.append(currentUrl)
        ident = saveToTable2(ini_url,currentLevel,urllisttem)
        if ident==False:
            
            print("写入表2失败")
        
        #if currentLevel < level-1:
        for i in range(level):
            print("循环第%s层："%i)
            currentLevel = i
            
            #根据完善后的接口改参数，获取表2中的数据，以进行下一步操作：
            #根据获取的参数值，去表4中去对应数据
            data2 = getdata2(ini_url,currentLevel)
            
            
            #根据完善后的接口改参数，获取表4中的匹配方式，表达式
            data4 = getdata4(ini_url,currentLevel)
            #根据返回的json结构解析出方式、表达式
            exp = data4['pattern']
            method = int(data4['token'])
            pageLocation = int(data4['wherePagenumber'])
            sizeLocation = int(data4['whereSize'])
            total = int(data4['total'])

            #如果不是倒数第二层，操作的对象是通过匹配，提取当前url页面中的内容
            #如果是倒数第二层，操作对象是通过匹配分割当前url本身，获得pagenum和urlmodel，存入表3
            #如果是最后一层，则为从表3中读取数据，抓取最终的分数线等信息
            if currentLevel < level-2:
                
                for j in range(len(data2)):
                    currentUrl = data2[j]
                    s = getPage(currentUrl,isStatic,headers)
                    if method ==1:
                        urllist = getByXpath(exp,s)
                    elif method ==2:
                        urllist = getByRegex(exp,s,total)
                    elif method == 3:
                        urllist = getByJpath(exp,s)
                    else:
                        print("模板输入的匹配方式有误，模板无效")
                    ident = saveToTable2(ini_url,currentLevel+1,urllist)
                    #currentLevel = currentLevel+1
                    
            elif currentLevel == level-2:
                #截取url_model和pagenum，存到表3，此时已是末页
                for j in range(len(data2)):
                    currentUrl = data2[j]
                    #根据从表4中读到的数据
                    if method ==2:
                        #正则匹配操作
                        NameSet = getByRegex(exp,currentUrl,total)
                        ret_temp = []
                        for k in range(len(NameSet)):
                            if k<pageLocation-1:
                                item = OrderedDict()
                                item.clear()
                                
                                item['rank'] = k
                                item['name'] = NameSet[k]
                                item['value'] = None
                                
                                ret_temp.append(item)
                            
                            elif k==pageLocation-1:
                                #当前NameSet[k]为页号，应该放到rank为k-1的那一条的value中
                                ret_temp[k-1]['value'] = NameSet[k]
                            elif k>pageLocation-1:
                                #因为pagenum没有占rank，所以后面的rank都要减一
                                item = OrderedDict()
                                item.clear()
                                
                                item['rank'] = k-1
                                item['name'] = NameSet[k]
                                item['value'] = None
                                ret_temp.append(item)
                        
                        r = saveToTable3(currentUrl,ret_temp)
                        
                        if r == False:
    
                            print("存储数据到表3失败")
                        
                    else:
                        print("截取方式输入有误，模板无效")
                
            elif currentLevel ==level-1:
                #抓取实际页面内容存，json传给数据库，存储起来
                #根据上一层表2中的数据得到url，根据url访问表3
                #把新网址拼起来，爬取，转为json，打包发送
                print("来自104行的测试，ini_url&level-1",ini_url,currentLevel-1)
                data2 = getdata2(ini_url,currentLevel-1)
                print("从表2里读到数据",data2)
                for a in range(len(data2)):
                    print("开始表2的第%s条数据"%a)
                    currentUrl = data2[a]
                    data3 = getdata3(currentUrl)
                    #data4 = getdata4(ini_url,currentLevel)
                    
                    #method = int(data4['token'])
                    #exp = data4['pattern']
                    #total = int(data4['total'])
                    print("拼接时读到的data3：",data3)
                    
                    #把新网址拼起来
                    #strfinal = []
                    str_ini = '%s'
                    strlist = [str_ini for c in range(len(data3)+1)]
                    pagenum_local = ''
                    strfinal = ''
                    for b in range(len(data3)):
                        print("拼接到了第%s层"%b)
                        
                        dict_here = data3[b]
                        
                        if int(dict_here['rank'])<pageLocation-1 and int(dict_here['rank'])!=pageLocation-2:
                            strlist[int(dict_here['rank'])] = dict_here['name']
                        elif int(dict_here['rank'])<pageLocation-1 and int(dict_here['rank'])==pageLocation-2:
                            
                            strlist[int(dict_here['rank'])] = dict_here['name']
                            pagenum_local = dict_here['value']
                            print("pagenum_local=",pagenum_local)
                        elif int(dict_here['rank'])>=pageLocation-1:
                            #因为页码占了一位
                            strlist[int(dict_here['rank'])+1] = dict_here['name']
                    
                    
                        
                    for n in range(len(strlist)):
                        strfinal = strfinal+strlist[n]
                    print("url_model:",strfinal)
                    print("pagenum_local=",pagenum_local)
                    for m in range(1,int(pagenum_local)):
                        
                        print("开始爬取第%s页"%m)
                        url_spider = strfinal%m
                        s = getPage(url_spider,isStatic,headers)
                        
                        if method==1:
                            if URL_DATABASE=='/addCutoff':
                                content = getXpathData(exp,s)
                            elif URL_DATABASE=='/addPcutoff':
                                content = getXpathData1(exp,s)
                            
                        elif method ==2:
                            content = getByRegex(exp,s,total)
                        elif method ==3:
                            content = getByJpath(exp,s)
                        else:
                            print("模板输入的匹配方式有误，模板无效")
                        
                        
        
                        data = {'cutoffs':content}
                        json_str = json.dumps(data,ensure_ascii=False)
        
                        print(json_str)
        
                        headers_send = {'Content-Type':'application/json'}
                        #request = requests.post(URL_JFK+'/addCutoff', data=json_str.encode('utf-8'), headers=headers_send)
                        print("发出去了，静态")        
                    
                    #r_send = 
        
        
        #else if currentLevel = level-1:
           #倒数第二层提取pagenum
        
       
            
    else:
        #动态网页的处理
        
        currentLevel = 0
        currentUrl = ini_url
        size = ''
        jsonstr=''
        
        for i in range(level):
            print("当前循环，level：",i)
            currentLevel = i
            data4 = getdata4(ini_url,currentLevel)
            
            exp = data4['pattern']
            method = int(data4['token'])
            pageLocation = int(data4['wherePagenumber'])
            sizeLocation = int(data4['whereSize'])
            total = int(data4['total'])
        
            if currentLevel==0:
                currentUrl = ini_url
                s = getPage(currentUrl,isStatic,headers)
                if method ==1:
                    res_str = getByXpath(exp,s)
                elif method ==2:
                    res_str = getByRegex(exp,s,total)
                    jsonstr = res_str
                elif method ==3:
                    res_str = getByJpath(exp,s)
                    totalRecord = res_str[0]['totalRecord']['num']
                    
                    item = OrderedDict()
                    item.clear()
                    
                    item['rank'] = -1
                    item['name'] = totalRecord
                    item['value'] = None
                    
                    r_here = saveToTable3(ini_url,item)
            elif currentLevel<level-2 and currentLevel>0:
                #提取获得所有url的必要信息
                currentUrl = ini_url
                rethere=[]
                s = jsonstr
                if method ==1:
                    res_str = getByXpath(exp,s)
                elif method ==2:
                    res_str = getByRegex(exp,s,total)
                elif method ==3:
                    #print("来自大方法的第220行，exp：",exp,"s:",s,"type of s:",type(s[0]))
                    res_str = getByJpath(exp,s[0])
                    
                    #json_sr = jsonstr[0]
                    #print("来自大方法的221行，jsonstr[0]：",jsonstr[0],"type of jsonstr[0]",type(json_sr))
                    
                    totalRecord = res_str[0]
                    #print("来自大方法第226行，totalRecord = ",totalRecord)
                    
                    item = OrderedDict()
                    item.clear()
                    
                    item['rank'] = -1
                    item['name'] = totalRecord
                    item['value'] = None
                    
                    rethere.append(item)
                    
                    r_here = saveToTable3(ini_url,rethere)
            
            elif currentLevel== level-2:
                #通过截取操作，获得所有url，url_model，pagenum存到表3
                if method ==2:
                    #用正则匹配把url匹配出来
                    NameSet = getByRegex(exp,ini_url,total)
                    ret_temp = []
                    for k in range(len(NameSet)):
                        print("第二轮的第%s个正则表达："%k,NameSet[k])
                        if k<pageLocation-1:
                            if k != sizeLocation-1:
                                print("进入循环分支：k<pageLocation-1中的k != sizeLocation-1")
                                item = OrderedDict()
                                item.clear()
                        
                                item['rank']=k
                                item['name']=NameSet[k]
                                item['value']=None
                                
                                ret_temp.append(item)
                                
                            elif k==sizeLocation-1:
                                print("进入循环分支：k<pageLocation-1中的k == sizeLocation-1")
                                #存sizeLocation
                                item1 = OrderedDict()
                                item2 = OrderedDict()
                                item1.clear()
                                item2.clear()
                                
                                item1['rank']=k
                                item1['name']=NameSet[k]
                                item1['value']=None
                                
                                item2['rank']=-2
                                item2['name']=NameSet[k]
                                item2['value']=None
                                
                                #print("item1",item1)
                                #print("item2",item2)
                                ret_temp.append(item1)
                                ret_temp.append(item2)
                                
                                
                                
                        #elif k==pageLocation-1:
                            
                        elif k>pageLocation-1:
                            if k!=sizeLocation-1:
                                print("进入循环分支：k>pageLocation-1中的k != sizeLocation-1")
                                item = OrderedDict()
                                item.clear()
                                
                                item['rank'] = k-1
                                item['name'] = NameSet[k]
                                item['value'] = None
                                ret_temp.append(item)
                            elif k==sizeLocation-1:
                                
                                print("进入循环分支：k>pageLocation-1中的k == sizeLocation-1")
                                item1 = OrderedDict()
                                item2 = OrderedDict()
                                item1.clear()
                                item2.clear()
                                
                                item1['rank']=k-1
                                item1['name']=NameSet[k]
                                item1['value']=None
                                
                                item2['rank']=-2
                                item2['name']=NameSet[k]
                                item2['value']=None
                                size = NameSet[k]
                                
                                print(item1)
                                print(item2)
                                ret_temp.append(item1)
                                ret_temp.append(item2)
                        
                    r = saveToTable3(currentUrl,ret_temp)    
                    #从表三里取ini_url对应的rank为-1的元素，除以rank为-2的
                    #得到pagenum，当前NameSet[k]为页号，应该放到rank为k-1的那一条的value中
                    
                    #ret_temp.clear()
                    
                    data3 = getdata3(ini_url)
                    print("from line 314,data3",data3)
                    for i in range(len(data3)):
                        dict_table3 = data3[i]
                        if int(dict_table3['rank'])==-1:
                            totalcount = int(dict_table3['name'])
                        elif int(dict_table3['rank'])==-2:
                            pagesize = int(dict_table3['name'])
                            print("来自第321行，pagesize=",pagesize)
                    print
                    pagenum = int(totalcount/pagesize)
                    ret_temp[pageLocation-2]['value'] = pagenum
                    
                    r = saveToTable3(currentUrl,ret_temp)
                    
                    if r==False:
                    
                        print("存储数据到表3失败")
                    
                    
                    
                else:
                    print("模板输入错误，匹配方式无法获得url_model")
                
            elif currentLevel == level-1:
                #抓取实际页面内容存，json传给数据库，存储起来
                currentUrl=ini_url
                data3 = getdata3(currentUrl)
                
                #把新网址拼起来
                #strfinal = []
                str_ini = '%s'
                strlist = [str_ini for c in range(len(data3)-1)]
                print("from line 357,strlist:",strlist)
                pagenum_local = ''
                strfinal = ''
                for b in range(len(data3)):
                        
                    dict_here = data3[b]
                        
                    if int(dict_here['rank'])<pageLocation-2 and int(dict_here['rank'])>=0:
                        strlist[int(dict_here['rank'])] = dict_here['name']
                        print("rank：",int(dict_here['rank']),"name:",dict_here['name'])
                    elif int(dict_here['rank'])==pageLocation-2:
                            
                        strlist[int(dict_here['rank'])] = dict_here['name']
                        pagenum_local = dict_here['value']
                        
                        print("from line 372")
                        print("strlist[%s]"%int(dict_here['rank']),dict_here['name'])
                        print(pagenum_local)
                        
                        
                    elif int(dict_here['rank'])>pageLocation-2:
                        #因为页码占了一位
                        strlist[int(dict_here['rank'])+1] = dict_here['name']
                    
                    
                
                for n in range(len(strlist)):
                    strfinal = strfinal+strlist[n]
                    #print()
                    
                print("from 387",strlist[1])
                
                
                for m in range(1,int(pagenum_local)):
                    
                    str1='\('
                    str2='\);'
                    content='(.*)'
                    print("来自385行，strfinal：",strfinal)
                    url_spider = strfinal%m
                    
                    response = getPage(url_spider,isStatic,headers)
                    #print("from line 399:",response,"response type",type(response))
                    matchObj = re.match(r''+(strlist[1]+str1+content+str2),response,re.S)
                    #print(matchObj)
                    json_str = matchObj.group(1)
                    #print(json_str)
        
                    s = json.loads(json_str)
                    
                    
                    if method==1:
                        content = getXpathData(exp,s)
                    elif method ==2:
                        content = getByRegex(exp,s,total)
                    elif method ==3:
                        #s = json.loads(jsonstr)
                        #print("size:",size)
                        content = getJpathData(exp,s,int(size))
                    else:
                        print("模板输入的匹配方式有误，模板无效")
                        
                    data = {'cutoffs':content}
                    json_str1 = json.dumps(data,ensure_ascii=False)
                    
                    print("爬到了")
        
                    print(json_str1)
        
                    headers_send = {'Content-TypeDatabasecation/json'}
                    #request = requests.post(URL_JFK+URL_DATABASE, data=json_str1.encode('utf-8'), headers=headers_send)
                    #print("发出去了",request)
                    print("发出去了，动态")
                    
                        
    return 0
        
        


# In[66]:



dataSet = getdata()
#print("data:  ",data)
for n in range(len(dataSet)) :
    data = dataSet[n]
    
    ini_url = data['startUrl']

    if data['dynamic']==True:
        isStatic = False
    else:
        isStatic = True 

    level = data['level']

    #headers = handleHeaders(data['headers'])
    headers = data['headers']
    URL_DATABASE=data['target']

    print(headers)
    print(type(headers))
    
    a=getUrlStr(ini_url=ini_url,headers_in=headers,isStatic=isStatic,level=level,URL_DATABASE=URL_DATABASE)

    #a=getUrlStr(ini_url=ini_url,headers_in=headers,isStatic=isStatic,level=level)



    


# In[67]:


#a=getUrlStr(ini_url=ini_url,headers_in=headers,isStatic=isStatic,level=level,URL_DATABASE=URL_DATABASE)

#a=getUrlStr(ini_url=ini_url,headers_in=headers,isStatic=isStatic,level=level)


