import math
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy.stats import norm
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def calculate_direct_visibility(h1, h2):
    a_e = 8500  # Эквивалентный радиус Земли (км)
    return math.sqrt(2 * a_e * h1) + math.sqrt(2 * a_e * h2)


def calculate_path_loss(frequency, distance):
    wavelength = 300 / frequency  # Длина волны (м)
    return 20 * math.log10(distance * 1000) + 20 * math.log10(frequency) - 147.55


def calculate_signal_to_noise(p1, g1, g2, loss):
    return p1 + g1 + g2 - loss


def calculate_emd(snr, required_snr):
    sigma = 3  # Среднеквадратичное отклонение
    u = (snr - required_snr) / sigma
    return norm.cdf(u)


def build_graph(objects, frequency, required_snr):
    G = nx.Graph()
    for i, obj1 in enumerate(objects):
        for j, obj2 in enumerate(objects):
            if i >= j:
                continue
            distance = math.sqrt((obj1['x'] - obj2['x']) ** 2 + (obj1['y'] - obj2['y']) ** 2) / 1000
            visibility = calculate_direct_visibility(obj1['height'], obj2['height'])
            if distance > visibility:
                continue
            loss = calculate_path_loss(frequency, distance)
            snr = calculate_signal_to_noise(obj1['power'], obj1['gain'], obj2['gain'], loss)
            emd = calculate_emd(snr, required_snr)
            if emd > 0.1:
                G.add_edge(i, j, weight=1 - emd)
    return G


def visualize_graph(G, objects, frame):
    fig, ax = plt.subplots()
    pos = {i: (obj['x'], obj['y']) for i, obj in enumerate(objects)}
    nx.draw(G, pos, with_labels=True, node_size=500, node_color='skyblue', ax=ax)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={k: f"{v:.2f}" for k, v in labels.items()}, ax=ax)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def run_gui():
    def add_object():
        try:
            x = float(entry_x.get())
            y = float(entry_y.get())
            height = float(entry_height.get())
            power = float(entry_power.get())
            gain = float(entry_gain.get())
            objects.append({'x': x, 'y': y, 'height': height, 'power': power, 'gain': gain})
            messagebox.showinfo("Успех", f"Объект добавлен: x={x}, y={y}, height={height}, power={power}, gain={gain}")
            update_table()
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числовые значения")

    def update_table():
        for i in tree.get_children():
            tree.delete(i)
        for idx, obj in enumerate(objects):
            tree.insert("", "end", values=(idx, obj['x'], obj['y'], obj['height'], obj['power'], obj['gain']))

    def build_and_show_graph():
        try:
            freq = float(entry_freq.get())
            required_snr = float(entry_snr.get())
            G = build_graph(objects, freq, required_snr)
            visualize_graph(G, objects, frame_graph)
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные параметры частоты и SNR")

    root = tk.Tk()
    root.title("Построение графа ЭМД")

    frame_inputs = tk.Frame(root)
    frame_inputs.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(frame_inputs, text="Добавить объект").pack()
    tk.Label(frame_inputs, text="x").pack()
    entry_x = tk.Entry(frame_inputs)
    entry_x.pack()
    tk.Label(frame_inputs, text="y").pack()
    entry_y = tk.Entry(frame_inputs)
    entry_y.pack()
    tk.Label(frame_inputs, text="Высота (m)").pack()
    entry_height = tk.Entry(frame_inputs)
    entry_height.pack()
    tk.Label(frame_inputs, text="Мощность (dBm)").pack()
    entry_power = tk.Entry(frame_inputs)
    entry_power.pack()
    tk.Label(frame_inputs, text="Коэф. усиления (dB)").pack()
    entry_gain = tk.Entry(frame_inputs)
    entry_gain.pack()
    tk.Button(frame_inputs, text="Добавить объект", command=add_object).pack(pady=5)

    tk.Label(frame_inputs, text="Параметры связи").pack()
    tk.Label(frame_inputs, text="Частота (МГц)").pack()
    entry_freq = tk.Entry(frame_inputs)
    entry_freq.pack()
    tk.Label(frame_inputs, text="Требуемый SNR (дБ)").pack()
    entry_snr = tk.Entry(frame_inputs)
    entry_snr.pack()

    tk.Button(frame_inputs, text="Построить граф", command=build_and_show_graph).pack(pady=10)

    # Таблица для отображения объектов
    frame_table = tk.Frame(root)
    frame_table.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

    tree = ttk.Treeview(frame_table, columns=("ID", "x", "y", "Height", "Power", "Gain"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("x", text="x")
    tree.heading("y", text="y")
    tree.heading("Height", text="Height")
    tree.heading("Power", text="Power")
    tree.heading("Gain", text="Gain")
    tree.pack(fill=tk.BOTH, expand=True)

    frame_graph = tk.Frame(root)
    frame_graph.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    root.mainloop()


if __name__ == "__main__":
    objects = []  # Список объектов
    run_gui()
