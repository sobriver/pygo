from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
import subprocess
from loguru import logger
import os
import zipfile
import shutil

logger.add('timer.log', level='INFO', format='{time:YYYY-MM-DD HH:mm:ss}-{file}-{line}-{message}', rotation="30 MB")

"""
定时脚本
"""

def backup_db():
    """
    备份数据库
    本地只保留最近30天的数据
    """
    # 备份数据目录
    try:
        # 数据保存目录
        backup_path = '/yunwei/timer/db'

        logger.info('start timer db data')
        dt_formatter = '%Y%m%d'
        now = datetime.now()
        file_name = now.strftime(dt_formatter) + '.sql'
        cmd_docker_id = 'docker ps|grep "acc-mysql"|awk \'{print $1}\''
        ret = subprocess.Popen(cmd_docker_id, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        docker_id = str(ret.stdout.read()).split('\'')[1][0:11]
        if not docker_id:
            logger.info('not get docker id')
            return
        cmd_export = 'docker exec -i ' + docker_id +  ' mysqldump -uroot -phuang1320 --host=127.0.0.1 --port=3306 --databases acc_app > ' + file_name
        ret1 = subprocess.run(cmd_export, shell=True)
        if ret1.returncode != 0:
            logger.info('export db data to file fail {}', str(ret1))
            return
        # 判断文件是否存在
        if not os.path.exists(file_name):
            logger.info('file not found')
            return
        logger.info('back up db data to disk complete')
        # 压缩文件并放入备份目录
        zip_name = file_name + '.zip'
        if os.path.exists(zip_name):
            os.remove(zip_name)
        if os.path.exists(os.path.join(backup_path, zip_name)):
            os.remove(os.path.join(backup_path, zip_name))
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as z:
            z.write(file_name)
        shutil.move(zip_name, backup_path)
        os.remove(file_name)
        logger.info('zip and move file complete')

        # 检查30天之前的文件并删除
        before_dt = now + timedelta(days=-30)
        for f_name in os.listdir(backup_path):
            f_dt_str = f_name.split('.')[0]
            f_dt = datetime.strptime(f_dt_str, dt_formatter)
            if f_dt < before_dt:
                logger.info('delete old file:{}', f_name)
                os.remove(os.path.join(backup_path, f_name))
        logger.info('end timer db data')
    except Exception as e:
        logger.exception(e)


def backup_app():
    """
    备份应用数据
    只保留最近30天的数据
    """
    print(f'{datetime.now()} timer app data')


def del_log():
    """
    删除日志
    只保留最近60天的文件
    """
    logger.info('start del log timer')
    log_path = '/workspace/acc/service/log'
    dt_formatter = '%Y-%m-%d'
    now = datetime.now()
    dt_before = now + timedelta(days=-60)
    for f_name in os.listdir(log_path):
        if f_name.endswith('.gz'):
            dt_str = f_name.split('.')[0].replace('acc-', '')
            dt = datetime.strptime(dt_str, dt_formatter)
            if dt < dt_before:
                logger.info("del log file:{}", f_name)
                os.remove(os.path.join(log_path, f_name))
    logger.info('end del log timer')



if __name__ == '__main__':
    schedule = BlockingScheduler()
    # 每天03:00执行
    schedule.add_job(del_log, 'cron', hour='3', minute='0')
    # 每天03:30执行
    schedule.add_job(backup_db, 'cron', hour='3', minute='30')
    schedule.start()
