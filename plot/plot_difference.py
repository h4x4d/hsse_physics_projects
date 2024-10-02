import glob

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Генерация n наборов координат (для примера - 3 множества)
n = len(glob.glob("logs/*.csv"))
coordinates_x = []
coordinates_y = []
coordinates_z = []
speeds = []
heights = []
fuels = []
times = []
names = []
print(sorted(glob.glob("logs/*.csv"), key=lambda x: float(x.split('logs')[-1][:-4])))
# Создаем координаты для n множеств
for i in sorted(glob.glob("logs/*.csv"), key=lambda x: float(x.split('logs')[-1][:-4])):
    file = pd.read_csv(i)
    pos = [list(map(float, i[1:-1].split(','))) for i in file.pos]
    x = [i[0] for i in pos]
    y = [i[1] for i in pos]
    z = [i[2] for i in pos]
    coordinates_x.append(x)
    coordinates_y.append(y)
    coordinates_z.append(z)
    speeds.append(file.speed_mag)
    fuels.append(file.fuel_mass)
    heights.append(file.height)
    times.append(file.time)

    names.append("dt = " + i.split('logs')[-1][:-4])

# Создаем фигуру и три оси для каждого графика
fig, axs = plt.subplots(2, 3, figsize=(20, 12))

# График координат x от времени
for i in range(n):
    axs[0][0].plot(times[i], coordinates_x[i], label=names[i])
axs[0][0].set_title('Координата X от времени')
axs[0][0].set_xlabel('Время')
axs[0][0].set_ylabel('X')
axs[0][0].legend()

# График координат y от времени
for i in range(n):
    axs[0][1].plot(times[i], coordinates_y[i], label=names[i])
axs[0][1].set_title('Координата Y от времени')
axs[0][1].set_xlabel('Время')
axs[0][1].set_ylabel('Y')
axs[0][1].legend()

# График координат z от времени
for i in range(n):
    axs[0][2].plot(times[i], coordinates_z[i], label=names[i])
axs[0][2].set_title('Координата Z от времени')
axs[0][2].set_xlabel('Время')
axs[0][2].set_ylabel('Z')
axs[0][2].legend()

for i in range(n):
    axs[1][0].plot(times[i], speeds[i], label=names[i])
axs[1][0].set_title('Скорость от времени')
axs[1][0].set_xlabel('Время (с)')
axs[1][0].set_ylabel('Скорость (км/ч)')
axs[1][0].legend()

# График: Топливо от времени
for i in range(n):
    axs[1][1].plot(times[i], fuels[i], label=names[i])
axs[1][1].set_title('Топливо от времени')
axs[1][1].set_xlabel('Время (с)')
axs[1][1].set_ylabel('Топливо (кг)')
axs[1][1].legend()

# График: Расстояние от земли от времени
for i in range(n):
    axs[1][2].plot(times[i], heights[i], label=names[i])
axs[1][2].set_title('Расстояние от земли от времени')
axs[1][2].set_xlabel('Время (с)')
axs[1][2].set_ylabel('Расстояние от земли (м)')
axs[1][2].legend()

# Подгонка и отображение графиков
plt.tight_layout()
plt.show()