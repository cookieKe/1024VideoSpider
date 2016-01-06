# -*- coding: utf-8 -*-
#!/usr/bin/env python

from flask.ext.script import Manager, Server
from app import app
from models import Url_Link

manager = Manager(app)
manager.add_command("runserver",Server(host = '127.0.0.1',port = 5000, use_debugger = True))

@manager.command
def save_url():
	url = Url_Link(name = 'hello',link='http://www.baidu.com')
	url.save()

@manager.command
def query_url():
	urls = Url_Link.objects.all()
	for item in urls:
		print item

@manager.command
def update():
	Url_Link.objects(name = 'hello').update(link = 'http://www.163.com')

@manager.command
def delete():
	Url_Link.objects(name = 'delete').delete()


if __name__ == '__main__':
	manager.run()