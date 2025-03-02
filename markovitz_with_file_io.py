import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def create_time_series_matrix(matrices, num_time_intervals=100):
    """
    Создает временную матрицу ЭМД (каналы x временные интервалы).
    :param matrices: список матриц вероятностей ЭМД.
    :param num_time_intervals: количество временных шагов.
    :return: итоговая матрица (каналы x время).
    """
    num_channels = len(matrices[0])  # Определяем число каналов
    result_matrix = np.zeros((num_channels, num_time_intervals))  # Создаем матрицу

    # Заполняем матрицу значениями
    for t in range(min(num_time_intervals, len(matrices))):
        for channel in range(num_channels):
            result_matrix[channel, t] = np.mean(matrices[t][channel])  # Усредняем по строке

    return result_matrix

def plot_matrix(matrix):
    """
    Отображает матрицу в виде таблицы с масштабируемым размером.
    """
    fig, ax = plt.subplots(figsize=(max(10, 0.1 * matrix.shape[1]), max(5, 0.3 * matrix.shape[0])))
    ax.set_frame_on(False)

    # Создаём таблицу Pandas DataFrame
    df = pd.DataFrame(matrix, columns=[f"t{i+1}" for i in range(matrix.shape[1])])

    # Отображаем таблицу с форматированием
    table = ax.table(cellText=df.round(2).values, colLabels=df.columns, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.2, 1.2)
    ax.axis("off")  # Отключаем оси
    plt.title("Матрица ЭМД (временные промежутки × каналы)")
    plt.show()

def save_matrix_to_file(matrix, filename="emd_matrix.csv"):
    """
    Сохраняет матрицу в CSV-файл.
    """
    df = pd.DataFrame(matrix, columns=[f"t{i+1}" for i in range(matrix.shape[1])])
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"Матрица сохранена в {filename}")

def plot_heatmap(matrix):
    """
    Визуализация матрицы в виде heatmap.
    """
    plt.figure(figsize=(max(10, 0.1 * matrix.shape[1]), max(5, 0.3 * matrix.shape[0])))
    sns.heatmap(matrix, cmap="coolwarm", annot=False)
    plt.xlabel("Временные промежутки")
    plt.ylabel("Каналы связи")
    plt.title("Тепловая карта ЭМД")
    plt.show()

# Пример генерации 100 интервалов времени
num_channels = 5  # Можно менять
num_time_intervals = 100  # Количество временных интервалов

# Пример случайных данных (замените на реальные матрицы ЭМД)
matrices = [np.random.rand(num_channels, num_channels) for _ in range(num_time_intervals)]

# Создаем матрицу
emd_time_matrix = create_time_series_matrix(matrices, num_time_intervals)

# Отображаем матрицу в виде таблицы
plot_matrix(emd_time_matrix)

# Сохраняем в CSV
save_matrix_to_file(emd_time_matrix)

# Визуализируем heatmap
plot_heatmap(emd_time_matrix)
