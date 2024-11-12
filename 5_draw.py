import time
import datetime
import csv
import matplotlib.pyplot as plt
import matplotlib.colors as cl
import numpy             as np

#Пример входной таблицы
#            "DateTime", "-90_-45", "-45_-00", "00_45", "45_90"
# "2000.01.01 00:00:00",       "0",       "0",   "1.1",     "0"

#Настройки
file_name_in   = "./draw.csv"  # Имя входного файла
area_multiple  = 0.1           # Множитель площади пятна

spot_size_min = 50.0
spot_size_max = 100.0

spot_color_min = cl.CSS4_COLORS['blue']
spot_color_mid = cl.CSS4_COLORS['green']
spot_color_max = cl.CSS4_COLORS['red']

#Открываем файл с данными на чтение
fd_r = open(file=file_name_in, mode='r')
#Создаем поток чтения
fd_r_csv = csv.DictReader(fd_r, delimiter=',', lineterminator='\r\n')
#Читаем заголовок
header = fd_r_csv.fieldnames
#Создаем переменные для осей графика и размера пятна
x_time_axis, y_lat_axis, s_size_spot, c_color_spot = [], [], [], []
#Вычитываем файл построчно
for r in fd_r_csv:
    #Создаем переменные для одной строки из таблицы
    xr, yr, sr, cr = [], [], [], []
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

        if(float(s) < spot_size_min):
            cr.append(spot_color_min)
        elif(float(s) >= spot_size_min and float(s) <= spot_size_max):
            cr.append(spot_color_mid)
        elif(float(s) > spot_size_max):
            cr.append(spot_color_max)

    #Добавляем данные в переменные построения графика
    x_time_axis.extend(xr)
    y_lat_axis.extend(yr)
    s_size_spot.extend(sr)
    c_color_spot.extend(cr)

#Рисуем график
plt.scatter(x=x_time_axis, y=y_lat_axis, s=s_size_spot, c=c_color_spot)
plt.xticks(rotation=30)
plt.xlabel('DateTime')
plt.ylabel('Latitude')
plt.show()
