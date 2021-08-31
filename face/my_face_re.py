import face_recognition
import cv2

video_capture = cv2.VideoCapture('rtsp://10.171.7.45/qibiao/500-100.264')

i = 0
try:
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face detection processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Find all the faces and face encodings in the current frame of video
        locations = face_recognition.face_locations(frame)
        print('face result:' + str(locations))
        if locations is None:
            break
        if len(locations) == 0:
            continue

        # Display the results
        for top, right, bottom, left in locations:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Extract the region of the image that contains the face
            face_image = frame[top:bottom, left:right]

            # Blur the face image
            face_image = cv2.GaussianBlur(face_image, (99, 99), 30)

            new_img = 'new_' + str(i) + '.jpg'
            cv2.imwrite(new_img, face_image)
            i = i + 1
finally:
    video_capture.release()
