import math
import numpy as np
from scipy.stats import norm
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, filedialog
import csv

matrices = []  # Список для хранения матриц

def calculate_direct_visibility(h1, h2):
    a_e = 8500  # Эквивалентный радиус Земли (км)
    return math.sqrt(2 * a_e * h1) + math.sqrt(2 * a_e * h2)

def calculate_path_loss(frequency, distance):
    wavelength = 300 / frequency  # Длина волны (м)
    return 20 * math.log10(distance * 1000) + 20 * math.log10(frequency) - 147.55

def calculate_signal_to_noise(p1, g1, g2, loss, noise_power, weather_loss):
    """Расчет отношения сигнал/шум с учетом мощности помехи и потерь из-за погоды."""
    loss_with_weather = loss + (loss * weather_loss / 100)  # Учитываем потери из-за погоды
    signal_power = p1 + g1 + g2 - loss_with_weather  # Мощность сигнала
    return signal_power - noise_power  # SNR = сигнал минус шум

def calculate_emd(snr, required_snr):
    sigma = 3  # Среднеквадратичное отклонение
    u = (snr - required_snr) / sigma
    return norm.cdf(u)

def build_matrix(objects, frequency, required_snr, weather_loss):
    n = len(objects)
    matrix = np.zeros((n, n))
    for i, obj1 in enumerate(objects):
        for j, obj2 in enumerate(objects):
            if i == j:
                continue
            distance = math.sqrt((obj1['x'] - obj2['x']) ** 2 + (obj1['y'] - obj2['y']) ** 2) / 1000
            visibility = calculate_direct_visibility(obj1['height'], obj2['height'])
            if distance > visibility:
                matrix[i][j] = 0
                continue
            loss = calculate_path_loss(frequency, distance)
            snr = calculate_signal_to_noise(obj1['power'], obj1['gain'], obj2['gain'], loss, obj1['noise_power'], weather_loss)
            emd = calculate_emd(snr, required_snr)
            matrix[i][j] = round(emd, 2)  # Округляем значение до сотых
    return matrix

def display_matrix(matrices, frame):
    # Очищаем только область для матриц, чтобы не перерисовывать все элементы
    for widget in frame.winfo_children():
        widget.destroy()

    # Начальный столбец для отображения матриц
    column_offset = 0

    # Отображаем все матрицы подряд по горизонтали
    for matrix_idx, matrix in enumerate(matrices):
        # Добавляем заголовок для каждой матрицы
        header = tk.Label(frame, text=f"Расчет ЭМД для случая №{matrix_idx + 1}", font=("Arial", 14, "bold"))
        header.grid(row=0, column=column_offset, columnspan=len(matrix) + 1, pady=10)

        # Добавляем заголовки столбцов
        for j in range(len(matrix)):
            header = tk.Label(frame, text=f"{j}", borderwidth=1, relief="solid", width=4, height=2, bg="lightgray")
            header.grid(row=1, column=column_offset + j + 1, padx=1, pady=1)

        # Добавляем заголовки строк и содержимое матрицы
        for i, row in enumerate(matrix):
            row_header = tk.Label(frame, text=f"{i}", borderwidth=1, relief="solid", width=4, height=2, bg="lightgray")
            row_header.grid(row=i + 2, column=column_offset, padx=1, pady=1)
            for j, value in enumerate(row):
                color = "lightgreen" if value > 0.5 else "yellow" if value > 0.1 else "lightcoral"
                label = tk.Label(frame, text=f"{value:.2f}", borderwidth=1, relief="solid", width=4, height=2, bg=color)
                label.grid(row=i + 2, column=column_offset + j + 1, padx=1, pady=1)

        # Обновляем offset для следующей матрицы, чтобы она была в следующем столбце
        column_offset += len(matrix) + 2

def save_matrix_to_file(matrix):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([f"Column {i}" for i in range(len(matrix))])
                writer.writerows(matrix)
            messagebox.showinfo("Успех", "Матрица успешно сохранена в файл")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")

def update_table(tree):
    for i in tree.get_children():
        tree.delete(i)
    for idx, obj in enumerate(objects):
        tree.insert("", "end", values=(idx, obj['x'], obj['y'], obj['height'], obj['power'], obj['gain'], obj['noise_power']))

def load_objects_from_file(tree):
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                objects.append({
                    'x': float(row['x']),
                    'y': float(row['y']),
                    'height': float(row['height']),
                    'power': float(row['power']),
                    'gain': float(row['gain']),
                    'noise_power': float(row['noise_power'])
                })
            messagebox.showinfo("Успех", "Объекты успешно загружены из файла")
            update_table(tree)
    except (ValueError, KeyError, FileNotFoundError) as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

def run_gui():
    def add_object():
        try:
            x = float(entry_x.get())
            y = float(entry_y.get())
            height = float(entry_height.get())
            power = float(entry_power.get())
            gain = float(entry_gain.get())
            noise_power = float(entry_noise_power.get())  # Мощность помехи
            objects.append({'x': x, 'y': y, 'height': height, 'power': power, 'gain': gain, 'noise_power': noise_power})
            messagebox.showinfo("Успех", f"Объект добавлен: x={x}, y={y}, height={height}, power={power}, gain={gain}, noise_power={noise_power}")
            update_table(tree)
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числовые значения")

    def build_and_show_matrix():
        if len(matrices) >= 3:
            messagebox.showwarning("Ограничение", "Можно создать не более 3 матриц.")
            return  # Прерываем выполнение функции, если уже 3 матрицы

        try:
            freq = float(entry_freq.get())
            required_snr = float(entry_snr.get())
            weather_loss = float(entry_weather_loss.get())  # Получаем коэффициент потерь из-за погоды
            matrix = build_matrix(objects, freq, required_snr, weather_loss)
            matrices.append(matrix)  # Добавляем матрицу в список
            display_matrix(matrices, frame_matrix)  # Отображаем все матрицы
            if messagebox.askyesno("Сохранение", "Сохранить полученную матрицу в файл?"):
                save_matrix_to_file(matrix)
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные параметры частоты, SNR и потерь из-за погоды")

    root = tk.Tk()
    root.title("Матрица связи ЭМД")

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
    tk.Label(frame_inputs, text="Мощность помехи (dBm)").pack()  # Добавляем ввод для мощности помехи
    entry_noise_power = tk.Entry(frame_inputs)
    entry_noise_power.pack()
    tk.Button(frame_inputs, text="Добавить объект", command=add_object).pack(pady=5)
    tk.Button(frame_inputs, text="Загрузить из файла", command=lambda: load_objects_from_file(tree)).pack(pady=5)

    tk.Label(frame_inputs, text="Параметры связи").pack()
    tk.Label(frame_inputs, text="Частота (МГц)").pack()
    entry_freq = tk.Entry(frame_inputs)
    entry_freq.pack()
    tk.Label(frame_inputs, text="Требуемый SNR (дБ)").pack()
    entry_snr = tk.Entry(frame_inputs)
    entry_snr.pack()
    tk.Label(frame_inputs, text="Потери из-за погоды (%)").pack()  # Новый ввод для коэффициента потерь
    entry_weather_loss = tk.Entry(frame_inputs)
    entry_weather_loss.pack()

    tk.Button(frame_inputs, text="Построить матрицу", command=build_and_show_matrix).pack(pady=10)

    # Таблица для отображения объектов
    frame_table = tk.Frame(root)
    frame_table.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

    tree = ttk.Treeview(frame_table, columns=("ID", "x", "y", "Height", "Power", "Gain", "Noise Power"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("x", text="x")
    tree.heading("y", text="y")
    tree.heading("Height", text="Height")
    tree.heading("Power", text="Power")
    tree.heading("Gain", text="Gain")
    tree.heading("Noise Power", text="Noise Power")
    tree.pack(fill=tk.BOTH, expand=True)

    frame_matrix = tk.Frame(root)
    frame_matrix.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    objects = []  # Список объектов
    run_gui()
