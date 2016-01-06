# -*- coding: utf-8 -*-
#!/usr/bin/env python

from app import app
from models import Url_Link
from flask import render_template

def get_url():
	urls = Url_Link.objects.all()
	return urls

@app.route('/')
def main_page():
	url_list = get_url()
	return render_template('index.html',url_list = url_list)

if __name__ == '__main__':
	app.run()
