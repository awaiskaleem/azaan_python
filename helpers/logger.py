import logging

logging.basicConfig(
                    handlers=[
                    logging.FileHandler("/home/awais/Desktop/azaan_python/logs/log.txt"),
                    logging.StreamHandler()
                    ],
                    format='%(asctime)s:%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger('azaanLogger')
