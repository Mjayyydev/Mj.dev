import face_recognition
import cv2
import subprocess
import os
import pyttsx3
import sys

def load_known_faces(image_paths, names):

   # image_paths (list): List of paths to the images.
   # names (list): List of names corresponding to the images.

     #(known_face_encodings, known_names) where known_face_encodings is a list of face encodings and known_names is a list of names.
    
    known_face_encodings = []
    known_names = []

    for image_path, name in zip(image_paths, names):
        if not os.path.exists(image_path):
            print(f"Image path {image_path} does not exist.")
            continue

        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)

        if face_encodings:
            known_face_encodings.extend(face_encodings)
            known_names.extend([name] * len(face_encodings))
        else:
            print(f"No face encodings found in image {image_path}.")

    return known_face_encodings, known_names

def recognize_faces(video_capture, known_face_encodings, known_names):
    
    #Recognize faces in the video stream and trigger a chatbot program when a face is recognized.

    #video_capture (cv2.VideoCapture): Video capture object.
   # known_names (list): List of names corresponding to the known face encodings.
    
    engine = pyttsx3.init()
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture frame from video stream.")
            break

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = face_distances.argmin()
            if matches[best_match_index]:
                name = known_names[best_match_index]
                print(f"Recognized {name}")

                
                # Speak the recognized name
                engine.say(f"Recognized {name}")
                engine.runAndWait()



            

                # Trigger the chatbot program when a face is recognized
                subprocess.Popen([sys.executable, "bott.py"])
                return  
            # Exit after starting the chatbot
            

            else:
                print(f" {name}")
                engine.say((f"{name}"))
                engine.runAndWait()
                break

        cv2.imshow('Jane Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
           break
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_capture = cv2.VideoCapture(0)  # Use the webcam

    image_paths = [r"C:\Users\Em_Jayyy\Desktop\BOT\jane.png"]
    names = ["Jane"]

    known_face_encodings, known_names = load_known_faces(image_paths, names)
    recognize_faces(video_capture, known_face_encodings, known_names)
