# 采用selenium的音乐下载器
# 目前仅支持QQ音乐；暂不支持网易云音乐
# 思路简单：对网址进行相应解析，即可得到歌曲链接，利用该链接进行下载即可
# 日期：2017.12.11
__author__ = 'SchrodingerY'

#!/usr/bin/env python
#coding:utf-8

import re
import requests
import time
import urllib.request
from selenium import webdriver
import os
# from contextlib import closing
# from pyvirtualdisplay import Display 
# 不显示窗口；参考网址：http://blog.csdn.net/qq_28053189/article/details/69950339?locationNum=2&fps=1
# 上述方法在Windows下无法使用

# import sys
# from PyQt4.QtGui import *
# from PyQt4.QtCore import *
# from PyQt4.QtWebKit import *

# # 加载js信息
# class Render(QWebPage):
# 	def __init__(self, url):
# 		self.app = QApplication(sys.argv)
# 		QWebPage.__init__(self)
# 		self.loadFinished.connect(self._loadFinished)
# 		self.mainFrame().load(QUrl(url))
# 		self.app.exec_()

# 	def _loadFinished(self, result):
# 		self.frame = self.mainFrame()
# 		self.app.quit()


# ====================网址打开==================
# 由于QQ音乐搜索页面采用js脚本动态加载，因此此处之间提取js脚本对应的headers信息中的实际搜索信息网址
def webopen():
	headers = {
		'Host': 'y.qq.com',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:47.0) Gecko/20100101 Firefox/47.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
		'Accept-Encoding': 'gzip, deflate, br',
		'Referer': 'http://y.qq.com/',
		'Connection': 'keep-alive',
		'Cache-Control': 'max-age=0',
	}

	url2 = '&g_tk=5381&jsonpCallback=searchCallbacksong5106&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
	url1 = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=55163902870355075&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w='
	print("=========================================================QQ音乐下载器===================================================\n")
	MusicName = input("请输入歌曲名称：")
	# MusicName = "崇拜"  # 测试用例
	urlMusicName = urllib.parse.quote(MusicName)  # 转换成url可以读取的字符串
	baseUrl = url1 + urlMusicName + url2
	
	# # 调用Render类得到全部js信息
	# r = Render(baseUrl)
	# result = r.frame.toHtml()
	
	response = requests.get(baseUrl, headers = headers)
	response.encoding = 'utf-8'
	
	return response, MusicName


# ================中文检测函数====================
# 参考网址：http://lib.csdn.net/article/python/66507?knId=160
def findChinese(source):
	# text = source.decode('utf8')   # python3 默认为unicode
	r = re.findall('[\u4e00-\u9fa5]', source)
	# 去除空格影响
	condition = lambda t: t != ' '
	results = list(filter(condition, r))
	return results


# ===============填充字符函数======================
# 参考网址：http://lib.csdn.net/article/python/66507?knId=160
# 输入变量说明：
# un_align_str: 输入字符串
# lenh: 半角字符个数；自己设置；默认为0
# lenf: 全角字符个数；自己设置；默认为0
# addh: 半角字符空格
# addf: 全角字符空格
def myAlign(un_align_str, lenh = 0, lenf = 0, addh = ' ', addf = u' '):
	assert isinstance(lenh, int)   # 断言半角长度为整形变量
	assert isinstance(lenf, int)   # 断言全角长度为整形变量
	slen = len(un_align_str)
	# print("长度：%d " %(slen))
	# 长度不足则返回字符串
	# lenf*2: 中文在默认的utf-8编码下一个中文占用3个字符，而显示占用约2个字符
	chn = findChinese(un_align_str)
	numchn = len(chn)
	numspn = slen - numchn
	str = addh * (lenh - numspn) + addf * (lenf - 2 * numchn)
	return str


# =======================显示函数==========================
# 从页面中提取"歌曲名称"，"歌手"，"发行时间"，"media_mid"
# 仅显示前三项内容供下载者进行选择
# media_mid: 用于提取实际歌曲播放网址
def display(data = None, musicName = None):
	if data == None and musicName == None:
		return
	print("\n=========================================================歌曲列表===================================================\n")

	totalInfo = str(data.text)

	midList = re.findall(r'("media_mid")(:)("\w+")', totalInfo)

	songList = re.findall(r'("time_public")(:)("\d+-\d+-\d+")(,)("title")(:)(".*?")', totalInfo)

	singerList = re.findall(r'(\[\{)("id")(:)(\d+)(,)("mid")(:)("\w+")(,)("name")(:)(".*?")', totalInfo)

	realMusicNameList = []
	realSingerList = []
	realTimeList = []
	realMidList = []

	for i in range(len(songList)):
		realMusicNameList.append(songList[i][6])
		realTimeList.append(songList[i][2])
	for i in range(len(singerList)):
		realSingerList.append(singerList[i][11])
	for i in range(len(midList)):
		realMidList.append(midList[i][2])

	totalList = list(zip(realMusicNameList, realSingerList, realTimeList, realMidList))
	totalDict = {}
	listLength = min(len(midList), len(songList), len(singerList))
	for i in range(listLength):
		num = i + 1
		totalDict[num] = totalList[i]

	# 显示标头
	MusicTitle = "歌曲名称"
	SingerTitle = "歌手"
	TimeTitle = "发行日期"
	print("序号\t  ", end = '')
	print(MusicTitle + myAlign(MusicTitle, 30, 20), end = '')
	print(SingerTitle + myAlign(SingerTitle, 20, 12), end = '')
	print(TimeTitle + myAlign(TimeTitle, 20, 10))
	for i in range(listLength):
		num = i + 1
		print("%-10d" %(num), end = '')
		print(realMusicNameList[i] + myAlign(realMusicNameList[i], 30, 20), end = '')
		print(realSingerList[i] + myAlign(realSingerList[i], 20, 12), end = '')
		print(realTimeList[i] + myAlign(realTimeList[i], 20, 10))
	chooseNum = input("\n请输入歌曲序号：")
	# chooseNum = 1   # 测试用例
	chooseList = list(totalDict.get(int(chooseNum)))
	midNum = chooseList[3]
	return midNum, chooseNum, realMusicNameList[int(chooseNum)-1].strip('""')


# ====================页面跳转函数====================
# 跳转到下载页面
def jump2playPage(mid = None):
	if mid == None:
		return
	url1 = "https://y.qq.com/n/yqq/song/"
	mid = re.search(r'\w+', mid).group()
	realUrl = url1 + mid + ".html"

	driver = webdriver.Firefox()
	driver.set_window_size(0, 0)
	# driver = webdriver.PhantomJS(executable_path = 'D:/phantomjs-2.1.1-windows/bin/phantomjs.exe')
	driver.get(realUrl)
	try:
		driver.find_element_by_class_name("js_all_play").click()  # by xpath 也可以
		time.sleep(1)
	except:
		print("\n对不起，该歌曲暂时无法下载. 请重新启动程序...\n")
		driver.quit()
	count = 0
	allhandles = driver.window_handles
	for handle in allhandles:
		count += 1
	if count == 2:
		driver.switch_to_window(driver.window_handles[1])
	else:
		time.sleep(5)
		driver.switch_to_window(driver.window_handles[1])
	downloadInfo = driver.page_source
	downloadUrl_temp = str(re.search(r'(source src)(=)(")(.*?)(")', downloadInfo).group(4))
	downloadUrl = downloadUrl_temp.replace('amp;', '')
	print("\n===================================================歌曲正在下载，请稍等片刻==============================================\n")
	driver.quit()
	return downloadUrl


# ====================歌曲下载和保存函数=========================
def downloadMusic(songUrl = None, musicName = None, chooseNum = None):
	if songUrl == None and musicName == None and chooseNum == None:
		return
	headers = {
		'Host': 'dl.stream.qqmusic.qq.com',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:57.0) Gecko/20100101 Firefox/57.0',
		'Accept': 'audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5',
		'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
		'Referer': 'http://y.qq.com/',
		'Connection': 'keep-alive',
		'Range': 'bytes=0-',
		'Cache-Control': 'max-age=0',
		# 'Cookie': 'pgv_pvi=6817996800; pgv_pvid=9270079499; pac_uid=1_2679261865; pt2gguin=o0502460524; RK=kJfTRwRDM5; ptcz=9efff9bb73e60a198dd1163f186f7cc9915eb79ef354714da50708fc58a13d60; o_cookie=502460524; tvfe_boss_uuid=6dc86c89eb9858e4; mobileUV=1_15c87c37b4c_35d06; lskey=0001000072fcda892c66a7139bd45e30fac0dae9a9bd6d1ed46743b730b5a9918e655135b108d24707c5c7a2; pgv_si=s1668688896; qqmusic_fromtag=66',
	}

	if not os.path.exists('QQ_Music_Download'):
		os.makedirs('QQ_Music_Download')

	try:
		music = requests.get(songUrl, timeout = 5, headers = headers)  #超时异常判断 5秒超时
	except requests.exceptions.ConnectionError:
		print('Sorry，当前歌曲无法下载')
	file_name = musicName + str(chooseNum) + ".m4a" #拼接歌曲名
	try:
		with open('QQ_Music_Download/%s' %file_name, "wb") as fp:
			fp.write(music.content)
			fp.close()
			print('\n%s下载完成\n' %(file_name))
	except:
		print('歌曲下载失败')


	# 显示进度条程序，由于IDE问题无法使用
	# with closing(requests.get(songUrl, stream = True)) as response:
	# 	chunk_size = 1024
	# 	content_size = int(response.headers['content-length'])
	# 	progress = ProgressBar(file_name, total = content_size, unit = "KB", chunk_size = chunk_size, run_status = "正在下载", fin_status = "下载完成")
	# 	with open('QQ_Music_Download/%s' %(file_name), "wb") as fp:
	# 		for data in response.iter_content(chunk_size = chunk_size):
	# 			fp.write(data)
	# 			progress.refresh(count = len(data))

# =======================显示下载进度条=======================
# 参考网址：http://blog.csdn.net/ribavnu/article/details/51323732
# 由于IDE问题无法使用
# class ProgressBar(object):

# 	def __init__(self, title, count = 0.0, run_status = None,
# 				fin_status = None, total = 100.0, unit = '', sep = '/', chunk_size = 1.0):
# 		super(ProgressBar, self).__init__()
# 		self.info = "【%s】 %s %.2f %s %s %.2f %s"
# 		self.title = title
# 		self.total = total
# 		self.count = count
# 		self.chunk_size = chunk_size
# 		self.status = run_status or ""
# 		self.fin_status = fin_status or " "*len(self.status)
# 		self.unit = unit
# 		self.seq = sep

# 	def __get_info(self):
# 		# 【名称】 状态 进度 单位 分割线 总数 单位
# 		_info = self.info % (self.title, self.status, self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
# 		return _info

# 	def refresh(self, count = 1, status = None):
# 		self.count += count
# 		# if status is not None
# 		self.status = status or self.status
# 		end_str = "\r"
# 		if self.count >= self.total:
# 			end_str = '\n'
# 			self.status = status or self.fin_status
# 		print(self.__get_info(), end = end_str)

if __name__ == '__main__':
	while True:
		(res, name) = webopen()
		(midNum, chooseNum, realName) = display(res, name)
		downloadUrl = jump2playPage(midNum)
		downloadMusic(downloadUrl, realName, chooseNum)
