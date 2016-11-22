var ctx = document.getElementById("myChart");
var data = [];
$.getJSON("/rawLogs/Test", function(rawJson){
  $.each(rawJson, function(key, value){
    data.push({x: key*1000, y: Number(value)});
  });
}).done(function () {
var myChart = new Chart(ctx, {
    type: 'line',
    data: {datasets: [{
            label: 'Test',
            data: data,
            fill: false,
            borderColor: "rgba(188, 0, 0, 0.5)",
            backgroundColor: "rgba(188, 0 , 0, 0.8)"
        }]},
    options: {
      scales: {
        xAxes: [{
          type: "time",
          time: {
            tooltipFormat: "DD.MM.YYYY HH:mm:ss",
            displayFormats: {
              minute: "Do MMM HH:mm:ss",
              second: "Do MMM HH:mm:ss",
              millisecond: "Do MMM HH:mm:ss",
            }
          }
        }]
      }
    }
});
});