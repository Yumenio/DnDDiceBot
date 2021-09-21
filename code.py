import telepot
import os
import pprint
from telepot.loop import MessageLoop

# TOKEN = os.environ['BOT_TOKEN']
# bot = telepot.Bot(TOKEN)
# pprint.pprint(bot.getMe())

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    print(command)

    if command == '/image':
        bot.sendMessage(chat_id, 'sarabada, one for all...')

bot = telepot.Bot(os.environ['BOT_TOKEN'])
MessageLoop(bot, handle).run_forever()