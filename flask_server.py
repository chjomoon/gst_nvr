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
#basic get
@app.route('/', methods=['GET'])
def hello_world():
	return "Hello World"

#onvif control API
@app.route('/api/camera/ptz', methods=['PUT'])
def ptz():
    json = request.get_json()
    print("received direction________:\n" ,json['direction'])
    ptz_controller.media_profile_configuration(json['direction'])
    return "true"

@app.route('/api/camera/info', methods=['POST'])
def get_info():
    json = request.get_json()
    data = {}
    if json is not None:
        #Create the media service
        mycam = ONVIFCamera(json['iaddr'],json['port'],json['id'],json['passwd'])
        media_service = mycam.create_media_service()
        #Get the target profile
        media_profile = media_service.GetProfiles()[0]
        #Get the information that needed
        data['model'] =  mycam.devicemgmt.GetDeviceInformation()["Model"]
        data['MAC_addr'] = mycam.devicemgmt.GetNetworkInterfaces()[0]["Info"]["HwAddress"])
    else:
        data['model'] = ""
        data['MAC_addr'] = ""

    return jsonify(data)

#Streaming running based on jsonData from a web server
def streaming(camera, return_data):
    global hash_table
    #print('Rec status : %d'%camera['isRec'])
    camProc = gst.StreamRecorder(str(camera['iaddr']),camera['isRec'],camera['seq'] ,str(camera['name']))
    print("outer1 : ", camProc.error_msg)
    camProc.start()
    print("outer2 : ", camProc.error_msg)
    data = {}
    if camProc.error_msg is not None:
        print("___________We got Error : %s" % camProc.error_msg)
        data['status'] = 0
        data['inserted'] = ""
        data['updated'] = ""
        data['stream_url'] = ""
        camProc.stop()
        camProc.terminate()
    else:
        print("Valid Addr")
        hash_table.append(camProc)
        data['status'] = 1
        data['inserted'] = camProc.register_date
        data['updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['stream_url'] = "http://192.168.0.237:8000/"+str(camera['seq'])+"/hls/index.m3u8"
        return_data.append(data)

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
    #Streaming running based on jsonData from a web server 
def streaming(camera, return_data):
    global hash_table
    #print('Rec status : %d'%camera['isRec'])    
    camProc = gst.StreamRecorder(str(camera['iaddr']),camera['isRec'],camera['seq'] ,str(camera['name']))    
    print("outer1 : ", camProc.error_msg)
    camProc.start()
    """
    t0 = time.time()
    while True:
        if time.time() - t0 > 2:
            break;
    """  
    print("outer2 : ", camProc.error_msg)
    data = {}
    if camProc.error_msg is not None:
        print("___________We got Error : %s" % camProc.error_msg)
        data['status'] = 0
        data['inserted'] = ""
        data['updated'] = ""
        data['stream_url'] = ""
        camProc.stop()
        camProc.terminate()
    else:       
        print("Valid Addr")
        hash_table.append(camProc)
        data['status'] = 1
        data['inserted'] = camProc.register_date
        data['updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['stream_url'] = "http://192.168.0.237:8000/"+str(camera['seq'])+"/hls/index.m3u8"
        return_data.append(data)

#Create camera streaming and register camera information
@app.route('/api/camera', methods=['POST'])
def createCamera():
    #get api
    jsonData = request.get_json()
    data =[]
    if jsonData is None:
        print("No valid data received\n")
        data ={}
        data['status'] = 0
        data['inserted'] = ""
        data['updated'] = ""
        data['stream_url'] = ""
        return jsonify(data)
    else:
        streaming(jsonData, data)
        print(data)
        t0 = time.time()
        while True:
            if time.time() - t0 > 20:
                return jsonify(data)

#request entire list of camera to run the flask server
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
    #get api
    info = request.get_json()
    data = {}
    if info is not None:
        for camera in hash_table:
            if camera.seq == info['seq']:
                data['status'] = 1
                data['inserted'] = camera.register_date
                data['isRec'] = camera.flag
                print("\n_______camera start time : %s\n" %camera.rec_start.strftime("%H:%M:%S"))
                data['recStartDate'] = camera.rec_start.strftime("%Y%m%d")
                data['recStartTime'] = camera.rec_start.strftime("%H:%M:%S")
                data['recEndTime'] = datetime.datetime.now().strftime("%H:%M:%S")
                data['updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data['stream_url'] = "http://192.168.0.237:8000/"+str(info['seq'])+"/hls/index.m3u8"
                if not camera.link == info['iaddr'] :
                    data['isRec'] = info['isRec']
                    camera.stop()
                    camera.terminate()
                    if camera.flag == 1 :
                        data['record_url']="http://192.168.0.237:8000/"+str(camera.seq)+"/"+camera.rec_start.strftime("%Y%m%d")+"/"+camera.rec_start.strftime("%H:%M:%S")+"/index.m3u8"
                    else:
                        data['record_url'] = ""
                        hash_table.remove(camera)
                        camProc = gst.StreamRecorder(str(info['iaddr']),info['isRec'],info['seq'],str(info['name']))
                        hash_table.append(camProc)
                        camProc.start()
                    break
                else:
                    data['isRec'] = info['isRec']
                    if info['isRec'] == 0 :
                        camera.save()
                        camera.flag = 0
                        data['record_url'] =  "http://192.168.0.237:8000/"+str(camera.seq)+"/"+camera.today+"/"+camera.init_time+"/index.m3u8"
                        data['isRec'] = 0
                    if info['isRec'] == 1 :
                        camera.rec()
                        camera.flag = 1
                        data['record_url'] = ""
                        data['isRec'] = 1
                    break
    else:
        print("Fail to update the camera")
        data['status'] = 0
        data['inserted'] = ""
        data['recStartTime'] = ""
        data['recStartDate'] = datetime.datetime.now().strftime("%Y%m%d")
        data['recEndTime'] = ""
        data['record_url'] = ""
        data['update'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['stream_url'] = ""
        data['isRec'] = 0
    t0 = time.time()
    while True:
        if time.time() - t0 > 20:
            break;
    return jsonify(data)

@app.route('/api/camera/record/status', methods=['PUT'])
def setRecord():
    global hash_table
    path = "/home/imr/nms/Node-Media-Server/public/"
    data = {}
    info = request.get_json()
    if info is not None:
        for camera in hash_table:
            if camera.seq == info['seq']:
                data['status'] = 1
                data['inserted'] = camera.register_date
                data['recStartDate'] = camera.rec_start.strftime("%Y%m%d")
                data['recStartTime'] = camera.rec_start.strftime("%H:%M:%S")
                data['recEndTime'] = datetime.datetime.now().strftime("%H:%M:%S")
                data['updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data['stream_url'] =  "http://192.168.0.237:8000/"+str(info['seq'])+"/hls/index.m3u8"
                if info['isRec'] == 0 :
                    camera.save()
                    camera.flag = 0
                    data['record_url'] = "http://192.168.0.237:8000/"+str(camera.seq)+"/"+camera.today+"/"+camera.init_time+"/index.m3u8"
                    #proc = gst_format.FormatRecorder(data['stream_url'],"avi",datetime.datetime.now().strftime("%Y%m%d"), camera.init_time,camera.seq)
                    #proc.run()
                    data['isRec'] = 0
                if info['isRec'] == 1 :
                    camera.rec()
                    camera.flag = 1
                    data['record_url'] = ""
                    data['isRec'] = 1
                break
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
    while True:
        if time.time() - t0 > 20:
            break;
    return jsonify(data)

#While deleting the camera information, the recording files remains 
@app.route('/api/camera/seq/<int:seq>', methods=['DELETE'])
def deleteCamera(seq=None):
    global hash_table
    for camera in hash_table:
        if camera.seq == seq:
            print("find the exact camera")
            if camera.flag == 1:
                camera.stop()
                url = "http://192.168.0.237:8000/"+str(camera.seq)+"/"+camera.today+"/"+camera.init_time+"/index.m3u8"
                #proc = gst_format.FormatRecorder(url,"avi",camera.today, camera.init_time,camera.seq)
                #proc.run()
            else:
                camera.rm_hls()
                camera.terminate()
                hash_table.remove(camera)
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
    proc = Process(target = req())
    proc2 = Process(target = app.run(host='0.0.0.0', port=5000, debug=False))
    
    mainProcs.append(proc)
    mainProcs.append(proc2)
    
    proc.start()
    proc2.start()
    
    for proc in mainProcs:
        proc.join()
    """
    try:

        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        exit() 
    
