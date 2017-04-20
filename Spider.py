# coding=utf-8
import random
import re
import urllib2
from bs4 import BeautifulSoup
import xlwt

#Some User Agents
hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
    {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
    {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
    {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
    {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]

def get_content(url="http://jn.58.com/chuzu/0/?PGTID=0d3090a7-0010-9239-0d99-87eb1a11b582&ClickID=4"):
    "获取源码"
    req = urllib2.Request(url, headers=hds[random.randint(0, len(hds) - 1)])
    source_code = urllib2.urlopen(req, timeout=10).read()
    soup = BeautifulSoup(source_code,"html.parser")
    return soup

def get(items):
    "获取内容"
    rows = []
    for listli in items.findAll('li', attrs={'logr': True,'sortid':True}):
        row = []
        #名称
        tongji_label = listli.find('h2').find('a').renderContents().strip()
        row.append(tongji_label)
        #厅室
        for i in listli.find('p','room').renderContents().strip().split():
            row.append(i.strip())
        #房东
        reg_geren = re.compile(r'<span>来自个人房源：</span>(.*?)<em class="bbonline".*?',re.S)
        row.append(re.findall(reg_geren,listli.find('p', 'geren').renderContents().strip())[0])
        #发表时间
        row.append(listli.find('div','sendTime').renderContents().strip().split()[0])
        #价格
        row.append(listli.find('div','money').find('b').renderContents().strip().split()[0])
        rows.append(row)
    return rows

def excel_write(rows):
    "写入excel"
    rownum = 1
    newTable = 'test.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('test1')
    headData = ['租房名称','厅室','面积','房东','发表时间','价格']
    for colnum in range(0,6):
        ws.write(0,colnum,headData[colnum],xlwt.easyxf('font: bold on'))

    for row in rows:
        for colnum in range(0, 6):
            ws.write(rownum, colnum, row[colnum])
        rownum+=1
    wb.save(newTable)

if __name__ == '__main__':
    items =  get_content()
    rows = get(items)
    excel_write(rows)
