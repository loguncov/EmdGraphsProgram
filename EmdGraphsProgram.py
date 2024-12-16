import math
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy.stats import norm

def calculate_direct_visibility(h1, h2):
    """
    Рассчитывает расстояние прямой радиовидимости между двумя антеннами.
    :param h1: Высота первой антенны (м)
    :param h2: Высота второй антенны (м)
    :return: Расстояние прямой радиовидимости (км)
    """
    a_e = 8500  # Эквивалентный радиус Земли (км)
    return math.sqrt(2 * a_e * h1) + math.sqrt(2 * a_e * h2)

def calculate_path_loss(frequency, distance):
    """
    Рассчитывает затухание сигнала в свободном пространстве.
    :param frequency: Частота сигнала (МГц)
    :param distance: Расстояние (км)
    :return: Затухание (дБ)
    """
    wavelength = 300 / frequency  # Длина волны (м)
    return 20 * math.log10(distance * 1000) + 20 * math.log10(frequency) - 147.55

def calculate_signal_to_noise(p1, g1, g2, loss):
    """
    Рассчитывает отношение сигнал/шум (SNR).
    :param p1: Мощность передатчика (дБм)
    :param g1: Коэффициент усиления передающей антенны (дБ)
    :param g2: Коэффициент усиления приемной антенны (дБ)
    :param loss: Затухание сигнала (дБ)
    :return: SNR (дБ)
    """
    return p1 + g1 + g2 - loss

def calculate_emd(snr, required_snr):
    """
    Рассчитывает вероятность электромагнитной доступности (ЭМД).
    :param snr: Отношение сигнал/шум (дБ)
    :param required_snr: Требуемый SNR (дБ)
    :return: Вероятность ЭМД (от 0 до 1)
    """
    sigma = 3  # Среднеквадратичное отклонение
    u = (snr - required_snr) / sigma
    return norm.cdf(u)

def build_graph(objects, frequency, required_snr):
    """
    Создает граф для заданного частотного диапазона.
    :param objects: Список объектов с их параметрами (координаты, высота антенны и т.д.)
    :param frequency: Частота сигнала (МГц)
    :param required_snr: Требуемый SNR (дБ)
    :return: Граф (NetworkX)
    """
    G = nx.Graph()
    for i, obj1 in enumerate(objects):
        for j, obj2 in enumerate(objects):
            if i >= j:
                continue
            distance = math.sqrt((obj1['x'] - obj2['x'])**2 + (obj1['y'] - obj2['y'])**2) / 1000  # в км
            visibility = calculate_direct_visibility(obj1['height'], obj2['height'])
            if distance > visibility:
                continue
            loss = calculate_path_loss(frequency, distance)
            snr = calculate_signal_to_noise(obj1['power'], obj1['gain'], obj2['gain'], loss)
            emd = calculate_emd(snr, required_snr)
            if emd > 0.1:  # Порог для добавления ребра
                G.add_edge(i, j, weight=1 - emd)
    return G

def visualize_graph(G, objects):
    """
    Визуализирует граф с объектами.
    :param G: Граф (NetworkX)
    :param objects: Список объектов с их параметрами
    """
    pos = {i: (obj['x'], obj['y']) for i, obj in enumerate(objects)}
    nx.draw(G, pos, with_labels=True, node_size=500, node_color='skyblue')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={k: f"{v:.2f}" for k, v in labels.items()})
    plt.show()

if __name__ == "__main__":
    # Пример объектов
    objects = [
        {'x': 0, 'y': 0, 'height': 50, 'power': 30, 'gain': 10},
        {'x': 1000, 'y': 1000, 'height': 50, 'power': 30, 'gain': 10},
        {'x': 2000, 'y': 0, 'height': 50, 'power': 30, 'gain': 10}
    ]

    # Параметры связи
    frequency = 300  # МГц
    required_snr = 10  # дБ

    # Построение графа
    G = build_graph(objects, frequency, required_snr)

    # Визуализация графа
    visualize_graph(G, objects)
