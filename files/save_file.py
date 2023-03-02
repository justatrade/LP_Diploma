import os
import config


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
    try:
        os.makedirs(f'{config.ROOT_DIR}/users/{user_id}', exist_ok=True)
        with open(os.path.join(f'{config.ROOT_DIR}/users/{user_id}', file_id), 'wb') as f:
            f.write(file)
    except (IOError, FileNotFoundError) as e:
        print(e)
        return False


if __name__ == '__main__':
    save_file(0, '', '')