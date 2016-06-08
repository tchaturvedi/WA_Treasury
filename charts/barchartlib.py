import json
from openpyxl import load_workbook

def createBarChart():
    with open("charts/barchartconfig.json") as config:
        jsonData = json.load(config)

    chart = jsonData['chart1']
    chartTitle = chart['chart-title']
    dataTitle = chart['data-title']
    rowOffset = chart['row-offset']

    wb = load_workbook(filename="static/Debt Affordability Study Data.xlsx", data_only=True)
    sheet = wb[dataTitle]

    items = ["VP GO", "MVFT GO", "Triple Pledge", "GARVEEs", "TIFIA", "State COPs"]
    data = []

    for item in items:
        dict = {
            "type": "stackedColumn",
            "name": item,
            "cursor": "pointer",
            "showInLegend": True
        }

        dataPoints = []
        for row in sheet.iter_rows(row_offset=int(rowOffset)):
            if item == "VP GO":
                d = {
                    "label": row[0].value,
                    "y": row[1].value
                }
            elif item == "MVFT GO":
                d = {
                    "label": row[0].value,
                    "y": row[2].value
                }
            elif item == "Triple Pledge":
                d = {
                    "label": row[0].value,
                    "y": row[3].value
                }
            elif item == "GARVEEs":
                d = {
                    "label": row[0].value,
                    "y": row[4].value
                }
            elif item == "TIFIA":
                d = {
                    "label": row[0].value,
                    "y": row[5].value
                }
            else:
                d = {
                    "label": row[0].value,
                    "y": row[5].value
                }
            if d["label"] != None:
                dataPoints.append(d)

        dict["dataPoints"] = dataPoints
        data.append(dict)

        # Create Chart Information
        chartInfo = {}
        chartInfo["chartTitle"] = chartTitle
        chartInfo["data"] = data
        chartInfo["json"] = json.dumps(data)
    return chartInfo