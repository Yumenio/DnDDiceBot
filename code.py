import telepot
import os
import pprint
from telepot.loop import MessageLoop
from pipeline import Pipeline
from grammar.executor import SemanticError
from whitelist import WHITELIST

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    mssg_id = msg['message_id']
    try:
        _ = msg['reply_to_message']
        return
    except:
        pass
    try:
        _ = msg['edit_date']
        return
    except:
        pass

    pprint.pprint(msg)
    if chat_id not in WHITELIST:
        return
    # if command == '/d':
    #     roll = randint(1,20)
    #     bot.sendMessage(chat_id, format(roll, 20), reply_to_message_id=mssg_id)
    if command[:2] == '/d':
        print('query: ' + command)
        verbose = False
        try:
            pipeline = Pipeline(command[3:], verbose)
            ans = pipeline.getString() + 'total =   ' + str(pipeline.getResult())
            print(ans)
            bot.sendMessage(chat_id, ans, parse_mode = 'HTML', reply_to_message_id=mssg_id)
        except SemanticError as e:
            bot.sendMessage(chat_id, 'Invalid query, ' + str(e), reply_to_message_id=mssg_id)
        except Exception as err:
            bot.sendMessage(chat_id, 'whoops, something went wrong', reply_to_message_id=mssg_id)
            print(err)
    else:
        bot.sendMessage(chat_id, '*bold*', parse_mode = 'Markdown')

bot = telepot.Bot(os.environ['BOT_TOKEN'])
MessageLoop(bot, handle).run_forever()