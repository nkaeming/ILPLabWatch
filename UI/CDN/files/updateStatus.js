$(function(){
    var intervalID;
    var sec = 0.5;
    intervalID = setInterval(refresh, sec * 1000);

    function refresh() {
        $.getJSON("/rawCurrentState", function (data) {
            $.each(data, function (index) {
                var name = data[index].name;
                var state = data[index].state;
                $("#current-Value-of-" + name).text(state);
            });
        });
    }
});