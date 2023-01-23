import requests
from pygame import mixer
import datetime
import time
import sys

city_id = 2673730
fajr_file = '/home/awais/Desktop/azaan_python/fajr.mp3'
normal_file = '/home/awais/Desktop/azaan_python/normal.mp3'
log_file = '/home/awais/Desktop/azaan_python/log.txt'

sys.stdout = open(log_file,'a+')

def extract_array(input_string, sub_start, sub_end):
    sub_start_idx = [i for i in range(len(input_string)) if input_string.startswith(sub_start, i)]
    sub_end_idx = [i for i in range(len(input_string)) if input_string.startswith(sub_end, i)]
    if len(sub_start_idx)!=len(sub_end_idx):
        sub_end_idx = sub_end_idx[1:]
    return [input_string[sub_start_idx[idx]+len(sub_start):sub_end_idx[idx]] for idx in range(len(sub_start_idx))]

def play_azaan(prayer_name):
    print(f"Initiating prayers call for {prayer_name} time... {datetime.datetime.now()}", flush = True)
    mixer.init()
    if prayer_name == 'Fajr':
        mixer.music.load('Fajr.mp3')
    elif prayer_name != 'Sunrise':
        mixer.music.load('Normal.mp3')
    mixer.music.play()
    while mixer.music.get_busy():  # wait for azaan to finish playing
        time.sleep(1)

def get_prayer_times():
    result = {}
    url = f"https://www.muslimpro.com/muslimprowidget.js?cityid={city_id}&Convention=Stockholm"
    response = requests.get(url).content.decode('ascii')

    prayer_names = extract_array(response, "innerHTML=\'<td>", "</td><td>")
    prayer_times = extract_array(response, "</td><td>", "</td>\'")
    for id in range(0,len(prayer_names)):
        result[prayer_names[id]] = prayer_times[id]
    return result

def todays_scheduler():
    prayer_dict = get_prayer_times()
    while True:
        now = datetime.datetime.now()
        if now.strftime('%H:%M') == '01:00':
            prayer_dict = get_prayer_times()
        # prayer_dict['Asr'] = '20:40'
        prayer_dict['Fjr'] = datetime.datetime.now().strftime('%H:%M')
        # get_prayer_times(prayer_dict)
        if now.strftime('%H:%M') in [*prayer_dict.values()]:
            play_azaan(list(prayer_dict.keys())[list(prayer_dict.values()).index(now.strftime('%H:%M'))])

todays_scheduler()
