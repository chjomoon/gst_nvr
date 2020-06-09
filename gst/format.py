import multiprocessing as mp
import sys
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst

class StreamRecorder(mp.Process):

    def __init__(self,seq,gid,name,format_type):
        """
        gst-launch-1.0 souphttpsrc location=http://192.168.0.14:8000/1/1/hls/index.m3u8 ! hlsdemux 
        ! filesink location=out.avi
        Initialize the stream recording prossess
        seq - sequence number of the camera
        gid - group id of the camera
        name - name of the camera
        format_type - Sink format
        """
        super().__init__()
        Gst.init(None)
        GObject.threads_init()

        self._seq = seq
        self._name = name
        self._gid = gid
        self._link = "http://192.168.0.237:8000/"+str(self._gid)+"/"+str(self._seq)+"/hls/index.m3u8"
        self._ftype = format_type
        
        self.pipeline = Gst.parse_launch("""souphttpsrc name=m_src ! hlsdemux ! filesink name=m_sink""")
        #directory details
        path="/home/imr/nms/Node-Media-Server/public/"
        self.directory = path+str(self._gid)+"/"+str(self._seq)

        #set location
        if self._ftype == "mp4":
            self.location = self.directory+"/hls/final.mp4"
        elif self._ftype == "avi":
            self.location = self.directory+"/hls/final.avi"
            
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

    def message(self, bus, pipeline):
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

    def run(self):
        #start to record
        self.pipeline.set_state(Gst.State.PLAYING)
        bus = self.pipeline.get_bus()
        #bus = self.pipeline.get_bus()
        print("Bus message gets")
        self.message(bus, self.pipeline)
        #free the streaming
        self.stop()
