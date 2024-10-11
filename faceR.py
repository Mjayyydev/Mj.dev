# Import necessary libraries
import face_recognition
import cv2
# Function to load known face encodings and names from image files
def load_known_faces(image_paths, names):
    known_face_encodings = []
    known_names = []

    for image_path, name in zip(image_paths, names):
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        known_face_encodings.extend(face_encodings)
        known_names.extend([name] * len(face_encodings))

    return known_face_encodings, known_names
# Function to recognize faces in a video stream
def recognize_faces(video_capture, known_face_encodings, known_names):
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        face_locations = face_recognition.face_locations(frame)

        for face_location in face_locations:
            top, right, bottom, left = face_location
            face_encoding = face_recognition.face_encodings(frame, [face_location])[0]
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

            print("Recognized Name:", name)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    # Specify the paths to the persons' image files
person_image_paths = [
    r"C:\Users\Em_Jayyy\Desktop\BOT\jane.png"
]

# Specify the names associated with each person
person_names = [
    "Jane",
    # Add more names as needed
    "Alien",
]

# Load the known face encodings and names
known_face_encodings, known_names = load_known_faces(person_image_paths, person_names)

# Open the webcam (0 corresponds to the default webcam)
video_capture = cv2.VideoCapture(0)

# Run face recognition on the live video stream
recognize_faces(video_capture, known_face_encodings, known_names)
