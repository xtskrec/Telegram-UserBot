# Copyright (C) 2019 The Raphielscape Company LLC.
# Copyright (C) 2020 TeamDerUntergang.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.

import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot import bot, CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern="^.q(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("`Reply to any user message.`")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.edit("`Reply to text message`")
       return
    chat = "@QuotLyBot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit("`Reply to actual users message.`")
       return
    await event.edit("`Making a Quote`")

    async with bot.conversation(chat, exclusive=False, replies_are_responses=True) as conv:
          response = None
          try:
              msg = await reply_message.forward_to(chat)
              response = await conv.get_response(message=msg, timeout=5)
          except YouBlockedUserError: 
              await event.edit("`Please unblock @QuotLyBot and try again`")
              return
          except Exception as e:
              print(e.__class__)

          if not response:
              await event.edit("`I can't get any response from bot!`")
          elif response.text.startswith("Hi!"):
             await event.edit("`Can you kindly disable your forward privacy settings for good?`")
          else: 
             await event.delete()
             await response.forward_to(event.chat_id)
          await conv.mark_read()
          await conv.cancel_all()

CMD_HELP.update({
        "quotly": 
        ".q \
          \nUsage: Enhance ur text to sticker.\n"
    })
