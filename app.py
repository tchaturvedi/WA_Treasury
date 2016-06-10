from datetime import datetime

from flask import Flask, render_template, redirect, request, jsonify
from flask_flatpages import FlatPages
from slugify import slugify
from util import buildChartInfo
from charts.piechartlib import CreatePieChart
from charts.barchartlib import createBarChart
import re

######################
# Configurations
######################
import conf

######################
# Initialization
######################
app = Flask(__name__)
app.config.from_object(conf)
pages = FlatPages(app)

# generate the Table of content and page slugs from the title
# exclude the index page as its can be accessed by clicking on the page logo
TOC = [(page['title'], slugify(page['title'])) for page in pages if page['title'].lower() != 'index']

######################
# Routes
######################

@app.route('/')
def index():
    return redirect('index')


@app.route('/<path:path>')
def page(path):
    '''
        Entry point for each page based on the page slug
    '''

    page = pages.get_or_404(path)
    charts = buildChartInfo(page.html)
    chartdic = {}
    for chart in charts:
        chartdic[chart] = createBarChart(chart)
    return render_template('page.html', page=page, toc=TOC, year=datetime.now().year, chartInfo=chartdic)


@app.route('/createPieChart', methods=['POST'])
def createPieChart():
    sentInData = request.get_json(force=True)
    chart = None
    for key in sentInData.keys():
        chart = key
    createPie = CreatePieChart(sentInData[chart]["label"], chart)
    return jsonify(createPie.createPieChart())

if __name__ == '__main__':
    app.run(debug=conf.DEBUG)