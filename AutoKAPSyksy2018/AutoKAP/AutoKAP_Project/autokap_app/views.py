import threading
import time

from django.shortcuts import render
from django.template import loader

from .models import SerialRead

serial_reader = SerialRead()
ser_read = None
latitude = "64.999"
longitude = "25.510"
speed = "0.0"
interval = 1
last_time = 0
lat_file = None
lon_file = None
spd_file = None
coordinates_file = None
coordinates = None


def start_thread():
    threading.Thread(target=loop).start()


def loop():
    global last_time, lat_file, lon_file, spd_file, latitude, longitude, speed
    while 1:
        if last_time + interval < time.time():
            ser_read.latitude = serial_reader.get_latitude()
            ser_read.longitude = serial_reader.get_longitude()
            ser_read.speed = serial_reader.get_speed()
            ser_read.save()

            last_time = time.time()
            lat_file = open("latFile.txt", 'w')
            lon_file = open("lonFile.txt", 'w')
            spd_file = open("spdFile.txt", 'w')
            latitude = serial_reader.get_latitude()
            longitude = serial_reader.get_longitude()
            speed = serial_reader.get_speed()

            lat_file.writelines(str(latitude))
            lon_file.writelines(str(longitude))
            spd_file.writelines(str(speed))
            lat_file.close()
            lon_file.close()
            spd_file.close()


def index(request):
    serialreader_list = SerialRead.objects.order_by('id')[:1]

    context = {
        'serialreader_list': serialreader_list,
    }
    return render(request, 'autokap_app/index.html', context)


def mapView(request, serialreader_id):
    global ser_read
    try:
        ser_read = SerialRead.objects.get(pk=serialreader_id)
        ser_read.latitude = serial_reader.get_latitude()
        ser_read.longitude = serial_reader.get_longitude()
        ser_read.speed = serial_reader.get_speed()
        ser_read.save()
        start_thread()
    except SerialRead.DoesNotExist:
        raise Http404("SerialRead does not exist")

    return render(request,'autokap_app/mapView.html', {'serialreader':ser_read})
