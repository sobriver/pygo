from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import subprocess
from loguru import logger
import os
import zipfile
import shutil

logger.add('backup.log',level='INFO',format='{time:YYYY-MM-DD HH:mm:ss}-{file}-{line}-{message}', rotation="30 MB")

"""
备份数据脚本
"""

def backup_db():
    """
    备份数据库
    每天备份一次， 本地只保留最近30天的数据
    """
    # 备份数据目录
    try:
        backup_path = '/yunwei/backup/db'

        logger.info('start backup db data')
        now = datetime.now()
        file_name = now.strftime('%Y%m%d') + '.sql'
        cmd_docker_id = 'docker ps|grep "app-service_mysql"|awk \'{print $1}\''
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
        # 压缩文件并放入备份目录
        zip_name = file_name + '.zip'
        if os.path.exists(zip_name):
            os.remove(zip_name)
        if os.path.exists(os.path.join(backup_path, zip_name)):
            os.remove(os.path.join(backup_path, zip_name))
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as z:
            z.write(file_name)
        shutil.move(zip_name, backup_path)

        # todo 检查30天之前的文件并删除, 暂时先这样吧
        logger.info('backup db data success')
    except Exception as e:
        logger.exception(e)


def backup_app():
    """
    备份应用数据
    每天备份一次， 本地只保留最近30天的数据
    :return:
    """
    print(f'{datetime.now()} backup app data')


if __name__ == '__main__':
    schedule = BlockingScheduler()
    schedule.add_job(backup_db, 'cron', hour='3', minute='30')
    schedule.start()
