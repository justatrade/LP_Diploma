import telebot
from files.save_get_file import save_file


def greeting(msg, bot):
    """
    Приветственное сообщение, а так же подсказка
    :param msg: Полное описание сообщения пользователя, класс 'telebot.Types.Message'
    :param bot: Экземпляр класса, через который можем отправлять сообщения
    :return:
    """
    bot.send_message(msg.chat.id, f'Please send a high resolution photo '
                                  f'to proceed (max 20Mb')


def get_photo(msg, bot):
    """
    Получаем id файла и скачиваем с последующим сохранением.
    :param msg: Полное описание сообщения пользователя, класс 'telebot.Types.Message'
    :param bot: Экземпляр класса, через который можем отправлять сообщения
    :return:
    """
    if msg.photo:
        """
        Если файл приходит в фото, то мы получаем массив PhotoSize, где нам всегда нужен
        последний элемент, так как это самый большой из доступных размеров файлов 
        (оригинальный или 1280х960, если превышает)
        """
        file_id = msg.photo[-1].file_id
    else:
        # Если файл приходит в виде документа, то в нём сразу есть file_id
        file_id = msg.document.file_id
    try:
        file_info = bot.get_file(file_id)
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

