function rateMeModal() {
    $('#rate-me-modal').modal();
}

$(".star").hover(function () {
   var starId = this.id;
    for (let i = 1; i <= Number(starId[4]); i++) {
        $(`#star${i}`).removeClass();
        $(`#star${i}`).addClass("fa fa-star star");
    }
    for (let i = Number(starId[4])+1; i <= 5; i++) {
         $(`#star${i}`).removeClass();
         $(`#star${i}`).addClass("far fa-star star");
         $(`#star${i}`).attr("aria-hidden", "true");
    }
});

$(".star").click(function () {
    var starId = this.id;
    for (let i = 1; i <= Number(starId[4]); i++) {
        $(`#star${i}`).removeClass();
        $(`#star${i}`).addClass("fa fa-star star");
    }
});

