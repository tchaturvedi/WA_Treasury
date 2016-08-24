import json
from sodapy import Socrata


def createLineChart(charttype):
    with open("database_charts/chartconfig.json") as config:
        jsonData = json.load(config)

    chart = jsonData[charttype]
    chartTitle = chart['chart-title']
    dataTitle = chart['data-title']
    colors = chart['color']
    yFormat = chart['y-axis-format']
    xaxis = chart['x-axis']
    items = chart['y-axis']

    with open("database_charts/url_info.json") as urlConfig:
        urlInfo = json.load(urlConfig)
    client = Socrata(urlInfo['url'], None, username=urlInfo['username'], password=urlInfo['password'])


    data = []
    for item in items:
        dict = {
            "type": "line",
            "name": item.replace("_", " "),
            "cursor": "pointer",
            "showInLegend": True,
            "color": colors[0]
        }
        request = client.get(dataTitle, select=xaxis + ", " + item)
        dataPoints = []
        for r in request:
            if len(r) > 1:
                num = r[item].replace("%", "")
                print(num)
                d = {
                    "label": int(r[xaxis]),
                    "y": float(num)/100.0 if num.replace(".", "").isdigit() else None
                }
            if d['label'] is not None:
                dataPoints.append(d)

        dict["dataPoints"] = dataPoints
        data.append(dict)

        # Create Chart Information
        chartInfo = {}
        chartInfo["chartTitle"] = chartTitle
        chartInfo["data"] = data
        chartInfo["json"] = json.dumps(data)
        chartInfo["valueFormat"] = yFormat
    return chartInfo