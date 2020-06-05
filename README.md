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
## Gstreamer

