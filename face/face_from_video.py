import os

import face_recognition
import cv2
import numpy as np

video_path = '/face/data/psl-lhy-1920x1080.264'
img_path = '/face/data/psl.png'
save_path = '/face/data/save/'

video_capture = cv2.VideoCapture(video_path)

# Load a sample picture and learn how to recognize it.
psl_image = face_recognition.load_image_file(img_path)
psl_face_encoding = face_recognition.face_encodings(psl_image)[0]


# Create arrays of known face encodings and their names
known_face_encodings = [
    psl_face_encoding,
]
known_face_names = [
    "PSL",
]

# Initialize some variables
face_locations = []
face_encodings = []
process_this_frame = True

i = 0
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
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
    i = i + 1

# Release handle to the webcam
video_capture.release()