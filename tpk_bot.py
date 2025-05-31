import telebot # <- Импорт скачанного модуля
import keyboards 
import fsm 
import ai
import loguru
import yaml
import sys

stater = fsm.FSM()
logger = loguru.logger

try:
    with open("./config2.yaml", 'r') as file:
         cfg = yaml.safe_load(file)
         logger.info("Успешно загружена конфигурация")
except Exception as e:
     logger.warning("Произошла ошибка при установки конфигурации ({})", str(e))
     input()
     sys.exit(1)

ai_service = ai.AI(cfg)
BOT_TOKEN = cfg['telegram_token'] # <- Здесь указываем свой телеграм токен из BotFather
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
        try:
            msg = bot.send_message(chat_id=message.chat.id, text='Генерирую...')
            image_url = ai_service.generate_image(message.text)
            bot.delete_message(chat_id=message.chat.id, message_id=msg.id)
            bot.send_photo(chat_id=message.chat.id, caption='Ваше фото', photo=image_url)
        except Exception as e:
            bot.send_message(message.chat.id, text=f'Произошла ошибка ({str(e)})')

def handle_text_state(message):
    if message.text == 'Its all over':
            ai_service.clear_dialog(message.chat.id)
            return_to_menu(message.chat.id)
    else:
        msg = bot.send_message(message.chat.id, 'Думаю над запросом...')
        txt = ai_service.generate_text(message.text, message.chat.id)
        msg = bot.edit_message_text(text=txt, chat_id=message.chat.id, message_id=msg.id) 

def return_to_menu(chat_id):
     stater.set_state(chat_id, fsm.default_state)
     bot.send_message(chat_id, 'Главное меню:', reply_markup=keyboards.kb2)



@bot.message_handler(func=lambda message: True) # <- Регистрируем обработчик события "на сообщение"
def on_message(message):
    state = stater.get_state(message.chat.id)

    logger.info(
            "Пользователь [{}:{}] отправил сообщение '{}' в состоянии {}",
            message.chat.id,
            message.from_user.first_name,
            message.text,
            state
    )

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
