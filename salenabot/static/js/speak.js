var english_voice = '';
$(document).ready(function() {
    speechSynthesis.onvoiceschanged = function () {
        // get all voices that browser offers
        var available_voices = speechSynthesis.getVoices();

        for (var i = 0; i < available_voices.length; i++) {
            if (available_voices[i].lang.toLowerCase().includes('en')) {
                if (available_voices[i].name.toLowerCase().includes("female")) {
                    english_voice = available_voices[i];
                    break;

                }
            }
        }
        if (english_voice === '')
            english_voice = available_voices[0];

    };
});

function speak(msg) {
// new SpeechSynthesisUtterance object
    var utter = new SpeechSynthesisUtterance();
    utter.rate = 0.8;
    utter.pitch = 1;
    utter.text = msg;
    utter.voice = english_voice;

// speak
    window.speechSynthesis.speak(utter);
}