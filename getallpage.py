#-*- coding:utf-8 -*-

import urllib2,random
import cookielib
import re
import threading
import os
import time

'''

url = 'http://t66y.com/htm_data/2/1512/1744885.html'
ua_index = random.randint(0,3)%4
print ua_index
request = urllib2.Request(url,headers={'user-agent':ua[ua_index]})

cookie = cookielib.MozillaCookieJar()
handler=urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)

response = opener.open(request)
cookie.save(ignore_discard=True, ignore_expires=True)
content = response.read()
request.close()

'''

ua = ['Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',\
		'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729; InfoPath.3; GWX:QUALIFIED)',\
		'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',\
		'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0']

class Spider1024(threading.Thread):
	def __init__(self,baseurl,store_path):
		threading.Thread.__init__(self)
		self.url = baseurl
		self.store_path = store_path

	def get_content(self,url,pattern):
		try:
			page_url = self.url
			request = urllib2.Request(url,headers={'user-agent':ua[random.randint(0,3)]})
			response = urllib2.urlopen(request)
			content = response.read()
			res = pattern.findall(content)
			return res
		except Exception as e:
			print('Error '+str(e)+'!')
			return ['']


	def run(self):
		#先提取单个页面具体链接
		pattern = re.compile('<h3><a href="(.*?)html" target="_blank" id="">')
		page_url_href = self.get_content(self.url,pattern)
		#再去获取具体的页面
		download_url_list = []
		page_url_prefix = 'http://t66y.com/'
		for item in page_url_href:
			page_url = page_url_prefix + item +'html'
			#print page_url
			download_pattern = re.compile('<a target="_blank" .*?rmdown.*?>(.*?)</a>')
			download_url = self.get_content(page_url,download_pattern)
			if download_url != []:	
				download_url_list.append(download_url)
			time.sleep(1)
		try:
			file=open(self.store_path,'w')
			for item in download_url_list:
				file.write(item+'\n')
			file.close()
		except Exception as e:
			print('Error '+str(e)+'!')


if __name__ == '__main__':
	#爬虫列表
	spider_list = []
	store_path = 'url.txt'
	#获取总页数
	page_pattern = re.compile('2">\D.*?</a><a href="thread0806.php\?fid=2&search=&page=(.*?)" id="last">')
	page_url = 'http://t66y.com/thread0806.php?fid=2'
	sp1 = Spider1024(page_url,'')
	page_count = sp1.get_content(page_url,page_pattern)
	print page_count
	page_count = page_count[0]
	if page_count == '':
		page_count = '0'
	#从每一页获取需要的链接
	for i in range(1,int(page_count)+1):
		link_url = 'http://t66y.com/thread0806.php?fid=2&search=&page='+str(i)
		spider_list.add(Spider1024(link_url,store_path))
	for spider in spider_list:
		try:
			spider.run()
		except:
			spider_list.add(spider)
		time.sleep(2)

	for spider in spider_list:
		spider.join()