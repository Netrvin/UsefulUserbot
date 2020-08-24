#!/usr/bin/python3
# -*- coding: utf-8 -*-

from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import InputStickerSetID
import time
import urllib.request
import os
import sys
import hashlib
import threading
from configparser import ConfigParser

script_path = os.path.realpath(sys.argv[0])
(scriptdir, scriptname) = os.path.split(script_path)
os.chdir(scriptdir)
config = ConfigParser()
config.read('userbot.conf', encoding='UTF-8')

try:
    api_id = config['Settings']['APIID']
    api_hash = config['Settings']['APIHASH']
except:
    print('Wrong configuration')
    sys.exit(0)


def restart():
    time.sleep(3)
    os.execl(sys.executable, 'python', script_path)


client = TelegramClient('anon', api_id, api_hash)
print('Starting userbot...')
client.start()


@client.on(events.NewMessage(from_users='me'))
async def my_event_handler(event):
    if event.raw_text[0] != '=':
        return
    command = event.raw_text[1:].split()
    if command[0] == 'ping':
        time1 = time.time() * 1000
        msg = await event.reply('**Pong!**')
        time2 = time.time() * 1000
        await msg.edit('**Pong!\nDelay: '+str(float('%.2f' % (time2 - time1)))+"ms**")
    elif command[0] == 'deleteallfromme':
        msg_list = []
        if (len(command) == 2) and (command[1] == 'silent'):
            await event.delete()
        async for message in client.iter_messages(event.to_id, from_user='me', reverse=True):
            msg_list.append(message.id)
        await client.delete_messages(event.to_id, message_ids=msg_list, revoke=True)
        if not ((len(command) == 2) and (command[1] == 'silent')):
            await event.reply('**'+str(len(msg_list))+'** messages have been deleted!')
    elif command[0] == 'chatid':
        await event.reply('```'+str(event.to_id)+'```')
    elif command[0] == 'info':
        if event.reply_to_msg_id:
            msg = await client.get_messages(event.to_id, ids=event.reply_to_msg_id)
            info = await client.get_entity(msg.from_id)
        else:
            info = await client.get_entity(event.from_id)
        await event.reply('**ID:** ```'+str(info.id)+'``` \n**DC:** ```'+str(info.photo.dc_id)+'```')
    elif command[0] == 'stop':
        await event.reply('Stopping userbot...')
        await client.disconnect()
    elif command[0] == 'restart':
        await event.reply('Restarting userbot...')
        threading.Thread(target=restart).start()
        await client.disconnect()

client.run_until_disconnected()
print('Stopping userbot...')
