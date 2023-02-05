import requests
import datetime
import time
import sys
import yaml
import os
from pathlib import Path
from utils import Utils
import ast
import os

# environment constants

ENV = yaml.safe_load(Path('/home/awais/Desktop/azaan_python/assets/env.yaml').read_text())
ut = Utils(ENV)


def todays_scheduler():
    print(f"Initiating startup time... {datetime.datetime.now()}")
    ut.play_audio('startup')
    ut.get_prayer_times()
    while True:
        now = datetime.datetime.now()
        
        ut.prayer_dict['Maghrib'] = now.strftime('%H:%M %p')
        print(f"{now.strftime('%H:%M %p')} in {[ut.prayer_dict.values()]} gvghv")
        
        if now.strftime('%H:%M %p') == '01:00 AM':
            ut.get_prayer_times()
            time.sleep(120)
            print(f"New prayer time fetching done... {datetime.datetime.now()}")
            
        if now.strftime('%H:%M %p') in ut.prayer_dict.values():
            current_audio = list(ut.prayer_dict.keys())[list(ut.prayer_dict.values()).index(now.strftime('%H:%M %p'))]
            print(f"Initiating {current_audio} time... {datetime.datetime.now()}")
            ut.play_audio(current_audio)
            
        if (now + datetime.timedelta(hours=0, minutes=10)).strftime('%H:%M %p') in [*ut.prayer_dict.values()]:
            current_audio = 'qadha'
            print(f"Initiating {current_audio} time... {datetime.datetime.now()}")
            ut.play_audio(current_audio, loop=10)
            
        if now.strftime('%M') == '00':
            ut.play_audio('hour_check')
            time.sleep(60)

        time.sleep(10)
        
if __name__ == '__main__':
    todays_scheduler()  
