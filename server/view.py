from app import app
from flask import render_template
import global_var
from task import SpiderTesk,RefreshCache

@app.route('/')
def main_page():
	url_list = global_var.g_data_from_mongo
	print url_list
	return render_template('index.html',url_list = url_list)

if __name__ == '__main__':
	st = SpiderTesk()
	rc = RefreshCache()
	st.start()
	print '-------------'
	rc.start()
	app.run()
