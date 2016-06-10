function createChart(data, options){
    this.data = data;
    this.options = options;
    this.createBarChart = function(){
        var self = this;
        for(var i = 0; i < data.length; i++) {
            var pieId= self.options.id.replace("bar", "pie");
            data[i]["click"] = function(e){
                // Create container if doesnt exists
                if ($('#parentPieChartContainer').length == 0){
                    var button = $('<button/>',{
                        type: 'button',
                        text: 'x',
                        class: 'button-primary',
                        click: function () {
                            $("#parentPieChartContainer").remove()
                        }
                    });
                    var parentPieChartContainer = $('<div/>', {
                        id: 'parentPieChartContainer',
                        style:"padding-top: 20px; margin-bottom: 40px; height: 450px"
                    });
                    var pieChartContainer = $('<div/>', {
                        id: pieId
                    });
                    $(parentPieChartContainer).insertAfter($('#' + self.options.id));
                    $('#parentPieChartContainer').append(button);
                    $('#parentPieChartContainer').append(pieChartContainer);
                }

                sendInData = new Object();
                sendInData[pieId] = e.dataPoint;
                $.ajax({
                    type: "POST",
                    url: "/createPieChart",
                    data: JSON.stringify(sendInData),
                    dataType: "json",
                    success: function(data){
                        var pieChart = new CanvasJS.Chart(pieId
                            , {
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
            };
        }

        var chart = new CanvasJS.Chart(self.options.id, {
            theme: self.options.theme,
            title:{
                text: self.options.title
            },
            data: self.data
        });
        chart.render();
    };
}