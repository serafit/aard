# aard
Aard (witcher's sign). Simple but powerful W-Fi jammer. You need a wireless wi-fi adapter (it will work from a laptop) and put it into monitoring mode

# Instalation (Linux/Termux with root) 

pip3 install scapy

git clone https://github.com/user22813/aard

cd aard

ifconfig wlan0 down

iwconfig wlan0 mode monitor

ifconfig wlan0 up

airodump-ng wlan0 --channel 3

python3 Aard.py
