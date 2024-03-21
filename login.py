# -*- coding: utf-8 -*-

import requests
import getpass
import cryptos
import time
import json
import bs4
import os

class Command_Login:
	def __init__(self)->None:
		self.name='login'
		self.long_description='Command: login\n\nDescription: Login to save credentials. A safe password input box is built-in.\nUsage: login'
	def run(self,args:list[str])->None:
		id=input('Select your operation:\n1. Login with password\n2. Login with another exist cookie\n\n> ')
		if id not in ('1','2'):
			return
		masterpass=getpass.getpass('Create a master password to save credentials. Non-null recommended: ')
		key_with_salt=cryptos.generate_key(masterpass.encode())
		salt=key_with_salt[:16]
		aes_key=key_with_salt[16:]
		if masterpass=='':
			if input('Are you sure you want to save your cookies without a password? [y/n] ') not in ('y','Y'):
				return
		id=int(id)
		if id==1:
			username=input('Input your username: ')
			password=getpass.getpass('Input your password: ')
			loginpage_response=requests.get('https://www.luogu.com.cn/auth/login',headers={
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
				'Accept-Encoding': 'gzip, deflate, br, zstd',
				'Accept-Language': 'zh-CN,zh;q=0.9',
				'Cache-Control': 'no-cache',
				'Pragma': 'no-cache',
				'Upgrade-Insecure-Requests': '1',
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
			})
			pagesource=loginpage_response.content.decode('utf-8')
			soup=bs4.BeautifulSoup(pagesource,'lxml')
			csrftoken=soup.find_all('meta',attrs={'name':'csrf-token'})[0]['content']
			print('Requesting a new client id...')
			clientid=loginpage_response.headers['Set-Cookie'][loginpage_response.headers['Set-Cookie'].find('=')+1:loginpage_response.headers['Set-Cookie'].find(';')]
			captcha_response=requests.get(f'https://www.luogu.com.cn/lg4/captcha?_t={time.time()}',headers={
				'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
				'Accept-Encoding': 'gzip, deflate, br, zstd',
				'Accept-Language': 'zh-CN,zh;q=0.9',
				'Cache-Control': 'no-cache',
				'Cookie': f'__client_id={clientid}',
				'Pragma': 'no-cache',
				'Referer': 'https://www.luogu.com.cn/auth/login',
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
			})
			with open('captcha.jpeg','wb') as f:
				f.write(captcha_response.content)
			os.startfile('captcha.jpeg')
			captcha=input('Input the captcha: ')
			data={
				'captcha': captcha,
				'password': password,
				'username': username
			}
			login_response=requests.post('https://www.luogu.com.cn/do-auth/password',headers={
				'Accept': 'application/json, text/plain, */*',
				'Accept-Encoding': 'gzip, deflate, br, zstd',
				'Accept-Language': 'zh-CN,zh;q=0.9',
				'Cache-Control': 'no-cache',
				'Cookie': f'__client_id={clientid}',
				'Origin': 'https://www.luogu.com.cn',
				'Pragma': 'no-cache',
				'Referer': 'https://www.luogu.com.cn/auth/login',
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
				'Sec-Fetch-Dest': 'empty',
				'Sec-Fetch-Mode': 'cors',
				'Sec-Fetch-Site': 'same-origin',
				'X-Csrf-Token': csrftoken,
				'X-Requested-With': 'XMLHttpRequest'
			},data=data)
			# print(login_response.status_code)
			# print(login_response.content)
			if login_response.status_code!=200:
				print(login_response.content.decode('utf-8'))
				jsonresult=json.loads(login_response.content.decode('utf-8'))
				print(f'Error code: {jsonresult['errorCode']}')
				print(f'Error type: {jsonresult['errorType']}')
				print(f'Error message: {jsonresult['errorMessage']}')
				return
			userid=login_response.headers['Set-Cookie'][login_response.headers['Set-Cookie'].find('=')+1:login_response.headers['Set-Cookie'].find(';')]
		elif id==2:
			clientid=input('Input __client_id: ')
			userid=input('Input User ID: ')
		if masterpass=='':
			with open('userinfo.dat','w') as f:
				f.write(f'{clientid} {userid}')
			print('Cookies saved.')
		else:
			with open('userinfo.dat','wb') as f:
				f.write(salt)
				f.write(cryptos.encode(f'{clientid} {userid}'.encode(),aes_key))
			print('Cookies saved.')
