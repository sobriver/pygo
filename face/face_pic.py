import face_recognition
import cv2



img_path = r'D:\test\hygs\5700.jpg'
dst_path = r'D:\test\hygs\new.jpg'
ret, frame = cv2.imread(img_path)
# Resize frame of video to 1/4 size for faster face detection processing
small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

# Find all the faces and face encodings in the current frame of video
locations = face_recognition.face_locations(frame)
print('face result:' + str(locations))

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

    new_img = 'new.jpg'
    cv2.imwrite(new_img, face_image)

