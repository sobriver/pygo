from datetime import datetime, timedelta
import subprocess
from loguru import logger
import os
import zipfile
import shutil

if __name__ == '__main__':

    logger.info('start del log timer')
    log_path = r'D:\tmp\332'
    dt_formatter = '%Y-%m-%d'
    now = datetime.now()
    dt_before = now + timedelta(days=-3)
    for f_name in os.listdir(log_path):
        if f_name.endswith('.gz'):
            dt_str = f_name.split('.')[0].replace('acc-', '')
            dt = datetime.strptime(dt_str, dt_formatter)
            if dt < dt_before:
                logger.info("del log file:{}", f_name)
                os.remove(os.path.join(log_path, f_name))
    logger.info('end del log timer')
