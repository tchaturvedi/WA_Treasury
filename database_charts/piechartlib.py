import json
from sodapy import Socrata

class CreatePieChart():

    def __init__(self, year, chartType):
        self.year = year
        self.chartType = chartType

    def createPieChart(self):
        with open("database_charts/chartconfig.json") as config:
            data = json.load(config)

        chartconfig = {}
        for key, value in data.items():
            if key == self.chartType:
                chartconfig = value

        # The position index from the excel file
        xaxis = chartconfig['x-axis']
        # An array of dictionary with Name of the category and index in excel file
        yaxis = chartconfig['y-axis']

        charttitle = chartconfig['chart-title']
        datatitle = chartconfig['data-title']
        colors = chartconfig['color']
        colorIndex = 0

        with open("database_charts/url_info.json") as urlConfig:
            urlInfo = json.load(urlConfig)
        client = Socrata(urlInfo['url'], None, username=urlInfo['username'], password=urlInfo['password'])

        request = client.get(datatitle, select=",".join(yaxis), where=xaxis + "=" + str(self.year))[0]
        newData = []
        dic = {
            "type": "pie",
            "showInLegend": True,
            "toolTipContent": "{y} - #percent %",
            "yValueFormatString": "#0.#,,. Million",
            "legendText": "{indexLabel}",
        }
        dataPoints = {}
        for cat in yaxis:
            if cat in request.keys() and int(request[cat]) > 0:
                if cat not in dataPoints.keys():
                    dataPoints[cat] = {'y': int(request[cat]), 'indexLabel': cat.replace("_", " "),
                                       'legendMarkerColor': colors[colorIndex], 'color': colors[colorIndex]}
                else:
                    dataPoints[cat]['y'] += int(request[cat])
            colorIndex += 1

        for item in dataPoints:
            newData.append(dataPoints[item])

        dic['dataPoints'] = newData
        pieChartInfo = {}
        pieChartInfo['title'] = charttitle + str(self.year)
        pieChartInfo['data'] = dic
        pieChartInfo['json'] = json.dumps(dic)
        return pieChartInfo