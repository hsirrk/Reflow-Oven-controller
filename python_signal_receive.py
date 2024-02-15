import time
import serial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys, time, math
from playsound import playsound
import socket

xsize=500
y_list=[]
# configure the serial port

# Connect to microcontroller server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('', 8080))

ser = serial.Serial(
    port='COM4',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS
)
ser.isOpen()

last_val = None  # Initialize a variable to store the last value
color = 'red'
temp_type = 'Celcius'
state0flag = 0
state1flag = 0
state2flag = 0
state3flag = 0
state4flag = 0
title = 'Reflow Oven'


def serial_read(ser):
    global last_val, color, temp_type, title  # Use the global variable to keep track across function calls
    while 1:
        strin = ser.readline()
        strin = strin.rstrip()
        strin = strin.decode()
        current_val = float(strin)  # Convert the current string to float
        # Send request for temperature reading
        client_socket.send(b'TEMP')

        # Receive response
        response = client_socket.recv(1024)
        print(response.decode())

        # Close connection
        client_socket.close()


        if current_val >= 300:
            temp = current_val
            current_val = last_val
            if temp == 300:
                color = 'red'
                title = 'Ramp to Soak'
            elif temp == 301:
                color = 'orange'
                title = 'Soak'
            elif temp == 302:
                color = 'yellow'
                title = 'Ramp to Reflow'
            elif temp == 303:
                color = 'green'
                title = 'Reflow'
            elif temp == 304:
                color == 'blue'
                title = 'Cooling'
            
        
        # Check and print the trend
        if last_val is not None:  # Ensure last_val has been set at least once
            if current_val > last_val:
                print("Temperature is increasing")
            elif current_val < last_val:
                print("Temperature is decreasing")

            # If current_val == last_val, do nothing (temperature is stable)
        
        last_val = current_val  # Update last_val for the next iteration
        yield current_val

def data_gen():
    t = data_gen.t
    while True:
        t+=0.5
        val= next(serial_read(ser))
        yield t, val
        
def run(data):
    # update the data
    t,y = data
    if t>-1:
        xdata.append(t)
        ydata.append(y)
        if t>xsize: # Scroll to the left.
            ax.set_xlim(t-xsize, t)
        line.set_data(xdata, ydata)
        line.set_color(color)
        
        ax.set_ylabel(temp_type)
        ax.set_title(title)
        fig.canvas.draw_idle()
        latest_temp_text.set_text(f'Latest Temp: {y:.2f} {temp_type}')
    return line,latest_temp_text

def on_close_figure(event):
    sys.exit(0)

data_gen.t = -1
fig = plt.figure()
fig.canvas.mpl_connect('close_event', on_close_figure)
ax = fig.add_subplot(111)
line, = ax.plot([], [], lw=2, color = color)
ax.set_ylim(0, 300)
ax.set_xlim(0, xsize)
ax.grid()
xdata, ydata = [], []
ax.set_xlabel('Time (s)')
ax.set_ylabel(temp_type)
ax.set_title(title)
latest_temp_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, verticalalignment='top')

# Important: Although blit=True makes graphing faster, we need blit=False to prevent
# spurious lines to appear when resizing the stripchart.
ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=100,repeat=False)
plt.show()



