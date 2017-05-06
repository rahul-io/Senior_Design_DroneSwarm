import serial
import math


class uwb:

    def __init__(self, a=10000, port='/dev/ttyACM0', mybaud=9600):
        self._n = 0
        self._x = []
        self._y = []
        self._anchor1 = 0
        self._anchor2 = 0
        self._ser = serial.Serial(port, baudrate=mybaud)
        self._distance = a
        self._buffer = ''

    def _getRawDist(self):
        while True:
            if '\n' in self._buffer:
                break
            else:
                self._buffer += self._ser.read(self._ser.inWaiting())

        line, self._buffer = self._buffer.split('\n')[-2:]
        # line = self._ser.readline()
        if line[:2] == 'mr':
            self._getRawDist()
        else:
            self._anchor1 = int(line[6:14], 16)/10
            self._anchor2 = int(line[15:23], 16)/10
            height = (math.pow(self._anchor1, 2)-math.pow(self._anchor2, 2) +
                      math.pow(self._distance, 2))/(2*self._distance)
            return height

    def range(self, textfile, rawfile, serverSocket, host, port):
        while True:
            n = self._n
            x = self._x
            y = self._y
            x.append(self._getRawDist())
            a = [1, -2.0651, 1.5200, -0.3861]
            b = [0.0086, 0.0258, 0.0258, 0.0086]
            if n >= 3:
                y.append(b[0]*x[n] + b[1]*x[n-1] + b[2]*x[n-2] + b[3]*x[n-3] -
                         a[1]*y[n-1] - a[2]*y[n-2] - a[3]*y[n-3])
            else:
                y.append(x[n])
            print y[n]
            n = n+1
            self._n = n
            self._x = x
            self._y = y

            rawfile.write(str(x[-1]) + '\n')
            print "Raw: " + str(self._x)
            textfile.write(str(y[-1]) + '\n')
            print "Filtered: " + str(self._y)
            serverSocket.sendto((str(y[-1]) + '\n'), (host, port))

    def getRange(self):
        return self._y[-1]
