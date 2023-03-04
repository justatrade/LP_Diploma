import os
import config


def get_file_by_user(user_id, file_id):
    """
    Функция которая возвращает файл пользователя в случае успеха, None во всех остальных
    :param user_id: id пользователя 'telebot.Types.Message.chat.id'
    :param file_id: id файла 'telebot.Types.Message.photo.file_id'
    :return:
    """
    try:
        with open(f'{config.ROOT_DIR}/users/{user_id}/{file_id}', 'rb') as f:
            file = f.read()
    except (FileNotFoundError, IOError) as e:
        print(e)
        return None
    return file


def check_format(file_id) -> bool:
    """
    Функция для проверки формата входящего файла.
    :param file_id: Название файла, расширение которого будет проверяться
    :return: True, если расширение допустимо. False во всех остальных случаях
    """
    extension = os.path.splitext(file_id)[-1][1::]
    return True if extension in config.ACCEPTABLE_FORMATS else False


def save_file(user_id: int, file_id: str, file) -> bool:
    """
    Функция принимает id пользователя и файл и сохраняет в директории, созданной для пользователя.
    Если директории нет, то она создаётся.
    Если файл с таким именем уже есть, то он перезаписывается.
    В будущем необходимо реализовать:
     - проверку на допустимый тип файла, на наличие аналогичного файла под другим именем
     - проверку на количество использованного дискового пространства пользователем
     - возвращать путь до файла для хранения в базе

    :param user_id: id чата бота с пользователем в ТГ
    :param file_id: строка с названием файла
    :param file: Набор байт, полученный в результате скачивания файла
    c помощью 'telebot.Telebot.download_file()'
    :return: True в случае успеха, False во всех остальных
    """
    if check_format(file_id):
        try:
            os.makedirs(f'{config.ROOT_DIR}/users/{user_id}', exist_ok=True)
            with open(os.path.join(
                    f'{config.ROOT_DIR}/users/{user_id}',
                    # Так как в file_id приходит путь от Телеграмм, который содержит директорию,
                    # мы отбрасываем его и берём только название файла
                    os.path.split(file_id)[-1]
            ), 'wb') as f:
                f.write(file)
                return True
        except (IOError, FileNotFoundError) as e:
            print(e)
            return False
    else:
        return False


if __name__ == '__main__':
    save_file(0, '', '')
