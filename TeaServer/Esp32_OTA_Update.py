import subprocess
import time

#this list contains array of esp32 clients,
# and each client contains mDNS name and the path to .bin file
#I only have 1 ESP so I duplicate mDNS entry for testing
esps = [
    #['192.168.5.125', 'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    #['192.168.5.44',  'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    #['192.168.5.245', 'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    #['192.168.5.148', 'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    #['192.168.5.24',  'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    #['192.168.5.8',   'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    #['192.168.5.9',   'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    #['192.168.5.40',  'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    #['192.168.5.249', 'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    #['192.168.5.16',  'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    #['192.168.5.36',  'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    #['192.168.5.117', 'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    #['192.168.5.48',  'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    #['192.168.5.218', 'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    #['192.168.5.160', 'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    #['192.168.5.180', 'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    #['192.168.5.164', 'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    ['192.168.5.133', 'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    #['192.168.5.52',  'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    #['192.168.5.213', 'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    #['192.168.5.41',  'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    #['192.168.5.5',   'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    #['192.168.5.28',  'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    #['192.168.5.176', 'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    #['192.168.5.161', 'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    #['192.168.5.201', 'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
]

ip_of_sender = '192.168.5.119'
esp_respond_sender_port = '3232'
sender_to_esp_port = '3232'
update_password = 'iotsharing'

for esp in esps:
    #cmd = 'python C:/Users/jay_d/Documents/ArduinoData/packages/esp32/hardware/esp32/1.0.2/tools/espota.py -i '+esp[0]+' -I '+ip_of_sender+ ' -p '+sender_to_esp_port+' -P '+esp_respond_sender_port+' -a '+update_password+' -f '+esp[1]
    cmd = 'python C:/Users/jay_d/Documents/ArduinoData/packages/esp32/hardware/esp32/1.0.3/tools/espota.py -i ' + esp[
        0] + ' -I ' + ip_of_sender + ' -p ' + sender_to_esp_port + ' -P ' + esp_respond_sender_port + ' -a ' + update_password + ' -f ' + \
          esp[1]
    print(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print(line)
    retval = p.wait()
