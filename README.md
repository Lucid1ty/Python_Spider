# Python_Spider
SteamGameHistoryPrice.py是一个爬取steam游戏历史价格的爬虫（未完成），它有三个阶段：

一：获取所有游戏的APP-ID(这样就可以构造出所有游戏页面的url)
二：利用selenium依次访问每一个游戏页面
三：然后访问下一个游戏页面并且重复步骤二直到所有的游戏页面都被爬取完毕。

目前阶段一已经完成。

SteamTest.py则能保存抓取到的APPID。（已完成）



