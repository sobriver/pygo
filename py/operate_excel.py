# -*- coding: UTF-8 -*-

import xlwt
import xlrd
import os
# import logging.config




def walkFile(path):
    """
    遍历某个目录下的所有文件,返回绝对文件名列表和相对文件名列表
    :return:
    """
    file_path_list = []
    for root, dirs, files in os.walk(path):
        for item in files:
            file_path_list.append(os.path.join(root, item))
    return file_path_list

def get(oriFile, outFile):
    """
    按照特定的格式将excel文件输出
    1.找到输入对应的行数
    2.找到输出对应的行数
    3.找到表头对应的行数
    4.计算输出的行数(输出-输入)

    :return:
    """
    book = xlrd.open_workbook(oriFile)
    sheet = book.sheet_by_index(1)
    # 表头对应的行数
    head_row = 1
    # 输入对应的行数
    in_row = 0
    # 输出对应的行数
    out_row = 0
    # 行数
    nrows = sheet.nrows
    # 列数
    ncols = sheet.ncols

    for row in range(nrows):
        for col in range(ncols):
            value = sheet.cell_value(row, col)
            if value == '输入':
                in_row = row
            elif value == '输出':
                out_row = row

    # 写文件
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    in_sheet = book.add_sheet('in', cell_overwrite_ok=True)
    out_sheet = book.add_sheet('out', cell_overwrite_ok=True)

    # 计数器,用来保证每行从头开始插入

    for col in range(ncols):
        in_num = 1
        out_num = 1
        for row in range(nrows):
            # 插入表头
            if row == 1:
                in_sheet.write(0, col, sheet.cell_value(1, col))
                out_sheet.write(0, col, sheet.cell_value(1, col))
            # 插入输入项
            if in_row < row < out_row:
                in_sheet.write(in_num, col, sheet.cell_value(row, col))
                in_num += 1
            # 插入输出项
            if row > out_row:
                out_sheet.write(out_num, col, sheet.cell_value(row, col))
                out_num += 1
    book.save(outFile)
    # logger.debug(str(outFile) + '输出成功')
    print(str(outFile) + '输出成功')




if __name__ == '__main__':
    # with open('operate_excel_logging.conf', encoding='utf-8') as file:
    #     logging.config.fileConfig(file)
    #     logger = logging.getLogger()

    # 源文件目录路径
    # path = r"E:\test1"
    path = input('请输入源文件目录路径:')
    # 输出文件目录路径
    # out_path = r"E:\test2"
    out_path = input('请输入输出文件目录路径:')

    file_path_list = walkFile(path)
    # logger.debug('所有文件遍历成功, 文件数量=' + str(len(file_path_list)))
    print('所有文件遍历成功, 文件数量=' + str(len(file_path_list)))
    for f in file_path_list:

        try:
            f_tmp = str(f).split('\\')
            f_name = f_tmp[len(f_tmp)-1].replace('xlsx', 'xls')
            out_file = out_path + '\\' + f_name
            get(f, out_file)
        except Exception as e:
            # logger.error(str(f_name) + '输出失败')
            # logger.error(e)
            print(str(f_name) + '输出失败')
            print(e)
            pass
    input('按Enter键结束:')