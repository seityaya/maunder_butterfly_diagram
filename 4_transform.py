import csv

#Настройки
file_name_in   = "./fits.csv"  # Имя входного файла
file_name_out  = "./draw.csv"  # Имя выходного файла
latitude_limit = 65            # Значение крайнего положения широты, максимум 90
latitude_step  = 5             # Шаг широты
area_column    = 'AREAS_1'     # Колонка площадей пятен, по которой будет производится построение графика

#Открываем файл с данными на чтение
fd_r = open(file=file_name_in, mode='r')
#Создаем поток чтения
fd_r_csv = csv.DictReader(fd_r, delimiter=',', lineterminator='\r\n')
#Переменная для сохранения новой таблицы
data = list()
#Вычитываем файл построчно
for r in fd_r_csv:
    #Переменная для сохранения строки
    line = dict()
    #Читаем дату и время из файла и записываем как единую переменную
    line["DateTime"] = ("{y}.{m}.{d} {H}:{M}:{S}").format(y=r["YEAR"], m=r["MONTH"], d=r["DAY"], H=r["HOUR"], M=r["MINUTE"], S=r["SECOND"])
    #Проходим по колонкам широт
    for i in range(latitude_limit * -1, latitude_limit * +1, latitude_step):
        #Определяем диапазон широт
        latitude_beg = i
        latitude_end = i + latitude_step
        #Создаем переменную диапазона
        latitude = str("{beg}_{end}").format(beg=latitude_beg, end=latitude_end)
        #Записываем ноль в диапазон
        line[latitude] = "0"
        #Читаем значение широты пятна
        latitude_spot = r["LAT-DE"]
        #Определям в какую колонку широт необходимо поместить значение
        if(float(latitude_spot) >= latitude_beg and float(latitude_spot) < latitude_end):
            #Читаем значение площади пятна в колонке и записываем в новую колонку
            line[latitude] = r[area_column]
    #Добавляем строку в таблицу
    data.append(line)


#Открываем файл с результатами на запись
fd_w = open(file=file_name_out, mode='w+')
#Создам заголовок таблицы
header = list()
header.append("DateTime")
for i in range(latitude_limit * -1, latitude_limit * +1, latitude_step):
    #Определяем диапазон широт
    latitude_beg = i
    latitude_end = i + latitude_step
    #Создаем переменную диапазона
    latitude = str("{beg}_{end}").format(beg=latitude_beg, end=latitude_end)
    #Добавляем данные в заголовок
    header.append(latitude)

#Создаем поток записи
fd_w_csv = csv.DictWriter(fd_w, fieldnames=header, delimiter=',', lineterminator='\r\n', quoting=csv.QUOTE_ALL)
#Записывае заголовок
fd_w_csv.writeheader()
#Записываем данные
fd_w_csv.writerows(data)
