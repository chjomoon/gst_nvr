# file name :test.py
# pwd : /nms/Node-Media-Server/run.py
from multiprocessing import Process
from flask import Flask, request,render_template, redirect,url_for, jsonify
from flask_cors import CORS
import gst.hls as gst
import datetime, time, os, shutil, sys, requests

app = Flask(__name__)
CORS(app)

isBoot = 0
hash_table =[]

def on_json_loading_failed_return_dict(e):  
    return {}

@app.route('/')
def index():
    return render_template('index.html')
"""
API Sample:
{
	"date" : "20200604",
	"iaddr" : "rtsp://192.168.0.11/profile2/media.smp"
}
"""
#Streaming running based on jsonData from a web server 
def streaming(camera, data):
    global hash_table
    global stream_table
    print('Rec status : %s'%(camera['date']))    
    camProc = gst.StreamRecorder(camera['iaddr'],camera['date'])
    hash_table.append(camProc)       
    camProc.start()
    data['status'] = 1
    data['inserted'] = camProc.register_date
    data['updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['stream_url'] = "http://192.168.0.237:8000/hls/index.m3u8"
    
#Create camera streaming and register camera information
@app.route('/api/camera', methods=['POST'])
def createCamera():
    if request.method == 'POST':
        #get api
        jsonData = request.get_json()
        data ={}
        if jsonData is None:
            print("\n__________No valid data type_________\n")
            data ={}
            data['status'] = 0
            data['inserted'] = ""
            data['updated'] = ""
            data['stream_url'] = ""
            return jsonify(data)
        else:
            
            streaming(jsonData, data)
            print(data)
            return jsonify(data)
    else:
        print("No valid methods received\n")
        data ={}
        data['status'] = 0
        data['inserted'] = ""
        data['updated'] = ""
        data['stream_url'] = ""
        return jsonify(data)

#request entire list of camera to run the flask server
def init_hls():
    data = {}
    jsonData = {
        "date" : datetime.datetime.now().strftime("%Y%m%d"),
        "iaddr" : "rtsp://170.93.143.139:1935/rtplive/0b01b57900060075004d823633235daa" 
        }
    streaming(jsonData,data)
def req():
    global API_HOST
    global API_PATH
    global isBoot
    url = API_HOST + API_PATH
    #request Web server to browse the previous items
    resp = requests.get(url)
    if resp :
        print("API request to %s" %(url))
        jsonData = resp.json()
        data = []
        if jsonData == [] :
            print("Empty List")
            isBoot = 0
            return
        else:
            for camera in jsonData:
                streaming(camera, data)
            isBoot = 1
    else:
        print("Empty List")
        isBoot = 0
    
#Update information based on API from frontend
@app.route('/api/camera', methods=['PUT'])
def setCamera():
    global hash_table
    global rec_table
    #get api
    info = request.get_json()
    data = {}
    if info is not None:
        for camera in hash_table:
            if camera.name == str(info['date']):
                data['status'] = 1
                data['inserted'] = camera.register_date
                data['isRec'] = camera.flag
                print("\n_______camera start time : %s\n" %camera.rec_start.strftime("%H:%M:%S"))
                data['recStartDate'] = camera.rec_start.strftime("%Y%m%d")
                data['recStartTime'] = camera.rec_start.strftime("%H:%M:%S")
                data['recEndTime'] = datetime.datetime.now().strftime("%H:%M:%S")
                data['updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data['stream_url'] = "http://192.168.0.237:8000/hls/index.m3u8"
                data['isRec'] = info['isRec']
                camera.stop()
                camera.terminate()
                data['record_url']="http://192.168.0.237:8000/"+camera.rec_start.strftime("%Y%m%d")+"/index.m3u8"
                hash_table.remove(camera)    
                camProc = gst.StreamRecorder(str(info['iaddr']),str(info['date']))
                hash_table.append(camProc)
                print("\n________camera reload___________\n")
                camProc.start()               
                return jsonify(data)
    else:
        print("Fail to update the camera")
        data['status'] = 0
        data['inserted'] = ""
        data['recStartTime'] = ""
        data['recStartDate'] = datetime.datetime.now().strftime("%Y%m%d")
        data['recEndTime'] = ""
        data['record_url'] = ""
        data['update'] =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['stream_url'] = ""
        data['isRec'] = 0
        
        return jsonify(data)

#While deleting the camera information, the recording files remains 
@app.route('/api/camera/<int:date>', methods=['DELETE'])
def deleteCamera(date=None):
    global hash_table
    global rec_table
    for camera in hash_table:
        if camera.name == str(date):
            print("find the exact camera")
            camera.stop()
            camera.terminate()
            return "1"
    print("Fail to find the camera")
    return "0"

#Check if the server embarks on successfully by returning 1, else return 0
@app.route('/api/boot/end',methods=['GET'])            
def end():
    global isBoot
    if isBoot == 1:
        print("Running Successful")
    else :
        print("Error to run")
    return str(isBoot)

#Main
if __name__ == '__main__':
    """
    if there is a recording preset,
    a module requests webserver to receive API information,
    running a flask server simutaneously 
    """
    """
    #Running all modules
    mainProcs = []
    proc = Process(target = init_hls())
    proc2 = Process(target = app.run(host='0.0.0.0', port=5000, debug=True))

    mainProcs.append(proc)
    mainProcs.append(proc2)
    
    proc.start()
    proc2.start()

    for proc in mainProcs:
        proc.join()
    """
    app.run(host='0.0.0.0', port=5000, debug=True)

