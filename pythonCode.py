print("начало работы")
from random import randint
import threading

video = 1 # переменная отвечаеет за запись видео

f = open("route", "w") #очищаем файлик с маршрутом
coordinatesActual = 0   #переменная отвечает за координаты в у.е. 
EMA_Degrees = [0,120,240] #градусы расположения датчиков
powers = [1,1,1] #сила на колесах
gyroscopeWas = [90,90,90 ] #первичные значения гироскопа

def diamat(): #функция записи данных от датчиков
    degrees = [] 
    for y in range(360):
        degrees.append("x") #для удобства
    for i in range(len(EMA_Degrees)): 
        for x in range(120):
            EMA_Degrees[i] = (EMA_Degrees[i] + 1) % 360 #двигаем датчик на градус
            degrees[EMA_Degrees[i]] = randint(3,6) #поскольку нет реальных данных, толщина стенки равна случайному значению от 3 до 6
    gyroscope = [randint(0, 359), randint(0, 359), randint(0, 359)] #нет реальных данных - генерируем их для гироскопа
    for i in range(len(gyroscope)):
        gyroscope[i] = gyroscope[i] - gyroscopeWas[i]
    sr = f":{degrees}=\n={gyroscope}; \n" #создаем строку с получившимися данными
    f = open("route", "r").read();
    open("route", "w").write(f"{f}{sr}") #записываем все в файлик route

def first_thread():
    global coordinatesActual, video, powers
    print("ситстемы в норме")
    while True:
        diamat()
        distanceMeters = [randint(0,100),randint(0,100,),randint(0,100,)] #симулируем значения датчиков дальнометра
        if distanceMeters[0] < 20 and distanceMeters[1] < 20 and distanceMeters[2] < 20: #если слишком близко 
            video = 0 #выключаем видео
            powers = [0,0,0]
            break #завершаем работу
        if distanceMeters[0] != distanceMeters[1] or distanceMeters[1] != distanceMeters[2] or distanceMeters[0] != distanceMeters[2]: #если показания различны
            for i in range(len(distanceMeters)):
                if distanceMeters[i] == max(distanceMeters): 
                    powers[i] = 0.2 #уменьшаем скорость колеса, если его датчик показал самое большое расстояние
                else:
                    powers[i] = 1
        else:
            for i in range (len(powers)): #восстанавливаем нормальные значения мощности колес
                powers[i] = 1 
        coordinatesActual += 1 #условно шаг вперед

def second_thread():
    global video
    while video:
        pass #записываем видео пока video == 1
first = threading.Thread(target = first_thread, name = "a")
second = threading.Thread(target = second_thread, name = "c")
first.start()
second.start()
