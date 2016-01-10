# coding:utf-8
from threading import Condition

'''
存储全局变量
'''

# 定时任务的条件变量和全局变量
global g_version_condition
g_version_condition = Condition()
global g_version_flag 
g_version_flag = 1

# 数据库数据缓存
g_data_from_mongo = []