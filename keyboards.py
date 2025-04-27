import telebot

button1 = telebot.types.KeyboardButton(text='Its all over')
button2 = telebot.types.KeyboardButton(text='text')
button3 = telebot.types.KeyboardButton(text='image')

kb1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
kb2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
kb1.add(button1)
kb2.add(button2, button3)
