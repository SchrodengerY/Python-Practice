# 采用bs4的爬虫
# version 1.0
# 仅针对当前百度贴吧有效
# 日期：2017.07.27
__author__ = 'SchrodengerY'

# -*- coding: utf-8 -*-

from urllib.request import urlopen  
from bs4 import BeautifulSoup  
import urllib.request
import urllib.error 
import re
import requests



class BDTB:
	# 初始化
	def __init__(self, baseUrl, schoolName, schoolnameChinese):
		# 转码为url可以读取的字符串
		self.schoolName = urllib.parse.quote(schoolName)
		self.baseUrl = baseUrl
		self.schoolnameChinese = schoolName
		
	def getPage(self, pageNum):
		try:
			# 得到真正的url
			url = self.baseUrl + self.schoolName + '&ie=utf-8&pn=' + str(pageNum*50)
			# 打开该网址
			html = urlopen(url)
			bsObj = bsObj = BeautifulSoup(html,"lxml")    #将html对象转化为BeautifulSoup对象  
			# 从BS对象中，查找全部符合判断条件的内容
			liList = bsObj.find_all("a",class_="j_th_tit ")
			for item in liList:
				# 获取链接网址
				href = item.get('href')
				hrefUrl = 'tieba.baidu.com' + href
				# 获取标题信息
				name = item.get('title')
				# 判断该标题是否满足我们的判决条件
				match = re.search("你",name) or re.search("我",name) or re.search("他",name) or re.search("她", name) or re.search("它", name) or re.search("我们", name)     # 可修改和补充关键字
				print(match)
				# 如果满足，则保存到txt中
				if match:
					targets = [hrefUrl, name]
					# txt的命名，我采用的是“学校名+.txt”的形式，但是很糟糕的是，“学校名”只能以16进制字符串的形式输入，试了各种编码解码，均无能为力，期待大神解答
					with open(self.schoolName+'.txt', 'a+') as f:
						# 保存格式为“学校:...\n 标题：...\n （链接）网址：...\n”
						f.write("学校："+str(self.schoolnameChinese)+"\n"+"标题："+str(targets[1])+"\t"+"网址："+str(targets[0])+"\n")

			# print(liList)
			return liList
		except urllib.error.URLError as e:
			if(e, 'reason'):
				print(u'连接百度贴吧失败，错误原因',e.reason)
				return None


exit = 'y'
while exit == 'y' or exit == 'Y':
	print("请输入学校名称：")
	baseURL = 'https://tieba.baidu.com/f?kw='
	schoolNAME = input()
	bdtb = BDTB(baseURL,schoolNAME,schoolNAME)
	# 搜索前50页
	for page in list(range(50)):
		bdtb.getPage(page)
	# bdtb.getPage(1)
	
	
	# 判断是否结束
	print("\nDo you want to continue?(y/n):")
	exit = input()
