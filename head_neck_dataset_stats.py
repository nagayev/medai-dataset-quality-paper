import os
import pydicom

# Предполагается что скрипт лежит внутри датасета
# Протестирован для датасета "КТ головы и шеи с оценкой лимфатических узлов по классификации Node-RADS", версия 1.0
path = os.path.join(os.getcwd(),'studies')

"""
Структура папок такая:
1. Сначала идут пациенты. Всего 84 пациента
2. Затем идут обследования. По факту всегда одно.
3. Дальше идут серии снимков. По факту всегда одно.
4. Затем идут уже сами снимки. Обрати внимание: внутри одного dcm файла может лежать куча других

Этот скрипт считает среднее кол-во снимков на пациента
"""
print('Hello!')
all_patients = [os.path.join(path, filename) for filename in os.listdir(path)]

#Внутри только  dcm файлы, поэтому получаем только их
print('Количество пациентов: ',len(all_patients))
#print(all_patients)

dcms_count = []
for patient in all_patients:
    #Сначала идет обследование
    all_studies = os.listdir(patient)
    assert len(all_studies)==1 # Исследований на пациента всегда 1
    path = os.path.join(patient,all_studies[0])
    all_series_by_patient = [os.path.join(path,filename) for filename in os.listdir(path)]
    assert len(all_series_by_patient)==1 #Серий на пациента всегда одна
    dcms_by_patient = 0
    for serie in all_series_by_patient:
        #all_dcms_by_serie = len(os.listdir(serie)) Не работает: может быть несколько снимков в одном файле
        all_dcms_by_serie = 0
        for image in os.listdir(serie):
            image = os.path.join(serie, image)
            pydicom_image = pydicom.dcmread(image, specific_tags=['NumberOfFrames'])
            pydicom_image.decode()
            try:
                frames = pydicom_image.NumberOfFrames
                all_dcms_by_serie += frames
            except:
                #Далеко не во всех файлах множество кадров
                all_dcms_by_serie += 1 
            #print(image)

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