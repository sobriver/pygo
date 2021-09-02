import os
import sys

import face_recognition
import cv2
import numpy as np

if __name__ == '__main__':
    # 视频url
    video_url = '/face/data/psl-lhy-1920x1080.264'
    # 底库图片路径， 底库图片按照人名进行命名
    img_path = '/face/data/base'
    # 抓拍图保存路径
    save_path = '/face/data/capture/'

    known_face_names = []
    known_face_encodings = []
    for img in os.listdir(img_path):
        face_name = img.split('.')[0]
        known_face_names.append(face_name)
        face_img = face_recognition.load_image_file(os.path.join(img_path, img))
        face_img_encoding = face_recognition.face_encodings(face_img)[0]
        known_face_encodings.append(face_img_encoding)
    print('known face names:%s' % str(known_face_names))

    video_capture = cv2.VideoCapture(video_url)
    if video_capture is None:
        print('video not ready')
        sys.exit()

    i = 0
    while True:
        i = i + 1
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            print('identify name:%s' % name)
            if name == 'PSL':
                new_img = os.path.join(save_path, str(i) + '.jpg')
                cv2.imwrite(new_img, frame)

    video_capture.release()