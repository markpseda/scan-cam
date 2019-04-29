from guizero import App, Text, PushButton, Slider, TextBox
import serial
import pynmea2
import requests
from PIL import Image
from google.cloud import firestore
from google.cloud import storage
import google.oauth2.credentials

storage_client = storage.Client.from_service_account_json('service_account.json')
db = firestore.Client.from_service_account_json('service_account.json')
doc_ref = db.collection(u'uploads')
bucket = storage_client.get_bucket('ud-senior-design-2018-scan-cam.appspot.com')

from time import sleep
# from picamera import PiCamera
from datetime import datetime
import time
# camera = PiCamera()
# camera.resolution = (1024, 768)

# URL to make POST request to: https://us-central1-ud-senior-design-2018-scan-cam.cloudfunctions.net/uploadData

# Website URL: https://ud-senior-design-2018-scan-cam.firebaseapp.com/
test_url='https://webhook.site/c1432c3c-805f-4a82-b470-e6103195a0ac'
prod_url='ud-senior-design-2018-scan-cam.appspot.com'

#GPS BLOCK
#--------------------------------------------
gps = serial.Serial("/dev/ttyUSB0", baudrate=4800, timeout=1)
lat='0'
long='0'
gpsCoords = lat+', '+long


def get_gps():
    line=gps.readline()
    if line.startswith( '$GPGGA'.encode('utf-8') ) :
        msg =pynmea2.parse(line.decode("utf-8"))
        lat = str(msg.latitude)
        long = str(msg.longitude)
        global gpsCoords
        gpsCoords = lat+', '+long
        print("Latitude: "+lat+"\n"+"Longitude: "+long)

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
    timestamp =time.time()

    licensePlateNum = datetime.now()
    message.value = "Recording Now"
    message.text_color ='red'
    flagbutton.visible=True
    stoprecordbutton.visible=True
    startrecordbutton.visible=False
    # app.repeat(1000, pic_func)
    app.repeat(1000,get_gps)


def flag_func():
    #response = requests.post('h    ttps://us-central1-ud-senior-design-2018-scan-cam.cloudfunctions.net/uploadData', json={'timestamp': str(timestamp),'license_number': str(licensePlateNum),'gps_coords': gpsCoords})
    global gpsCoords
    new_doc = doc_ref.document()    
    new_doc.set({
        u'timestamp' : timestamp,
        u'gps_coords' : gps_coords,
        u'imageRef' : imageRef,
        u'license_number' : license_number
    })

    f.close()

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
flagbutton = PushButton(app, command=flag_func, text='Post', visible=False, height='fill',width='fill', align='right')
flagbutton.bg ='white'

stoprecordbutton = PushButton(app, command=stop_func, text='Stop Recording', height='fill',width='fill', align='left', visible=False)
stoprecordbutton.bg ='lavender'

#slider1 = Slider(app, command=slider1_changed, align='bottom')
#textbox1 = TextBox(app, align='bottom')

#slider2 = Slider(app, command=slider2_changed, align='bottom')
#textbox2 = TextBox(app, align='bottom')
app.display()
