import json
from sodapy import Socrata

def createBarChart(charttype):
    with open("database_charts/chartconfig.json") as config:
        jsonData = json.load(config)
    config.close()
    chart = jsonData[charttype]

    chartTitle = chart['chart-title']
    dataTitle = chart['data-title']
    yFormat = chart['y-axis-format']

    xaxis = chart['x-axis']
    items = chart['y-axis']
    colors = chart['color']

    with open("database_charts/url_info.json") as urlConfig:
        urlInfo = json.load(urlConfig)
    client = Socrata(urlInfo['url'], None, username=urlInfo['username'], password=urlInfo['password'])

    colorIndex = 0
    data = []

    for item in items:
        dict = {
            "type": chart["chart-type"],
            "legendText": item.replace("_", " "),
            "cursor": "pointer" if len(items) > 1 else "default",
            "showInLegend": True,
            'legendMarkerColor': colors[colorIndex],
            "toolTipContent": item.replace("_", " ") + " in year " + "{label}: {y}"
        }

        dataPoints = []
        request = client.get(dataTitle, select=xaxis + ", " + item)
        for r in request:
            if len(r) > 1:
                d = {
                    "label": int(r[xaxis]),
                    "y": int(r[item]),
                    "color": colors[colorIndex],
                }
            if d['label'] is not None:
                dataPoints.append(d)
        colorIndex += 1

        dict["dataPoints"] = dataPoints
        data.append(dict)

        # Create Chart Information
        chartInfo = {}
        chartInfo["chartTitle"] = chartTitle
        chartInfo["data"] = data
        chartInfo["json"] = json.dumps(data)
        chartInfo["valueFormat"] = yFormat
        chartInfo['addClick'] = False if len(items) == 1 else True
    return chartInfo
