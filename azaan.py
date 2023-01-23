import requests
from pygame import mixer
import datetime
import time
import sys

city_id = 2673730
fajr_file = '/home/awais/Desktop/azaan_python/assets/fajr.mp3'
normal_file = '/home/awais/Desktop/azaan_python/assets/normal.mp3'
morning_file = '/home/awais/Desktop/azaan_python/assets/morning.mp3'
log_file = '/home/awais/Desktop/azaan_python/logs/log.txt'
startup_file = '/home/awais/Desktop/azaan_python/assets/startup.mp3'
qadha_file = '/home/awais/Desktop/azaan_python/assets/qadha.mp3'

sys.stdout = open(log_file,'a+')

def extract_array(input_string, sub_start, sub_end):
    sub_start_idx = [i for i in range(len(input_string)) if input_string.startswith(sub_start, i)]
    sub_end_idx = [i for i in range(len(input_string)) if input_string.startswith(sub_end, i)]
    if len(sub_start_idx)!=len(sub_end_idx):
        sub_end_idx = sub_end_idx[1:]
    return [input_string[sub_start_idx[idx]+len(sub_start):sub_end_idx[idx]] for idx in range(len(sub_start_idx))]

def play_audio(audio_name):
    print(f"Initiating {audio_name} time... {datetime.datetime.now()}", flush = True)
    mixer.init()
    mixer.music.set_volume(1.0)
    if audio_name == 'startup':
        mixer.music.load(startup_file)
    elif audio_name == 'Fajr':
        mixer.music.load(fajr_file)
    elif audio_name == 'qadha':
        mixer.music.load(qadha_file)
    elif audio_name == 'Sunrise':
        mixer.music.load(morning_file)
    else:
        mixer.music.load(normal_file)
    mixer.music.play()
    while mixer.music.get_busy():  # wait for audio to finish playing
        time.sleep(1)

def get_prayer_times():
    result = {}
    url = f"https://www.muslimpro.com/muslimprowidget.js?cityid={city_id}&Convention=Stockholm"
    try:
        response = requests.get(url).content.decode('ascii')
    except Exception as e:
        print(e, flush=True)

    prayer_names = extract_array(response, "innerHTML=\'<td>", "</td><td>")
    prayer_times = extract_array(response, "</td><td>", "</td>\'")
    for id in range(0,len(prayer_names)):
        result[prayer_names[id]] = prayer_times[id]
    print(result, flush=True)
    return result

def todays_scheduler():
    play_audio('startup')
    prayer_dict = get_prayer_times()
    while True:
        now = datetime.datetime.now()
        if now.strftime('%H:%M') == '01:00':
            prayer_dict = get_prayer_times()
        # prayer_dict['Maghrib'] = now.strftime('%H:%M')
        if now.strftime('%H:%M') in [*prayer_dict.values()]:
            play_audio(list(prayer_dict.keys())[list(prayer_dict.values()).index(now.strftime('%H:%M'))])
        if (now + datetime.timedelta(hours=0, minutes=10)).strftime('%H:%M') in [*prayer_dict.values()]:
            play_audio('qadha')

todays_scheduler()
