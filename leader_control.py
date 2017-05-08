from uwb import uwb
from serversocket import serversocket

host = "192.168.1.106"
port = 5454

print "Initializing UWB radio."
radio = uwb(a=2000, port='/dev/ttyACM0')  # UWB init
server = serversocket(host, port)
radiothread = threading.Thread(target=radio.range,
                               args=(uwb_file, uwb_raw, server))
radiothread.start()
