import re
import telebot
import random
import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telebot import types
import asyncio
from datetime import datetime

bot_token = "6526333880:AAGQkRsEinZQAht1UmDSIHb-4iX5wA5DkGc"
admin_id = 6264668799

async def get_last_messages(username, limit, bin):
    session_string = "1AZWarzoBuz1FZKtjXxk7BchfGJKr5TepbQs_ArIkG6u6pW8x083CU1CQLqAhVmsKYZM8RemNykBCmW7PXg2IoECv6w8VJSx6WgXxDQgYQxLrTi6tdMVDvXxo9LyxC5mEB7mfNpva7wc2ULRM9CkxZuBQD0Y0qL5ZJr8UJru6KDaIqeEL2OYH-o19pp5RXQz9l1ca6B8TKlP07oIXz-3l0ldN1fBZWPZZD9y_CxpKpMkmv0k4fp5bwvjEIRQiCp5bWhtURdXuViME9WLjZTHv4i6mUpoCMR3ZxTcrXgUj8pjZ8oqOaRCkHOvb8fe8GpJnZ9ggCDqx7naG3vPuzPgxVOQ0u-Fc3Wo="
    api_id = 27096137
    api_hash = "ae0b5ca26f7e604066666bd1e2bff182"

    async with TelegramClient(StringSession(session_string), api_id, api_hash) as client:
        try:
            username = int(username)
        except Exception:
            pass
        if isinstance(username, int):
            entity = username
            try:
                entity = await client.get_entity(username)
                name = entity.title
            except Exception:
                name = username
        else:
            entity = await client.get_entity(username)
            name = entity.title
        
        messages = await client.get_messages(entity, limit=limit)
        
        matching_texts = []
        for message in messages:
            if not isinstance(message.text, (str, bytes)):
                continue
            card_pattern = r'(\d{15,16})[^0-9]+([0-9]{1,2})[^0-9]+([0-9]{2,4})[^0-9]+([0-9]{3,4})'
            try:
                match = re.search(card_pattern, message.text)
                if match:
                    formatted_text = f"{match.group(1)}|{match.group(2)}|{match.group(3)}|{match.group(4)}"
                    print(formatted_text)
                else:
                    formatted_text = None
            except Exception:
                formatted_text = None
            if formatted_text is not None and bin is None:
                matching_texts.append(formatted_text)
            elif formatted_text is not None and bin is not None:
                if formatted_text.startswith(bin):
                    matching_texts.append(formatted_text)
        
        random.shuffle(matching_texts)
        return "\n".join(matching_texts), name

def save_to_file(text):
    if os.path.exists('combo.txt'):
        os.remove('combo.txt')
    with open('combo.txt', 'w') as file:
        file.write(text)

bot = telebot.TeleBot(bot_token, parse_mode='html')
print("Started")
bot.send_message(admin_id, "Started")

# Message handler for /scr command
command_pattern = r'^(?:/|\.|)scr(?:\s+(.*))?$'
@bot.message_handler(regexp=command_pattern)
def send_scr_messages(message):
    chat_id = message.chat.id
    language = 'en'
    msg = "Scraping Started...⏳"
    msg1 = ["Amount", "Took", "Source"]
    msg2 = "command format. Use /scr [username] [limit]"
    if language == 'es':
        msg = "Raspado iniciado...⏳"
        msg1 = ["Cantidad", "Tomó", "Fuente"]
        msg2 = "formato de comando. Utilice /scr [nombre de usuario] [límite]"
    initial_message = bot.reply_to(message, msg)
    start_time = datetime.now()
    command_parts = message.text.split()
    if (len(command_parts) == 4 and command_parts[0].endswith('scr')) or (len(command_parts) == 3 and command_parts[0].endswith('scr')):
        username = command_parts[1]
        limit = int(command_parts[2])
        try:
            bin = command_parts[3]
        except:
            bin = None
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        messages_text = loop.run_until_complete(get_last_messages(username, limit, bin))
        
        save_to_file(messages_text[0])
        
        file_len = len(messages_text[0].split('\n'))
        end_time = datetime.now()
        time_taken_seconds = (end_time - start_time).total_seconds()
        time_taken_formatted = "{:.0f}".format(time_taken_seconds)
        captain_info = f"""
<==============>
• {msg1[2]} -» {messages_text[1]}
• {msg1[0]} -» {file_len}
• {msg1[1]} -» {time_taken_formatted}sec
<==============>"""
        with open('combo.txt', 'rb') as file:
            try:
                markup = types.InlineKeyboardMarkup()
                team_button = telebot.types.InlineKeyboardButton(text="قناة البوت 🍿", url='https://t.me/tcrep1')
                dev_button = telebot.types.InlineKeyboardButton(text="𝐂𝐎𝐅𝐅𝐄𝐄 𓃠", url='https://t.me/KOK0KK')
                speed_button = telebot.types.InlineKeyboardButton(text="ᔆ ᴾ ᴱ ᴱ ᴰ ™𝓼", url='https://t.me/l_s_I_I')
                leo_button = telebot.types.InlineKeyboardButton(text="《 𝑳𝐒 》⏤͟͞ LEO𓆪", url='https://t.me/V_1_1_1_0')
                markup.add(team_button, dev_button, speed_button, leo_button)
                bot.send_document(message.chat.id, file, caption=captain_info, parse_mode='none', reply_markup=markup)
                bot.delete_message(message_id=initial_message.message_id, chat_id=chat_id)
            except Exception as e:
                bot.edit_message_text(message_id=initial_message.message_id, chat_id=chat_id, text=f"An error has occurred, May The Channel Has No Cards To Scrap. {e}")
    else:
        bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, text=msg2)

# Message handler for /help command
@bot.message_handler(commands=['start'])
def send_help_message(message):
    help_text = """
    <b>أهلاً بك في بوت كومبو!</b>
    هذا البوت يجمع الرسائل لإنشاء كومبو من البطاقات من اسم مستخدم أو قناة محددة.
    
    <b>الأوامر:</b>
     - يجمع الرسائل من اسم المستخدم المحدد مع فلتر BIN اختياري.
    
    <b>مثال:</b>
    /scr xenscrape 100

      إذا كنت بحاجة إلى مزيد من المساعدة، يرجى الاتصال بفريق التطوير. @KOK0KK
    """
    bot.send_video(message.chat.id, video_url, caption=welcome_text, parse_mode='html')

# Welcome message for new users
@bot.message_handler(commands=['start'])
def send_welcome_message(message):
    welcome_text = """
    <b>هذا البوت هو بوت كومبو يقوم بإنشاء كومبو من بين معين أو عشوائي.</b>
    للحصول على مزيد من المعلومات حول كيفية استخدام البوت، استخدم الأمر /help.
    """
    video_url = "https://telegra.ph/file/f48b45d973150c4802594.mp4"
    bot.send_video(message.chat.id, video_url, caption=welcome_text, parse_mode='html')

bot.infinity_polling()
