jQuery(function ($){
    'use strict';
    
    $('#datetimepicker-camera').datetimepicker({
	locale: 'ko',
	inline: true,
	format: 'YYYYMMDD',
	minDate: moment('20200601', 'YYYYMMDD'),
	sideBySide: false
    });

    $("#datetimepicker-camera").on("dp.change", function (e){
	loadVideo(e.date.format('YYYYMMDD'));
    });
    
    $('#stream').on("click", function(){
      var live_url = 'http://192.168.0.237:8000/test/hls/index.m3u8'
      var live = document.getElementById('hls');
      if (live.canPlayType('application/vnd.apple.mpegurl')){
         live.src = vide_url;
         console.log("stream play")
         live.addEventListener('loadedmetadata',function(){
  		    live.play();
  	    });
           }else{
        var player = new Hls();
        console.log("stream play")
        player.loadSource(live_url);
        player.attachMedia(live)
        player.on(Hls.Events.MANIFEST_PARSED,function(){
          
		      live.play();
      });
      }       
    });
   

    
    function loadVideo(date) {
	    var cameraRoute = '/home/imr/nms/Node-Media-Server/public/test/'+date + '/index.m3u8';
	    var video = document.getElementById('video');
	
	    var video_url = 'http://192.168.0.237:8000/test/'+ date +'/index.m3u8';
       if (video.canPlayType('application/vnd.apple.mpegurl')){
         video.src = vide_url;
         console.log("play")
         video.addEventListener('loadedmetadata',function(){
  		    video.play();
  	    });
  	  }else{

	        var hls = new Hls();
	        hls.loadSource(video_url);
	        hls.attachMedia(video);
         console.log(video_route + ' is played');
	        hls.on(Hls.Events.MANIFEST_PARSED,function(){
		        video.play();
    	    });        
  	    } 
    }
    
});
