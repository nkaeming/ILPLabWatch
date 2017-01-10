function drawPortChart(portName="", startDate=null, endDate=null, dataPoints=0) {
    moment.locale('de');

    elementId = 'portChart';

    //das Canvaselement auf dem der Chart erstellt werden soll.
    ctx = $("#" + elementId + " > canvas");
    ctx.hide();

    //Wenn der Portname, das Start oder Enddatum nicht angegeben wird, benutze den Portnamen, Start oder Enddatum vom ctx.
    if (portName == "") {
        portName = ctx.data('portName');
    } else {
        ctx.data('portName', portName);
    }
    if (startDate != null) {
        ctx.data('startDate', startDate);
    }
    if (endDate != null) {
        ctx.data('endDate', endDate);
    }

    portName = ctx.data('portName');
    startDate = ctx.data('startDate');
    endDate = ctx.data('endDate');

    //zeige Ladebalken
    loadingBar = $("#" + elementId + " > .progress");
    loadingBar.show();
    //Infobox
    infoBox = $("#" + elementId + " > .alert");
    infoBox.hide();
    //Datenpunktauswahl setzen
    $('#portChartPointsInput').val(dataPoints);
    //zunächst Infos zum Port holen.
    var portUnit = ""
    $.getJSON("/api/currentStatus", {portName: portName}, function(data) {
        portUnit = data.settings.unit;
        var yAxisString = "";

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

            //zerstöre das alte Chartelement sofern nötig.
            if(ctx.data('chartInstance') != null){
                ctx.data('chartInstance').destroy();
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
                        }],
                        yAxes: [{
                            scaleLabel:{
                                labelString: portUnit,
                                display: true,
                            }
                        }]
                    },
                    title: {
                        display: true,
                        text: "Portname: " + portName,
                    },
                    legend: {
                        display: false,
                    },
                    animation: {
                        duration: 0,
                    }
                },
            });
            ctx.data('chartInstance', myLineChart);
            if (dataPoints > 0) {
                infoBox.show();
            }
            ctx.show();
            loadingBar.hide();
        });
    });
}

$('#portChartRedrawByPoints').mouseup(function(){
    drawPortChart("", null, null, $('#portChartPointsInput').val());
});

$('#portChartPointsInput').keyup(function(e){
    var code = e.which;
    if(code==13)e.preventDefault();
    if(code==32||code==13||code==188||code==186){
        drawPortChart("", null, null, $('#portChartPointsInput').val());
    }
});