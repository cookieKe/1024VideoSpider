# coding:utf-8
#from getallpage import Spider1024
from threading import Thread
from models import Url_Link
from getallpage import Spider1024
import global_var
import time
import re

# 定时起爬虫的类
class SpiderTesk(Thread):
	def run(self):
		if global_var.g_version_condition.acquire():
			while True:
				if global_var.g_version_flag%2 == 1: 
					global_var.g_data_from_mongo = self.getallpage()
					global_var.g_version_flag += 1
					global_var.g_version_condition.notify()
					
					print global_var.g_version_flag
				global_var.g_version_condition.wait()
				# 调试设为36s
				time.sleep(36)

	def getallpage(self):
		spider_list = []
		if global_var.g_version_flag == 1:
			page_pattern = re.compile('2">\D.*?</a><a href="thread0806.php\?fid=2&search=&page=(.*?)" id="last">')
			page_url = 'http://t66y.com/thread0806.php?fid=2'
			spider = Spider1024(page_url,'')
			page_count = spider.get_content(page_url,page_pattern)
			page_count = page_count[0]
			if page_count == '':
				page_count = '0'
		# 调试 page_count ＝ '2'
		page_count = str(global_var.g_version_condition % 10)
		#从每一页获取需要的链接
		for i in range(1,int(page_count)+1):
			print 'dscsdcdscdcsd'
			link_url = 'http://t66y.com/thread0806.php?fid=2&search=&page='+str(i)
			spider_list.append(Spider1024(link_url,''))
		for spider in spider_list:
			try:
				spider.run()
			except:
				spider_list.append(spider)
			time.sleep(2)

		for spider in spider_list:
			if spider.is_alive():
				spider.join()
		print 'getallpage to db OK!'

# 收到爬虫消息，刷新缓存的类
class RefreshCache(Thread):
	def run(self):
		print '---'
		if global_var.g_version_condition.acquire():
			print global_var.g_version_flag

			while True:
				if global_var.g_version_flag%2 == 0:
					self.refreshCache()
					global_var.g_version_condition.notify()
					global_var.g_version_flag += 1
				global_var.g_version_condition.wait()
				time.sleep(1)
		else:
			print 'something wrong'

	def refreshCache(self):
		global_var.g_data_from_mongo = Url_Link.objects.all()
		print 'refreshCache OK'

if __name__ == '__main__':
	print global_var.g_version_condition
	st = SpiderTesk()
	rc = RefreshCache()
	st.start()
	print '-------------'
	rc.start()