import cv2


if __name__ == '__main__':
    img_path = r'D:\test\hygs\5700.jpg'
    dst_path = r'D:\test\hygs\new.jpg'
    img = cv2.imread(img_path)
    # 高度、宽度、通道数
    print(img.shape)
    # [y0:y1, x0:x1]，其中原图的左上角是坐标原点
    cop = img[0:1080, 640:1280]
    cv2.imwrite(dst_path, cop)