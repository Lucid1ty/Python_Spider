

# Python爬虫(爬取steam游戏历史价格)

## 总体思路：

步骤一：获取所有游戏的APP-ID(这样就可以构造出所有游戏页面的url)



步骤二：利用selenium依次访问每一个游戏页面

访问时：需要等待页面加载完全（确保下载按钮加载出来），然后用find_element_by_class_name等方法定位到下载按钮，点击下载。



步骤三：然后访问下一个游戏页面并且重复步骤二直到所有的游戏页面都被爬取完毕。



步骤四：等待下载，全部游戏的数据下载完毕后：

```python
print("下载完毕！！！")
```





## 分而治之：

### 步骤一：抓取所有游戏的APP-ID

首先研究下需要爬取的网页：https://steamdb.info/sales/  （主url）

页面如下：

![image-20210316135633060](C:\Users\Lucidity\AppData\Roaming\Typora\typora-user-images\image-20210316135633060.png)

分析这个页面：可以发现右边显示有2787个游戏或产品（2021.3.16，下午1：57）

我们点击第一个游戏（[ Metro 2033](https://steamdb.info/app/43110/)）进入页面：

![image-20210316140136199](C:\Users\Lucidity\AppData\Roaming\Typora\typora-user-images\image-20210316140136199.png)

很碰巧的是这款游戏似乎从一开始就是免费的，所以这款游戏没有历史价格的页面。

我们先不管这个，回到之前的页面点击第二个游戏（[Going Under](https://steamdb.info/app/1154810/)）：

![image-20210316140413487](C:\Users\Lucidity\AppData\Roaming\Typora\typora-user-images\image-20210316140413487.png)

鼠标滚轮往下拉就能看到以上页面，注意到：这个历史价格图标和那个下载按钮是下拉到下面的时候才刷新出来的（这意味着我们要爬取的这部分内容是动态加载出来的---需要用到动态网页爬取相关知识）。

我们点击按钮，选择下载CSV文件，

![image-20210316140801709](C:\Users\Lucidity\AppData\Roaming\Typora\typora-user-images\image-20210316140801709.png)

![image-20210316141053571](C:\Users\Lucidity\AppData\Roaming\Typora\typora-user-images\image-20210316141053571.png)

电脑就会自动开始下载，会在浏览器的左下角出现。

打开下载好的文件：就能看到历史价格了。

![image-20210316141214384](C:\Users\Lucidity\AppData\Roaming\Typora\typora-user-images\image-20210316141214384.png)

以上就是下载一个游戏历史价格的操作过程，让我们回到：https://steamdb.info/sales/

我们先获取这个网页的源码：

```python
import urllib.request,urllib.error      # 制定URL，获取网页数据
url = 'https://steamdb.info/sales/'
request = urllib.request.Request(url)      # 调用urllib库中的Request函数来获取请求
html=""
try:
    response = urllib.request.urlopen(request)  # 用urllib库中的urlopen函数打开刚刚获取到的数据
    html = response.read().decode("utf-8")  # 读取其中的数据，并且以utf-8的方式解码
except urllib.error.URLError as e:
    if hasattr(e, "code"):
        print(e.code)
    if hasattr(e, "reason"):
        print(e.reason)

print(html)           
    
```

运行后：

![image-20210316142833133](C:\Users\Lucidity\AppData\Roaming\Typora\typora-user-images\image-20210316142833133.png)

注意到：我们把url换成百度的话是能正常返回网页源码的。

所以我们需要伪装一下（伪装成一个浏览器）

在我们正常访问这个页面时（https://steamdb.info/sales/）

按下F12：

![image-20210316143231005](C:\Users\Lucidity\AppData\Roaming\Typora\typora-user-images\image-20210316143231005.png)

选择我用红色框起来的“网络”（右上角），然后刷新页面：

出现一堆东西，我们把进度条拉到最上，然后点击第一个：

![image-20210316143647380](C:\Users\Lucidity\AppData\Roaming\Typora\typora-user-images\image-20210316143647380.png)

点开后：

![image-20210316143727027](C:\Users\Lucidity\AppData\Roaming\Typora\typora-user-images\image-20210316143727027.png)

可以看到我们正常访问时向网页发送的请求头：其中的user-agent和cookie是我们需要模拟的。

我们把它们复制下来，开始模拟头部：

```python
import urllib.request,urllib.error      # 制定URL，获取网页数据
url = 'https://steamdb.info/sales/'
head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54 FS",
        "cookie": "__cfduid=dbbed75d3ef9e52f13aca76ae680b96ce1615473064; _ga=GA1.2.3493531793.1615473083; cf_clearance=6d607da9057861f87e062ff41fc9944982ffdcdc-1615867031-0-150; __cf_bm=bfba887cb5cdb113b147db2c72f9ad4c77bde81a-1615877382-1800-AXREWjoL5zsbUABtQzPf8+j1LAdwUxw2J+ZxQTwd0hX9pt5sLJJ3GAGECPMLW4CIpo/6ahhbFvStpjAFQr4oRacT6vftYHi/12STXlPus0Dp5kmmHWAav99vgInq6vIELg=="
}

request = urllib.request.Request(url,headers=head)      # 调用urllib库中的Request函数来获取请求
html = " "
try:
    response = urllib.request.urlopen(request)  # 用urllib库中的urlopen函数打开刚刚获取到的数据
    html = response.read().decode("utf-8")  # 读取其中的数据，并且以utf-8的方式解码
except urllib.error.URLError as e:
    if hasattr(e, "code"):
        print(e.code)
    if hasattr(e, "reason"):
        print(e.reason)

print(html)
```

运行后就能得到源码（如果报错“503”或者“无法获取到地址信息”请检查你的cookie是否是最新的，需要及时更新cookie）

源码太长就不放上来了

通过阅读部分源码，聪明的你不难发现其中的神秘数字似乎代表着什么：

![image-20210316150245999](C:\Users\Lucidity\AppData\Roaming\Typora\typora-user-images\image-20210316150245999.png)

把这个数字放到![image-20210316150331203](C:\Users\Lucidity\AppData\Roaming\Typora\typora-user-images\image-20210316150331203.png)这里。

回车，惊奇的发现它就是每个游戏都有的独一无二的APP-ID！！！

也就是说所有的APP-ID都藏在了https://steamdb.info/sales/这个页面的源码里。





那么接下来我们就抓取这些APP-ID：

需要先引入一些库：

```python
from bs4 import BeautifulSoup           # 网页解析，获取数据
import re                               # 正则表达式，进行文字匹配
import urllib.request,urllib.error      # 制定URL，获取网页数据
```

```python
findApp_ID = re.compile(r'<tr.*data-appid="(.*?)".*>',re.S)     # 找App_ID的规则(正则表达式)

```

写成函数：

```python
def getApp_ID(url):
    datalist =[]                # 创建一个数据清单用来存放数据
    html = askURL(url)          # 调用askURL函数，它会返回一个页面的html，askURL()的函数定义在下面
    soup = BeautifulSoup(html, "html.parser")       # 利用BeautifulSoup来解析获取到的html
    for item in soup.find_all('tr', class_="app appimg"):   # 找到APP_ID所在的节点中的所有内容
        # print(item)
        item = str(item)                                    # 将这些获取到内容转为字符串
        App_ID = re.findall(findApp_ID, item)               # 利用正则表达式来找到这些内容中所有的APP_ID
        App_ID = str(App_ID)                                # 将APP_ID转为字符串
        # 去除多余的字符：
        App_ID = App_ID.replace("'","")
        App_ID = App_ID.replace("[", "")
        App_ID = App_ID.replace("]", "")
        datalist.append(App_ID)                             # 将这些APP_ID都存入datalist中
        print(App_ID)                                       # 打印所有的APP_ID
    return datalist                                         # 返回这些datalist
```

访问url的函数：

```python
def askURL(url):
    # 模拟浏览器，之前只加user-agent就行，但现在要再加个cookie才行
    # 需要及时跟换cookie
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54 FS",
        "cookie": "__cfduid=dbbed75d3ef9e52f13aca76ae680b96ce1615473064; _ga=GA1.2.3493531793.1615473083; cf_clearance=6d607da9057861f87e062ff41fc9944982ffdcdc-1615867031-0-150; __cf_bm=bfba887cb5cdb113b147db2c72f9ad4c77bde81a-1615877382-1800-AXREWjoL5zsbUABtQzPf8+j1LAdwUxw2J+ZxQTwd0hX9pt5sLJJ3GAGECPMLW4CIpo/6ahhbFvStpjAFQr4oRacT6vftYHi/12STXlPus0Dp5kmmHWAav99vgInq6vIELg=="
}


    request = urllib.request.Request(url,headers=head)      # 调用urllib库中的Request函数来获取请求，并向服务器发送我们刚刚封装的头部信息
    html=""
    # 错误捕获
    try:
        response = urllib.request.urlopen(request)      # 用urllib库中的urlopen函数打开刚刚获取到的数据
        html = response.read().decode("utf-8")          # 读取其中的数据，并且以utf-8的方式解码
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html             # 注意这里不要把return html 放到if的作用域里了，不然上面接受不到html自然会报错
```

所以代码现在长这样：

```python
from bs4 import BeautifulSoup           # 网页解析，获取数据
import re                               # 正则表达式，进行文字匹配
import urllib.request,urllib.error      # 制定URL，获取网页数据
# 宏定义：
findApp_ID = re.compile(r'<tr.*data-appid="(.*?)".*>',re.S)     # 找App_ID的规则

# 主函数：
def main():
    print("Begin！")
    url = "https://steamdb.info/sales/"         # 主url
    datalist = getApp_ID(url)  # 调用getData(url)来抓取所有的APP_ID
    
# 抓取所有游戏的APP-ID函数定义：
def getApp_ID(url):
    datalist =[]                # 创建一个数据清单用来存放数据
    html = askURL(url)          # 调用askURL函数，它会返回一个页面的html，askURL()的函数定义在下面
    soup = BeautifulSoup(html, "html.parser")       # 利用BeautifulSoup来解析获取到的html
    for item in soup.find_all('tr', class_="app appimg"):   # 找到APP_ID所在的节点中的所有内容
        # print(item)
        item = str(item)                                    # 将这些获取到内容转为字符串
        App_ID = re.findall(findApp_ID, item)               # 利用正则表达式来找到这些内容中所有的APP_ID
        App_ID = str(App_ID)                                # 将APP_ID转为字符串
        # 去除多余的字符：
        App_ID = App_ID.replace("'","")
        App_ID = App_ID.replace("[", "")
        App_ID = App_ID.replace("]", "")
        datalist.append(App_ID)                             # 将这些APP_ID都存入datalist中
        print(App_ID)                                       # 打印所有的APP_ID
    return datalist                                         # 返回这些datalist

# 得到一个指定URL的网页内容
def askURL(url):
    # 模拟浏览器，之前只加user-agent就行，但现在要再加个cookie才行
    # 需要及时跟换cookie
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54 FS",
        "cookie": "__cfduid=dbbed75d3ef9e52f13aca76ae680b96ce1615473064; _ga=GA1.2.3493531793.1615473083; cf_clearance=6d607da9057861f87e062ff41fc9944982ffdcdc-1615867031-0-150; __cf_bm=bfba887cb5cdb113b147db2c72f9ad4c77bde81a-1615877382-1800-AXREWjoL5zsbUABtQzPf8+j1LAdwUxw2J+ZxQTwd0hX9pt5sLJJ3GAGECPMLW4CIpo/6ahhbFvStpjAFQr4oRacT6vftYHi/12STXlPus0Dp5kmmHWAav99vgInq6vIELg=="
}
    request = urllib.request.Request(url,headers=head)      # 调用urllib库中的Request函数来获取请求，并向服务器发送我们刚刚封装的头部信息
    html=""
    # 错误捕获
    try:
        response = urllib.request.urlopen(request)      # 用urllib库中的urlopen函数打开刚刚获取到的数据
        html = response.read().decode("utf-8")          # 读取其中的数据，并且以utf-8的方式解码
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html             # 注意这里不要把return html 放到if的作用域里了，不然上面接受不到html自然会报错

if __name__ == '__main__':
    main()
```

运行后就能得到所有的APP-ID

部分结果如下：

![image-20210316152804435](C:\Users\Lucidity\AppData\Roaming\Typora\typora-user-images\image-20210316152804435.png)

通过以上代码，步骤一就完成了。

### 步骤二：

利用selenium访问（需要配置好selenium和浏览器驱动器：chromedrive或者geckodriver）

我这里用的是Firefox所以需要配置geckodriver

```python
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
options = webdriver.FirefoxOptions()
# 模拟头部
options.add_argument('User-Agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0')

browser = webdriver.Firefox(options=options)
browser.get('https://steamdb.info/app/1318690/')

cookie_1 = {"name": "__cfduid", "value": "d4035db3bb96795383bd5a320d6a18fab1615641573"}
cookie_2 = {"name": "_ga", "value": "GA1.2.471995972.1608102460"}
cookie_3 = {"name": "cf_clearance", "value": "5ba95d114299813011dbfbe7df7faee9ebd15cfc-1615867660-0-150"}
# 第三个cookie需要及时更新
time.sleep(5)

browser.add_cookie(cookie_1)
browser.add_cookie(cookie_2)
browser.add_cookie(cookie_3)

# 拖拽进度条至最下面
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
```

以上代码运行时浏览器中的价格图表出不来：

![image-20210316154356133](C:\Users\Lucidity\AppData\Roaming\Typora\typora-user-images\image-20210316154356133.png)

解决办法？

未完待续。。。









### 步骤三：





### 步骤四：

















# 其他：

## 1.selenium携带user-agent

![image-20210314224047199](C:\Users\Lucidity\AppData\Roaming\Typora\typora-user-images\image-20210314224047199.png)

```python
from selenium import webdriver
browser = webdriver.Firefox()
browser.get('https://www.baidu.com')
print(browser.page_source)
browser.close()
```

以上代码就能直接访问百度并且返回源码

换成https://steamdb.info/app/1203630/

访问时页面如下：

![image-20210315000548787](C:\Users\Lucidity\AppData\Roaming\Typora\typora-user-images\image-20210315000548787.png)

RAY一直刷新，进不去页面，但能返回源码。



让selenium携带user-agent试试？

```python
from selenium import webdriver
import time
# 进入浏览器设置
options = webdriver.FirefoxOptions()
# 更换头部
options.add_argument('User-Agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0')
browser = webdriver.Firefox(options=options)
browser.get('https://steamdb.info/app/1203630/')
time.sleep(25)
print(browser.page_source)
browser.close()
```

注意User-Agent后面的空格，把冒号换成等号也可以

但是还是进不去页面，能返回源码。





携带cookies试试？

1.获取cookies

```python
from selenium import webdriver
from time import sleep
import json
if __name__ == '__main__':
    driver = webdriver.Firefox()
    # driver.maximize_window()
    driver.get('https://steamdb.info/app/1203630/')
    sleep(3)
    dictCookies = driver.get_cookies()  # 获取list的cookies
    jsonCookies = json.dumps(dictCookies)  # 转换成字符串保存
    with open('Steam_cookies.txt', 'w') as f:
        f.write(jsonCookies)
    print('cookies保存成功！')
```

```
[{"name": "__cfduid", "value": "d87dc650a4845864db5ab138a8a7fce2e1615739014", "path": "/", "domain": ".steamdb.info", "secure": true, "httpOnly": true, "expiry": 1618331014, "sameSite": "Lax"}, {"name": "cf_chl_2", "value": "7f9e53970356bf5", "path": "/", "domain": "steamdb.info", "secure": false, "httpOnly": false, "expiry": 1615742630, "sameSite": "None"}, {"name": "cf_chl_prog", "value": "e", "path": "/", "domain": "steamdb.info", "secure": false, "httpOnly": false, "expiry": 1615742630, "sameSite": "None"}]
```

这就是针对https://steamdb.info/app/1203630/获取到的cookies

2.携带cookies

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
def browser_initial():
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # browser = webdriver.Chrome(options=chrome_options)
    browser = webdriver.Firefox()
    # browser.maximize_window()
    browser.get(
        'https://steamdb.info/app/1203630/')
    return browser

def log_csdn(browser):
    with open('steam_cookies.txt', 'r', encoding='utf8') as f:
        listCookies = json.loads(f.read())

    # 往browser里添加cookies

    for cookie in listCookies:
        cookie_dict = {
            'domain': '.douyu.com',
            'name': cookie.get('name'),
            'value': cookie.get('value'),
            "expires": '',
            'path': '/',
            'httpOnly': False,
            'HostOnly': False,
            'Secure': False
        }
        browser.get('https://steamdb.info/app/1203630/')
        browser.add_cookie(cookie_dict)
    browser.refresh()  # 刷新网页,cookies才成功

if __name__ == "__main__":
    browser = browser_initial()
    log_csdn(browser)

```

# 报错：

C:\Users\Lucidity\AppData\Local\Programs\Python\Python38\python.exe D:/Code/Python/Spider/selenium(携带cookies).py
Traceback (most recent call last):
  File "D:/Code/Python/Spider/selenium(携带cookies).py", line 40, in <module>
    log_csdn(browser)
  File "D:/Code/Python/Spider/selenium(携带cookies).py", line 35, in log_csdn
    browser.add_cookie(cookie_dict)
  File "C:\Users\Lucidity\AppData\Local\Programs\Python\Python38\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 894, in add_cookie
    self.execute(Command.ADD_COOKIE, {'cookie': cookie_dict})
  File "C:\Users\Lucidity\AppData\Local\Programs\Python\Python38\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 321, in execute
    self.error_handler.check_response(response)
  File "C:\Users\Lucidity\AppData\Local\Programs\Python\Python38\lib\site-packages\selenium\webdriver\remote\errorhandler.py", line 242, in check_response
    raise exception_class(message, screen, stacktrace)
**selenium.common.exceptions.InvalidCookieDomainException: Message: Cookies may only be set for the current domain (steamdb.info)**

Process finished with exit code 1

![image-20210315003156863](C:\Users\Lucidity\AppData\Roaming\Typora\typora-user-images\image-20210315003156863.png)

## error：只能为当前域设置Cookie

# 解决办法？

## 办法一：

![image-20210315150445581](C:\Users\Lucidity\AppData\Roaming\Typora\typora-user-images\image-20210315150445581.png)

![image-20210315004640996](C:\Users\Lucidity\AppData\Roaming\Typora\typora-user-images\image-20210315004640996.png)

这个方法不行



## 办法二：

![image-20210315131204392](C:\Users\Lucidity\AppData\Roaming\Typora\typora-user-images\image-20210315131204392.png)

这个方法不知道怎么操作



现在的代码：

```python
from selenium import webdriver
import time
options = webdriver.FirefoxOptions()
options.add_argument('User-Agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0')

browser = webdriver.Firefox(options=options)
browser.get('https://steamdb.info/app/1203630/')
cookie_1 = {"name": "__cf_bm ","value": "d3077fd727e44dbdb11bdc03a1f8114756d0f2b5-1615786644-1800-AaP8e+8WqBbCBhyHjwA7My6s8VBolq+cOIzC12JWy4oFCIJMqkcs9SfRtPiyfD2Rcwjc+jbaMvg+ChkulODJBSYXGlyzCcjm+taKeMyqDaImFQJh6SZUNuYGybwtRCy+Pg=="}
cookie_2 = {"name": "__cfduid","value": "d4035db3bb96795383bd5a320d6a18fab1615641573"}


time.sleep(5)
browser.get('https://steamdb.info/app/1203630/')
browser.add_cookie(cookie_1)
browser.add_cookie(cookie_2)
browser.get('https://steamdb.info/app/1203630/')
```

# 携带cookies登录百度：

```python
from selenium import webdriver
import time
browser = webdriver.Firefox()
browser.get('https://www.baidu.com')
cookie_1 = {"name": "BAIDUID","value": "CDE20A37A9EDA248CEC6E6328261FE44:FG=1"}
cookie_2 = {"name": "BDUSS","value": "FlDN0h2OXRUQnRzVFEtY1l3a0FsWUFwa1lIRko5MThYakxTMUl1SU9FRFVsM1pnSVFBQUFBJCQAAAAAAAAAAAEAAAAueBbmvtjV89Xz1fPV8wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANQKT2DUCk9gd"}
time.sleep(3)
browser.add_cookie(cookie_1)
browser.add_cookie(cookie_2)
browser.get('https://www.baidu.com')
print("登录成功")
```

## 抓cookies的时候要在自动打开的浏览器抓？







## 现在能用selenium打开https://steamdb.info/app/1203630/了！！！



代码如下：

```python
from selenium import webdriver
import time
options = webdriver.FirefoxOptions()
# 模拟头部
options.add_argument('User-Agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0')

browser = webdriver.Firefox(options=options)
browser.get('https://steamdb.info/app/1318690/')

cookie_1 = {"name": "__cfduid", "value": "d4035db3bb96795383bd5a320d6a18fab1615641573"}
cookie_2 = {"name": "_ga", "value": "GA1.2.471995972.1608102460"}
cookie_3 = {"name": "cf_clearance", "value": "757ebdb21b983439bbbff2f863429181d683aed7-1615738118-0-150"}
# cookie_4 = {"name": "", "value": ""}
# cookie_5 = {"name": "", "value": ""}
# cookie_6 = {"name": "", "value": ""}

time.sleep(5)

browser.add_cookie(cookie_1)
browser.add_cookie(cookie_2)
browser.add_cookie(cookie_3)
browser.get('https://steamdb.info/app/1318690/')
# 拖拽进度条至最下面
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
# browser.execute_script('alert("To Bottom")')
print("访问成功")
time.sleep(5)

button = browser.find_element_by_class_name('highcharts-button-symbol')
button.click()
```

但是。。

![image-20210315160435734](C:\Users\Lucidity\AppData\Roaming\Typora\typora-user-images\image-20210315160435734.png)



这里加载不出来？？？

在正常访问时要拉到下面才会刷出来这个价格图标页面

![image-20210315170509519](C:\Users\Lucidity\AppData\Roaming\Typora\typora-user-images\image-20210315170509519.png)



