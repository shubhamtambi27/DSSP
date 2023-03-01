import cv2
import os
import numpy as np
from PIL import Image
import sqlite3


def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


def generate_dataset():
    # Starting the web cam by invoking the VideoCapture method
    vid_cam = cv2.VideoCapture(0)
    # For detecting the faces in each frame we will use Haarcascade Frontal Face default classifier of OpenCV
    face_detector = cv2.CascadeClassifier('https://drive.google.com/file/d/1km8Z1IUVNakPeDooJ6_efa8js1P9xCKg/view?usp=share_link')
    # Set unique id for each individual person
    face_id =int(input()) #Attach DaTABASE here
    # Variable for counting the no. of images
    count = 0
    #checking existence of path
    assure_path_exists("https://drive.google.com/drive/u/0/folders/1iXFF5m9rIJyvcCH-3hsRhjjRmLqTgDAs/")
    
    while(True):
        # Capturing each video frame from the webcam
        _, image_frame = vid_cam.read()
        # Converting each frame to grayscale image
        gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
        # Detecting different faces
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
         # Looping through all the detected faces in the frame
        for (x,y,w,h) in faces:
            # Crop the image frame into rectangle
            cv2.rectangle(image_frame, (x,y), (x+w,y+h), (255,0,0), 2)
            # Increasing the no. of images by 1 since frame we captured
            count += 1
             # Saving the captured image into the training_data folder
            cv2.imwrite("https://drive.google.com/drive/u/0/folders/1iXFF5m9rIJyvcCH-3hsRhjjRmLqTgDAs/Person." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
            # Displaying the frame with rectangular bounded box
            cv2.imshow('frame', image_frame)
        # press 'q' for at least 100ms to stop this capturing process
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
         #We are taking 100 images for each person for the training data
         # If image taken reach 100, stop taking video
        elif count>100:
            break
    
    vid_cam.release()
    cv2.destroyAllWindows()




def model_training():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("https://drive.google.com/file/d/1km8Z1IUVNakPeDooJ6_efa8js1P9xCKg/view?usp=share_link");
    faces,ids = getImagesAndLabels('https://drive.google.com/drive/u/0/folders/1iXFF5m9rIJyvcCH-3hsRhjjRmLqTgDAs')
    # Training the model using the faces and IDs
    recognizer.train(faces, np.array(ids))
    # Saving the model into s_model.yml
    assure_path_exists('https://drive.google.com/drive/u/0/folders/1PzsXiVSwubGzqX-gvZQIK9_y08lTqOoz/')
    recognizer.write('https://drive.google.com/drive/u/0/folders/1PzsXiVSwubGzqX-gvZQIK9_y08lTqOoz/s_model.yml')






def face_recognition():
    # Create Local Binary Patterns Histograms for face recognization
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    assure_path_exists("https://drive.google.com/drive/u/0/folders/1PzsXiVSwubGzqX-gvZQIK9_y08lTqOoz/")
    # Load the  saved pre trained mode
    recognizer.read('https://drive.google.com/drive/u/0/folders/1PzsXiVSwubGzqX-gvZQIK9_y08lTqOoz/s_model.yml')
    # Load prebuilt classifier for Frontal Face detection
    cascadePath = "https://drive.google.com/file/d/1km8Z1IUVNakPeDooJ6_efa8js1P9xCKg/view?usp=share_link"
    # Create classifier from prebuilt model
    faceCascade = cv2.CascadeClassifier(cascadePath);
    # font style
    font = cv2.FONT_HERSHEY_SIMPLEX
    # Initialize and start the video frame capture from webcam
    cam = cv2.VideoCapture(0)
    # Looping starts here
    while True:
      # Read the video frame
      ret, im =cam.read()
      # Convert the captured frame into grayscale
      gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
      # Getting all faces from the video frame
      faces = faceCascade.detectMultiScale(gray, 1.2,5) #default
      for(x,y,w,h) in faces:
        # Create rectangle around the face
        cv2.rectangle(im, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 4)
        # Recognize the face belongs to which ID
        Id, confidence = recognizer.predict(gray[y:y+h,x:x+w])  #Our trained model is working here
        # Set the name according to id

        #Use Database
        if Id == 1:
            Id = "Shubham {0:.2f}%".format(round(100 - confidence, 2))
            # Put text describe who is in the picture
        elif Id == 2 :
            Id = "Suchi {0:.2f}%".format(round(100 - confidence, 2))
            # Put text describe who is in the picture
        elif Id == 45:
            Id = "Shubham Tambi {0:.2f}%".format(round(100 - confidence, 2))
        elif Id == 160:
            Id = "Shruti Choudhary {0:.2f}%".format(round(100 - confidence, 2))
        else:
            pass

        # Set rectangle around face and name of the person
        cv2.rectangle(im, (x-22,y-90), (x+w+22, y-22), (0,255,0), -1)
        cv2.putText(im, str(Id), (x,y-40), font, 1, (255,255,255), 3)
      # Display the video frame with the bounded rectangle
      cv2.imshow('im',im) 
      # press q to close the program
      if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    # Terminate video
    cam.release()
    # Close all windows
    cv2.destroyAllWindows()








def getImagesAndLabels(path):
    # Getting all file paths
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]    
    #empty face sample initialised
    faceSamples=[]    
    # IDS for each individual
    ids = []
    # Looping through all the file path
    for imagePath in imagePaths:
        # converting image to grayscale
        PIL_img = Image.open(imagePath).convert('L')
        # converting PIL image to numpy array using array() method of numpy
        img_numpy = np.array(PIL_img,'uint8')
        # Getting the image id
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        # Getting the face from the training images
        faces = detector.detectMultiScale(img_numpy)
        # Looping for each face and appending it to their respective IDs
        for (x,y,w,h) in faces:
            # Add the image to face samples
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            # Add the ID to IDs
            ids.append(id)
    # Passing the face array and IDs array
    return faceSamples,ids


generate_dataset()
#model_training()
#face_recognition()