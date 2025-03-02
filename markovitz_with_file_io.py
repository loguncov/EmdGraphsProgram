import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import tkinter as tk
from tkinter import ttk

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

def plot_matrix_with_scroll(matrix):
    """
    Отображает матрицу в виде таблицы с прокруткой.
    """
    root = tk.Tk()
    root.title("Матрица ЭМД")

    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(xscrollcommand=scrollbar.set)

    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    df = pd.DataFrame(matrix, columns=[f"t{i+1}" for i in range(matrix.shape[1])])
    table = ttk.Treeview(scrollable_frame, columns=list(df.columns), show="headings")

    for col in df.columns:
        table.heading(col, text=col)
        table.column(col, width=50)

    for row in df.itertuples(index=False):
        table.insert("", "end", values=row)

    table.pack()
    root.mainloop()

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
    plt.figure(figsize=(max(15, 0.2 * matrix.shape[1]), max(8, 0.5 * matrix.shape[0])))
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

# Отображаем матрицу в виде таблицы с прокруткой
plot_matrix_with_scroll(emd_time_matrix)

# Сохраняем в CSV
save_matrix_to_file(emd_time_matrix)

# Визуализируем heatmap
plot_heatmap(emd_time_matrix)
