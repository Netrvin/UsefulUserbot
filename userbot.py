#!/usr/bin/python3
# -*- coding: utf-8 -*-

from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import InputStickerSetID

# Use your own values from my.telegram.org
api_id = YOUR_ID
api_hash = 'YOUR_HASH'

client = TelegramClient('anon', api_id, api_hash)
print('Starting userbot...')
client.start()

@client.on(events.NewMessage(from_users='me'))
async def my_event_handler(event):
    if event.raw_text[0] != '/':
        return
    command = event.raw_text[1:].split()
    if command[0] == 'ping':
        await event.reply('**Pong!**')
    elif command[0] == 'deleteallfromme':
        msg_list = []
        if (len(command) == 2) and (command[1] == 'silent'):
            await event.delete()
        async for message in client.iter_messages(event.to_id,from_user='me',reverse=True):
            msg_list.append(message.id)
        await client.delete_messages(event.to_id,message_ids=msg_list,revoke=True)
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
    elif command[0] == 'mo':
        stickers = await client(GetStickerSetRequest(
            stickerset=InputStickerSetID(
                id=1360886329340068023, access_hash=9182915015938691431
            )
        ))
        times = 1
        if (len(command) == 2) and (command[1].isdigit()):
            times = int(command[1])
        for i in range(times):
            if event.reply_to_msg_id:
                await client.send_file(event.to_id, stickers.documents[12], reply_to=event.reply_to_msg_id)
            else:
                await client.send_file(event.to_id, stickers.documents[12])

client.run_until_disconnected()
print('Stopping userbot...')
