import telebot # <- Импорт скачанного модуля
import keyboards 
BOT_TOKEN = '8068581430:AAEiJHvGmTkaDR3IBOvp7N1vABOVkMgoD74' # <- Здесь указываем свой телеграм токен из BotFather
bot = telebot.TeleBot(BOT_TOKEN) # <- Создаем обьект телеграм бота

@bot.message_handler(func=lambda message: True) # <- Регистрируем обработчик события "на сообщение"
def echo_all(message): # <- Тогда будет выполнена функция "echo_all"
    msg_text = message.text
    if msg_text == 'image':
        bot.send_message(message.chat.id, text='Напиши описание фото', reply_markup=keyboards.kb1)
    elif msg_text == 'text':
        bot.send_message(message.chat.id, text='Напиши то, о чём ты хочешь меня спросить', reply_markup=keyboards.kb1)
    else:
        bot.send_message(message.chat.id, text='Я не понял твоей команды', reply_markup=keyboards.kb2)



    #                   ^^^
    # Которая просто отошлет наш же текст "message.text",
    # нам же (наш ID) "message.chat.id"
 
bot.polling() # <- Старт 
