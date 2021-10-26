"""
将指定文件夹下面（包括递归的子文件）所有包含指定后缀的文件复制或移动到另一文件夹
"""
import os
import shutil

# 源路径
from_path = r'E:\tmp\4455\sync1'
# 保存路径
to_path = r'E:\tmp\4455\sync2'
# 文件后缀
formatters = ['txt', 'tx']
# 使用方式， copy or move
f_type = 'copy'


def get_file(path):
    all_files = []
    files = os.listdir(path)
    for f_name in files:
        f_path = os.path.join(path, f_name)
        if os.path.isdir(f_path):
            all_files.extend(get_file(f_path))
        elif os.path.isfile(f_path):
            for formatter in formatters:
                if f_name.endswith(formatter):
                    all_files.append(f_path)
                    break
        else:
            print('未知文件错误 %s' % f_path)
    return all_files



if __name__ == '__main__':
    filter_files = get_file(from_path)
    print('共筛选出符合条件文件数：%d' % len(filter_files))
    for index, f in enumerate(filter_files):
        print('%s 第 %d 个文件，name:%s' %(f_type, index+1, f))
        if f_type == 'copy':
            shutil.copy(f, to_path)
        elif f_type == 'move':
            shutil.move(f, to_path)
