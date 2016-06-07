function createBarChart(data, options) {
    for(var i = 0; i < data.length; i++) {
            data[i]["click"] = showPieChart;
        }

    var chart = new CanvasJS.Chart("chart1", {
        theme: options.theme,
        title:{
            text: options.title
        },
        data: data
    });
    chart.render();
}

function showPieChart(e){
    // Create container if doesnt exists
    if ($('#parentPieChartContainer').length == 0){
        var button = $('<button/>',{
            type: 'button',
            text: 'x',
            class: 'button-primary',
            click: function () {
                $("#parentPieChartContainer").remove()
            }
        })
        var parentPieChartContainer = $('<div/>', {
            id: 'parentPieChartContainer',
            style:"padding-top: 20px; margin-bottom: 40px"
        })
        var pieChartContainer = $('<div/>', {
            id: 'pieChartContainer'
        })
        $('#parentChartContainer').append(parentPieChartContainer)
        $('#parentPieChartContainer').append(button)
        $('#parentPieChartContainer').append(pieChartContainer)
    }

    $.ajax({
        type: "POST",
        url: "/createPieChart",
        data: JSON.stringify({"chart1": e.dataPoint}),
        dataType: "json",
        success: function(data){
            var pieChart = new CanvasJS.Chart("pieChartContainer", {
                title:{
                    text: data["title"]
                },
                legend: {
                    maxWidth: 350,
                    itemWidth: 120
                },
                data: [data["data"]]
            });
            pieChart.render();
        }
    });
}