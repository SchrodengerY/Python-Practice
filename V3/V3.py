# 采用bs4的爬虫
# version 3.0
# 优化：1.页面布局； 2.程序运行。
# 仅针对当前百度贴吧有效
# 日期：2017.09.09
__author__ = 'SchrodengerY'

# -*- coding: utf-8 -*-

from urllib.request import urlopen  
from bs4 import BeautifulSoup  
import urllib.request
import urllib.error 
import re
import requests
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox as mBox
import os

# 定义退出函数
def _quit():
	win.quit()
	win.destroy()
	exit()

# 定义About弹出messageBox	
def _msgBox():
	mBox.showinfo('版权归属:SchrodingerY', '这是彩蛋：欢迎来到王者荣耀')
	
def _msgBox2():
	mBox.showinfo('欢迎来到我的酒馆', '功能尚在开发中')
	
def _msgBox3():
	mBox.showinfo('炉石传说旅程', '功能尚在开发中')

class BDTB:
	# 初始化
	def __init__(self, baseUrl, schoolName, schoolnameChinese, keyWords):
		# 转码为url可以读取的字符串
		self.schoolName = urllib.parse.quote(schoolName)
		self.baseUrl = baseUrl
		self.schoolnameChinese = schoolName
		self.keyWords = keyWords.split()
		# print("*" + self.keyWords[0] + "**" + self.keyWords[1])
		# self.trueKey = []
		
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
				match = None
				# 判断该标题是否满足我们的判决条件
				for word in self.keyWords:
					if word != ' ':
						# self.tureKey.append(word)
					 match = match or re.search(word, name)
				# match = re.search(self.keyWords[0], name) or re.search(self.keyWords[2], name)
				# match = re.search("你",name) or re.search("我",name) or re.search("他",name) or re.search("她", name) or re.search("它", name) or re.search("我们", name)     # 可修改和补充关键字
				# print(match)
				# 如果满足，则保存到txt中
				# targets = []
				if match:
					# global targets
					targets = [hrefUrl, name]
					# T.insert(END, "学校：" + self.schoolName)
					T.insert(END, "标题：" + str(targets[1]) + "\n")
					T.insert(END, "网址：" + str(targets[0]) + "\n\n")
					# txt的命名，我采用的是“学校名+.txt”的形式，但是很糟糕的是，“学校名”只能以16进制字符串的形式输入，试了各种编码解码，均无能为力，期待大神解答
					with open(self.schoolName+'.txt', 'a+') as f:
						# 保存格式为“学校:...\n 标题：...\n （链接）网址：...\n”
						f.write("学校："+str(self.schoolnameChinese)+"\n"+"标题："+str(targets[1])+"\t"+"网址："+str(targets[0])+"\n")

			# print(liList)
			# return targets
		except urllib.error.URLError as e:
			if(e, 'reason'):
				print(u'连接百度贴吧失败，错误原因',e.reason)
				return None
	
				
win = tk.Tk()
win.title('帖子搜索器beta1.0')
# win.geometry('350x150')
# 修改默认图标
win.iconbitmap('C:\\Users\\Administrator.CXREVL7GFCBU590\\Documents\\C语言\\爬虫博客\\PYTHON\\V3版本\\smart.ico')

# 设置命令行
menuBar = Menu(win)
win.config(menu = menuBar)
fileMenu = Menu(menuBar, tearoff = 0)
fileMenu.add_command(label = '新建', command = _msgBox2)
fileMenu.add_separator()
fileMenu.add_command(label = '打开', command = _msgBox3)
fileMenu.add_separator()
fileMenu.add_command(label = '退出', command = _quit)
menuBar.add_cascade(label = '文件', menu = fileMenu)

helpMenu = Menu(menuBar, tearoff = 0)
helpMenu = Menu(menuBar, tearoff = 0)
helpMenu.add_command(label = "About", command = _msgBox)
menuBar.add_cascade(label = "Help", menu = helpMenu)

# 设置小Label
monty = ttk.LabelFrame(win, text = ' 当你畏惧一样东西的时候，你不会去触碰他 ')
monty.grid(column = 3, row = 0, columnspan = 2, padx = 20, pady = 10)

# 设置名称输入
ttk.Label(monty, text = "请输入贴吧名称:").grid(column = 0, row = 0, columnspan = 2, sticky = 'W')
name = tk.StringVar()
nameEntered = ttk.Entry(monty, width = 20, textvariable = name)
nameEntered.focus()
nameEntered.grid(column = 2, row = 0, columnspan = 4, sticky = tk.W)

# 设置关键字输入
ttk.Label(monty, text = "请输入关键字(以空格分离):").grid(column = 0, row = 1, columnspan = 2, sticky = 'W')
keyword = tk.StringVar()
keywordEntered = ttk.Entry(monty, width = 20, textvariable = keyword)
keywordEntered.grid(column = 2, row = 1, columnspan = 4, sticky = tk.W)

# 设置结果显示框
ttk.Label(monty, text = "查询结果显示:").grid(column = 0, row = 2, columnspan = 2, sticky = tk.W)

S = tk.Scrollbar(monty)
T = tk.Text(monty, height = 10, width = 40)
T.grid(column = 1, row = 3, columnspan = 4, padx = 10, pady = 10, sticky = tk.N)
S.config(command = T.yview)
T.config(yscrollcommand = S.set)
# T.insert(END, quote)

# 定义Button操作

def clickMe():
	T.delete(1.0, tk.END)
	baseURL = 'https://tieba.baidu.com/f?kw='
	schoolNAME = name.get()
	keyWords = keyword.get()
	# print("schoolName:" + schoolNAME + " Keywords:" + keyWords)
	bdtb = BDTB(baseURL,schoolNAME,schoolNAME,keyWords)
	T.insert(END, "[" + schoolNAME + "]" + "\n")
	# 搜索前50页
	for page in list(range(50)):
		bdtb.getPage(page)
		print(page)
		# T.insert(END, schoolNAME)
		# T.insert(END, "标题：" + str(li[1]))
		# T.insert(END, "网址：" + str(li[0]))
		if page != 49:
			ttk.Label(monty, text = "拼命搜索中，请稍等...").grid(column = 2, row = 2)
		else:
			ttk.Label(monty, text = "搜索完成，请查阅。").grid(column = 2, row = 2)

action = ttk.Button(monty, text = "搜索", command = clickMe)
action.grid(column = 1, row = 4, pady = 5)

exit = ttk.Button(monty, text = "退出", command = _quit)
exit.grid(column = 2, row = 4, pady = 5)

win.mainloop

input()

os.system("pause")
