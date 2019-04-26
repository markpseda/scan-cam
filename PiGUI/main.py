from guizero import App, Text, PushButton, Slider, TextBox
import structure
import serial
import pynmea2

from time import sleep
from picamera import PiCamera
from datetime import datetime
camera = PiCamera()
camera.resolution = (1024, 768)

# URL to make POST request to: https://us-central1-ud-senior-design-2018-scan-cam.cloudfunctions.net/uploadData

# Website URL: https://ud-senior-design-2018-scan-cam.firebaseapp.com/


#GPS BLOCK
#--------------------------------------------
gps = serial.Serial("/dev/ttyUSB0", baudrate=4800, timeout=1)
lat=''
long=''


def get_gps():
    line=gps.readline()
    if line.startswith( '$GPGGA'.encode('utf-8') ) :
        msg =pynmea2.parse(line.decode("utf-8"))
        print("Latitude: "+str(msg.latitude)+"\n"+"Longitude: "+str(msg.longitude))

       #lat, _, lon = line.strip().split(',')[2:5]
    msg =pynmea2.parse(line.decode("utf-8"))
    #print(str(msg))
#--------------------------------------------------

def stop_func():
    message.text_color ='white'
    message.value="Scan Cam Application GUI"
    stoprecordbutton.visible=False
    startrecordbutton.visible=True
    flagbutton.visible=False
    app.cancel(pic_func)
    app.cancel(get_gps)

def rec_func():
    message.value = "Recording Now"
    message.text_color ='red'
    flagbutton.visible=True
    stoprecordbutton.visible=True
    startrecordbutton.visible=False
    # app.repeat(1000, pic_func)
    # app.repeat(10,get_gps)


def flag_func():
    message2 =Text(app,text='flaggin placeholder', text_color='white')


def pic_func():
    get_gps()
    imglabel=str(datetime.now())+'.jpg'
    camera.capture('Images/'+imglabel);

def slider1_changed(slider_value):
    textbox1.value = slider_value
def slider2_changed(slider_value):
    textbox2.value = slider_value

app = App(title="Scan Cam", bg = 'black')
#Uncomment Before Deployment
#app.tk.attributes("-fullscreen",True)
#run 'chown root main.py' before deployment


message = Text(app, text='Scan Cam Application GUI')
message.text_color ='white'

startrecordbutton = PushButton(app, command=rec_func, text='Start Recording', height='fill',width='fill', align='left')
startrecordbutton.bg ='dark slate blue'
flagbutton = PushButton(app, command=flag_func, text='Flag', visible=False, height='fill',width='fill', align='right')
flagbutton.bg ='white'

stoprecordbutton = PushButton(app, command=stop_func, text='Stop Recording', height='fill',width='fill', align='left', visible=False)
stoprecordbutton.bg ='lavender'

#slider1 = Slider(app, command=slider1_changed, align='bottom')
#textbox1 = TextBox(app, align='bottom')

#slider2 = Slider(app, command=slider2_changed, align='bottom')
#textbox2 = TextBox(app, align='bottom')
app.display()
