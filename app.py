from datetime import datetime
from flask import Flask, render_template, redirect, request, jsonify
import json, os
from flask_flatpages import FlatPages
from openpyxl import load_workbook
import conf
from slugify import slugify

class App():

    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object(conf)
        self.pages = FlatPages(self.app)

        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/<path:pagename>', 'page', self.page)
        self.app.add_url_rule('/createPieChart', 'createPieChart', self.createPieChart, methods=["POST"])

        # generate the Table of content and page slugs from the title
        # exclude the index page as its can be accessed by clicking on the page logo
        self.toc = [(page['title'], slugify(page['title'])) for page in self.pages if page['title'] != 'Index']

    def index(self):
        # redirect to index page if current page is pointing to '/'
        return redirect('index')

    def page(self, pagename):

        chart1Info = self.getChart1Info()
        for page in self.pages:
            if pagename == slugify(page['title']):
                return render_template('page.html', page=page, toc=self.toc, year=datetime.now().year, chart1Info=chart1Info)
        return render_template('404.html', toc=self.toc)

    def getChart1Info(self):
        wb = load_workbook(filename="static/Debt Affordability Study Data.xlsx", data_only=True)
        sheet = wb.get_sheet_by_name('Outstanding (Fig 2)')

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
            for row in sheet.iter_rows(row_offset=3):
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
            chartInfo["chartTitle"] = "Outstanding Bonds and COPs FY 2000-2016 ($ Billions)"
            chartInfo["data"] = data
            chartInfo["json"] = json.dumps(data)
        return chartInfo

    def createPieChart(self):
        sentInData = request.get_json(force=True)
        chart = None
        for key in sentInData.keys():
            chart = key

        if chart == "chart1":
            return jsonify(self.getPieChartInfo(sentInData[chart]["label"], self.getChart1Info()))
        elif chart == "chart2":
            return jsonify(self.getPieChartInfo(sentInData[chart]["label"], self.getChart2Info()))
        elif chart == "chart3":
            return jsonify(self.getPieChartInfo(sentInData[chart]["label"], self.getChart3Info()))
        elif chart == "chart4":
            return jsonify(self.getPieChartInfo(sentInData[chart]["label"], self.getChart4Info()))

    def getPieChartInfo(self, year, chartInfo):
        oldData = chartInfo["data"]
        newData = []
        dic = {
            "type": "pie",
            "showInLegend": True,
            "toolTipContent": "{y} - #percent %",
            "yValueFormatString": "#0.#,,. Million",
            "legendText": "{indexLabel}",
        }
        dataPoints = {}
        for item in oldData:
            for dataItem in item["dataPoints"]:
                if dataItem["label"] == year:
                    if item["name"] not in dataPoints.keys():
                        dataPoints[item["name"]] = {"y": dataItem["y"], "indexLabel": item["name"]}
                    else:
                        dataPoints[item["name"]]["y"] += dataItem["y"]

        for item in dataPoints:
            newData.append(dataPoints[item])

        dic["dataPoints"] = newData
        pieChartInfo = {}
        pieChartInfo["title"] = "Detailed Data " + str(year)
        pieChartInfo["data"] = dic
        pieChartInfo["json"] = json.dumps(dic)
        return pieChartInfo
