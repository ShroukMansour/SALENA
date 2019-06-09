navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia ||
    navigator.mozGetUserMedia || navigator.msGetUserMedia ||
    navigator.oGetUserMedia;

var webcamStream;
var canvas, ctx;
var boolWebCamAvailable = false;
var csrftoken = "";

var calling_user_caption = "";
var recommended_product_caption = "";
var video_link = "";
var video_tag = "";

function init() {
    canvas = document.getElementById("myCanvas");
    ctx = canvas.getContext('2d');
    startWebcam();
}


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
                    startConversation();
                } catch (error) {
                    video.src = window.URL.createObjectURL(stream);
                }
            }, (error) => {
                console.log(error);
            }
        );
    }
}


// take snapshot and request captions
function takeSnapshot() {
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
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

// get calling caption and call welcome the user
function get_calling_user_caption() {
    $.ajax({
        url: '/salenabot/get_calling_user_caption',
        type: 'POST',
        data: {csrfmiddlewaretoken: csrftoken},
        success: function (data) {
            console.log("calling user caption: ", data["calling_caption"]);
            calling_user_caption = data["calling_caption"];
            if (calling_user_caption === "none") {
                sleep(3000).then(function () {
                   startConversation();
                });
            } else {
                welcome();
            }
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

function addUserMsg(msg="") {
    if (msg === "") {
        msg = $('#msg').val();
    }
    $('#messages').append($(`<li class="user-msg">`).text(msg));
    $('#msg').val('');
}

function addBotMsg(text) {
    $('#messages').append($(`<li class="bot-msg">`).text(text));
}

function addPlayVideoElements() {
    $("#play-video-modal .modal-footer").append(`<a class="play-1 btn btn-primary" href="${video_link}" id="play-video" type="button"
                             data-dismiss="modal">Play</a>`);
    var script = document.createElement("script");
    script.innerHTML = `$(".play-1").yu2fvl({ratio: 4 / 3});
    $("#play-video").click(function () {
        changeBot("whistle");
        addUserMsg("Play video");
        sleep(12000).then(function(){startConversation()});  
    });
     `;
    sleep(2000).then(function () {
        document.body.appendChild(script);
    });
}


function playMsg(text) {
    meSpeak.speak(text, {
        amplitude: 100,
        pitch: 70,
        speed: 130,
        variant: 'f5'
    });
}

function sayToUser(msg) {
    var result = $.Deferred();
    addBotMsg(msg);
    playMsg(msg);
    result.resolve();
    return result.promise();
}

function changeBot(botType) {
    if (botType === "happy")
        $("#bot-img").attr("src", "/static/images/happy.png");
    else if (botType === "poker")
        $("#bot-img").attr("src", "/static/images/poker.png");
    else if (botType === "sad")
        $("#bot-img").attr("src", "/static/images/sad.png");
    else if (botType === "think")
        $("#bot-img").attr("src", "/static/images/think.png");
    else if (botType === "whistle")
        $("#bot-img").attr("src", "/static/images/whistle.png");
    else
        $("#bot-img").attr("src", "/static/images/heart.png");
}


var sleep = function (ms) {
    var result = $.Deferred();
    setTimeout(result.resolve, ms);
    return result.promise();
};

// calc waiting time based on msg size
function calcTimeToWait(msg) {
    var timeToWait = msg.split(" ").length/2;
    return (timeToWait) * 1000;
}


function requestAnswer(question) {
    $('#modal-question').html(`${question}`);
    $('#request-answer-modal').modal();
}

function requestPlayVideo(question) {
    $("#modal-video-question").html(`${question}`);
    $('#play-video-modal').modal();
}


$("#play-video").click(function () {
    changeBot("whistle");
});

$("#dont-play-video").click(function () {
    addUserMsg("No");
   changeBot("sad");
   startConversation();
});

$("#answer-yes").click(function () {
    addUserMsg("Yes");
    changeBot("happy");
    addPlayVideoElements(); // so when requesting video, the button is ready
    var msg = "Okay, let me think.";
    sleep(500).then(function () {
        changeBot("think");
        sayToUser(msg);
        return sleep(calcTimeToWait(msg));
    }).then(function () {
        msg = `I think ${video_tag} will be good for you.`;
        sayToUser(msg);
        changeBot("poker");
        return sleep(calcTimeToWait(msg));
    }).then(function () {
        requestPlayVideo("Do you want to see the video? you will like it ^_^");
    });
});

$("#answer-no").click(function(){
    addUserMsg("No");
    changeBot("sad");
    var msg = "I thought we will be friends, Bye";
    sayToUser(msg);
    startConversation();
});


function welcome() {
    var msg = `Hi, I am Salena. I can recommend you a
        product based on your appearance, Would you like to try me?`;
    sayToUser(msg).then(function () {
        return sleep(calcTimeToWait(msg));
    }).then(function () {
        requestAnswer("Would you like to try me? I'm sure you will like me :) ");
    })
}

function startConversation() {
    sleep(10000).then(function () {
        $("#messages").empty();
        $(".play-1").remove();
        changeBot("heart");
        takeSnapshot();
    });
}

// window.setInterval(function(){
//     if (boolWebCamAvailable) {
//       takeSnapshot()
//     }
// }, 20000);

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


