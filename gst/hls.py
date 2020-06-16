import multiprocessing as mp
import sys, os, time, datetime, re, json
import gi
import json,shutil
import requests

gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst

class StreamRecorder(mp.Process):

    def __init__(self,link,name):
        """
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

        self._name = name#name of camera
        self._link = link
        self._register_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._rec_start = datetime.datetime.now()
        self._rec_done = datetime.datetime.now()
        self._table = {}
        self._init_time = self._rec_start.strftime("%H:%M:%S")
        
        self.pipeline = Gst.parse_launch("""rtspsrc name=m_rtspsrc ! capsfilter caps="application/x-rtp,media=video" ! decodebin ! clockoverlay time-format="%D %H:%M:%S" shaded-background=true halignment=center valignment=top text="녹화 : " font-desc="Sans, 24" ! x264enc ! mpegtsmux ! hlssink name=m_hlssink""")
        
        #directory details
        self.today = datetime.date.today().strftime('%Y%m%d')
        
        #make directory
        if not os.path.isdir("hls"):
            os.mkdir("hls")
        self.location = "hls/file%06d.ts"
        self.playlist = "hls/index.m3u8"
        
        #source params
        self.source = self.pipeline.get_by_name("m_rtspsrc")
        self.source.set_property('location', self.link)

        #hlssink params
        self.sink = self.pipeline.get_by_name("m_hlssink")
        self.sink.set_property('location', self.location)
        self.sink.set_property('playlist-location', self.playlist)
        self.sink.set_property('target-duration', 3)
        self.sink.set_property('max-files', 28800)       
        self.sink.set_property('playlist-length', 28800)
        
    #Getters and Setters
    @property
    def name(self):
        return self._name
    @property
    def link(self):
        return self._link
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
        self._gid = gid
    @name.setter
    def name(self,name):
        self._name = name
                   
    def message(self, bus, pipeline, today, start, done):
        while True:
            try:
                msg = bus.poll(Gst.MessageType.ANY, int(1e6))
                if msg is None:
                    #After streaming 24hours, it updates new record path
                    if today != datetime.date.today().strftime('%Y%m%d'):
                        print("\n___________Today's Record Done______________\n")
                        pipeline.set_state(Gst.State.PAUSED)                
                        
                        start = datetime.datetime.now()
                        self._init_time = start.stftime("%H:%M:%S")
                        shutil.move("hls/", "/"+ today)
                        shutil.mkdir("hls")
                        
                        self.location = "hls/file%04d.ts"
                        self.playlist = "hls/index.m3u8"
                        self.sink.set_property('location', self.location)
                        self.sink.set_property('playlist-location', self.playlist)
                        self.sink.set_property('playlist-length', 28800)
                        self.sink.set_property('target-duration', 3)
                        self.sink.set_property('max-files', 28800)
                        today = datetime.date.today().strftime('%Y%m%d')
                        pipeline.set_state(Gst.State.PLAYING)
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
                break
        return 

    def stop(self):     
        self.pipeline.set_state(Gst.State.NULL)
        shutil.move("hls", self.today)
                
    def run(self):
        """
        gst-launch-1.0 rtspsrc location=rtsp://your.rtsp.address ! 
        capsfilter caps="application/x-rtp,media=video" ! decodebin ! clockoverlay time-format="%D %H:%M:%S" ! 
        x264enc ! mpegtsmux ! hlssink location=segment%04d.ts

        multiple sink
        gst-launch-1.0 rtspsrc location=rtsp://192.168.0.11/profile2/media.smp ! 
        capsfilter caps="application/x-rtp,media=video" ! decodebin ! clockoverlay time-format="%D %H:%M:%S" ! 
        x264enc ! mpegtsmux ! tee name = t t. ! queue ! hlssink location="/home/imr/media/file%03d.ts"  
        \t. ! queue ! hlssink location="/home/imr/nms/test%04d.ts"
        """      
        #start to record
        print("Streaming Registered on %s" %(self._register_date))
        self.pipeline.set_state(Gst.State.PLAYING)

        bus = self.pipeline.get_bus()
        print("Bus message gets")

        #bus = self.pipeline.get_bus()
        print("Bus message gets")
        self.message(bus, self.pipeline,self.today,self._rec_start,self._rec_done)
        
        #free the streaming
        self.stop()
