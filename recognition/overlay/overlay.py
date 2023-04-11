import config
import cv2
import graph
import matplotlib.pyplot as plt
import numpy as np
import recognition.space.space_recognition as sr
import time
from collections import Counter
from numpy.typing import NDArray


def place_contour_on_space(base_shape: tuple[int, int],
                           offset: tuple[int, int],
                           contour_matrix: NDArray
                           ) -> NDArray:
    """
    Функция размещения контура на матрице заданного размера в заданной позиции.
    :param base_shape: Размер матрицы для размещения контура.
    :param offset: Смещение контура.
    :param contour_matrix: Матрица контура типа NDArray.
    :return: Матрица заданного размера с контуром. Тип NDArray.
    """
    base = np.zeros(base_shape)
    base[
    offset[0]:offset[0] + contour_matrix.shape[0],
    offset[1]:offset[1] + contour_matrix.shape[1]
    ] = contour_matrix
    return base


def prepare_matrix(point_coordinates: list[tuple[int, int]],
                   shape: tuple[int, int],
                   default_value: int = 1) -> NDArray:
    """
    Подготовка нулевой двумерной матрицы из набора координат и размера с заданием значения для
    каждой точки
    координат.
    :param point_coordinates: Список координат в формате кортежа с двумя целыми числами (y, x)
    :param shape: Размер создаваемой матрицы.
    :param default_value: Значение для точки с соответствующей координатой.
    :return: Двумерная матрица типа NDArray.
    """
    matrix = np.zeros(shape, dtype=np.int8)
    for each in point_coordinates:
        matrix[each] = default_value
    return matrix


def create_weighted_matrix(star_matrix: NDArray) -> NDArray:
    """
    Создание взвешенной матрицы неба, где у каждой точки окружающей точку с центром звезды,
    есть значение.
    :param star_matrix: Матрица неба типа NDArray.
    :return: Взвешенная матрица неба типа NDArray.
    """
    # TODO: Реализовать проверку граничных точек при добавлении значений вокруг точки

    shape = star_matrix.shape
    borders_y = [0, shape[0] - 1, shape[0] - 2]  # Исключение граничных точек, чтобы избежать
    borders_x = [0, shape[1] - 1, shape[1] - 2]  # проверки на превышение границ

    def create_point_weight(coordinates: tuple):
        """
        Создание веса для заданной точки
        :param coordinates: Координаты точки в виде кортежа с двумя целыми числами (y, x).
        :return:
        """
        for each in config.FIRST_CIRCLE:
            cur_point = (coordinates[0] + each[0], coordinates[1] + each[1])
            if star_matrix[cur_point] > 0:
                continue
            else:
                star_matrix[cur_point] = config.FIRST_CIRCLE_VALUE
        for each in config.SECOND_CIRCLE:
            cur_point = (coordinates[0] + each[0], coordinates[1] + each[1])
            if star_matrix[cur_point] > 0:
                continue
            else:
                star_matrix[cur_point] = config.SECOND_CIRCLE_VALUE

    for every in list(zip(*np.where(star_matrix == config.DEFAULT_MATRIX_VALUE))):
        if every[0] not in borders_y and every[1] not in borders_x:
            create_point_weight(every)
    return star_matrix


def crop_matrix(matrix: NDArray,
                y_slice: tuple[int, int] = None,
                x_slice: tuple[int, int] = None) -> NDArray:
    """
    Усечение матрицы путём создания срезов.
    :param matrix: Двумерная матрица типа NDArray
    :param y_slice: Необязательный. Значения для вертикального среза.
    :param x_slice: Необязательный. Значения для горизонтального среза.
    :return:
    """
    if y_slice is not None:
        matrix = matrix[y_slice[0]:y_slice[1], :]
    if x_slice is not None:
        matrix = matrix[:, x_slice[0]:x_slice[1]]
    return matrix


def search_match(star_matrix: NDArray,
                 contour_matrix: NDArray) -> dict:
    """
    Функция поиска совпадений контура со взвешенной матрицей неба. Возвращает словарь со
    смещениями в виде ключей, и полученным значением веса совпадений в виде их значений.
    :param star_matrix: Двумерная матрица неба типа NDArray.
    :param contour_matrix: Двумерная матрица контура типа NDArray.
    :return:
    """

    offsets = {}
    contour_size = contour_matrix.shape

    for row in range(10): # star_matrix.shape[0] - contour_size[0]):
        column_search_time_s = time.time()
        for column in range(star_matrix.shape[1] - contour_size[1]):
            tmp_matrix = star_matrix[
                         row:(row + contour_size[0]),
                         column:(column + contour_size[1])
                         ]
            overlay_matrix = tmp_matrix + contour_matrix
            full_match = (overlay_matrix == 9).sum()
            half_match = (overlay_matrix == 5).sum()
            quarter_match = (overlay_matrix == 3).sum()

            offsets[(row, column)] = full_match + half_match + quarter_match
        column_search_time_f = time.time()
        if config.SPACE_DEBUG_MODE_TEXT:
            print(f'Passed row {row} of {star_matrix.shape[0] - contour_size[0]}'
                  f'in {column_search_time_f - column_search_time_s}')
    return offsets


def find_best_match(offsets: dict,
                    matches_number: int = 1) -> list[tuple[tuple, int]]:
    """
    Функция для получения списка смещений с наибольшим числом совпадений
    :param offsets: Словарь смещений с весом.
    :param matches_number: Число возвращаемых лучших совпадений.
    :return: Список вида tuple[tuple[int, int], int]
    """
    offsets_cnt = Counter(offsets)
    return offsets_cnt.most_common()[0:matches_number]


if __name__ == '__main__':
    # Katya_150 best match (855,103) 125
    # img = cv2.imread('../../test_img/Katya_2.jpg')
    # ratio = 150.0 / img.shape[1]
    # dim = (150, int(img.shape[0] * ratio))
    # img = cv2.resize(img, dim, interpolation=cv2.INTER_LINEAR)
    # cv2.imwrite('../../test_img/Katya_150.jpg', img)
    # img = image_params('../../test_img/Katya_150.jpg')
    load_contour_s = time.time()
    # contour = np.load('../face/test.np.npy',
    #                   allow_pickle=True,
    #                   fix_imports=True)
    load_contour_f = time.time()
    print(f'Contour load time: {load_contour_f - load_contour_s}')
    # Test drawing of static contour
    contour = np.load('../face/Katya.npy',
                      allow_pickle=True,
                      fix_imports=True)
    # img = cv2.imread('../../test_img/space/DwarfGalaxyWLM.png')
    # for idx, _ in enumerate(contour):
    #     print(idx, contour[idx])
    #     print(contour[idx][0])
    #     contour[idx][0][0] += 103
    #     contour[idx][0][1] += 855
    # cv2.waitKey(0)
    # cv2.drawContours(img, contour, contourIdx=-1, color=(0, 0, 255),
    #                  thickness=2, lineType=cv2.LINE_AA)
    # cv2.imshow('Test', img)
    # cv2.waitKey(0)
    ######################

    graph_create_s = time.time()
    contour_graph = graph.contour_graph_create(contour, 1)
    graph_create_f = time.time()
    print(f'Graph create time: {graph_create_f - graph_create_s}')
    get_stars_timer_s = time.time()
    stars = sr.get_stars()
    get_stars_timer_f = time.time()
    print(f'Get stars in: {get_stars_timer_f - get_stars_timer_s}')

    star_matrix_prepare_s = time.time()
    star_matrix = prepare_matrix(stars['stars'],
                                 stars['image_size'],
                                 config.DEFAULT_MATRIX_VALUE)
    star_matrix_prepare_f = time.time()

    star_matrix_crop_s = time.time()
    #star_matrix = crop_matrix(star_matrix, (0, 999))
    star_matrix_crop_f = time.time()

    star_matrix_weighted_s = time.time()
    star_matrix = create_weighted_matrix(star_matrix.copy())
    star_matrix_weighted_f = time.time()

    smp = star_matrix_prepare_f - star_matrix_prepare_s
    smc = star_matrix_crop_f - star_matrix_crop_s
    smw = star_matrix_weighted_f - star_matrix_weighted_s
    print(f'Prepare star matrix in '
          f'{smp} + {smc} + {smw} with total: {smp + smc + smw}')

    contour_prepare_timer_s = time.time()
    contour = [point.cv2_coords for point in list(contour_graph)]
    contour_size = graph.contour_size(contour_graph)
    contour_matrix = prepare_matrix(contour, contour_size)
    contour_matrix = crop_matrix(contour_matrix, y_slice=(50, 150), x_slice=(0, 30))
    contour_size = contour_matrix.shape
    contour_prepare_timer_f = time.time()
    print(f'Contour time: {contour_prepare_timer_f - contour_prepare_timer_s}')

    search_match_timer_s = time.time()
    offsets = search_match(star_matrix, contour_matrix)
    search_match_timer_f = time.time()

    #print(offsets)
    print(f'Search time: {search_match_timer_f - search_match_timer_s}')
    offsets_cnt = Counter(offsets)
    v = list(offsets.values())
    k = list(offsets.keys())
    max_matches = k[v.index(max(v))]
    print(max_matches, offsets[max_matches])
    print(offsets_cnt.most_common()[0:10])
    max_matches = find_best_match(offsets)[0][0]
    total_time = sum([
        load_contour_f - load_contour_s,
        graph_create_f - graph_create_s,
        get_stars_timer_f - get_stars_timer_s,
        smp, smc, smw,
        contour_prepare_timer_f - contour_prepare_timer_s,
        search_match_timer_f - search_match_timer_s
    ])
    print(f'Total time: {total_time}')
    # Test drawing of best
    # max_matches = (95, 2)
    ############################
    a = np.copy(star_matrix[
                max_matches[0]:(max_matches[0] + contour_size[0]),
                max_matches[1]:(max_matches[1] + contour_size[1])
                ])
    final = place_contour_on_space(star_matrix.shape,
                                   max_matches,
                                   contour_matrix)
    _, axs = plt.subplots(2, 2)
    ax1 = axs[0, 0]  # Contour
    ax2 = axs[0, 1]  # Stars
    ax3 = axs[1, 0]  # Stars[Part]
    ax4 = axs[1, 1]  # Combined
    # Test drawing of best
    # _, axs = plt.subplots(1, 2)
    # ax1 = axs[0]
    # ax4 = axs[1]
    ####################################
    ax1.spy(contour_matrix, markersize=2, c='green')
    ax2.spy(star_matrix == 8, markersize=4, c='red')
    ax2.spy(star_matrix == 4, markersize=2, c='green')
    ax2.spy(star_matrix == 2, markersize=1, c='blue')
    ax3.spy(a == 8, markersize=4, c='red')
    ax3.spy(a == 4, markersize=2, c='green')
    ax3.spy(a == 2, markersize=1, c='blue')
    wlm_image = config.USER_CHOICE_MAPPING['DwarfWLM'].image()
    wlm_image = cv2.cvtColor(wlm_image, cv2.COLOR_BGR2RGB)
    ax4.imshow(wlm_image, zorder=0)

    ax4.spy((star_matrix + final) == 9, markersize=10, c='green')
    ax4.spy((star_matrix + final) == 5, markersize=7, c='yellow')
    ax4.spy((star_matrix + final) == 3, markersize=5, c='orange')
    ax4.spy((star_matrix + final) == 1, markersize=1, c='blue')

    # ax4.spy((a + contour_matrix) == 9, markersize=10, c='green')
    # ax4.spy((a + contour_matrix) == 5, markersize=7, c='yellow')
    # ax4.spy((a + contour_matrix) == 3, markersize=5, c='orange')
    # ax4.spy((a + contour_matrix) == 1, markersize=1, c='blue')
    plt.show()