# -*- codeing = utf-8 -*-
# @Time : 2021/4/1 20:41
# @Author : Lucidity
# @File : Test_Steam.py
# @Software: PyCharm
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt
import selenium
# 宏定义：
findApp_ID = re.compile(r'<tr.*data-appid="(.*?)".*>', re.S)  # 找App_ID的规则


# 主函数：
def main():
    print("Begin！")
    url = "https://steamdb.info/sales/"  # 访问url
    datalist = getData(url)  # 调用getData(url)来抓取所有的APP_ID

    # for i in datalist:
    #     All_Url = 'https://steamdb.info/app/' + i + '/'  # 构造出所有的APP_ID
    #     print(All_Url)
    # for i in datalist:
        # All_APPID = i
        # print(All_APPID)
        # data = datalist[i]
        # print(i)




    # 3.保存数据
    savepath = ".\\APPID.xls"  # 保存路径    .\\表示保存在当前路径,如果不写就默认保存在当前路径下
    saveData(datalist, savepath)
    print("保存完毕！")



def getData(url):
    datalist = []  # 创建一个数据清单用来存放数据
    html = askURL(url)  # 调用askURL函数，它会返回一个页面的html，askURL()的函数定义在下面
    soup = BeautifulSoup(html, "html.parser")  # 利用BeautifulSoup来解析获取到的html
    for item in soup.find_all('tr', class_="app appimg"):  # 找到APP_ID所在的节点中的所有内容
        # print(item)
        item = str(item)  # 将这些获取到内容转为字符串
        App_ID = re.findall(findApp_ID, item)  # 利用正则表达式来找到这些内容中所有的APP_ID
        App_ID = str(App_ID)  # 将APP_ID转为字符串
        # 去除多余的字符：
        App_ID = App_ID.replace("'", "")
        App_ID = App_ID.replace("[", "")
        App_ID = App_ID.replace("]", "")
        datalist.append(App_ID)  # 将这些APP_ID都存入datalist中
        # print(App_ID)  # 打印所有的APP_ID   (2320个，2021.4.1)
    return datalist  # 返回这些datalist


# 得到一个指定URL的网页内容
def askURL(url):
    # 模拟浏览器，之前只加user-agent就行，但现在要再加个cookie才行
    # 需要及时跟换cookie
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.63",
        "cookie": "__cfduid=dbbed75d3ef9e52f13aca76ae680b96ce1615473064; _ga=GA1.2.3493531793.1615473083; cf_chl_2=f95a1fb79f4aa98; cf_chl_prog=x19; cf_clearance=4791655e501515f626248fd9d25bd968489b9b00-1617281476-0-150; __cf_bm=57f57f024a3bf01fcc61547d656eaf19d11afe09-1617281488-1800-Ac9+Y2JolvGr90SRuBmH2ouJ8Htf3hx03roGTRIvIV0E3zHeUnH+OyN00sLjQ7rYx/pKh0QjcCMDsbwbfhfXBKSK7wR1g4KIDEYyHYFYyxXkLX7E9SxLDM3HjIM7NAbR1Q=="
    }

    request = urllib.request.Request(url, headers=head)  # 调用urllib库中的Request函数来获取请求，并向服务器发送我们刚刚封装的头部信息
    html = ""
    # 错误捕获
    try:
        response = urllib.request.urlopen(request)  # 用urllib库中的urlopen函数打开刚刚获取到的数据
        html = response.read().decode("utf-8")  # 读取其中的数据，并且以utf-8的方式解码
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html  # 注意这里不要把return html 放到if的作用域里了，不然上面接受不到html自然会报错

def saveData(datalist,savepath):
    print("saving...")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象，style_compression=0表示压缩样式
    sheet = book.add_sheet('APPID',cell_overwrite_ok=True)  # 创建一个工作表，并且取名为豆瓣电影SteamGameHistoryPrice，cell_overwrite_ok=True表示覆盖以前的信息


    # col = ("APPID")      # 一些信息
    # 把col这个信息放进excel表格里，有几个就是0到几
    # for i in range(0, 1):          # 1列
    sheet.write(0,0, "APPID")  # 把APPID  放进第一行第一列中


    # APPID都放进第一列中
    for i in range(2315):       # 2361行
        # data = datalist[i] # 报错：TypeError: list indices must be integers or slices, not str
        # for j in datalist:
        data = datalist[i]

        sheet.write(i+1,0,data) # 报错： TypeError: can only concatenate str (not "int") to str


    book.save(savepath)



if __name__ == '__main__':
    main()
    print("Well Down!")
