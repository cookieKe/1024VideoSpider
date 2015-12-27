#-*- coding:utf-8 -*-
import os,re,urllib2,urllib,gzip
from io import BytesIO
import randomUA,random
import time
import cookielib
import socket

UA_Boundary = {'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36':'----WebKitFormBoundary',\
				'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko':'-------------------------',\
				'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0':'---------------------------'}

def rand(flag):
	text = ''
	possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
	if flag == 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0':
		for i in range(0,14):
			text += possible[random.randint(0,61)];
	elif flag == 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko':
		for i in range(0,14):
			text += possible[random.randint(0,61)];
	else:
		for i in range(0,15):
			text += possible[random.randint(52,61)];
	return text;

def post_request(rmdownloadurl,random_ua):
	request2 = urllib2.Request(url = 'http://www.rmdown.com/download.php')#,data = data)
	request2.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36')
	request2.add_header('Connection','keep-alive')
	request2.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	request2.add_header('Referer',rmdownloadurl.replace('\n',''))
	request2.add_header('Accept-Encoding','gzip, deflate')
	
	return request2

def download_start():
	#1024.txt存储了所有的下载链接
	fs = open('1024.txt','r')
	url_list = fs.readlines()
	fs.close()
	flag = 0
	interval = 10
	torrent_list = []
	for rmdownloadurl in url_list:
		print rmdownloadurl
		random_ua = randomUA.random_ua()
		request = urllib2.Request(rmdownloadurl)
		request.add_header('User-Agent',random_ua)
		request.add_header('Refer',rmdownloadurl)
		request.add_header('Upgrade-Insecure-Requests','1')
		request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
		if flag != 0:
			request.add_header('Cookie',cookie_value)
		#创建cookie处理器
		cookie = cookielib.CookieJar()
		handler=urllib2.HTTPCookieProcessor(cookie)
		opener = urllib2.build_opener(handler)
		#此处的open方法同urllib2的urlopen方法，也可以传入request
		try:
			response = opener.open(request,timeout=30)
			downloadpage = response.read()
					#读取boundary reff
			regex_download_pattern = re.compile('')
			reff_reg = re.compile('<INPUT .*?reff.*?value="(.*?)">')
			reff = re.findall(reff_reg,downloadpage)[0]
		except socket.timeout as e:
			print '-----------------------------------------'
		except:
			print '-----------------Game over---------------'
		
		if flag == 0:
			for item in cookie:
				cookie_value = item.name+'='+item.value
				break
			flag = 1

		#发起POST请求

		post_req = post_request(rmdownloadurl,random_ua)
		#boundary = '------WebKitFormBoundary'+rand()
		boundary = UA_Boundary[random_ua]+rand(random_ua)
		hashvalue = rmdownloadurl.split('=')[1]
		#与浏览器相关
		post_req.add_header('Content-type','multipart/form-data; boundary='+boundary)
		post_req.add_header('Cookie',cookie_value)
		payload = '--'+boundary+'\r\n'+'Content-Disposition: form-data; name="ref"'+'\r\n\r\n'+hashvalue.replace('\n','')+'\r\n'+'--'+boundary \
					+'\r\n'+'Content-Disposition: form-data; name="reff"'+'\r\n\r\n'+reff+'\r\n'+'--'+boundary+'\r\n'+'Content-Disposition: form-data; name="submit"'+'\r\n\r\n' \
					+'download'+'\r\n'+'--'+boundary+'--'+'\r\n'
		post_req.add_data(payload)
		try:
			req = urllib2.urlopen(post_req,timeout=30)
			data = BytesIO(req.read())
			torrent_list.append(data)
		except socket.timeout as e:
			time.sleep(30)
			print '-----------------------------------------'
			url_list.append(rmdownloadurl)
		except:
			print 'boom!'
		#StringIO 会出错
		
		response.close()
		req.close()
		print len(torrent_list)
		
		#interval += 10
		#time.sleep(0.1)
	for item in torrent_list:
		gziper = gzip.GzipFile(fileobj = item)
		decode = gziper.read()
		torrent_fs = open('F:\\1024torrent\\'+rand('1')+'.torrent','wb')
		torrent_fs.write(decode)
		torrent_fs.close()

if __name__ == '__main__':
	download_start()

