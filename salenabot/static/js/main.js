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
var video_duration = 0;

var userResponsedForWelcome = false;

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
                    startNewConversation();
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
                   startNewConversation();
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
            video_duration = calcVideoDurationMS(data["video_duration"]);
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
        sleep(video_duration + 2000).then(function(){
            $('#play-video-modal').hide();
            $('.modal-backdrop').hide();
            $(".yu2fvl").remove();
            $(".yu2fvl-overlay").remove();
            sleep(3000).then(function(){
                rateMeModal();
            });
        });  
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
    // playMsg(msg);
    speak(msg);
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
    var timeToWait = (msg.split(" ").length/200) * 100;
    return (timeToWait) * 1000;
}

function calcVideoDurationMS(time) {
    timeParts = time.split(":");
    return (timeParts[0] * (60000)) + (timeParts[1] * 1000)
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
    sayToUser("Okay, see you soon");
    startNewConversation();
});

$("#answer-yes").click(function () {
    addUserMsg("Fine");
    changeBot("happy");
    sleep(500).then(function () {
        var msg = "That's great.";
        changeBot("happy");
        sayToUser(msg);
        return sleep(calcTimeToWait(msg))
    }).then(function () {
        var msg = "Let me think of something that will make you happier.";
        changeBot("think");
        sayToUser(msg);
        return sleep(calcTimeToWait(msg) + 1000);
    }).then(function () {
        // msg = `I think ${video_tag} will be good for you.`;
        msg = recommended_product_caption;
        sayToUser(msg);
        changeBot("happy");
        return sleep(calcTimeToWait(msg));
    }).then(function () {
        requestPlayVideo("Do you want to see the video? you will like it ^_^");
    });
});

$("#answer-no").click(function(){
    addUserMsg("I'm not fine");
    changeBot("sad");
    sleep(500).then(function () {
        var msg = "Oh, why?.";
        changeBot("sad");
        sayToUser(msg);
        return sleep(calcTimeToWait(msg))
    }).then(function () {
        var msg = "Ok. let me think of something that can improve your mode.";
        changeBot("think");
        sayToUser(msg);
        return sleep(calcTimeToWait(msg) + 1000);
    }).then(function () {
        // msg = `I think ${video_tag} will be good for you.`;
        msg = recommended_product_caption;
        sayToUser(msg);
        changeBot("happy");
        return sleep(calcTimeToWait(msg));
    }).then(function () {
        requestPlayVideo("Do you want to see the video? you will like it ^_^");
    });
});

function talkYesClicked () {
    userResponsedForWelcome = true;
    sleep(1000).then(function () {
        sayToUser("Hi, I'm Salena");
        userName = "Shrouk";
        changeBot("happy");
        addPlayVideoElements(); // so when requesting video, the button is ready
        return sleep(3000);
    }).then(function () {
        // msg = `${userName}, I can recommend you a product based on your appearance`;
        msg = "How are you?";
        sayToUser(msg);
        return sleep(calcTimeToWait(msg));
    }).then(function () {
        requestAnswer("Are you well?");
    });
    //     return sleep(calcTimeToWait(msg));
    // }).then(function () {
    //     var msg = "Let me think";
    //     changeBot("think");
    //     sayToUser(msg);
    //     return sleep(calcTimeToWait(msg) + 1000);
    // }).then(function () {
    //     msg = recommended_product_caption;
    //     sayToUser(msg);
    //     changeBot("happy");
    //     return sleep(calcTimeToWait(msg));
    // }).then(function () {
    //     requestPlayVideo("Do you want to see the video? you will like it ^_^");
    // });
}

function openWelcomeModal() {
    $("#welcome-page-modal").modal();
}

function welcome() {
    var msg = calling_user_caption;
    $(".bot-msgs ul").append(`<li class="bot-msg calling-user-caption">${msg}</li>`);
    speak(msg);
    sleep(calcTimeToWait(msg)).then(function () {
        msg = "Do you want to talk with me? ";
        $(".bot-msgs ul").append(`<li class="bot-msg">${msg}</li>`);
        speak(msg);
        return sleep(calcTimeToWait(msg));
    }).then(function () {
        $(".user-welcome-respone").append(`<button id="talk-no" onclick="talkNoClicked()" type="button" class="btn btn-secondary">No</button>
                        <button id="talk-yes" onclick="talkYesClicked()" type="button" class="btn btn-primary" data-dismiss="modal">Ok, let's
                            talk
                        </button>`);
        sleep(10000).then(function () {
            if (!userResponsedForWelcome) {
                startNewConversation();
            }
        });
    });
}


function talkNoClicked() {
    userResponsedForWelcome = true;
    startNewConversation();
}

function startNewConversation() {
    sleep(20000).then(function () {
        $("#messages").empty();
        $('#request-answer-modal').hide();
        $('#play-video-modal').hide();
        $('.modal-backdrop').hide();
        $(".play-1").remove();
        $("#welcome-page-modal ul").empty();
        $(".user-welcome-respone").empty();
        userResponsedForWelcome = false;
        changeBot("heart");
        openWelcomeModal();
        sleep(3000).then(function () {
            takeSnapshot();
        });
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


