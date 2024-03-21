# -*- coding: utf-8 -*-

import rich.console
import constant
import getpass

# modules
import storage
import cryptos
import fileio
import login

def split(command:str)->list[str]:
	result=command.split(' ')
	result=[item for item in result if item]
	return result

class Command_Load:
	def __init__(self)->None:
		self.name='load'
		self.long_description='Builtin command: load\n\nDescription: Load cookie from userinfo.dat.\nUsage: load'
	def run(self,args:list[str])->None:
		with open('userinfo.dat','rb') as f:
			data=f.read()
		masterpass=getpass.getpass('Enter your master password to decrypt cookies: ')
		if masterpass=='':
			try:
				plaintext=data.decode()
			except UnicodeDecodeError:
				print(f'Error: Password needed.')
				return
		else:
			key_with_salt=cryptos.generate_key_with_given_salt(masterpass.encode(),data[:16])
			try:
				plaintext=cryptos.decode(data[16:],key_with_salt).decode()
			except ValueError as exc:
				print(f'Error while decoding: {exc.args[0]} Check your password and try again.')
				return
		clientid=plaintext[:plaintext.find(' ')]
		userid=plaintext[plaintext.find(' ')+1:]
		for i in clientid:
			if (ord(i)<ord('0') or ord(i)>ord('9')) and (ord(i)<ord('a') or ord(i)>ord('f')):
				print('Invalid client id found. Password needed.')
				return
		for i in userid:
			if ord(i)<ord('0') or ord(i)>ord('9'):
				print('Invalid user id found. Password needed.')
				return
		storage.storage['__client_id']=clientid
		storage.storage['__user_id']=userid
		print(f'Successfully loaded cookies of userid {userid}.')

class Command_Clear:
	def __init__(self)->None:
		self.name='clear'
		self.long_description='Builtin command: clear\n\nDescription: Clear the terminal.\nUsage: clear'
	def run(self,args:list[str])->None:
		console.clear()

class Command_Help:
	def __init__(self)->None:
		self.name='help'
		self.long_description='Builtin command: help\n\nDescription: Show helps.\nUsage: help [name]'
	def run(self,args:list[str])->None:
		if len(args)==0:
			print('Available commands:')
			for i in sorted(command_name):
				print(i)
			return
		elif args[0].lower() in command_name:
			print(command_manual[command_name.index(args[0].lower())])
		else:
			print('Unknown command: '+args[0].lower())

class Command_Exit:
	def __init__(self)->None:
		self.name='exit'
		self.long_description='Builtin command: exit\n\nDescription: Exit the terminal.\nUsage: exit'
	def run(self,args:list[str])->None:
		exit(0)

def register_command(command)->None:
	instance=command()
	command_name.append(instance.name)
	command_manual.append(instance.long_description)
	command_instance.append(instance)

def execute(command:str)->None:
	command:list[str]=split(command)
	if len(command)==0:
		return
	command[0]=command[0].lower()
	if command[0] in command_name:
		command_instance[command_name.index(command[0])].run(command[1:])
	else:
		print('Unknown command: '+command[0])

def main()->None:
	# print(f'{constant.titletext}\n\n')
	print(f'Luogu Terminal {constant.update_type} v{constant.version}\nType "help" for help.\n')
	while True:
		try:
			command=input('> ')
			execute(command)
		except KeyboardInterrupt:
			pass
		print()

if __name__=='__main__':
	console=rich.console.Console()
	command_name=[]
	command_manual=[]
	command_instance=[]
	register_command(Command_Exit)
	register_command(Command_Help)
	register_command(Command_Load)
	register_command(Command_Clear)
	register_command(login.Command_Login)
	main()