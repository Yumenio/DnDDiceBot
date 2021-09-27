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
    update.message.reply_text(help_message)


def handle(update, context):
    """Handles the query"""
    msg = update.message
    chat_id = msg['chat']['id']
    command = msg['text']
    mssg_id = msg['message_id']
    verbose = False
    pipeline = Pipeline(verbose)
    if msg['reply_to_message'] or msg['edit_date']:
        return

    # debugging the time
    # print('currentTime: ', time.time())
    # print('mssgTime:', msg['date'].now().timestamp())

    if chat_id not in WHITELIST or time.time() - 120 > msg['date'].now().timestamp():
        return
        
    # pprint.pprint(msg)
    if command[:2] == '/d':
        print('query: ' + command)
        try:
            pipeline.execute(command[2:])
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
    elif command[:6] == '/aiuda':
        update.message.bot.sendMessage(chat_id, help_message, parse_mode='HTML', reply_to_message_id=mssg_id)
    
    return
    # update.message.reply_text(update.message.text)


def error(update, context):
    print('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    token = ''
    with open('./token.txt') as f:
        token = f.read()
    updater = Updater(token)

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
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()