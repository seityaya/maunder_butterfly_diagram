import wget
import os
import csv

def silent_print(silent, *args):
    if not silent:
        for each in args:
            print(each, end='')
        print()


# Загружает файлы FITS с сервера в папку
# Возвращает путь к папке с файлами
def download_FITS(link: str, prefix: str, beg_year: int, end_year: int, file_dir: str,  silent: bool) -> str:
    silent_print(silent, "==============")
    silent_print(silent, "Download FITS file(s) begin")

    os.makedirs(name=file_dir, exist_ok=True)

    path = os.path.join(os.getcwd(), file_dir)
    silent_print(silent, "Directory: ", path)

    for y in range(beg_year, end_year + 1):
        url = link.format(prefix=prefix, year = y)
        filename = os.path.basename(url)
        if not os.path.exists(os.path.join(path, filename)):
            silent_print(silent, "Download file: ", filename)
            wget.download(url=url, out=path)
        else:
            silent_print(silent, "Skip file: ", filename)
    silent_print(silent, "Download file(s) end")
    silent_print(silent, "Return Path:", path)
    silent_print(silent, "==============")
    return path

# Берет все файлы в папке
# Возвращает путь к файлу
def concatenate_FITS(path_files: str, file_dir: str, file_name: str, beg_year: int, end_year: int, silent: bool) -> str:
    silent_print(silent, "==============")
    silent_print(silent, "Concatenate FITS file(s) begin")

    os.makedirs(name=file_dir, exist_ok=True)
    path = os.path.join(os.getcwd(), file_dir)
    file = os.path.join(path, file_name + ".txt")

    silent_print(silent, "Concatenate file: ", file)
    fd_w = open(file=file, mode='w+')

    all_files = []
    for f in os.listdir(path_files):
        for y in range(beg_year, end_year + 1):
            if f.endswith("{year}.txt".format(year=y)):
                all_files.append(os.path.join(path_files, f))

    all_files = sorted(all_files)

    for f in all_files:
        silent_print(silent, "Open file: ", f)
        fd_r = open(file=f, mode='r')
        fd_w.write(fd_r.read())

    silent_print(silent, "Concatenate FITS file(s) end")
    silent_print(silent, "Return File:", file)
    silent_print(silent, "==============")
    return file

def convert_FITS_ASCII_to_CSV(format, fits_file: str, file_dir: str, file_name: str, silent: bool) -> str:
    silent_print(silent, "==============")
    silent_print(silent, "Convert FITS file to CSV begin")

    fd = open(file=fits_file, mode='r')
    data = fd.read().splitlines()

    # Преобразование в двумерный массив
    lines = []
    for l in data:
        line = []
        line.append(l)
        lines.append(l)

    # Создание таблицы
    table = []
    if(format != None):
        for l in lines:
            line = []
            for f in format:
                if(f["name"] != "blank"):
                    beg = f["beg"]-1
                    end = f["end"]
                    if(end == 0):
                        end = len(l)
                    cell = l[beg:end]
                    cell = cell.strip()
                    line.append(cell)
            table.append(line)

    # Вставка названий колонок
    line = []
    for f in format:
        if(f["name"] != "blank"):
            cell = f["name"]
            line.append(cell)
    table.insert(0, line)

    # Сохранение
    if file_dir != "":
        os.makedirs(name=file_dir, exist_ok=True)
    path = os.path.join(os.getcwd(), file_dir)
    file = os.path.join(path, file_name + ".csv")
    fd = open(file=file, mode='w')
    fdcsv = csv.writer(fd, delimiter=',', lineterminator='\r\n', quoting=csv.QUOTE_ALL)

    for d in table:
        fdcsv.writerow(d)

    silent_print(silent, "Convert FITS file to CSV end")
    silent_print(silent, "Return File:", file)
    silent_print(silent, "==============")
    return file

#====================================================================================================================================================================================
#====================================================================================================================================================================================
#====================================================================================================================================================================================
#====================================================================================================================================================================================

#Формат таблиц
FORMAT_S = [
    {"name": "CODE"      , "beg": 1 , "end": 1 , "type": "str", "description": "Data code"                                                                    },
    {"name": "YEAR"      , "beg": 3 , "end": 6 , "type": "str", "description": "Year"                                                                         },
    {"name": "MONTH"     , "beg": 8 , "end": 9 , "type": "str", "description": "Month"                                                                        },
    {"name": "DAY"       , "beg": 11, "end": 12, "type": "str", "description": "Day"                                                                          },
    {"name": "HOUR"      , "beg": 14, "end": 15, "type": "str", "description": "Hour UT"                                                                      },
    {"name": "MINUTE"    , "beg": 17, "end": 18, "type": "str", "description": "Minute UT"                                                                    },
    {"name": "SECOND"    , "beg": 20, "end": 21, "type": "str", "description": "Second UT"                                                                    },
    {"name": "G_NUM"     , "beg": 23, "end": 28, "type": "str", "description": "NOAA sunspot"                                                                 },
    {"name": "S_G_NUM"   , "beg": 30, "end": 34, "type": "str", "description": "No. of spot within the group"                                                 },
    {"name": "AREAS_1"   , "beg": 36, "end": 40, "type": "str", "description": "Projected U umbra area in millionths of the solar disc"                       },
    {"name": "AREAS_2"   , "beg": 42, "end": 46, "type": "str", "description": "Projected WS whole spot area in millionths of the solar disc"                 },
    {"name": "AREAS_3"   , "beg": 48, "end": 52, "type": "str", "description": "Corrected U umbra area in millionths of the solar hemisphere"                 },
    {"name": "AREAS_4"   , "beg": 54, "end": 58, "type": "str", "description": "Corrected WS whole spot area in millionths of the solar hemisphere"           },
    {"name": "LAT-DE"    , "beg": 60, "end": 65, "type": "str", "description": "Heliographic latitude B; positive: North, negative: South"                    },
    {"name": "LON-DE"    , "beg": 68, "end": 72, "type": "str", "description": "Heliographic longitude L"                                                     },
    {"name": "LCM"       , "beg": 74, "end": 79, "type": "str", "description": "Longitudinal distance from the Sun's central meridian (LCM)"                  },
    {"name": "P_ANGLE"   , "beg": 81, "end": 86, "type": "str", "description": "Position angle"                                                               },
    {"name": "DIST_CENT" , "beg": 88, "end": 0 , "type": "str", "description": "Distance from the centre of Sun's disc measured in units of the solar radius" },
    ]

FORMAT_G = [
    {"name": "CODE"      , "beg": 1 , "end": 1 , "type": "str", "description": "Data code"                                                                             },
    {"name": "YEAR"      , "beg": 3 , "end": 6 , "type": "str", "description": "Year"                                                                                  },
    {"name": "MONTH"     , "beg": 8 , "end": 9 , "type": "str", "description": "Month"                                                                                 },
    {"name": "DAY"       , "beg": 11, "end": 12, "type": "str", "description": "Day"                                                                                   },
    {"name": "HOUR"      , "beg": 14, "end": 15, "type": "str", "description": "Hour UT"                                                                               },
    {"name": "MINUTE"    , "beg": 17, "end": 18, "type": "str", "description": "Minute UT"                                                                             },
    {"name": "SECOND"    , "beg": 20, "end": 21, "type": "str", "description": "Second UT"                                                                             },
    {"name": "G_NUM"     , "beg": 23, "end": 28, "type": "str", "description": "NOAA sunspot"                                                                          },
    {"name": "AREAS_1"   , "beg": 36, "end": 40, "type": "str", "description": "Total projected U umbra area of the group in millionths of the solar disc"             },
    {"name": "AREAS_2"   , "beg": 42, "end": 46, "type": "str", "description": "Total projected WS whole spot area area of the group in millionths of the solar disc"  },
    {"name": "AREAS_3"   , "beg": 48, "end": 52, "type": "str", "description": "Total corrected U umbra area of the group in millionths of the solar hemisphere"       },
    {"name": "AREAS_4"   , "beg": 54, "end": 58, "type": "str", "description": "Total corrected WS whole spot area of the group in millionths of the solar hemisphere" },
    {"name": "LAT-DE"    , "beg": 60, "end": 65, "type": "str", "description": "Heliographic latitude B; positive: North, negative: South"                             },
    {"name": "LON-DE"    , "beg": 67, "end": 72, "type": "str", "description": "Heliographic longitude L"                                                              },
    {"name": "LCM"       , "beg": 74, "end": 79, "type": "str", "description": "Longitudinal distance from the Sun's central meridian (LCM)"                           },
    {"name": "P_ANGLE"   , "beg": 81, "end": 86, "type": "str", "description": "Position angle"                                                                        },
    {"name": "DIST_CENT" , "beg": 88, "end": 0 , "type": "str", "description": "Distance from the centre of Sun's disc measured in units of the solar radius"          },
    ]

#====================================================================================================================================================================================
#====================================================================================================================================================================================

#Настройки
BEG_YEAR = 1974
END_YEAR = 2016

#====================================================================================================================================================================================
#====================================================================================================================================================================================

#Константы
PREFIX   = "g"

LINK_WEB            = "http://fenyi.solarobs.epss.hun-ren.hu/ftp/pub/DPD/data/{prefix}DPD{year}.txt"
FITS_DIR            = "123"

FITS_CONCAT_DIR     = "123"
FITS_CONCAT_FILE    = "CSV_{prefix}DPD_CONCATENATE_{beg}_{end}".format(prefix=PREFIX, beg=BEG_YEAR, end=END_YEAR)

CSV_CONCAT_DIR      = ""
CSV_CONCAT_FILE     = "fits"

if __name__ == '__main__':
    # Скачиваем
    path_FITS = download_FITS(link=LINK_WEB,
                              prefix=PREFIX,
                              beg_year=BEG_YEAR,
                              end_year=END_YEAR,
                              file_dir=FITS_DIR,
                              silent=False)

    # Объединяем
    file_FITS = concatenate_FITS(path_files=path_FITS,
                                 beg_year=BEG_YEAR,
                                 end_year=END_YEAR,
                                 file_dir=FITS_CONCAT_DIR,
                                 file_name=FITS_CONCAT_FILE,
                                 silent=False)

    # Преобразовываем в CSV
    file_CSV = convert_FITS_ASCII_to_CSV(format=FORMAT_S,
                                         fits_file=file_FITS,
                                         file_dir=CSV_CONCAT_DIR,
                                         file_name=CSV_CONCAT_FILE,
                                         silent=False)
