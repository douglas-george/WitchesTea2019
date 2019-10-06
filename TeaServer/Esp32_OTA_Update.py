import subprocess
import time

#this list contains array of esp32 clients,
# and each client contains mDNS name and the path to .bin file
#I only have 1 ESP so I duplicate mDNS entry for testing
esps = [
  #mDNS name of ESP   #absolute path to ".bin" file
    #['esp32.local', 'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
    ['192.168.5.142', 'C:/Users/jay_d/PycharmProjects/WitchesTea2019/ArduinoWand/wand/wand.ino.esp32.bin'],
]

ip_of_sender = '192.168.5.177'
esp_respond_sender_port = '3232'
sender_to_esp_port = '3232'
update_password = 'iotsharing'

for esp in esps:
    cmd = 'python C:/Users/jay_d/Documents/ArduinoData/packages/esp32/hardware/esp32/1.0.2/tools/espota.py -i '+esp[0]+' -I '+ip_of_sender+ ' -p '+sender_to_esp_port+' -P '+esp_respond_sender_port+' -a '+update_password+' -f '+esp[1]
    print(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print(line)
    retval = p.wait()
    time.sleep(10)