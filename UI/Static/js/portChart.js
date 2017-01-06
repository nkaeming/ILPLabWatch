function drawPortChart(elementId, portSettings, startDate, endDate) {
    moment.locale('de');
    var ctx = document.getElementById(elementId);
    var portName = portSettings.name;
    var unit = portSettings.unit;
    $.getJSON("/api/getLog", {
            portName: portName,
            startDate: startDate,
            endDate: endDate
        },
        function (rawData) {
            var dataset = [];
            var labels = [];
            for (var i = 0; i < rawData.length; i++) {
                dataset.push({x: rawData[i][1], y: rawData[i][2]});
                labels.push(rawData[i][1]);
            }

            var myLineChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        data: dataset,
                        label: portName,
                        radius: 0,
                        borderColor: 'rgba(41, 59, 179, 1)',
                        backgroundColor: 'rgba(41, 59, 179, 0.1)',
                    }]
                },
                options: {
                    scales: {
                        xAxes: [{
                            ticks: {
                                //min: labels[0],
                                //max: labels[labels.length - 1],
                                callback: function(value) {
                                    return moment.unix(value).format('L LTS');
                                },
                                beginAtZero: false,
                                fontFamily: 'sans-serif',
                            }
                        }]
                    },
                    title: {
                        display: true,
                        text: portName,
                    },
                    legend: {
                        display: false,
                    },
                    animation: {
                        duration: 0,
                    }
                },
            });
        });
}