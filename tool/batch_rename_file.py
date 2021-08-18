"""
批量命名文件
"""
import os


def batch_rename(src_path, out_path):
    """
    批量命名
    :param file_path 文件路径
    """
    for item in os.listdir(src_path):
        new_name = item.replace('capture', 'target')
        os.rename(os.path.join(src_path, item), os.path.join(out_path, new_name))


if __name__ == '__main__':
    src = r'D:\test\重点人员告警抓拍图\old'
    out = r'D:\test\重点人员告警抓拍图\new'
    batch_rename(src, out)


