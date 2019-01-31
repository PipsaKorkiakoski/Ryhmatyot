import serial
import threading
from django.db import models


class SerialRead(models.Model):
    port_gps = None
    port_acc = None
    line = None
    previousLine = None
    status = None
    latitude = models.CharField(max_length=30, default=0)
    longitude = models.CharField(max_length=30, default=0)
    speed = models.CharField(max_length=30, default=0)
    direction = None
    data_received = False
    buf = ""

    def __init__(self, *args):
        super(SerialRead, self).__init__(*args)

    def __str__(self):
        return "SerialReader1"

    def read_port(self):
        if self.port_acc is None:
            self.port_acc = serial.Serial("/dev/ttyACM1", 9600)
        if self.port_gps is None:
            self.port_gps = serial.Serial("/dev/ttyACM0", 9600)
        if self.port_gps.is_open and self.port_gps.inWaiting() != 0:
            if self.line is not None:
                self.previousLine = self.line
            self.line = self.port_gps.readline(35)
            self.port_gps.flush()
        if self.line is not None:
            if self.line[0] == 86:
                self.get_data_from_acc()
            self.pick_values_from_line()

    def pick_values_from_line(self):
        #if self.line is not None:
        self.status = chr(self.line[0])
        self.get_field(1)
        self.latitude = self.buf
        self.get_field(2)
        self.longitude = self.buf
        self.get_field(3)
        self.speed = self.buf
        self.get_field(4)
        self.direction = self.buf

    def get_field(self, index):
        line_pos = 0
        field_pos = 0
        comma_count = 0
        self.buf = ""
        while line_pos < len(self.line):
            if self.line[line_pos] is 44:
                comma_count += 1
            if comma_count is index and self.line[line_pos] is not 44:
                self.buf = self.buf + chr(self.line[line_pos])
                field_pos += 1
            line_pos += 1

    def get_latitude(self):
        self.read_port()
        return self.latitude

    def get_longitude(self):
        self.read_port()
        return self.longitude

    def get_speed(self):
        self.read_port()
        return self.speed

    def get_data_from_acc(self):
        if self.port_acc.isOpen() is not True:
            self.port_acc.open()
        if self.port_acc.writable():
            print("Haetaan rivi acc:lta")
            counter = 0
            send_line = self.previousLine
            while len(send_line) < 35:
                temp_line = send_line + b"0"
                send_line = temp_line
            self.port_acc.write(send_line) #Syötetään parametrit Nucleolle
            while self.data_received is False or counter is 50: #Ohjelma jää odottamaan tuloksia
                counter += 1
                if self.port_acc.inWaiting() > 35: #Tulokset ovat saapuneet :)
                    self.line = self.port_acc.readline(37)
                    if self.port_acc.inWaiting() > 0:
                        self.port_acc.readline(50)
                    self.port_acc.flush()
                    self.data_received = True
                    print(self.line)
                if counter is 50:
                    print("Ei saatu dataa")
                    self.line = self.previousLine
            self.data_received = False

