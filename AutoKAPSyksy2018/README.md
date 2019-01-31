# AutoKAP
Auto, kamera, gps, kiihtyvyys, nopeus, matka


AutoKAP will be a navigation software for vehicles. Vehicle position is shown on a map. A microcontroller is used to read gps coordinates and send it over serial to server. Another microcontroller is used to calculate gps position from accelerometer and gyroscope data. This data is used for vehicle positioning if GPS data from module is not available, for example in tunnels. A camera is used with OpenCV to automatically detect speed limit signs. Speed limit is overlayed on video stream from the camera.
All of this is built into a Django web app which is run on a Raspberry Pi.
Hardware used: Two nucleo f303re microcontrollers and a Raspberry Pi, Raspberry pi camera, GPS module, GY-50 accelerometer and GY-61 gyroscope.
Software used: Python, OpenCV, Django, Google Maps API
