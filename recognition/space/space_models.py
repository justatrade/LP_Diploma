import config
import cv2
from numpy.typing import NDArray
import os
from typing import TypeVar


class SpaceImage:
    """
    Класс для получения распознанного изображения и массива точек
    """
    def __init__(self, file_name,
                 threshold_level=150,
                 threshold_type=cv2.THRESH_BINARY):
        """
        Конструктор класса для получения контуров звёзд на изображении звёздного неба.
        :param threshold_level: Уровень предельного значения пикселя для преобразования в ч/б.
        :param threshold_type: Тип преобразования в ч/б.
        """
        self._threshold_level = threshold_level
        self._threshold_type = threshold_type
        self._contours_mode = cv2.RETR_EXTERNAL
        self._contours_method = cv2.CHAIN_APPROX_NONE
        if config.FULL_RES_FLAG:
            self._file_name = os.path.splitext(file_name)[0] + \
                              '_fullres' + \
                              os.path.splitext(file_name)[1]
        else:
            self._file_name = file_name
        self._original_img = self._get_original_image()
        self._img = self._get_threshold_image(
            self._get_gray_image(self._original_img))

    # def __setattr__(self, key, value):
    #     """
    #     Ограничение изменений атрибутов класса откуда-либо, кроме как из дочернего класса.
    #     :param key: Ключ.
    #     :param value: Значение.
    #     :return: Возвращает None при нарушении условия обращения, иначе устанавливает атрибут класса
    #     """
    #     if not issubclass(type(self), SpaceImage):
    #         return None
    #     else:
    #         self.__dict__[key] = value

    def image(self) -> NDArray:
        """
        Получение исходного изображения.
        :return: Массив NDArray исходного изображения.
        """
        return self._get_original_image()

    def contours(self) -> list:
        """
        Получение списка контуров.
        :return:
        """
        return self._get_contours(self._img)

    # noinspection PyMethodMayBeStatic
    def _get_original_image(self) -> NDArray:
        # TODO: Добавить обработку исключений здесь и во всех вызовах класса.
        #       Использовать полный путь к файлу или os.path.split() в месте вызова
        """
        Получаем оригинальное, не изменённое изображение по имени файла.
        :return: Массив, описывающий изображение
        :rtype: np.ndarray
        """
        img = cv2.imread(os.path.join(*[config.ROOT_DIR,
                                        config.SPACE_IMG_PATH,
                                        self._file_name]))
        return img

    # noinspection PyMethodMayBeStatic
    def _get_gray_image(self, img: NDArray) -> NDArray:
        """
        Преобразование изображения к оттенкам серого.
        :param img: Массив NDArray изображения.
        :return: Возвращается массив NDArray изображения в сером цвете.
        """
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def _get_threshold_image(self, img: NDArray) -> NDArray:
        """
        Преобразование серого изображения в ч/б по пороговому значению.
        :param img: Массив NDArray изображения в сером цвете.
        :return: Возвращается массив NDArray изображения в ч/б цвете.
        """
        _, img = cv2.threshold(img, self._threshold_level,
                               255, self._threshold_type)
        return img

    def _get_contours(self, img: NDArray) -> NDArray:
        """
        Приватный метод, для создания списка контуров
        Получение контуров по параметрам, заданным при инициализации класса.
        :param img: Массив NDArray ч/б изображения.
        :return: Возвращается список контуров, которые длиннее указанного значения
        """
        contours, _ = cv2.findContours(img,
                                       self._contours_mode,
                                       self._contours_method)
        contours_list = []
        for each in contours:
            if len(each) > config.MIN_CONTOUR_SIZE:
                contours_list.append(each)
        return contours_list


SpaceImageInheritor = TypeVar('SpaceImageInheritor', bound=SpaceImage)
