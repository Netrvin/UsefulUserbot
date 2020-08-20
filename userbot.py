#!/usr/bin/python3
# -*- coding: utf-8 -*-

from telethon import TelegramClient, events

# Use your own values from my.telegram.org
api_id = YOUR_ID
api_hash = 'YOUR_HASH'

client = TelegramClient('anon', api_id, api_hash)
client.start()

@client.on(events.NewMessage(from_users='me'))
async def my_event_handler(event):
    if '/ping' == event.raw_text:
        await event.reply('**Pong!**')
    elif '/deleteallfromme' == event.raw_text:
        msg_list = []
        async for message in client.iter_messages(event.to_id, from_user='me', reverse=True):
            msg_list.append(message.id)
        await client.delete_messages(event.to_id, message_ids=msg_list, revoke=True)
        await event.reply('**'+str(len(msg_list))+'** messages have been deleted!')

client.run_until_disconnected()
