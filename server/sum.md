#mongodb 在 flask 中的使用
##插件的安装
使用falsk的mongoengine插件
｀pip install mongoengine-flask｀
##简单使用
 1. 创建mongoengine
 ｀｀
 2. 创建model类，继承类｀db.Document｀
 ｀｀
 3. 基本的增删改查
 ｀
 class Url_Link(db.Document):
	name = db.StringField(max_length = 500)
	link = db.StringField(max_length = 200)
  增：
  url_link = Url_link('sss','dcsdc')
  url_link.save()
  删：
  Url_Link.objects(name = 'sss').delete()
  改：
  Url_Link.objects(name = 'sss').update(link = 'sxsx')
  查：
  url_link = Url_Link.objects.all() #
  url_link = Url_Link.objects.all(name = 'sss') #
  ｀

##错误
 － pymongo.errors.ServerSelectionTimeoutError: localhost:27017: [Errno 61] Connection refused
 在执行插入操作时，出现上述错误，是因为mongo的进程没有起来

 － Unable to create/open lock file: /data/db/mongod.lock errno:13 Permission denied Is a mongod instance already running?, terminating
 权限的问题，执行｀sudo chown $USER /data/db｀后解决

循环依赖
