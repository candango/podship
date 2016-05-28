steal("jquery", "can", "can/model", "can/view/stache", "./post_form", function($, can) {

    $("#stream_post").html(can.stache("<stream-post></stream-post>")());
});
