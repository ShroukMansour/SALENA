
navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia ||
                            navigator.mozGetUserMedia || navigator.msGetUserMedia ||
                             navigator.oGetUserMedia;

var webcamStream;
var boolWebCamAvailable = false;
var csrftoken = "";

var calling_user_caption = "";
var recommended_product_caption = "";
var video_link = "";
var video_tag = "";

function startWebcam() {
    if (navigator.getUserMedia) {
        navigator.getUserMedia({
            video: true
        }, (stream) => {
            video = document.querySelector('video');
            webcamStream = stream;
            try {
              video.srcObject = stream;
              boolWebCamAvailable = true;
              snapshot();
            } catch (error) {
              video.src = window.URL.createObjectURL(stream);
            }
          }, (error) => {
             console.log(error);
          }
        );
    }
}

var canvas, ctx;

function init() {
    canvas = document.getElementById("myCanvas");
    ctx = canvas.getContext('2d');
    startWebcam()
}

function snapshot() {
    ctx.drawImage(video, 0,0, canvas.width, canvas.height);
    var dataURL = canvas.toDataURL();
    csrftoken = getCookie('csrftoken');

    $.ajax({
      url: '/salenabot/wrtie_captured_img',
      type: 'POST',
      data: {'imgBase64': dataURL, csrfmiddlewaretoken: csrftoken},
      success: function (data) {
            get_calling_user_caption();
            get_recommendation_data();
      },
      error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
      }
    });

}

function get_calling_user_caption() {
    $.ajax({
        url: '/salenabot/get_calling_user_caption',
        type: 'POST',
        data: {csrfmiddlewaretoken: csrftoken},
        success: function (data) {
            console.log("calling user caption: ", data["calling_caption"]);
            calling_user_caption = data["calling_caption"];
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}

function get_recommendation_data() {
    $.ajax({
        url: '/salenabot/get_recommendation_data',
        type: 'POST',
        data: {csrfmiddlewaretoken: csrftoken},
        success: function (data) {
            recommended_product_caption = data["recommendation_caption"];
            video_link = data["video_link"];
            video_tag = data["video_tag"];
            console.log("get_recommendation_data", recommended_product_caption);
            console.log("link", video_link);
            console.log("tag", video_tag);
        },
        error: function (xhr, errmsg, err) {
            console.log("error");
        }
    });
}


// window.setInterval(function(){
//     if (boolWebCamAvailable) {
//       snapshot()
//     }
// }, 5000);

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}