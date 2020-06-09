import multiprocessing as mp
import sys, os, time, datetime, re, json
import gi
import json,shutil
import requests
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst

class StreamRecorder(mp.Process):

    def __init__(self,seq,gid,name,format_type):
        """
        gst-launch-1.0 souphttpsrc location=http://192.168.0.14:8000/1/1/hls/index.m3u8 ! hlsdemux 
        ! filesink location=out.mp4

        Initialize the stream recording prossess
        link - rtsp link of stream
        rec - flag whether to determine recording or not
        seq - sequence number of the camera
        gid - group id of the camera
        name - name of the camera
        """
        super().__init__()
        Gst.init(None)
        GObject.threads_init()

        self._seq = seq
        self._name = name
        self._gid = gid
        self._link = "http://192.168.0.237:8000/"+str(self._gid)+"/"+str(self._seq)+"/hls/index.m3u8"
        self._ftype = format_type
        self._register_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._rec_start = datetime.datetime.now()
        self._rec_done = datetime.datetime.now()
        self._init_time = self._rec_start.strftime("%H:%M:%S")

        self.pipeline = Gst.parse_launch("""souphttpsrc name=m_src ! hlsdemux ! filesink name=m_sink""")
        #directory details
        path="/home/imr/nms/Node-Media-Server/public/"
        self.directory = path+str(self._gid)+"/"+str(self._seq)
        self.today = datetime.date.today().strftime('%Y%m%d')

        #make directory
        """
        if not os.path.isdir(path+str(self._gid)):
            os.mkdir(path+str(self._gid))    
        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)
        
        if not os.path.isdir(self.directory +"/"+ self.today):
            os.mkdir(self.directory+"/"+ self.today)
        if not os.path.isdir(self.directory+"/"+self.today+"/"+self._init_time):
            os.mkdir(self.directory+"/"+ self.today+"/"+self._init_time)
        """
        if self._ftype == "mp4":
            self.location = self.directory+"/hls/file.mp4"
        elif self._ftype == "avi":
            self.location = self.directory+"/hls/file.avi"
            
        #source params
        self.source = self.pipeline.get_by_name("m_src")
        self.source.set_property('location', self.link)

        #hlssink params
        self.sink = self.pipeline.get_by_name("m_sink")
        self.sink.set_property('location', self.location)

    #Getters and Setters
    @property
    def seq(self):
        return self._seq
    @property
    def gid(self):
        return self._gid
    @property
    def name(self):
        return self._name
    @property
    def link(self):
        return self._link
    @property
    def ftype(self):
        return self._ftype
    @property
    def rec_start(self):
        return self._rec_start
    @property
    def rec_done(self):
        return self._rec_done
    @property
    def register_date(self):
        return self._register_date
    #date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    @rec_start.setter
    def rec_start(self, date):
        self._rec_start = date
    @rec_done.setter
    def rec_done(self, date):
        self._rec_done = date
    @register_date.setter
    def register_date(self, date):
        self._register_date = date
    @link.setter
    def link(self,link):
        self._link = link
    @seq.setter
    def seq(self,seq):
        self._seq = seq
    @gid.setter
    def gid(self,gid):
        self._gid = gid
    @name.setter
    def name(self,name):
        self._name = name
    @ftype.setter
    def ftype(self,format_type):
        self._ftype = format_type

    def message(self, bus, pipeline, today, start, done):
        t0 = time.time()
        while True:
            try:
                msg = bus.poll(Gst.MessageType.ANY, int(1e6))
                if msg is None:
                    #After streaming 24hours, it updates new record path
                    if time.time() - t0 > 200:
                        print("break")
                        pipeline.send_event(Gst.Event.new_eos())
                        break
                    continue
                t = msg.type
                if t ==Gst.MessageType.EOS:
                    print("End of Stream")
                    break
                elif t == Gst.MessageType.ERROR:          
                    err, debug = msg.parse_warning()
                    print("Error: %s" % err, debug)
                    break
                elif t == Gst.MessageType.WARNING:
                    err, debug = msg.parse_warning()
                    print("Warning: %s" % err, debug)
                    pass
                elif t == Gst.MessageType.STATE_CHANGED:
                    if msg.src == pipeline:
                        old_state, new_state, pending_state = msg.parse_state_changed()
                        print("Pipeline state changed from {0:s} to {1:s}".format(
                            Gst.Element.state_get_name(old_state),Gst.Element.state_get_name(new_state)))
                        pass
                elif t == Gst.MessageType.STREAM_START:
                    print("Stream Start")
                    start = datetime.datetime.now()
                    print(self._rec_start.strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    print(t)
                    print("Unknown message: %s" % msg)
            except KeyboardInterrupt:
                print("Keyboard Interrupt")
                pipeline.send_event(Gst.Event.new_eos())
                break
        return 

    def stop(self):     
        self.pipeline.set_state(Gst.State.NULL)
        #shutil.move(self.directory+"/hls", self.directory+"/"+ self.today +"/"+self._init_time)

    def run(self):
        #start to record
        print("Streaming Registered on %s" %(self._register_date))
        self.pipeline.set_state(Gst.State.PLAYING)

        bus = self.pipeline.get_bus()

        #bus = self.pipeline.get_bus()
        print("Bus message gets")
        self.message(bus, self.pipeline,self.today,self._rec_start,self._rec_done)

        #free the streaming
        """
        self.pipeline.set_state(Gst.State.NULL)
        shutil.move(self.directory+"/hls", self.directory+"/"+ self.today +"/"+self._init_time)
        """
        self.stop()
