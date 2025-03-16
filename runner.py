import cv2
import decoder

cap = cv2.VideoCapture(1)
detector = cv2.QRCodeDetector()

first_run = True

while True :
  decoder.run(False, first_run, cap, detector)
  first_run = False