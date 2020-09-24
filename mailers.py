#!/usr/bin/python
# encoding=utf-8
#auth: haochenxiao
# Filename: mailer.py

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  
import smtplib  
import datetime,time
import os
import importlib,sys 
importlib.reload(sys)

class SendEmail:
	# 构造函数：初始化基本信息
	def __init__(self, host, user, passwd, port = 465):
		lInfo = user.split("@")
		self._user = user
		self._account = lInfo[0]
		self._me = self._account + "<" + self._user + ">" 
		
		#server = smtplib.SMTP()  
		server = smtplib.SMTP_SSL(host,port)
		server.connect(host)  
		#server.login(self._account, passwd)
		server.login(self._user, passwd)
		self._server = server	  
	
	# 发送文件或html邮件	
	def sendTxtMail(self, to_list, sub, content, subtype='html'):	
		# 如果发送的是文本邮件，则_subtype设置为plain
		# 如果发送的是html邮件，则_subtype设置为html
		msg = MIMEText(content, _subtype=subtype, _charset='utf-8')  
		msg['Subject'] = sub  
		msg['From'] = self._me  
		msg['To'] = ";".join(to_list)  
		try:
			self._server.sendmail(self._me, to_list, msg.as_string())   
			return True  
		except Exception as e:    
			print (e)
			return False
		
	# 发送带附件的文件或html邮件	   
	def sendAttachMail(self, to_list, sub, content, subtype='html'):
		# 创建一个带附件的实例
		msg = MIMEMultipart()  
		# 增加附件1
		att1 = MIMEText(open(r'D:\javawork\PyTest\src\main.py','rb').read(), 'base64', 'utf-8')
		att1["Content-Type"] = 'application/octet-stream'
		# 这里的filename可以任意写，写什么名字，邮件中显示什么名字
		att1["Content-Disposition"] = 'attachment; filename="main.py"'
		msg.attach(att1)
		
		# 增加附件2
		att2 = MIMEText(open(r'D:\javawork\PyTest\src\main.py','rb').read(), 'base64', 'utf-8')
		att2["Content-Type"] = 'application/octet-stream'
		att2["Content-Disposition"] = 'attachment; filename="main.txt"'
		msg.attach(att2)
		
		# 增加邮件内容
		msg.attach(MIMEText(content, _subtype=subtype, _charset='utf-8'))
		
		msg['Subject'] = sub  
		msg['From'] = self._me
		msg['To'] = ";".join(to_list)
		 
		try:
			self._server.sendmail(self._me, to_list, msg.as_string())   
			return True  
		except Exception as e:   
			return False
	 # 发送带附件的文件或html邮件	   
	def sendImageMail(self, to_list, sub, content, subtype='html'):
		# 创建一个带附件的实例
		msg = MIMEMultipart()
		
		# 增加邮件内容
		msg.attach(MIMEText(content, _subtype=subtype, _charset='utf-8'))
		
		# 增加图片附件
		image = MIMEImage(open(r'D:\javawork\PyTest\src\test.jpg','rb').read())
		#附件列表中显示的文件名
		image.add_header('Content-Disposition', 'attachment;filename=p.jpg')	 
		msg.attach(image)  
		
		msg['Subject'] = sub  
		msg['From'] = self._me
		msg['To'] = ";".join(to_list)
		
		try:
			self._server.sendmail(self._me, to_list, msg.as_string())   
			return True  
		except Exception as e:  
			return False
		
	# 析构函数：释放资源  
	def __del__(self):
		self._server.quit()
		self._server.close()


def SendMessages(mailto_list,ERROR_LIST,job_name):

	h1='''
	<html>
	<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>NCC 运维管理系统</title>
	
	<style type="text/css">
	body {margin:40px 30% 10px 15%;}
	</style>
	</head>
	</br></br></br></br>
	<body>
	'''

	h2 = '''
	<p><font size="3" color="red"><b>%s</b></font></p>
		
	'''

	h4='''
	</br></br></br>
	<p><font size="3" color="green">汇报时间:   %s</font></p>
	<p><font size="3" color="green">  执行人:  XX</font></p>
	</body>
	</html>
	'''
	
	#业务层
	nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	html = ''
	html = html + h1

	for m in ERROR_LIST:
		html += h2%(m)
	html += h4%(nowtime)
	print (html)
	sub = 'NCC jenkins {}编译错误汇报'.format(job_name)
	mail = SendEmail('', '', '')
	if mail.sendTxtMail(mailto_list, sub, str(html)):  
		print("NCC发送成功")
	else:  
		print("NCC发送失败")
