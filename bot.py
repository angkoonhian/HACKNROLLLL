from telegram.ext import CommandHandler, Updater, CallbackQueryHandler, StringCommandHandler, PrefixHandler
from telegram import ChatAction, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
import json
import os
import requests
import logging

# Initialise logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Load bot token
with open('token.ini', 'r') as file:
    BOT_TOKEN = file.read()

# Create the bot
updater = Updater(token=BOT_TOKEN, use_context=True)

# Add /start handler
Users = {}

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Hello {update.effective_message.chat.first_name}! To start, enter either /Give or /Take with the name space amount'
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Enter /balance for overall summary'
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Type /help to see all functions available."
    )
    if update.effective_message.chat.first_name not in Users:
        Users[update.effective_message.chat.first_name] = {}
    

    
def helpme(update, context):
  context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Press /Give and type in who did you give $ to and how much. \nPress /Take and type in who u Took $ from and how much.'
    )

def clear(update, context):
    Users[update.effective_message.chat.first_name] = {} # KIV
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'DAS RIGHT NO DEBT!!!'
    )

def digit(string1):
    if string1.replace(" ","").isdigit():
        return False
    if string1.replace(" ","").isalpha():
        return False

    for i in range(len(string1)):
        if string1[i] == ' ':
            return int(string1[i+1:])

def char(string1):
    for i in range(len(string1)):
        if string1[i] == ' ':
            return string1[:i]

with open('Sticker.tgs', 'rb') as file:
     f = file.read()
with open('TRAPCARD.webp', 'rb') as file:
    g = file.read()

def lend(update, context):
    data = update.message.text.partition(' ')[2]
    if len(data) == 0:
        context.bot.send_message(
  	    chat_id=update.effective_chat.id,
    	    text=f'Enter Name (space) Amount'
        )
        with open('TRAPCARD.webp', 'rb') as f: # Name sticker file as Sticker.tgs
            context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=f, timeout=50).sticker
        context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'CB DOG U BLIND OR SMTH AH CB CANNOT READ INSTRUCTIONS AH NBCB'
            )
    else:
        amount = digit(data)
        friend = char(data)
        if amount == False:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'Enter Name (space) Amount'
            )
            with open('TRAPCARD.webp', 'rb') as f: # Name sticker file as Sticker.tgs
                context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=f, timeout=50).sticker
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'CB DOG U BLIND OR SMTH AH CB CANNOT READ INSTRUCTIONS AH NBCB'
            )
        elif friend not in Users[update.effective_message.chat.first_name]:
            Users[update.effective_message.chat.first_name][friend] = amount
        else:
            Users[update.effective_message.chat.first_name][friend] += amount
        context.bot.send_message(
        chat_id=update.effective_chat.id,
            text=f'{friend} owe you ${Users[update.effective_message.chat.first_name][friend]}'
        )

def borrow(update, context):
    data = update.message.text.partition(' ')[2]
    if len(data) == 0:
        context.bot.send_message(
  	    chat_id=update.effective_chat.id,
    	    text=f'Enter Name (space) Amount'
        )
        with open('TRAPCARD.webp', 'rb') as f: # Name sticker file as Sticker.tgs
            context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=f, timeout=50).sticker
        context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'CB DOG U BLIND OR SMTH AH CB CANNOT READ INSTRUCTIONS AH NBCB'
            )
    else:
        amount = digit(data)
        friend = char(data)
        if amount == False:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'Enter Name (space) Amount'
            )
            with open('TRAPCARD.webp', 'rb') as f: # Name sticker file as Sticker.tgs
                context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=f, timeout=50).sticker
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'CB DOG U BLIND OR SMTH AH CB CANNOT READ INSTRUCTIONS AH NBCB'
            )
        elif friend not in Users[update.effective_message.chat.first_name]:
            Users[update.effective_message.chat.first_name][friend] = amount
        else:
            Users[update.effective_message.chat.first_name][friend] -= amount
        context.bot.send_message(
        chat_id=update.effective_chat.id,
            text=f'You owe {friend} ${Users[update.effective_message.chat.first_name][friend]}'
    )

def balance(update, context):
  context.bot.send_message(
  	chat_id=update.effective_chat.id,
    text=f'Please give me a moment..... xD ><!!'
  )
  
  context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

  if len(Users[update.effective_message.chat.first_name]) == 0:
      context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'ALLS GOOD'
      )
      with open('Sticker.tgs', 'rb') as f: # Name sticker file as Sticker.tgs
        context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=f, timeout=50).sticker
  
  for friend in Users[update.effective_message.chat.first_name]:
    if Users[update.effective_message.chat.first_name][friend] > 0:
      context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'{friend} owes you ${Users[update.effective_message.chat.first_name][friend]}'
      )
    elif Users[update.effective_message.chat.first_name][friend] < 0:
      context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'You owe {friend} ${-1 * Users[update.effective_message.chat.first_name][friend]}'
      )
    else:
      context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'{friend} and your debt has been cleared!'
      )

  for friend in Users[update.effective_message.chat.first_name]:
      if Users[update.effective_message.chat.first_name][friend] == 0:
         del Users[update.effective_message.chat.first_name][friend]

updater.dispatcher.add_handler(
    CommandHandler('start', start)
)

updater.dispatcher.add_handler( # Change botFather exit to clear
    CommandHandler('clear', clear)
)

updater.dispatcher.add_handler(
    CommandHandler('Give', lend)
)
  
updater.dispatcher.add_handler(
    CommandHandler('Take', borrow)
)

updater.dispatcher.add_handler(
    CommandHandler('help', helpme)
)

updater.dispatcher.add_handler(
    CommandHandler('balance', balance)
)



# Start the bot
updater.start_polling()
print('Bot started!')

# Wait for the bot to stop
updater.idle()

print('Bot stopped!')
