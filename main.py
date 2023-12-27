import threading
import cv2
import io
import time
import serial

from flask import Flask, send_file, request, session, redirect, url_for
from werkzeug.datastructures import ImmutableMultiDict
ser = serial.Serial('/dev/ttyAMA0', 9600)

app = Flask(__name__)

@app.route('/status')
def test():
	received_data = '0'  
	#print(ser.in_waiting)
	#try:
	if (ser.in_waiting>0):
		received_data = ser.readline().decode().strip()  # Đọc dữ liệu từ UART
	#except Exception as e:
	#	print("Không thể đọc dữ liệu từ UART:", str(e))
    
	print(received_data)
	return f'{received_data}'
    
@app.route('/data_control', methods=['POST', 'GET'])
def handle_request():
	
	if request.method == 'POST':
		data = request.form.to_dict() # Dữ liệu POST được gửi đến
		
		keys = list(data.keys())  # Lấy danh sách các khóa (keys) trong từ điển
		values = list(data.values())  # Lấy danh sách các giá trị (values) trong từ điển

		#cmdSpeed = values[0]
		#cmdControl = values[1]
		direction = values[0]
		
		
		print("===>> DIRECTION:  ", direction)
		
		string1 = direction + '\b'
		ser.write(string1.encode())
		ser.flush()
		
		
		#if (ser.in_waiting>0):
		#	string1 = cmdControl + '\r'
		#	ser.write(string1.encode())
		#	ser.flush()
		#else:
		#	print('===> Error')

		return 'Dữ liệu đã được nhận và xử lý thành công!'
		
	elif request.method == 'GET':
        # Xử lý yêu cầu GET ở đây
        # ...

		return 'Yêu cầu GET đã được xử lý!'

		
@app.route('/data_img')
def read_data_img():
	
	cap = cv2.VideoCapture(0)

	ret, frame = cap.read()
	 
	if ret:
		# Chuyển đổi hình ảnh thành dữ liệu JPEG
		_, jpeg_image = cv2.imencode('.jpg', frame)

		# Chuyển đổi dữ liệu thành mảng byte
		#image_data = jpeg_image.tobytes()
		image_stream = io.BytesIO(jpeg_image)

		# Trả về tệp hình ảnh cho người dùng
		return send_file(image_stream, mimetype='image/jpeg')
		

	return 'Unable to capture image'


if __name__ == '__main__':
	
    app.run(host='0.0.0.0', debug=True, threaded=True)
    
    print("-------------------")

