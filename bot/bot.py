import handlers as h
import config
from telebot import TeleBot


def main():
    bot = TeleBot(config.BOT_TOKEN)
    h.all_handlers(bot)
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        bot.stop_polling()


if __name__ == '__main__':
    main()