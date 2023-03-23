import telebot
import openai
import os
import config
import json

# Установить токен вашего телеграм-бота
bot = telebot.TeleBot(config.TOKEN)

# Установить ключ API OpenAI
openai.api_key = config.OPENAI_TOKEN

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('/home/severus/openaiwithtelegrambot/static/images/stick.webp','rb')
    bot.send_sticker(message.chat.id,sti)
    bot.send_message(message.chat.id, "Welcome,{0.first_name}!\nЯ-<b>{1.first_name}</b>,бот созданный чтобы быть твоим другом.".format(message.from_user,bot.get_me()),parse_mode='html')

# Обработчик всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Отправить индикатор набора сообщения, чтобы пользователь знал, что мы обрабатываем его сообщение
    bot.send_chat_action(message.chat.id, 'typing')

    # Используйте API OpenAI "davinci-003" для генерации ответа на вопрос пользователя
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message.text,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5
    )

    # Отправьте сгенерированный ответ пользователю
    bot.reply_to(message, response.choices[0].text)

    

# Опционально, сохраните беседу в файл журнала
with open("./tmp/conversation.json", "a") as f:
    log_entry = {
        "user": message.from_user.username,
        "message": message.text,
        "bot_response": response.choices[0].text
    }
    json.dump(log_entry, f)
    f.write("\n")

# Запуск бота
bot.polling()


