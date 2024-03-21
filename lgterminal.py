import rich.console
import constant
import time

def split(command:str)->list[str]:
	result=command.split(' ')
	result=[item for item in result if item]
	return result

class Command_Clear:
	def __init__(self)->None:
		self.name='clear'
		self.long_description='Builtin command: clear\n\nClear the terminal.\n\nUsage: clear'
	def run(self,args:list[str])->None:
		console.clear()

class Command_Help:
	def __init__(self)->None:
		self.name='help'
		self.long_description='Builtin command: help\n\nShow helps.\n\nUsage: help [name]'
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
		self.long_description='Builtin command: exit\n\nExit the terminal.\n\nUsage: exit'
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
	register_command(Command_Clear)
	main()