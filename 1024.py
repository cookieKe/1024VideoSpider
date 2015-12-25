#-*- coding:utf-8 -*-
import os,re,urllib2,urllib,gzip
from io import BytesIO

#1024.txt存储了网页的整个内容
fs = open('1024.txt','r')
whole_content = fs.read()
pattern = re.compile('<a target="_blank" .*?rmdown.*?>(.*?)</a>')
items = re.findall(pattern,whole_content)
print items[0]
request = urllib2.Request(items[0])
request.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
request.add_header('Refer',items[0])
reponse = urllib2.urlopen(request)
downloadpage = reponse.read()

#获取下载链接
#读取boundary reff
regex_download_pattern = re.compile('')
reff_reg = re.compile('<INPUT .*?reff.*?value="(.*?)">')
reff = re.findall(reff_reg,downloadpage)[0]
#发起POST请求
#post_content = {'ref':'153d470b3e4a1f473fea0e63a4d21572a4d4e52146a','reff':'MTQ1MTA1MjI2MQ=='}
#data = urllib.urlencode(post_content)
request2 = urllib2.Request(url = 'http://www.rmdown.com/download.php')#,data = data)
request2.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
request2.add_header('Refer',items[0])
request2.add_header('Connection','keep-alive')
request2.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
request2.add_header('Accept-Encoding','gzip, deflate')
boundary = '------WebKitFormBoundary2MKxAbZpb2lcLLop'
hashvalue = '153d470b3e4a1f473fea0e63a4d21572a4d4e52146a'
request2.add_header('Content-type','multipart/form-data; boundary=----WebKitFormBoundary2MKxAbZpb2lcLLop')
payload = boundary+'\r\n'+'Content-Disposition: form-data; name="ref"'+'\r\n\r\n'+hashvalue+'\r\n'+boundary \
			+'\r\n'+'Content-Disposition: form-data; name="reff"'+'\r\n\r\n'+reff+'\r\n'+boundary+'\r\n'+'Content-Disposition: form-data; name="submit"'+'\r\n\r\n' \
			+'download'+'\r\n'+boundary+'--'+'\r\n'
print payload
request2.add_data(payload)
req = urllib2.urlopen(request2)
#StringIO 会出错
data = BytesIO(req.read())
gziper = gzip.GzipFile(fileobj = data)
decode = gziper.read()
torrent_fs = open('xxx.torrent','wb')

#decode = decode.replace('\n\r','')
torrent_fs.write(decode)
fs.close()