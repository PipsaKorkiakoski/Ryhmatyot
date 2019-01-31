import serial


class SerialRead:

    port_gps = None
    port_acc = None
    line = None
    status = None
    latitude = None
    longitude = None
    speed = None
    direction = None
    data_received = False
    mode = "dd"

    #"/dev/ttyUSB0" USB port name for serial connection
    # "/dev/ttyUSB1" USB port name for serial connection

    def __init__(self):
        self.port_gps = serial.Serial("COM13",9600)
        self.port_acc = serial.Serial("COM11",9600)
        super(SerialRead, self).__init__()

    def read_port(self):
        if self.port_gps.in_waiting !=0 and self.port_gps.is_open:
            self.line = self.port_gps.readline(63)
        if self.line[0] == 86: #86 = V in ASCII
            self.get_data_from_acc()

    def modify_to_dms(self):
        for i in range(7, 8):
            self.latitude += str().join(chr(self.line[i]))
            self.latitude += "°"
        for i in range(9, 10):
            self.latitude += str().join(chr(self.line[i]))
            self.latitude += "'"
        for i in range(12, 13):
            self.latitude += str().join(chr(self.line[i]))
            self.latitude += "."
        for i in range(14, 15):
            self.latitude += str().join(chr(self.line[i]))
            self.latitude += "\""
            self.latitude += str().join(chr(self.line[16]))

        for i in range(24, 26):
            self.longitude += str().join(chr(self.line[i]))
            self.longitude += "°"
        for i in range(27, 28):
            self.longitude += str().join(chr(self.line[i]))
            self.longitude += "'"
        for i in range(30, 31):
            self.longitude += str().join(chr(self.line[i]))
            self.longitude += "."
        for i in range(32, 33):
            self.longitude += str().join(chr(self.line[i]))
            self.longitude += "\""
            self.longitude += str().join(chr(self.line[34]))

    def modify_to_dd(self):
        if self.line[16] == 78:  # 78 = N in ASCII
            for i in range(7, 16):
                self.latitude += str().join(chr(self.line[i]))
        elif self.line[16] == 83:  # 83 = S in ASCII
            self.latitude = "-"
            for i in range(7, 16):
                self.latitude += str().join(chr(self.line[i]))

        if self.line[34] == 69:  # 69 = E in ASCII
            for i in range(24, 34):
                self.longitude += str().join(chr(self.line[i]))
        elif self.line[34] == 87:  # 87 = W in ASCII
            self.longitude = "-"
            for i in range(24, 34):
                self.longitude += str().join(chr(self.line[i]))

    def pick_values_from_line(self):
        if self.line is not None:
            self.status = self.line[0]
            self.latitude = " "
            self.longitude = " "
            if self.mode is "dd":
                self.modify_to_dd()
            elif self.mode is "dms":
                self.modify_to_dms()
            self.speed = " "
            for i in range(42, 46):
                self.speed += str().join(chr(self.line[i]))
            self.direction = " "
            for i in range(58, 62):
                self.direction += str().join(chr(self.line[i]))

    def get_data_from_acc(self):
        if self.port_acc.isOpen() is not True:
            self.port_acc.open()
        if self.port_acc.writable():
            self.port_acc.write(self.latitude + "," + self.longitude + "," + self.speed + "," + self.direction) #Syötetään parametrit Nucleolle
        while self.data_received is False: #Ohjelma jää odottamaan tuloksia
            if self.port_acc.inWaiting() > 0: #Tulokset ovat saapuneet :)
                self.line = self.port_acc.readline(63)
                self.data_received = True
        self.data_received = False


def main():
    serial_reader = SerialRead()
    while 1:
        serial_reader.read_port()
        serial_reader.pick_values_from_line()
        if serial_reader.line is not None:
            print("%s", serial_reader.line)
            print("%c" % serial_reader.status)
            print("%s" % serial_reader.latitude)
            print("%s" % serial_reader.longitude)
            print("%s" % serial_reader.speed)


main()
