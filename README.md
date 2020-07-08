# Gstreamer Network Video Recorder
Python app designed for continnous video recording from IoT devices ( IP web cameras ) 
over Internet to the local hard drive through RTSP.

- Intended for 24/7 video surveillance with IoT resources and simple video review on daily basis.
- Http live streaming with Gstreamer pipeline media process.
- Gstreamer, Flask for video capture. 
- ONVIF PTZ Control available if the device supports PTZ
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
- PTZ control over UI

# Sample User Interface
- From the first tab, User can review recorded video format (.m3u8) by choosing a date on UI. The other tab contains HLS from NVR devices that is available to watch real time video from the HLS.js media player. 
- Calendar at right shows dates for which recorded files are found. User can choose date, choose camera, watch recorded video on any tablet or smartphone.
- Based on HTML5, UI is designed not only for a desktop PC, but also various devices such as smartphones, or iPad/ Android tablets by using Bootstrap library	
- Quickly review a whole day at a glance

![alt example](/images/ui4.png "UI layout2")

# Recording
## Http Live Streaming (HLS)
HTTP Live Streaming (HLS) sends audio and video over HTTP from an ordinary web server for playback on mobile devices, especially for iOS-based devices, and personal computers. Using the same protocol that powers the web, HLS deploys content using ordinary web servers and content delivery networks. HLS is designed for reliability and dynamically adapts to network conditions by optimizing playback for the available speed of wired and wireless connections.

This app supports a HLS format to stream and record at the same time to increase the functionality and reduce a time consuming tasks by multiprocessing the modules. Since the sample UI is designed with Hls.js, not only user can watching HLS media on Safari, but also any types of web broswer can be played HLS as well.  

![alt example](/images/ts_sample.png "UI CRUD")

## Gstreamer
GStreamer is a streaming media framework based on a pipelined structure. The functionality to process media is provided by plugins such as  elements, bins, etc. This allows new functionality to be added simply by installing new plug-ins.

Based on configuration and schedule, python app creates instances of gstreamer pipeline and live streaming media player. 

GStreamer plays a role as filtering RTSP sources with high quality and overlayed real-time records. Furthermore, it produces bunch of mpegts files for streaming and recording simultaneously. These files are saved at the end of day at specific format for playing back later.

![alt example](/images/gst_constructor.png "Pipeline design")

While a pipeline receives sources(RTSP, file, or URI), it passes through each steps of elements to produce the output by exchanging specific messages. A bus is a simple system that takes care of forwarding messages from the streaming threads to an application in its own thread context. When the mainloop is running or the pipeline state is PLAYING, the bus will periodically be checked for new messages, and the callback will be called when any message is available.

![alt example](/images/gst_message.png "Message Bus")

![alt example](/images/gst_message2.png "State Update")

## Flask
This Python app used to control video recording process, recording itself is performed by Gstreamer media processing. 
Flask server makes this Python app available to communicate with UI by sending and receiving API to run a program. 
App performs recording monitoring, recording scheduling, and cleaning.

![alt example](/images/flask_crud1.png "UI CRUD")

![alt example](/images/API_test.png "API Test")

## H.264 format
h264 is an inevitable encoding format. It is much better than MJPEG. With the same frame rate, h264 will require five times smaller network bandwidth than MJPEG. That mean that at the same bit rate you will get much better image quality.


# GStreamer

https://gstreamer.freedesktop.org/documentation

파이프라인 기반의 영상처리 오픈소스 프레임워크.

핵심기능 : plugin, data flow, media type handling 및 negotiation을 위한 프레임워크 제공

하나의 파이프라인 구조에서 각기 다른 기능을 가진 Element들을 연결하여 결과물을 생성(src → sink)

`$ gst-launch-1.0 rtspsrc location=rtsp://192.168.0.11/profile2/media.smp 
! capsfilter caps="application/x-rtp,media=video" ! decodebin  
! clockoverlay time-format="%D %H:%M:%S" ! x264enc 
! tee name = t 
\t. ! queue ! mpegtsmux ! hlssink location="/home/imr/media/file%03d.ts"
\t. ! queue ! splitmuxsink location="/home/imr/nms/test%04d.mp4" max-size-time=10000000000 
`

Gst-launch-1.0 : Gstreamer상에서 파이프라인을 실행시켜주는 도구.  파이프라인을 parsing하여 영상처리

## 설치 

리눅스상에서 Gstreamer 설치유무 확인:

`$ which gst-launch-1.0`

설치 경로가 출력됐을 경우, 설치 필요 無

`/usr/bin/gst-launch-1.0`

필요한 패키지 설치:

`$ sudo apt-get install libgstreamer1.0-0 sudo apt-get install gstreamer1.0-plugins-base gstreamer1.0-plugins-good 
sudo apt-get install gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly 
sudo apt-get install gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools`

에러 발생시 한줄씩 설치:
<pre><code>
$ sudo apt-get install libgstreamer1.0-0 

$ sudo apt-get install gstreamer1.0-plugins-base gstreamer1.0-plugins-good

$ sudo apt-get install gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly

$ sudo apt-get install gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools
</pre></code>
파이썬 GStreamer 라이브러리 설치:

`$sudo apt-get install python-gst-1.0 python3-gst-1.0`

dev-packages 설치 :
<pre><code>
$ sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev 

$ sudo apt-get install libfontconfig1-dev libfreetype6-dev libpng-dev

$ sudo apt-get install libcairo2-dev libjpeg-dev libgif-dev 

$ sudo apt-get install libgstreamer-plugins-base1.0-dev
</pre></code>
기본 command line:

`$ gst-launch-1.0 videotestsrc ! autovideosink`


## Element : GstElement class 에서 파생된 object. 

소스와 싱크는 패드를 통해 연결

Element는 서로간 연결될때 특정 기능을 제공

    ex) source element는 stream에 data를 제공하고, filter element는 stream상의 data에 따라 행동한다.

Element는 plugin으로 감싸져야 Gstreamer 에서 사용

한 개의 plugin은 한 개 또는 다수 element 구현

데이터의 생산자(source or src)와 소비자(sink element) Element

## 주요 Elements (RTSP streaming 기능 위주) :

* rtspsrc : RTSP로 생성된 영상 소스를 불러오는 Element

* filter : 현재 pad에 동작하는 미디어에 대해 제한을 걸기 위한 용도로 cap을 사용

        ex) capsfilter caps="application/x-rtp,media=video"
    
* decodebin : 자동으로 알맞은 decoder와 demuxer기능을 구성

* encoder : 포맷에 맞는 결과물을 처리하기 위해 소스를 인코딩해주는 기술 

        ex) x264enc : H.264 코덱으로 인코딩

* hlssink : HLS형식으로 sink 생성.

     이외에도 다양한 sink elements와 mux를 사용하여 원하는 포맷으로 저장 가능

        ex) filesink, appsink, autovideosink, ximagesink...etc

* autovideosink : Gstreamer상에서 내장된 시스템의 기본적인 sink를 자동 선택

* tee : 다양한 결과물을 처리하고자 할때 파이프라인 병렬처리 시켜주는 Element

* queue : 순서에 맞게  Element 간의 쓰레드를 분리. 


## Bin: element를 모아놓은 container. 

* 여러개의 element를 연결하여 하나의 논리적 element로 통합 가능

* Pipeline을 이용해 bin을 작은 단위로 쪼갤수 있기때문에 Pipeline의 복잡도가 상승 할 때 사용하면 용이함

## Pipeline : element를 조합하여 동기화 및 버스 메시지 관리를 위한 포괄적인 container. 

* GStreamer 영상 처리 시 가장 기본적으로 구성  

* State에 따라 파이프라인 작동 유무 판단.

        PLAYING, PAUSED, READY, NULL

* GST_STATE_NULL:

    this is the default state. This state will deallocate all resources held by the element.

* GST_STATE_READY:

    in the ready state, an element has allocated all of its global resources, that is, resources that can be kept within streams. You can think about opening devices, allocating buffers and so on. However, the stream is not opened in this state, so the stream positions is automatically zero. If a stream was previously opened, it should be closed in this state, and position, properties and such should be reset.

* GST_STATE_PAUSED:

    in this state, an element has opened the stream, but is not actively processing it. An element is allowed to modify a stream’s position, read and process data and such to prepare for playback as soon as state is changed to LAYING, but it is not allowed to play the data which would make the clock run. In summary, PAUSED is the same as PLAYING but without a running clock. Elements going into the PAUSED state should prepare themselves for moving over to the PLAYING state as soon as possible. 

* GST_STATE_PLAYING:

    in the PLAYING state, an element does exactly the same as in the PAUSED state, except that the clock now runs.

## Bus - application과 pipeline 사이의 데이터 교환 또는 통신을 위한 메커니즘

    메시지를 생성하여 event를 확인하고 결과값을 파이프라인으로 전송. 
    
    메시지 핸들러 함수를 통해 element간 주고받는 메시지를 확인하고 처리

        ex)  ERROR, WARNING, EOS, STREAM_START...etc


프로그래밍 기본 구성(Python) :

<pre><code>
gi.require_version('Gst', '1.0')

from gi.repository import GObject, Gst #파이썬 상에서 Gstreamer 프레임워크 적용


Gst.init(None) #초기화

pipeline = Gst.parse_launch(“””파이프라인 구성 요소 추가“””)

element = pipeline.get_by_name(“element name”)
element.set_property(‘option’, ‘value’)

pipeline.set_state(Gst.State.PLAYING) #Gstreamer 기능 수행

bus = pipeline.get_bus() #파이프라인 element간 메시지 공유, message 함수 필요

pipeline.set_state(Gst.State.NULL) #작업완료, EOS, 또는 에러 발생시 기능종료

</pre></code>
# HTTP Live Streaming (HLS)

* 스트리밍 : 네트워크 기반 비디오, 오디오 등의 멀티미디어 정보를 제공하는 기술로 다운로드없이 실시간으로 재생가능.
* 재생 시간이 단축되며 HDD 용량에도 영향을 받지 않는다.

## HLS : m3u8의 확장자를 가진 재생목록 파일과 다수의 ts 영상을 HTTP를 통해 전송하는 방식

* m3u8 : UTF-8으로 인코딩된 m3u파일

    가장 첫 줄은 #EXTM3U로 시작

    m3u8 포맷의 지시어는 맨 앞을 #EXT로 시작 

        #EXT로 시작하지 않으면 # 이후의 문자열을 주석으로 간주

* m3u : ts 파일의 재생목록을 관리하는 파일,  m3u에는 Latin-1 문자 인코딩, 단순 파일 목록 나열할 뿐이므로 재생할 파일에 대한 정보를 재생하기 전에 미리 알 수 없다.

* ts (Transport Stream) : MPEG-4 형식의 분할 저장 파일

    HLS로 화면을 자연스럽게 재생하려면 각 ts 파일이 I-frame 포함

        I-frame (Intra frame) : 화면 전체가 압축되어 들어 있는 frame

<pre><code>
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-ALLOW-CACHE:NO
#EXT-X-MEDIA-SEQUENCE:1

#EXT-X-TARGETDURATION:3
#EXTINF:3.4995403289794922,
file000000.ts
EXTINF:3.3863615989685059,
file000001.ts
#EXTINF:3.3931219577789307,
file000002.ts
</pre></code>

|  지시어 | 형식 | 설명 |
| ------ | ------ | ------ |
| #EXTM3U | #EXTM3U | 파일이 m3u8 포맷임을 명시 |
| #EXT-X-MEDIA-SEQUENCE | #EXT-X-MEDIA-SEQUENCE: <첫 파일의 일련번호> | 제일 먼저 플레이하는 파일의 일련번호를 명시. 이 지시어가 포함되지 않은 경우 첫 분할 파일의 일련 번호는 0으로 간주 |
| #EXT-X-TARGETDURATION | #EXT-X-TARGETDURATION: <시간: 초> | 파일 목록 각 파일의 최대 재생 시간을 명시 |
| #EXTINF | #EXTINF: <재생 시간:초>,<제목> | 콘텐츠의 재생 시간과 제목을 명시시 |
| #EXT-X-STREAM-INF | #EXT-X-STREAM-INF  | ts파일 정보 제공. #EXTINF는 재생 시간, 제목 정보만 제공, #EXT-X-STREAM-INF : BANDWIDTH, CODEC, RESOLUTION|
|#EXT-X-ENDLIST| #EXT-X-ENDLIST| 플레이 리스트에서 재생할 콘텐츠가 더 이상 없음을 의미한다. 이 지시어가 표시된 줄 이후의 콘텐츠는 무시한다. |
|#EXT-X-DISCONTINUITY | #EXT-X-DISCONTINUITY | 이 지시어가 표지된 줄을 기준으로 이전 줄과 이후 줄에서 재생하는 콘텐츠의 정보 변경되었음을 표시.|
|#EXT-X-KEY |#EXT-X-KEY: <암호화 방법>[, <key>]| 암호화된 파일을 해독하는 키 값을 명시. HTTP Live Streaming에서는 재생 시간에 따라 분할된 각 파일을 암호화하여 전송. 암호화된 파일을 해독할 때 필요한 키 값을 플레이어에게 알려 주기 위해 사용. |

# ONVIF

## ONVIF(Open Network Video Interface Forum) : IP Web Camera 제어 목적으로 사용하는 HTTP 기반 국제 표준 프로토콜. 

네트워크 비디오 장치 간 통신의 표준화

제조업체와 무관한 네트워크 비디오 제품 간 상호 운용성

모든 기업과 단체에 대한 개방

주요 기술:

* Web Service: HTTP, XML 기반으로 제공되는 서비스

* WSDL(Web Services Description Language) : 어떤 Web Service를 제공하는지 기술한 XML 문서

* SOAP(Simple Object Access Protocol) : HTTP, HTTPS, SMTP를 사용하여 통신하고 XML을 주고받는 프로토콜

## PTZ(Pan-Tilt-Zoom) : 카메라에 내장된 옵션으로 방향과 확대/축소를 원격으로 제어기능 

* Pan : 디바이스의 수평적 움직임 또는 회전

* Tilt : 디바이스의 수직적 움직임 또는 회전

* Zoom : 디바이스 렌즈의 초점 조절, 출력 화면의 확대 및 축소 

## NVIF 파이썬 라이브러리 

설치: 

` pip3 install --upgrade onvif_zeep `

실패시 onvif_zeep.tar.gz 를 받아서( ) 설치 :

` cd python-onvif-zeep && python setup.py install `

ONVIFCamera 라이브러리 적용 :
<pre><code>
from onvif import ONVIFCamera
#Initialize ONVIFCamera 
mycam = ONVIFCamera(IP_ADDRESS , PORT , USER , PASSWD ) `
</pre></code>
ONVIF 라이브러리 : http://www.onvif.org/onvif/ver20/util/operationIndex.html

디바이스 정보 확인

DeviceMGMT(Device Management)를 통해 디바이스의 정보를 확인 가능
<pre><code>
print("Device Model : %s" % mycam.devicemgmt.GetDeviceInformation()["Model"])
print("MAC Address : %s" % mycam.devicemgmt.GetNetworkInterfaces()[0]["Info"]["HwAddress"])

#Device Model : XNP-6040H
#MAC addrress : E4:30:22:1F:CC:DD
</pre></code>
# PTZ(Pan-Tilt-Zoom)

PTZ Service설정 :
<pre><code>
#Create ptz service
ptz_service = mycam.create_ptz_service()

#Get ptz configuration
mycam.ptz.GetConfiguration()


#Get PTZ configuration
request = ptz.create_type('GetConfigurationOptions')
request.ConfigurationToken = media_profile.PTZConfiguration.token
ptz_configuration_options = ptz.GetConfigurationOptions(request)

#Create request 
moverequest = ptz.create_type('ContinuousMove')
moverequest.ProfileToken = media_profile.token
</pre></code>
## ContinuousMove

정의: 지속적인 PTZ 동작을 작동하기위한 함수. 기본적인 space set은 PTZConfiguration 적용.

기본적인 명령은 request를 통해 변경 가능

Input:

[ContinuousMove]

* ProfileToken [ReferenceToken] MediaProfile 참조 기능.

* Velocity [PTZSpeed] : PTZ의 조작 속도 조절. 기본 설정 : 1.0

* PanTilt - optional; [Vector2D] Pan, Tilt의 속도 설정. x 컴포넌트는 Pan, y 컴포넌트는 Tilt에 상응. request 제외시 움직임 변화 없음

* Zoom - optional; [Vector1D] zoom의 속도 설정. 

* Timeout - optional; [duration] timeout 설정 옵션

Output:

[ContinuousMoveResponse]

예제:

<pre><code>
YMAX = 1.0
def move_right(ptz, request):
  request.Velocity.PanTilt.x = 0
  request.Velocity.PanTilt.y = YMAX
  ptz.ContinousMove(request)
</pre></code>

## Stop

정의: 절대적, 상대적, 지속적 형식으로 진행중인 PTZ 움직임을 정지시키는 함수. Pan, tilt, zoom 의 설정이 없을시, 디바이스 전체동작 정지

Input:

[Stop]

* ProfileToken [ReferenceToken] 무엇을 정지시킬 것 인지에 대한 MediaProfile을 참조 

* PanTilt - optional; [boolean] 진행중인 Pan과 Tilt 움직임를 멈추고자 할때 설정. 만약 특정 Pan,Tilt 인수가 제시되지 않았을때, Pan, Tilt 움직임을 정지 시킴.

* Zoom - optional; [boolean] 진행중인 zoom 움직임을 멈추고자 할때 설정. 만약 특정 Pan,Tilt인수가 제시되지 않았을때, Zoom 움직임을 정지 시킴.

Output:

[StopResponse]

예제:

`ptz.Stop({'ProfileToken': request.ProfileToken})`
