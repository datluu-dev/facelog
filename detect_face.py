from imutils.video import WebcamVideoStream
from datetime import date, datetime
from db import FacelogDbManager
from threading import Thread
from pathlib import Path

import numpy as np 
import imutils 
import cv2
import time
import yaml
import sys


prototxt_file = 'models/deploy.prototxt.txt'
model = 'models/res10_300x300_ssd_iter_140000.caffemodel'
confidence = 0.7
net = cv2.dnn.readNetFromCaffe(prototxt_file, model)

def handle_frame(frame, thresh_hold, size=(300, 300)):
	today_date = date.today().strftime("%b-%d-%Y")
	Path(f'static/img/{today_date}').mkdir(parents=True, exist_ok=True)

	frame = imutils.resize(frame, width=400)
	h, w = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, size), 1.0,
		size, (104, 177, 123))
	
	net.setInput(blob)
	detections = net.forward()

	# img_name = path.split("/")[-1].split(".")[0]

	for i in range(detections.shape[2]):
		confidence = detections[0, 0, i, 2]

		# By pass the detection if the range of confidence is not enough
		if confidence < thresh_hold: 
			# print(confidence)
			continue

		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		startX, startY, endX, endY = box.astype("int")

		roi = frame[startY:endY, startX:endX]
		roi = imutils.resize(roi, width=256)
		roi = imutils.resize(roi, height=256)

		dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		img_name = int(datetime.now().timestamp())
		outpath = f'static/img/{today_date}/{img_name}.jpg'
		outpath_db = f'img/{today_date}/{img_name}.jpg' 

		# thread_write_db = Thread(target=write_db, args=(outpath, dt_string, "database/facelog-test.db", ))
		thread_write_db = Thread(target=write_db, args=(outpath_db, dt_string, "database/facelog.db", ))
		thread_write_db.start()
		thread_write_db.join()

		cv2.imwrite(outpath, roi)
		print("Detect face, done writing")

def write_db(outpath, dt_string, database_path="database/facelog.db"):
	db = FacelogDbManager(database_path)
	db.open(database_path)

	db.create_data_table()
	db.insert_to_db(table="FaceData", data=(dt_string, outpath), columns=("datetime, path"))
	db.close()

def start_detect(src_arg=0):
	print("Start detecting")
	vs = WebcamVideoStream(src=src_arg).start()
	time.sleep(2)
	trigger = True
	while True:
		frame = vs.read()
		handle_frame(frame, confidence)
		time.sleep(5)

if __name__ == '__main__':
	Path('static/img').mkdir(parents=True, exist_ok=True)
	with open("camera_info.yaml", "r") as f:
		try:
			data = yaml.safe_load(f)
			cam_info = data['cam_info']
		except yaml.YAMLError as exc:
			# print(exc)
			# sys.exit()
			cam_info = 0
	start_detect(cam_info) 









