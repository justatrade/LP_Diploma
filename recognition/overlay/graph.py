import pprint

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from numpy.typing import NDArray

import config
from recognition.overlay.point import Point


def contour_graph_create(contour: NDArray, simple_lvl: int = 10) -> nx.DiGraph:
    # TODO: Использовать адаптивный уровень упрощения, в случае, если при полученном, число точек
    #       контура будет меньше заданного.
    """
    Создание направленного графа из контура (массива точек).
    :param contour: Массив точек контура типа NDArray.
    :param simple_lvl: Уровень упрощения контура. Целое число, показывающее, во сколько раз
    уменьшится число исходных элементов контура.
    :return: Направленный граф networkx.DiGraph.
    """
    contour = [(x[0][0], x[0][1]) for x in contour[0::simple_lvl]]  # Распаковываем NDArray в list
    min_x, min_y = _normalisation_shift(contour)
    normalised_contour = [(x[0] - min_x, x[1] - min_y) for x in contour]

    if config.SPACE_DEBUG_MODE:
        print(min_x, min_y)
        pprint.pprint(contour)
        pprint.pprint(normalised_contour)

    contour_point = [Point(x[0], x[1]) for x in normalised_contour]
    contour_graph = nx.path_graph(contour_point, create_using=nx.DiGraph)
    return contour_graph


def contour_size(contour_graph: nx.DiGraph) -> tuple[int, int]:
    width, height = 0, 0
    for each in list(contour_graph):
        if each.x > width: width = each.x
        if each.y > height: height = each.y
    return height + 1, width + 1


def draw_graph(contour_graph: nx.DiGraph):
    """
    Функция для рисования направленного графа..
    :param contour_graph: Направленный граф, подготовленный для отрисовки (присутствует n вершин
    и n-1 рёбер.
    :return:
    """
    if contour_graph.number_of_nodes()-1 != contour_graph.number_of_edges():
        return

    contour_point = list(contour_graph)
    mapping = {point_obj: point_obj.name for point_obj in contour_point}
    contour_graph = nx.relabel_nodes(contour_graph, mapping)
    pos = {point.name: (point.x, -point.y) for point in contour_point}

    nx.draw_networkx(
        contour_graph,
        arrows=True,
        with_labels=False,
        pos=pos,
        node_size=10,
        node_color='green',
        width=1,
        arrowsize=2
    )
    plt.show()


def _normalisation_shift(contour: NDArray) -> (int, int):
    min_x = min([x[0] for x in contour])
    min_y = min([x[1] for x in contour])
    return min_x, min_y


if __name__ == '__main__':
    test_contour = np.load('../face/test.np.npy',
                           allow_pickle=True,
                           fix_imports=True)
    # contour_point = [(x[0][0], x[0][1]) for x in test_contour[0::10]]
    # print(contour_point[0], contour_point[-1])
    # # new_contour = []
    # # for i, _ in enumerate(contour_point):
    # #     if i % 10 == 0:
    # #         new_contour.append(contour_point[i])
    # # contour_point = new_contour
    # print(len(contour_point))
    # contour_point = [Point(x[0], -x[1]) for x in contour_point]
    # contour_graph = nx.path_graph(contour_point, create_using=nx.DiGraph)
    # print(list(contour_graph))
    graph = contour_graph_create(test_contour)
    # pprint.pprint(contour_graph.edges)

    # print(contour_point[-1], contour_point[0])
    # for each, _ in enumerate(contour_point):
    #     contour_graph.add_edge(contour_point[each-1],
    #                            contour_point[each])

    # for each in contour_graph.adjacency():
    #     print(each)
