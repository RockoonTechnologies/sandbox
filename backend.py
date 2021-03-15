
from PIL import Image

import pytesseract
import pafy
import cv2

import threading
import time


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


cache = {
    "delay": 500,
    "data": {}
}

def getEvents():
    totalEvents = []
    totalEvents.extend(cache["data"])
    return totalEvents

def parsePadre(data):
    events = []

    lines = data.split("\n")
    #lines.pop(lines.index("Road Open"))
    lines.pop(lines.index("LIVE STATUS"))
    for item in lines:
        try:
            float(item[0])
            continue
        except:
            pass

        if not item:
            continue

        splitted = item.split(" ")
        if len(splitted) <= 1:
            continue


        if splitted[0] == "v":
            name = " ".join(splitted[1:])
            if name == "":
                continue
            events.append({
                "StarShipEvent": {
                    "name": name,
                    "completed": True,
                    "time": None
                }
            })
        else:
            name = " ".join(splitted[0:])
            if name == "":
                continue
            events.append({
                "StarShipEvent": {
                    "name": name,
                    "completed": False,
                    "time": None
                }
            })

    return events


def backgroundUpdate():
    while True:
        #updates padre info
        url = "https://www.youtube.com/watch?v=sTA0GTgFn5E"
        video = pafy.new(url)
        best = video.getbest(preftype="mp4")

        capture = cv2.VideoCapture(best.url)
        grabbed, frame = capture.read()
        frame = frame[10:350,10:160]
        cv2.imwrite("a.png", frame)
        string = pytesseract.image_to_string(Image.open('a.png'))
        rep = parsePadre(string)
        cache["data"] = rep

        print("updated events")
        time.sleep(cache["delay"])




threading.Thread(target=backgroundUpdate).start()