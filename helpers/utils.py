import requests
from pygame import mixer
import datetime
import time
import sys
from helpers.logger import logger

class Utils:
    def __init__(self, env):
        self.env = env
        self.MUSLIM_PRO_URL = f"http://www.muslimpro.com/muslimprowidget.js?cityid={self.env['city_id']}&Convention=Stockholm&timeformat=24"
        self.prayer_dict = {}

    def extract_array(self, input_string, sub_start, sub_end):
        sub_start_idx = [i for i in range(len(input_string)) if input_string.startswith(sub_start, i)]
        sub_end_idx = [i for i in range(len(input_string)) if input_string.startswith(sub_end, i)]
        if len(sub_start_idx)!=len(sub_end_idx):
            sub_end_idx = sub_end_idx[1:]
        return [input_string[sub_start_idx[idx]+len(sub_start):sub_end_idx[idx]] for idx in range(len(sub_start_idx))]

    def play_audio(self, audio_name, loop=1):
        logger.info("Playing an audio now")
        mixer.init()
        mixer.music.set_volume(1.0)
        if audio_name in ['startup', 'hour check']:
            mixer.music.load(self.env['file_system'].get('startup_file'))
        elif audio_name == 'Fajr':
            mixer.music.load(self.env['file_system'].get('fajr_file'))
        elif audio_name == 'qadha':
            mixer.music.load(self.env['file_system'].get('qadha_file'))
        elif audio_name == 'Sunrise':
            mixer.music.load(self.env['file_system'].get('morning_file'))
        else:
            mixer.music.load(self.env['file_system'].get('normal_file'))
        for i in range(0,loop):
            mixer.music.play()
            while mixer.music.get_busy():  # wait for audio to finish playing
                time.sleep(1)

    def get_prayer_times(self):
        try:
            logger.info("Fetching prayer times")
            response = requests.get(self.MUSLIM_PRO_URL).content.decode('ascii')
        except Exception as e:
            logger.error(f"Fetching prayers failed with error : {e}")
            pass

        prayer_names = self.extract_array(response, "innerHTML=\'<td>", "</td><td>")
        prayer_times = self.extract_array(response, "</td><td>", "</td>\'")
        for id in range(0,len(prayer_names)):
            self.prayer_dict[prayer_names[id]] = prayer_times[id]
        logger.info(f"Extracted Prayer Times: {self.prayer_dict}")
