# -*- coding: utf-8 -*-
#!/usr/bin/env python

from app import db
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# mongodbengine 默认按照类名生成collection
class Url_Link(db.Document):
	name = db.StringField(max_length = 500)
	link = db.StringField(max_length = 200)

	def __str__(self):
		return 'name:%s----url:%s' % ((self.name).encode('utf-8'),self.link)