import telebot
from filesfiles.save_get_file import save_file


def all_handlers(bot: telebot.TeleBot):
    """
    Тут будут содержаться обработчики всех типов сообщений от пользователя
    :param bot:
    :return:
    """

    @bot.message_handler(commands=['start', 'help'])
    def greeting(msg):
        """
        Приветственное сообщение, а так же подсказка
        :param msg:
        :return:
        """
        bot.send_message(msg.chat.id, f'Please send a high resolution photo '
                                      f'to proceed (max 20Mb')

    @bot.message_handler(content_types=['photo', 'document'])
    def get_photo(msg):
        """
        Получаем id файла и скачиваем с последующим сохранением.
        :param msg: Полное описание сообщения пользователя, класс 'telebot.Types.Message'
        :return:
        """
        if msg.photo:
            """
            Если файл приходит в фото, то мы получаем массив PhotoSize, где нам всегда нужен
            последний элемент, так как это самый большой из доступных размеров файлов 
            (оригинальный или 1280х960, если превышает)
            """
            doc_type = 'photo[-1]'
        else:
            # Если файл приходит в виде документа, то в нём сразу есть file_id
            doc_type = 'document'
        try:
            file_info = bot.get_file(eval(f'msg.{doc_type}.file_id'))
            file = bot.download_file(file_info.file_path)
            bot.send_chat_action(msg.chat.id, action='upload_photo')
            if not save_file(msg.chat.id, file_info.file_path, file):
                raise IOError("Couldn't save file")
        except (ConnectionError,
                telebot.apihelper.ApiHTTPException,
                IOError) as e:
            print(e)
            bot.send_message(msg.chat.id, "Photo downloading failed. "
                                          "Please, try again")
