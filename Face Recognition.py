import cv2
import pyautogui as p

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

font = cv2.FONT_HERSHEY_SIMPLEX

id = 2

names = ['', 'Alamdaar']

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 740)
cam.set(4, 580)

minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

def Unlock():
    cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
    cv2.putText(img, str(accuracy), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
    cv2.imshow('camera', img)
    p.press('esc')
    print('Verification Successful.')


def Lock():
    cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
    cv2.putText(img, str(accuracy), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
    cv2.imshow('camera', img)
    p.press('esc')
    print('User Authentication Failed.')


while True:

    ret, img = cam.read()

    converted_image = cv2.cvtColor(img,
                                   cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        converted_image,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )

    for (x, y, w, h) in faces:

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        id, accuracy = recognizer.predict(converted_image[y:y + h, x:x + w])

        # Check if accuracy is less them 100 ==> "0" is perfect match
        if (accuracy < 60):
            id = names[id]
            accuracy = "  {0}%".format(round(100 - accuracy))
            Unlock()
            print('Welcome ',id)
            break

        else:
            id = "Unknown"
            accuracy = "  {0}%".format(round(100 - accuracy))
            Lock()
            break

        cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, str(accuracy), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

    cv2.imshow('camera', img)

    k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
    if k == 27:
        break

print("Thanks for using this program, have a good day.")
cam.release()
cv2.destroyAllWindows()