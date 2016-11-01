$(function(){
    var intervalID;
    var sec = 1;
    intervalID = setInterval(refresh, sec * 1000);

    function refresh() {
        $.getJSON("/rawCurrentState", function (data) {
            $.each(data, function (index) {
                var name = data[index].name;
                var state = data[index].state;
                if (state == 1){
                    $("#" + name).attr("class", "input-status red");
                    $("#" + name).text(state);
                } else {
                    $("#" + name).attr("class", "input-status green");
                    $("#" + name).text(state);
                }
            });
        });
    }
});