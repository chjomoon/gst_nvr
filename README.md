# Gstreamer Network Video Recorder
Python app designed for continnous video recording from IoT devices ( IP web cameras ) 
over Internet to the local hard drive through RTSP.

- Intended for 24/7 video surveillance with IoT resources and simple video review on daily basis.
- Http live streaming with Gstreamer pipeline media process.
- Gstreamer, Flask for video capture. 
- Tested on Ubuntu Server 18.04 LTS.

![alt example](/images/ui.png "UI layout")

# Features
- H264, HLS or RTSP streaming mode
- Live Streaming view
- x264 Encoding output
- Recording time overlayed with file outputs
- HLS file segmentation 
- Simultaneous recording and streaming from IP web cams over Mobile environment
- Rest API to play a role as CRUD

# Recording
## Http Live Streaming (HLS)
HTTP Live Streaming (HLS) sends audio and video over HTTP from an ordinary web server for playback on mobile devices, especially for iOS-based devices, and personal computers. Using the same protocol that powers the web, HLS deploys content using ordinary web servers and content delivery networks. HLS is designed for reliability and dynamically adapts to network conditions by optimizing playback for the available speed of wired and wireless connections.

This app supports a HLS format to stream and record at the same time to increase the functionality and reduce a time consuming tasks by multiprocessing the modules. Since the sample UI is designed with Hls.js, not only user can watching HLS media on Safari, but also any types of web broswer can be played HLS as well.  

![alt example](/images/ts_sample.png "UI CRUD")

![alt example](/images/ui4.png "UI layout2")

## Gstreamer
GStreamer is a streaming media framework based on a pipelined structure. The functionality to process media is provided by plugins such as  elements, bins, etc. This allows new functionality to be added simply by installing new plug-ins.

Based on configuration and schedule, python app creates instances of gstreamer pipeline and live streaming media player. 

GStreamer plays a role as filtering RTSP sources with high quality and overlayed real-time records. Furthermore, it produces bunch of mpegts files for streaming and recording simultaneously. These files are saved at the end of day at specific format for playing back later.

![alt example](/images/gst_constructor.png "Pipeline design")

## Flask
This Python app used to control video recording process, recording itself is performed by Gstreamer media processing. 
Flask server makes this Python app available to communicate with UI by sending and receiving API to run a program. 
App performs recording monitoring, recording scheduling, and cleaning.

![alt example](/images/flask_crud1.png "UI CRUD")

![alt example](/images/API_test.png "API Test")

## H.264 format
h264 is an inevitable encoding format. It is much better than MJPEG. With the same frame rate, h264 will require five times smaller network bandwidth than MJPEG. That mean that at the same bit rate you will get much better image quality.

