Highcharts.theme = {
    title: {
        style: {
            color: '#000',
            font: 'bold 16px "Helvtica", Arial, sans-serif'
        }
    },
    subtitle: {
        style: {
            color: '#666666',
            font: 'bold 12px "Helvtica", Arial, sans-serif'
        }
    },
    legend: {
        itemStyle: {
            font: '9pt Helvtica, Arial, sans-serif',
            color: 'black'
        },
        itemHoverStyle:{
            color: 'gray'
        }   
    }
};
// Apply the theme
Highcharts.setOptions(Highcharts.theme);

Highcharts.chart('container', {
    chart: {
        type: 'bar'
    },
    title: {
        text: 'League Summary'
    },
    subtitle: {
        text: 'ESPN Fantasy Sports'
    },
    xAxis: {
        categories: ['Points', 'Rebounds', 'Assists', 'Blocks', 'Steals'],
        title: {
            text: null
        }
    },
    yAxis: {
        min: 0,
        title: {
            text: '',
            align: 'high'
        },
        labels: {
            overflow: 'justify'
        }
    },
    tooltip: {
        valueSuffix: ' units'
    },
    plotOptions: {
        bar: {
            dataLabels: {
                enabled: true
            }
        }
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'top',
        x: -40,
        y: 280,
        floating: true,
        borderWidth: 1,
        backgroundColor:
            Highcharts.defaultOptions.legend.backgroundColor || '#FFFFFF',
        shadow: true
    },
    credits: {
        enabled: false
    },
    series: createSeries(roster_data)
});


function createSeries(data) {
    var updatedData = []
    for (var i = 0; i < data.length; i++) {
        tmp = {
            "name": data[i]["teamId"],
            "data": [data[i]["points"], data[i]["rebounds"], data[i]["assists"], data[i]["blocks"], data[i]["steals"]]
        }
        updatedData.push(tmp)
    }
    return updatedData
}