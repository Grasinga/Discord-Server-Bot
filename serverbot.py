#!/usr/bin/env python3

import os.path
import discord
from time import sleep

client = discord.Client()

line = ''
users = []
ids = []

@client.event
async def on_ready():
	print('Successfully logged in as:', str(client.user)[:-5])
	while True:
		await check_log_status()
	
async def check_log_status():
	log = open('/var/log/auth.log')
	lines = log.readlines()
	log.close()
	global line
	global ids
	global users
	if lines[-1] != line:
		line = lines[-1]
		if 'New session' in line:
			ids.append(line[56:61])
			users.append(line[70:-2])
			logon = ("User '" + users[-1] + "' logged in on " + line[:6] + " at " + line[7:15] + ".")
			await message_channel('server-activity', logon)
		if 'Removed session' in line:
			if line[-7:-2] in ids:
				user = ids.index(line[-7:-2])
				del ids[user]				
				logoff = ("User '" + users[user] + "' logged off on " + line[:6] + " at " + line[7:15] + ".")
				del users[user]
				await message_channel('server-activity', logoff)

async def message_channel(name, message):
	for channel in client.get_all_channels():
		if channel.name == name:
			await client.send_message(channel, message)

def get_token():
	if os.path.isfile('bot.properties'):
		f = open('bot.properties','r')
		token = f.readline()
		if token == '':
			return input('Could not find the bot token! Enter a bot token: ')
		return token
	else:
		return(input('Could not find the bot token! Enter a bot token: '))
		
client.run(get_token())