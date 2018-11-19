from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests, urllib, json


#Вытягиваем креды апихам
with open('env.json') as f:
    data = json.load(f)


updater = Updater(token=data['token']) # Токен API к Telegram
dispatcher = updater.dispatcher


# Обработка команд
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hi! I am bot with small functional,\n"
                                                          "I can post some random gif by tag \n"
                                                          "You can do it with following command:\n"
                                                          "/gif <tag> - for example '/gif cats'\n"
                                                          "Also, in the future, there will be able more commandsr\n "
                                                          "Good luck!")

def textMessage(bot, update):
    if update.message.text == 'Hi':
        response = 'Получил Ваше сообщение: ' + update.message.text
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        response = 'Are you serious? Your words are there ' + update.message.text
        bot.send_message(chat_id=update.message.chat_id, text=response)

def post_gif(bot,update, args):
    message = ' '.join(args)
    if message:
        quote_page = requests.get('http://api.giphy.com/v1/gifs/random?&api_key='+data['gif_api_key']+'&tag='+str(message))
        bot.send_message(chat_id=update.message.chat_id, text=quote_page.json()['data']['url'])
    else:
        bot.send_message(chat_id=update.message.chat_id, text="You didn't specify any tag, \n"
                                                              "you should use example: `/gif <tag>`")

# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
post_gif_by_tag = CommandHandler('gif', post_gif, pass_args=True)
text_message_handler = MessageHandler(Filters.text, textMessage)


# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
dispatcher.add_handler(post_gif_by_tag)

# Начинаем поиск обновлений
updater.start_polling(clean=True)


