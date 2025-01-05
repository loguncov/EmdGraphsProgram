import tkinter as tk
from tkinter import ttk

# Словарь с потерями сигнала в процентах для различных погодных условий
losses_percent = {
    "L-диапазон": {"Дождь": [2.28, 10.87], "Снег": [2.28, 10.87], "Облачность": [2.28, 6.67]},
    "S-диапазон": {"Дождь": [10.87, 29.21], "Снег": [10.87, 29.21], "Облачность": [10.87, 20.57]},
    "C-диапазон": {"Дождь": [20.57, 49.88], "Снег": [20.57, 49.88], "Облачность": [20.57, 36.90]},
    "X-диапазон": {"Дождь": [36.90, 68.38], "Снег": [36.90, 68.38], "Облачность": [36.90, 49.88]},
    "Ku-диапазон": {"Дождь": [49.88, 90.00], "Снег": [49.88, 90.00], "Облачность": [49.88, 68.38]},
    "Ka-диапазон": {"Дождь": [68.38, 99.00], "Снег": [68.38, 99.00], "Облачность": [68.38, 90.00]},
}


# Функция для расчета потерь сигнала с учетом интенсивности
def calculate_loss():
    freq = freq_combobox.get()
    condition = condition_combobox.get()
    intensity = intensity_combobox.get()

    if freq in losses_percent and condition in losses_percent[freq]:
        loss_range = losses_percent[freq][condition]

        # В зависимости от интенсивности выбираем соответствующий процент
        if intensity == "Сильно":
            avg_loss = loss_range[1]  # Верхняя граница
        elif intensity == "Средне":
            avg_loss = (loss_range[0] + loss_range[1]) / 2  # Среднее значение
        elif intensity == "Слабо":
            avg_loss = loss_range[0]  # Нижняя граница
        else:
            result_label.config(text="Ошибка! Выберите корректную интенсивность.")
            return

        result_label.config(text=f"Потери сигнала: {avg_loss:.2f}%")
    else:
        result_label.config(text="Ошибка! Выберите корректные значения.")


# Создание основного окна
root = tk.Tk()
root.title("Калькулятор потерь сигнала")

# Метки и комбобоксы для выбора частоты, погодных условий и интенсивности
freq_label = tk.Label(root, text="Выберите частотный диапазон:")
freq_label.grid(row=0, column=0, padx=10, pady=10)

freq_combobox = ttk.Combobox(root, values=["L-диапазон", "S-диапазон", "C-диапазон", "X-диапазон", "Ku-диапазон",
                                           "Ka-диапазон"])
freq_combobox.grid(row=0, column=1, padx=10, pady=10)

condition_label = tk.Label(root, text="Выберите тип осадков:")
condition_label.grid(row=1, column=0, padx=10, pady=10)

condition_combobox = ttk.Combobox(root, values=["Дождь", "Снег", "Облачность"])
condition_combobox.grid(row=1, column=1, padx=10, pady=10)

intensity_label = tk.Label(root, text="Выберите интенсивность:")
intensity_label.grid(row=2, column=0, padx=10, pady=10)

intensity_combobox = ttk.Combobox(root, values=["Сильно", "Средне", "Слабо"])
intensity_combobox.grid(row=2, column=1, padx=10, pady=10)

# Кнопка для расчета потерь
calculate_button = tk.Button(root, text="Рассчитать", command=calculate_loss)
calculate_button.grid(row=3, column=0, columnspan=2, pady=20)

# Метка для отображения результата
result_label = tk.Label(root, text="Потери сигнала: ")
result_label.grid(row=4, column=0, columnspan=2)

# Запуск интерфейса
root.mainloop()
