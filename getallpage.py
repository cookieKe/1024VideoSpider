#-*- coding:utf-8 -*-

import urllib2,random
import cookielib
import re
import threading
import os
import time
import randomUA
from models import Url_Link
from app import db

class Spider1024(threading.Thread):
	def __init__(self,baseurl,store_path):
		threading.Thread.__init__(self)
		self.url = baseurl
		self.store_path = store_path

	def get_content(self,url,pattern):
		try:
			page_url = self.url
			request = urllib2.Request(url,headers={'user-agent':randomUA.random_ua()})#,'cookie':'__cfduid=d50071b2a7f9ad6ebd19e90bb50be84981452179480; 227c9_lastfid=0; 227c9_lastvisit=0%091452179585%09%2Fprofile.php%3Faction%3Dshow%26uid%3D18844; CNZZDATA950900=cnzz_eid%3D970883499-1452175128-%26ntime%3D1452175549'})
			response = urllib2.urlopen(request)
			content = response.read()
			res = pattern.findall(content)
			print res
			return res
		except Exception as e:
			print 'Get content Error '+str(e)+'!'
			return ['']

	def get_src_content(self,url):
		try:
			page_url = self.url
			request = urllib2.Request(url,headers={'user-agent':randomUA.random_ua()})#,'cookie':'__cfduid=d50071b2a7f9ad6ebd19e90bb50be84981452179480; 227c9_lastfid=0; 227c9_lastvisit=0%091452179585%09%2Fprofile.php%3Faction%3Dshow%26uid%3D18844; CNZZDATA950900=cnzz_eid%3D970883499-1452175128-%26ntime%3D1452175549'})
			response = urllib2.urlopen(request)
			content = response.read()
			#response.close()
			return content
		except Exception as e:
			print 'Get content Error '+str(e)+'!'
			return ''

	def run(self):
		print self.url
		#先提取单个页面具体链接
		pattern = re.compile('<h3><a href="(.*?)html" target="_blank" id="">')
		page_url_href = self.get_content(self.url,pattern)
		#再去获取具体的页面
		page_url_prefix = 'http://t66y.com/'
		for item in page_url_href:
			page_url = page_url_prefix + item +'html'
			#print page_url
			
			try:
				download_pattern = re.compile('<a target="_blank" .*?rmdown.*?>(.*?)</a>')
				download_content = self.get_src_content(page_url)
				download_url = download_pattern.findall(download_content)

			
				if download_url != []:
					#获取下载链接	
					download_url_link = download_url[0]
					print download_url_link
					#获取标题内容
					title_pattern = re.compile('<title>(.*?)</title>')
					title_content = title_pattern.findall(download_content)[0]
					title_content = title_content.decode('gbk').encode('utf-8')
					print title_content
					if download_url_link != '':
						url_link = Url_Link(title_content,download_url_link)
						url_link.save()
				time.sleep(1)
			except Exception as e:
				print 'Run Error '+str(e)+'!'


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
	page_count = '2'
	#从每一页获取需要的链接
	for i in range(1,int(page_count)+1):
		print 'dscsdcdscdcsd'
		link_url = 'http://t66y.com/thread0806.php?fid=2&search=&page='+str(i)
		spider_list.append(Spider1024(link_url,store_path))
	for spider in spider_list:
		try:
			spider.run()
		except:
			spider_list.append(spider)
		time.sleep(2)

	for spider in spider_list:
		spider.join()