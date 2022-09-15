from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import pprint
from pipeline import Pipeline
# from grammar.parser import SyntacticError
# from grammar.executor import SemanticError
from utils import WHITELIST, help_message, SemanticError, SyntacticError
import time

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! \n \nType /aiuda if you need help.')


def aiuda(update, context):
    """Send a message when the command /aiuda is issued."""
    msg = update.message
    chat_id = msg['chat']['id']
    mssg_id = msg['message_id']
    update.message.bot.sendMessage(chat_id, help_message, parse_mode = 'HTML', reply_to_message_id=mssg_id)


def handle(update, context):
    """Handles the query"""
    msg = update.message
    chat_id = msg['chat']['id']
    command = msg['text']
    mssg_id = msg['message_id']
    verbose = False
    pipeline = Pipeline(verbose)
    # if msg['reply_to_message'] or msg['edit_date']:
    # if msg['edit_date']:
    #    return

    # debugging the time
    # print('currentTime: ', time.time())
    # print('mssgTime:', msg['date'].timestamp())

    print('actual ', time.time() - 3600 - 120)
    print('msg', msg['date'].timestamp())

    # if chat_id not in WHITELIST.values() or time.time() - 120 > msg['date'].timestamp():  #original
    if chat_id not in WHITELIST.values() or time.time() - 3600 - 120 > msg['date'].timestamp(): #for some weird reason, time in my code atm has a 3594secs(~1hr) offset, idfk why
        return

    pprint.pprint(msg)
    if command[:3] == '/dm':
        print('dm roll:' + command)
        try:
            pipeline.execute(command[3:])
            ans = pipeline.getString() + 'total =   ' + str(pipeline.getResult())
            print(ans)
            update.message.bot.sendMessage(chat_id, ans, parse_mode = 'HTML', reply_to_message_id=mssg_id)
            update.message.bot.sendMessage(WHITELIST['main'], 'DM roll: ' + str(pipeline.getResult()), parse_mode = 'HTML')
        except SyntacticError as e:
            update.message.bot.sendMessage(chat_id, 'Invalid query, ' + str(e) + '\n\nType /aiuda if you need help', reply_to_message_id=mssg_id)
        except SemanticError as e:
            update.message.bot.sendMessage(chat_id, 'Invalid query, ' + str(e), reply_to_message_id=mssg_id)
        except Exception as err:
            update.message.bot.sendMessage(chat_id, 'whoops, something went wrong, check the /aiuda command if you need help', reply_to_message_id=mssg_id)
            print(err)


    elif command[0] == '/':
        if len(command) > 1 and (command[1] =='i' or command[1] =='s' or command[1] =='m' or command[1] =='r'):
            print(command[1])
            return
        print('query: ' + command)
        try:
            pipeline.execute(command[1:])
            ans = pipeline.getString() + 'total =   ' + str(pipeline.getResult())
            print(ans)
            update.message.bot.sendMessage(chat_id, ans, parse_mode = 'HTML', reply_to_message_id=mssg_id)
        except SyntacticError as e:
            update.message.bot.sendMessage(chat_id, 'Invalid query, ' + str(e) + '\n\nType /aiuda if you need help', reply_to_message_id=mssg_id)
        except SemanticError as e:
            update.message.bot.sendMessage(chat_id, 'Invalid query, ' + str(e), reply_to_message_id=mssg_id)
        except Exception as err:
            update.message.bot.sendMessage(chat_id, 'whoops, something went wrong, check the /aiuda command if you need help', reply_to_message_id=mssg_id)
            print(err)
    # elif command[:6] == '/aiuda':
    #     help_message = "e.g.:    d d20!+5 [(<u>19</u>,18)] = 24"
    #     update.message.bot.sendMessage(chat_id, help_message, parse_mode = 'HTML', reply_to_message_id=mssg_id)
    
    return

def error(update, context):
    print('Update "%s" caused error "%s"', update, context.error)

def main():
    print('b5')
    """Start the bot."""
    # token = ''
    # with open('./token.txt') as f:
    #     token = f.read()
    # print('id', os.environ['API_ID'])
    # print('hash', os.environ['API_HASH'])
    print('token', os.environ['BOT_TOKEN'])
    token = os.environ['BOT_TOKEN']
    # bot = Bot(token= token)
    # bot.setWebhook('https://bokunodice.herokuapp.com/'+token)
    updater = Updater(token)
    # port = os.getenv('PORT', default = 8443)
    # print('binding to port:',port)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("aiuda", aiuda))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, handle))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    # updater.start_webhook(url_path='https://bokunodice.herokuapp.com/'+token , port=port)
    updater.start_polling()
    print('b6')

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
