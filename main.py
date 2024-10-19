import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller
import time

# Initialisation de la webcam
cap = cv2.VideoCapture(0)
cap.set(3, 720)  # Largeur de l'image
cap.set(4, 420)  # Hauteur de l'image

# Initialisation du détecteur de mains
detector = HandDetector(detectionCon=0.7, maxHands=1)
keyboard = Controller()

# Variable pour stocker l'état précédent des touches
previous_key_state = None

while True:
    # Capture de l'image
    _, img = cap.read()
    hands, img = detector.findHands(img)
    
    if hands:
        fingers = detector.fingersUp(hands[0])  # Vérifie quels doigts sont levés
        
        # Vérifie si la main est à plat
        if fingers == [0, 0, 0, 0, 0]:
            if previous_key_state != "left":
                keyboard.press(Key.left)
                keyboard.release(Key.right)
                print("Pressing LEFT")
                previous_key_state = "left"
        # Vérifie si tous les doigts sont levés
        elif fingers == [1, 1, 1, 1, 1]:
            if previous_key_state != "right":
                keyboard.press(Key.right)
                keyboard.release(Key.left)
                print("Pressing RIGHT")
                previous_key_state = "right"
        # Si aucun geste n'est détecté, relâche les touches
        else:
            if previous_key_state != None:
                keyboard.release(Key.left)
                keyboard.release(Key.right)
                print("Releasing keys")
                previous_key_state = None
    else:
        keyboard.release(Key.left)
        keyboard.release(Key.right)
        print("Releasing keys")
        previous_key_state = None

    # Affiche l'image
    cv2.imshow("Let's Play", img)

    # Quitter le programme avec le geste de fermeture de main
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()  # Libère la webcam
cv2.destroyAllWindows()  # Ferme toutes les fenêtres
