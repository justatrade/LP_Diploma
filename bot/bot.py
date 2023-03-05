import handlers as h
import config
from telebot import TeleBot


def main():
    bot = TeleBot(config.BOT_TOKEN)
    bot.register_message_handler(h.get_photo,
                                 content_types=['photo', 'document'],
                                 pass_bot=True)
    bot.register_message_handler(h.greeting,
                                 commands=['start', 'help'],
                                 pass_bot=True)
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        bot.stop_polling()


if __name__ == '__main__':
    main()
