import os

# Предполагается что скрипт лежит внутри датасета, рядом с источниками, а структура папок указана ниже
# Протестирован для датасета "Рассеянный склероз", версия 1.0
path = os.getcwd()

"""
Структура папок такая:
1. Сначала идут источники. Это видимо больницы из которых выгружали данные
2. Потом идут пациенты. Из каждой больницы ну допустим 4 пациента
3. Дальше идут серии снимков для 1 пайциента
4. Затем идут уже сами снимки

Этот скрипт считает среднее кол-во снимков на пациента
Кол-во снимков на пациента = сумме кол-ва снимков его серий
"""
print('Hello!')
all_items = os.listdir(path)

# Фильтруем только директории
all_sources = []
for item in all_items:
    source_path = os.path.join(path, item)
    if os.path.isdir(source_path):
        all_sources.append(source_path)

all_patients = [] #Пути ко всем пациентам

for path in all_sources:
    all_patients_by_source = [os.path.join(path, source_path) for source_path in os.listdir(path)]
    #print(all_patients_by_source)
    all_patients_by_source = list(filter(os.path.isdir, all_patients_by_source))
    #print('----------------------------')
    #Внутри только папки, поэтому так можно
    all_patients.extend(all_patients_by_source)

#Внутри только  dcm файлы, поэтому получаем только их
print('Количество пациентов: ',len(all_patients))
dcms_count = []
for patient in all_patients:
    all_series_by_patient = [os.path.join(patient,raw_path) for raw_path in os.listdir(patient)]
    dcms_by_patient = 0
    for serie in all_series_by_patient:
        all_dcms_by_serie = len(os.listdir(serie))
        dcms_by_patient += all_dcms_by_serie
    dcms_count.append(dcms_by_patient)

#print(dcms_count) --Отладка: количество снимков для каждого пациента
#dcms_count = np.array(dcms_count)
print('Статистика:')
print('Минимально снимков на пациента: ',min(dcms_count))
print('Максимально снимков на пациента: ',max(dcms_count))
print('В среднем снимков на пациента: ',int(sum(dcms_count)/len(dcms_count)))
threshold = 200 #Количество снимков, при котором обследование считается неудачным
filtered = list(filter(lambda x: x<threshold, dcms_count))
print(f'Количество пациентов с числом снимков <{threshold}: ',len(filtered))