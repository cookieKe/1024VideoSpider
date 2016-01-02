# 1024VideoSpider
A spider to download the torrent file of rmdown.com used by 1024 automatically

## 想要实现的功能
爬取1024外链在rmdown的网页，自动下载相关种子。
 - getallpage.py 因为网站被墙，爬取原始网页的部分放在VPS上，用来获取rmdown的相关链接。这一部分最后想利用Flask做一个简单的服务器，方便墙内获取资源。
 - 1024.py rmdown在国内可以访问，下载种子的部分放在国内。
 - 1024.txt 是getallpage.py获取到的内容。
 
## 需要学习的内容
1. python多线程
2. 爬虫进阶
3. Flask框架
4. mongodb
