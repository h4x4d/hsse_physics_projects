import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv(open('../logs2.csv', 'r', encoding='utf-8'))

# Пример данных
time = data.time  # время в часах
speed = data.speed_mag  # скорость в км/ч
fuel = data.fuel_mass  # топливо в литрах
distance_from_ground = data.height  # расстояние от земли в метрах

# Создаем фигуру и оси для каждого графика
fig, axs = plt.subplots(3, 1, figsize=(8, 10))

# График: Скорость от времени
axs[0].plot(time, speed, color='blue')
axs[0].set_title('Скорость от времени')
axs[0].set_xlabel('Время (с)')
axs[0].set_ylabel('Скорость (км/ч)')

# График: Топливо от времени
axs[1].plot(time, fuel, color='green')
axs[1].set_title('Топливо от времени')
axs[1].set_xlabel('Время (с)')
axs[1].set_ylabel('Топливо (кг)')

# График: Расстояние от земли от времени
axs[2].plot(time, distance_from_ground, color='red')
axs[2].set_title('Расстояние от земли от времени')
axs[2].set_xlabel('Время (с)')
axs[2].set_ylabel('Расстояние от земли (м)')

# Подгонка и отображение графиков
plt.tight_layout()
plt.show()