# import json
# import pandas as pd
# from datetime import datetime
#
# # Загрузка JSON-файла
#
# with open('nvdcve-1.1-2024.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)
#
# # Извлечение дат публикации и преобразование их в datetime
# published_dates = [datetime.strptime(item['publishedDate'], '%Y-%m-%dT%H:%MZ') for item in data['CVE_Items']]
#
# # Создание DataFrame с датами публикации
# df = pd.DataFrame(published_dates, columns=['publishedDate'])
#
# # Преобразование даты в формат без времени для группировки
# df['publishedDate'] = df['publishedDate'].dt.date
#
# # Группировка по датам и подсчет количества CVE
# cve_per_day = df.groupby('publishedDate').size()
#
# # Вывод результата
# print(cve_per_day)


# 2
# import json
# from pandas.io.json import json_normalize
# import pandas as pd
# import glob
#
# # Получение списка всех JSON файлов в папке
# json_files = glob.glob('*.json')
#
# # Чтение и объединение данных из всех файлов
# data = pd.DataFrame()
# for file in json_files:
#     with open(file, 'r', encoding='utf-8') as f:
#         json_data = json.load(f)
#         cve_items = json_data.get('CVE_Items', [])
#         for item in cve_items:
#             # Создание DataFrame для каждого элемента и добавление его в общий DataFrame
#             item_df = pd.DataFrame([item])
#             data = pd.concat([data, item_df], ignore_index=True)
#
# # Обработка и анализ данных
# data['publishedDate'] = pd.to_datetime(data['publishedDate'])
# cve_per_day = data.groupby(data['publishedDate'].dt.date).size()
#
# # Вывод результата
# print(cve_per_day)

# 3
# import pandas as pd
# import json
# import glob
# from pandas import json_normalize  # Исправленный импорт
#
# # Получение списка всех JSON файлов в папке
# json_files = glob.glob('*.json')
#
# # Сбор данных в список
# data_list = []
# for file in json_files:
#     with open(file, 'r', encoding='utf-8') as f:
#         json_data = json.load(f)
#         cve_items = json_data.get('CVE_Items', [])
#         for item in cve_items:
#             # Преобразование каждого элемента в DataFrame и добавление в список
#             item_df = json_normalize(item)
#             data_list.append(item_df)
#
# # Объединение всех DataFrame в один
# data = pd.concat(data_list, ignore_index=True)
#
# # Обработка и анализ данных
# data['publishedDate'] = pd.to_datetime(data['publishedDate'])
# cve_per_day = data.groupby(data['publishedDate'].dt.date).size()
#
# # Вывод результата
# print(cve_per_day)

#4
import pandas as pd
import glob
from concurrent.futures import ThreadPoolExecutor
import orjson

# Установка настроек отображения для полного вывода данных
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def read_file(filename):
    with open(filename, 'rb') as f:
        return orjson.loads(f.read())['CVE_Items']


# Чтение и объединение данных из всех файлов с использованием многопоточности
with ThreadPoolExecutor() as ex:
    merged_data = [item for lst in ex.map(read_file, glob.glob('*.json')) for item in lst]

# Преобразование списка в DataFrame
data = pd.json_normalize(merged_data)

# Обработка и анализ данных
data['publishedDate'] = pd.to_datetime(data['publishedDate'])
cve_per_day = data.groupby(data['publishedDate'].dt.date).size()

# Вывод результата
print(cve_per_day)

summary_stats = cve_per_day.agg(['min', 'max', 'mean'])
date_with_max_cve = cve_per_day.idxmax()
date_with_min_cve = cve_per_day.idxmin()
print(summary_stats, date_with_max_cve, date_with_min_cve)
