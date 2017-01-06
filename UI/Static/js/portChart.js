function drawPortChart(elementId, portName="", startDate=0, endDate=0, dataPoints=0) {
    moment.locale('de');

    //das Canvaselement auf dem der Chart erstellt werden soll.
    ctx = $("#" + elementId + " > canvas");
    ctx.hide();

    //Wenn der Portname nicht angegeben wird, benutze den Portnamen vom ctx.
    if (portName == "") {
        portName = ctx.attr('portname');
    }

    //zeige Ladebalken
    loadingBar = $("#" + elementId + " > .progress");
    loadingBar.show();
    //Infobox
    infoBox = $("#" + elementId + " > .alert");
    infoBox.hide()
    //zunächst Infos zum Port holen.
    var portUnit = ""
    $.getJSON("/api/currentStatus", {portName: portName}, function(data) {
        portUnit = data.settings.unit;

        //im dataset sind alle Messdaten des Abfragezeitraums.
        var dataset = []
        //alle Labels zum Graphen.
        var labels = []

        //Die Logdaten abrufen
        requestData = {
            portName: portName,
            startDate: startDate.format('X'),
            endDate: endDate.format('X'),
            aboutPoints: dataPoints,
        }
        $.getJSON("/api/getLog", requestData, function(rawData) {
            for (var i = 0; i < rawData.length; i++) {
                dataset.push({x: rawData[i][1], y: rawData[i][2]});
                labels.push(rawData[i][1])
            }

            //das eigentliche Chartelement.
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
            if (dataPoints > 0) {
                infoBox.show();
            }
            ctx.show();
            ctx.attr('portname', portName)
            loadingBar.hide();
        });
    });
}