# ©️biisal jai shree krishna 😎
from pyrogram import Client, filters , enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import random
import time
from info import *
from .db import *
import asyncio
user_cooldowns = {}


@Client.on_message(filters.command("start") & filters.incoming)
async def startcmd(client, message):
    userMention = message.from_user.mention()
    if not userList.find_one({'userId': message.from_user.id}):
        addUser(message.from_user.id , message.from_user.first_name)
        await client.send_message(
            LOG_CHANNEL,
            text=f"#New_user_started\n\nUser: {message.from_user.mention()}\nid :{message.from_user.id}",
        )
    await message.reply_photo(
        photo="https://telegra.ph/file/595e38a4d76848c01b110.jpg",
        caption=f"<b>Jai Shree Krishna {userMention},\n\nIᴍ Hᴇʀᴇ Tᴏ Rᴇᴅᴜᴄᴇ Yᴏᴜʀ Pʀᴏʙʟᴇᴍs..\nYᴏᴜ Cᴀɴ Usᴇ Mᴇ As ʏᴏᴜʀ Pʀɪᴠᴀᴛᴇ Assɪsᴛᴀɴᴛ..\nAsᴋ Mᴇ Aɴʏᴛʜɪɴɢ...Dɪʀᴇᴄᴛʟʏ..\n\nMʏ Cʀᴇᴀᴛᴏʀ : <a href=https://t.me/biisal>Bɪɪsᴀʟ</a>\nMʏ Lᴏᴠᴇʀ : <a href=tg://settings/>Tʜɪs Pᴇʀsᴏɴ</a></b>",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ᴍᴏᴠɪᴇ ʀᴇǫᴜᴇsᴛ ɢʀᴏᴜᴘ 🚩", url=f"https://t.me/+PA8OPL2Zglk3MDM1"
                    )
                ]
            ]
        ),
    )
    return


async def ai_res(message ,query):
    try:
        print(query)
        userMention = message.from_user.mention()
        url = f'https://bisal-nothing-org.koyeb.app/biisal?query={query}&bot_name={BOT_NAME}&bot_admin={ADMIN_NAME}' #dont try to change anything here ⚠️
        res = requests.get(url)
        if res.status_code == 200:
            print(res)
            response_json = res.json()  
            api_response = response_json.get('response')  
            if len(query) <= 280:
                await message.reply_text(text=f"<b>ᴊᴀɪ sʜʀᴇᴇ ᴋʀɪsʜɴᴀ {userMention}\nʏᴏᴜʀ ǫᴜᴇʀʏ : <code>{query}</code>\n\n{BOT_NAME} :\n{api_response}</b>",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "sᴛᴀʀᴛ ᴍᴇ 🚩", url=f"https://t.me/bisal_gpt_bot?start=z"
                                    )
                                ]
                            ]
                        ),
                        disable_web_page_preview=True,
                    )
            else:
                cut_query_str = query[:77]
                await message.reply_text(text=f"<b>ᴊᴀɪ sʜʀᴇᴇ ᴋʀɪsʜɴᴀ {userMention}\nʏᴏᴜʀ ǫᴜᴇʀʏ : <code>{cut_query_str}</code>\n\n{BOT_NAME} :\n{api_response}</b>",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "sᴛᴀʀᴛ ᴍᴇ 🚩", url=f"https://t.me/bisal_gpt_bot?start=z"
                                )
                            ]
                        ]
                    ),
                    disable_web_page_preview=True,
                )
                await client.send_message(
                LOG_CHANNEL,
                text=f"user: {userMention}\n\nAsked to Ai : {query}\n\nAi Res: {api_response}",
            )
            
    except Exception as e:
        print(f'i got this err : {e}')
        await message.reply_text(f'sry i got this err : {e}')
    return


@Client.on_message(filters.command("bol") & filters.chat(CHAT_GROUP))
async def grp_res(client , message):
    grp_query = (
        message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else None
            )
    print(grp_query)
    if not grp_query:
        return await message.reply_text("<b>Abe gadhe /bol k baad kuch likh to le !!.\n\nExample Use:\n<code>/bol Who is lord krshna??</code>\n\nHope you got it.Try it now..</b>")
    current_time = time.time()
    coolDownUser = message.from_user.id
    if (
        coolDownUser in user_cooldowns
        and current_time - user_cooldowns[coolDownUser] < COOL_TIMER
    ):
        remaining_time = int(COOL_TIMER - (current_time - user_cooldowns[coolDownUser]))
        remTimeMsg = await message.reply_text(
            f"<b>Nope..!! Spaming not allowed bro...\nPlease wait {remaining_time} seconds before sending new message...</b>"
        )
        await asyncio.sleep(remaining_time)
        await remTimeMsg.delete()
        return
    thinkStc = await message.reply_sticker(sticker=random.choice(STICKERS_IDS))
    await ai_res(message , grp_query)
    user_cooldowns[coolDownUser] = current_time
    await thinkStc.delete()
    return


@Client.on_message(
    filters.command("broadcast") & (filters.private) &  filters.user(ADMIN)
)
async def broadcasting_func(client, message):
    if message.from_user.id != ADMIN:
        return
    count = 0
    failed = 0
    bAdminText = (
        message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else None
    )
    if not bAdminText:
        return await message.reply_text("caption to likh gadhe !!")
    # bmsg = await message.reply_text(
    #     text=f"Do u want to Broadcast :\n\n{bAdminText}",
    #     reply_markup=InlineKeyboardMarkup(
    #         [
    #             [
    #                 InlineKeyboardButton("Yes", callback_data="brdcstYes"),
    #                 InlineKeyboardButton("No", callback_data="brdcstNo"),
    #             ]
    #         ]
    #     ),
    # )
    bmsg = await message.reply_text(text=f"Broadcast Started for :\n\n{bAdminText}")
    if message.reply_to_message and message.reply_to_message.audio:
        audio_message = message.reply_to_message.audio
        audio_file_id = audio_message.file_id
        bmsg = await bmsg.edit(
            f"Broadcast started for...\n\nMsg Text : {bAdminText}",
        )
        for userDoc in userList.find():
            try:
                userId = userDoc["userId"]
                await client.send_audio(
                    userId,
                    audio_file_id,
                    caption=f"<b>{bAdminText}</b>",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "ᴀᴅᴍɪɴ sᴜᴘᴘᴏʀᴛ 🚩",
                                    url=f"https://bit.ly/bisal",
                                )
                            ]
                        ]
                    ),
                )
                count += 1  # counting successful broadcasts
                if count % 20 == 0:
                    await bmsg.edit(
                        f"broadcasted to {count} users...done..!!\nFailed : {failed}"
                    )
            except Exception as loopErr:
                failed += 1
                print(f"got this err in for loop for broadcasting aud : {loopErr}")
    else:
        try:
            for userDoc in userList.find():
                try:
                    userId = userDoc["userId"]
                    await client.send_message(
                        userId,
                        text=f"<b>{bAdminText}</b>",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "ᴀᴅᴍɪɴ sᴜᴘᴘᴏʀᴛ 🚩",
                                        url=f"https://bit.ly/bisal",
                                    )
                                ]
                            ]
                        ),
                    ),
                    count += 1  # counting succesfull broadcasts
                    if count % 20 == 0:
                        await bmsg.edit(
                            f"broadcasted to {count} users...done..!!\nFailed : {failed}"
                        )
                except Exception as loopErr:
                    failed += 1
                    print(f"got this err in for loop for broadcasting : {loopErr}")
        except Exception as loopErr:
            failed += 1
            print(f"got this err in for loop for broadcasting : {loopErr}")
    await bmsg.edit(
        f"succesfully broadcasted to {count} users...\n\n Failed : {failed}"
    )
    return




@Client.on_message(filters.text & filters.private)
async def AiMsgHanDl(client, message):
    if not userList.find_one({'userId': message.from_user.id}):
        addUser(message.from_user.id , message.from_user.first_name)
        await client.send_message(
            LOG_CHANNEL,
            text=f"#New_user_started\n\nUser: {message.from_user.mention()}\nid :{message.from_user.id}",
        )
    if message.text.startswith("/"):
        return
    current_time = time.time()
    coolDownUser = message.from_user.id
    if (
        coolDownUser in user_cooldowns
        and current_time - user_cooldowns[coolDownUser] < COOL_TIMER
    ):
        remaining_time = int(COOL_TIMER - (current_time - user_cooldowns[coolDownUser]))
        remTimeMsg = await message.reply_text(
            f"<b>Nope..!! Spaming not allowed bro...\nPlease wait {remaining_time} seconds before sending new message...</b>"
        )
        await asyncio.sleep(remaining_time)
        await remTimeMsg.delete()
        return
    thinkStc = await message.reply_sticker(sticker=random.choice(STICKERS_IDS))
    private_query = message.text
    await ai_res(message , private_query)
    user_cooldowns[coolDownUser] = current_time
    await thinkStc.delete()
    return
