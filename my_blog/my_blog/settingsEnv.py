# -*-coding:utf-8-*-
'''
    
'''
import os

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RobotManSys.settings')

profile = os.environ.get('my_blog_PROFILE', 'develop')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_blog.settings.%s" % profile)
