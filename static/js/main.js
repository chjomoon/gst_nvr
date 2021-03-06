jQuery(function ($){
    'use strict';
    
    $('#datetimepicker-camera').datetimepicker({
	locale: 'ko',
	inline: true,
	format: 'YYYYMMDD',
	minDate: moment('20200601', 'YYYYMMDD'),
	sideBySide: false
    });//datetimepicker

    $("#datetimepicker-camera").on("dp.change", function (e){
	loadVideo(e.date.format('YYYYMMDD'),'video');
    });//dpchange

    
    //Form data to Json
    jQuery.fn.serializeObject = function() {
	var obj = null;
	try {
            if (this[0].tagName && this[0].tagName.toUpperCase() == "FORM") {
		var arr = this.serializeArray();
		if (arr) {
                    obj = {};
                    jQuery.each(arr, function() {
			obj[this.name] = this.value;
                    });
		}//if ( arr ) {
            }
	} catch (e) {
            alert(e.message);
	} finally {
	}
	return obj;
    };//serialize Object
    
    $("#form").on('submit',function(e){
	var formData = $("#form").serializeObject();
	console.log(formData);
	$.ajax({
            url: "/api/camera",
            type: 'post',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(data) {
		alert('Register success');
		loadVideo('hls','hls');
            },error:function(xhr,status,error){
		alert('error');
	    }//success
        });//ajax
	return false;
    });//submit
    
    function loadVideo(date,id) {
	var cameraRoute = '/home/imr/nms/Node-Media-Server/public/test/'+date+'/index.m3u8';
	var video = document.getElementById(id);
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
            console.log(video_url + ' is played');
	    hls.on(Hls.Events.MANIFEST_PARSED,function(){
		video.play();
    	    });        
  	} //if
    }//loadvideo
    
});
