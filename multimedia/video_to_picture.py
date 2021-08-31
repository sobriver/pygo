import cv2

"""
将视频按照帧率截取成一张张的图片
"""

# 视频地址
VIDEO_PATH = r'D:\test\hus\jinyu3f01.ts'
# 存放帧图片的位置
EXTRACT_FOLDER = r'D:\test\hus\cap'
# 帧提取频率
EXTRACT_FREQUENCY = 1


def extract_frames(video_path, dst_folder, index):
    video = cv2.VideoCapture()
    if not video.open(video_path):
        print("can not open the video")
        exit(1)
    count = 1
    while True:
        _, frame = video.read()
        if frame is None:
            break
        if count % EXTRACT_FREQUENCY == 0:
            save_path = "{}/{:>03d}.jpg".format(dst_folder, index)
            cv2.imwrite(save_path, frame)
            print('save path:' + str(save_path))
            index += 1
        count += 1
    video.release()
    # 打印出所提取帧的总数
    print("Totally save {:d} pics".format(index-1))



if __name__ == '__main__':
    # 递归删除之前存放帧图片的文件夹，并新建一个
    import shutil
    try:
        shutil.rmtree(EXTRACT_FOLDER)
    except OSError:
        pass
    import os

    os.mkdir(EXTRACT_FOLDER)
    # 抽取帧图片，并保存到指定路径
    extract_frames(VIDEO_PATH, EXTRACT_FOLDER, 1)
