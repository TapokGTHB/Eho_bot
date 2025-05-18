import telebot # <- Импорт скачанного модуля
import keyboards 
import fsm 
BOT_TOKEN = '8068581430:AAGqJAspHbkciXZfToem8BFQA3bxPMuidBc' # <- Здесь указываем свой телеграм токен из BotFather
stater = fsm.FSM()
bot = telebot.TeleBot(BOT_TOKEN) # <- Создаем обьект телеграм бота

def handle_default_state(message):
    if message.text == 'image':
            stater.set_state(message.chat.id, fsm.image_state)
            bot.send_message(message.chat.id, text='Напиши описание фото', reply_markup=keyboards.kb1)
    elif message.text == 'text':
            stater.set_state(message.chat.id, fsm.text_state)
            bot.send_message(message.chat.id, text='Напиши то, о чём ты хочешь меня спросить', reply_markup=keyboards.kb1)
    else:
            return_to_menu(message.chat.id)

def handle_image_state(message):
    if message.text == 'Its all over':
            return_to_menu(message.chat.id)
    else:
        # TODO image gn...
        bot.send_message(message.chat.id, 'Скоро буду генерировать фото. . .')

def handle_text_state(message):
    if message.text == 'Its all over':
            return_to_menu(message.chat.id)
    else:
        #TODO text gn...
        bot.send_message(message.chat.id, text='Скоро буду генерировать текст. . .')

def return_to_menu(chat_id):
     stater.set_state(chat_id, fsm.default_state)
     bot.send_message(chat_id, 'Главное меню:', reply_markup=keyboards.kb2)



@bot.message_handler(func=lambda message: True) # <- Регистрируем обработчик события "на сообщение"
def on_message(message):
    state = stater.get_state(message.chat.id)

    print(f"user msg '{message.text}' - on state {state}")
    if state == fsm.default_state:
        handle_default_state(message)
    elif state == fsm.image_state:
        handle_image_state(message)
    elif state == fsm.text_state:
        handle_text_state(message)
    else:
        return_to_menu(message.chat.id)

    #                   ^^^
    # Которая просто отошлет наш же текст "message.text",
    # нам же (наш ID) "message.chat.id"
 
bot.polling() # <- Старт 
