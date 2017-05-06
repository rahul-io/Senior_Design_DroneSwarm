from uwb import uwb
import time

radio = uwb(a=248, port='/dev/tty.usbmodem1411')
filename1 = "uwb_raw_data" + time.strftime("%m_%d_%H%M") + ".txt"
filename2 = "uwb_filtered_data" + time.strftime("%m_%d_%H%M") + ".txt"
pos_file = open(filename1, 'w+')
corr_file = open(filename2, 'w+')
pos_file.truncate
corr_file.truncate

t_end = time.time() + (60*5)
while time.time() < t_end:
    rawheight = radio.getRawDist()
    height = radio.range(corr_file)
    pos_file.write(str(rawheight) + "\n")

pos_file.close()
corr_file.close()

# print("--- %s seconds ---" % (time.time() - start_time))
