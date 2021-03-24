# -*- codeing = utf-8 -*-
# @Time : 2020/12/9 19:55
# @Author : Lucidity
# @File : spider(douban).py
# @Software: PyCharm
#mainURL:https://movie.douban.com/top250
from bs4 import BeautifulSoup           # 网页解析，获取数据
import re       # 正则表达式，进行文字匹配
import urllib.request,urllib.error      # 制定URL，获取网页数据
import xlwt     # 进行excel操作
import sqlite3  # 进行SQLite数据操作

#主函数
def main():
    baseurl = "https://movie.douban.com/top250?start="
    datalist = getData(baseurl)     # 利用getData（）函数来得到网页中的数据
    savepath = ".\\豆瓣电影Top250.xls"   # 保存路径    .\\表示保存在当前路径,如果不写就默认保存在当前路径下
    # 3.保存数据
    saveData(datalist,savepath)


    # askURL("https://movie.douban.com/top250?start=")


'''宏定义变量：'''
# 电影详情连接                   宏定义变量：findLink  表示正则表达式的规则（获取影片详情连接的规则）
findLink = re.compile(r'<a href="(.*?)">',re.S)      # 创建正则表达式对象，表示规则（字符串模式），.表示字符（单个字符），*表示很多个，？表示一个或很多个，因为连接里面有双引号，所以这里用单引号
# 影片图片的连接的规则
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)    # 与上面那个findLink同理，记得带上括号表示一组,re.S 让换行符包含在字符中    因为.（点）这个概念是不包含换行符的
# 影片的片名：
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 影片的一句短评：
findsentence = re.compile(r'<span class="inq">(.*?)</span>',re.S)           # 别忘了问号
# 评价人数:
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 豆瓣评分：
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')

# 找到一句短评：
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 找到影片相关内容：
findBd = re.compile(r'<p class="">(.*?) </p>',re.S)



#爬取网页
def getData(baaeurl):
    datalist =[]
    # 写个for循环来得到豆瓣电影top250的所有页面，总共拿到了10页（一页有25个电影）
    for i in range(0,10):       # 通过控制循环次数来控制访问获取的页面数
        url = baaeurl + str(i*25)
        html = askURL(url)      # 保存获取到的页面源代码

        # 然后逐一解析网页，得到一个网页解析一个，所以要在for循环里解析，#查找符合要求的字符串，形成列表
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):
            # print(item)   # 测试：查看电影item全部信息
            data = []       # 保存一部电影的所有信息
            item = str(item)# 把item里面都东西都变成字符串，这样方便正则表达式进行匹配


            # 下面我们利用正则表达式来找我们需要的信息，找到一个我们就利用append（）函数来添加一个到data里面
            # 影片详情的连接：
            link = re.findall(findLink,item)[0]# re库用来通过正则表达式查找指定的字符串，findLink：正则表达式的规则，item：符合这个规则的字符串，[0]表示我们只获取找到的字符串中的第一个
            data.append(link)                  # 把找到的link加到data里
            # 电影的图片连接：
            imgSrc = re.findall(findImgSrc,item)[0]
            data.append(imgSrc)
            # 电影名字：
            Titles = re.findall(findTitle, item)    # 可能只有一个中文名或者有多个外文名
            if (len(Titles) == 2):                  # 如果Titles=2，就说明它既有中文名又有外文名
                Chinese_name = Titles[0]
                data.append(Chinese_name)           # 添加中文名
                other_name = Titles[1].replace("/","")# 添加外文名并将其中的/替换为空格（去除无关符号）
                data.append(other_name)             # 添加外文名
            else:                                   # 只有中文名的情况
                data.append(Titles[0])
                data.append('')                     # 没有外文名就留空


            # 评分：
            rating = re.findall(findRating,item)[0]
            data.append(rating)

            # 评论人数：
            judgeNum = re.findall(findJudge,item)[0]
            data.append(judgeNum)

            # 概述：（有些电影可能没有概述）
            inq = re.findall(findInq,item)
            if len(inq) != 0:       # 有概述时：
                inq = inq[0].replace("。","")        # 将其中的句号替换成空格
                data.append(inq)
            else:
                data.append(" ")        # 留空

            # 影片相关内容：
            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)     # 去掉<br/>,把bd中的<br(\s+)?/>(\s+)?替换成空格
            bd = re.sub('/'," ",bd)                     # 把/替换成空格
            data.append(bd.strip())     # 用strip去掉里面的空格

            datalist.append(data)           # 把上面处理好的data放入datalist
    # print(datalist)


    return datalist


# 得到一个指定URL的网页内容
def askURL(url):
    # 模拟浏览器头部，封装信息
    head ={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.57"}
    # 调用urllib库中的Request函数来获取请求，并向服务器发送我们刚刚封装的头部信息
    request = urllib.request.Request(url,headers=head)
    html=""
    # 错误捕获（可能会出现一些异常）
    try:
        # 用urllib库中的urlopen函数打开刚刚获取到的数据
        response = urllib.request.urlopen(request)
        # 读取其中的数据，并且以utf-8的方式解码
        html = response.read().decode("utf-8")
        # 打印得到的内容
        # print(html)
    except urllib.error.URLError as e:
        # 捕获错误：如果遇到编码错误则打印出来
        if hasattr(e,"code"):
            print(e.code)
        # 捕获错误：把错误原因打印出来
        if hasattr(e,"reason"):
            print(e.reason)
    return html             # 注意这里不要把return html 放到if的作用域里了，不然上面接受不到html自然会报错


# 保存数据的函数定义
def saveData(datalist,savepath):
    print("save...")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)# 创建workbook对象，style_compression=0表示压缩样式
    sheet = book.add_sheet('豆瓣电影top250',cell_overwrite_ok=True)  # 创建一个工作表，并且取名为豆瓣电影top250，cell_overwrite_ok=True表示覆盖以前的信息
    col = ("电影详情连接","图片连接","影片中文名","影片外文名","评分","评价数","一句短评","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i]) # 列名一个个写进去
    for i in range(0,250):
        print("第%d条"%(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])

    book.save(savepath)            # 保存





if __name__ == "__main__":          # 当程序执行时就执行以下的内容
    main()
    print("爬取完毕！")














