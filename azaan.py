import requests
import datetime
import time
import sys
import yaml
from pathlib import Path
from helpers.utils import Utils
from helpers.logger import logger

# environment constants

ENV = yaml.safe_load(Path('/home/awais/Desktop/azaan_python/helpers/env.yaml').read_text())
ut = Utils(ENV)


def todays_scheduler():
    logger.info(f"Initiating startup time...")
    ut.play_audio('startup')
    ut.get_prayer_times()
    while True:
        now = datetime.datetime.now()
        
        # ut.prayer_dict['Fajr'] = now.strftime('%H:%M')
        
        if now.strftime('%H:%M') in ['00:01', '01:00', '02:00', '12:00']:
            ut.get_prayer_times()
            time.sleep(120)
            
        if now.strftime('%H:%M') in ut.prayer_dict.values():
            current_audio = list(ut.prayer_dict.keys())[list(ut.prayer_dict.values()).index(now.strftime('%H:%M'))]
            logger.info(f"Initiating {current_audio} time...")
            ut.play_audio(current_audio)
            
        if (now + datetime.timedelta(hours=0, minutes=10)).strftime('%H:%M') in [*ut.prayer_dict.values()]:
            current_audio = 'qadha'
            logger.info(f"Initiating {current_audio} time...")
            ut.play_audio(current_audio, loop=10)
            
        if now.strftime('%M') == '00':
            logger.info(f"Hour check {now.strftime('%H %M')}")
            ut.play_audio('hour-clock')
            num_bells = int(now.strftime('%H %M')[0:2]) if int(now.strftime('%H %M')[0:2])<13 else int(now.strftime('%H %M')[0:2])-12
            ut.play_audio('hour-bell', loop = num_bells)
            time.sleep(60)

        time.sleep(15)
        
if __name__ == '__main__':
    todays_scheduler()  
