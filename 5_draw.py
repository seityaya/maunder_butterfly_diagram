import time
import datetime
import csv
import matplotlib.pyplot as plt
import numpy             as np

#Настройки
file_name_in   = "./draw.csv"  # Имя входного файла
area_multiple  = 0.1           # Множитель, на которую будет умножаться площадь пятна

#Открываем файл с данными на чтение
fd_r = open(file=file_name_in, mode='r')
#Создаем поток чтения
fd_r_csv = csv.DictReader(fd_r, delimiter=',', lineterminator='\r\n')
#Читаем заголовок
header = fd_r_csv.fieldnames
#Создаем переменные для осей графика и размера пятна
x_time_axis, y_lat_axis, s_size_spot = [], [], []
#Вычитываем файл построчно
for r in fd_r_csv:
    #Создаем переменные для одной строки из таблицы
    xr, yr, sr = [], [], []
    #Получаем ДатуВремя строки и переводим в объект
    dt = r.pop('DateTime')
    dt = time.strptime(dt, '%Y.%m.%d %H:%M:%S')
    dt = datetime.datetime.fromtimestamp(time.mktime(dt))
    #Проходится по значениям в строке и создаем разреженый массив данных
    #для построения графика
    for y, s in r.items():
        xr.append(dt)
        yr.append(y)
        sr.append(float(s) * area_multiple)
    #Добавляем данные в переменные построения графика
    x_time_axis.extend(xr)
    y_lat_axis.extend(yr)
    s_size_spot.extend(sr)

#Рисуем график
plt.scatter(x=x_time_axis, y=y_lat_axis, s=s_size_spot)
plt.xticks(rotation=30)
plt.xlabel('DateTime')
plt.ylabel('Latitude')
plt.show()
