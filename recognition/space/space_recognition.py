import config
import cv2
import matplotlib.pyplot as plt
import numpy


def get_stars(user_choice='DwarfWLM') -> dict:
    """
    Основная управляющая функция распознавания.
    :param user_choice: Выбор фонового изображения пользователем.
    :return: Словарь с описанием успеха функции, списком точек и размером исходного изображения
    """
    base_space_img = config.USER_CHOICE_MAPPING[user_choice]
    contours = base_space_img.contours()
    centroids, new_contours, except_contours = _get_contour_center(contours)
    current_image = base_space_img.image()

    if config.SPACE_DEBUG_MODE:
        cv2.drawContours(current_image, contours=contours, contourIdx=-1,
                         color=(0, 255, 0), thickness=1, lineType=cv2.LINE_AA)
        cv2.drawContours(current_image, contours=new_contours, contourIdx=-1,
                         color=(0, 0, 255), thickness=1, lineType=cv2.LINE_AA)
        cv2.drawContours(current_image, contours=except_contours, contourIdx=-1,
                         color=(0, 255, 255), thickness=1, lineType=cv2.LINE_AA)
        for each in centroids:
            current_image[each] = [0, 0, 255]
        plt_image = cv2.cvtColor(current_image, cv2.COLOR_BGR2RGB)
        plt.imshow(plt_image)
        plt.show()

    return {'success': True,
            'stars': centroids,
            'image_size': (current_image.shape[0], current_image.shape[1])}


def _find_center_by_average_coordinates(contour: numpy.typing.NDArray) -> tuple:
    """
    Получение координат центра контура по среднему значению его минимальной и максимальной
    координат x и y
    :param contour: Контур в виде NDArray.
    :return: Кортеж из координат y и x. Возвращаются в таком порядке, чтобы использовать на
    изображении без переворота
    """
    min_x, min_y = contour[0][0][0], contour[0][0][1]
    max_x, max_y = contour[0][0][0], contour[0][0][1]
    for each in contour:
        current_x = each[0][0]
        current_y = each[0][1]
        if current_x < min_x:
            min_x = current_x
            continue
        if current_y < min_y:
            min_y = current_y
            continue
        if current_x > max_x:
            max_x = current_x
            continue
        if current_y > max_y:
            max_y = current_y
    return int((min_y + max_y) / 2), int((min_x + max_x) / 2)


def _get_contour_center(contours: list) -> (list, list, list):
    """
    Функция для получения списка центров всех контуров, а так же списка контуров с повторяющимися
    вершинами, и контуров, момент которых равен 0.
    :param contours: Список контуров для обработки типа NDArray.
    :return: Список центров, список ассиметричных контуров (число вершин не совпадает с длиной
    контура), список контуров с нулевым моментом.
    """
    list_of_centers = []
    asymmetric_contours = []
    except_contours = []
    for cnt in contours:
        moments = cv2.moments(cnt)
        unique_points = [list(x) for x in set(tuple(x[0]) for x in cnt)]
        if len(unique_points) != len(cnt):
            # print('BEGIN: Unique points != cnt')
            # print((len(unique_points), len(cnt)))
            # pprint.pprint(cnt)
            # pprint.pprint(moments)
            # print('END: Unique points != cnt')
            asymmetric_contours.append(cnt)
        if moments['m00'] != 0:
            cx = int(moments['m10']/moments['m00'])
            cy = int(moments['m01']/moments['m00'])
            list_of_centers.append((cy, cx))
        else:
            list_of_centers.append(_find_center_by_average_coordinates(cnt))
            # print('BEGIN: Exception')
            # pprint.pprint(e)
            # pprint.pprint(cnt)
            # pprint.pprint(moments)
            # print((len(unique_points), len(cnt)))
            # print('END: Exception')
            except_contours.append(cnt)
    return list_of_centers, asymmetric_contours, except_contours


if __name__ == '__main__':
    get_stars()
