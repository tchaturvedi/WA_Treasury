
from datetime import datetime

from flask import Flask, render_template, redirect, request, jsonify
from flask_flatpages import FlatPages
from slugify import slugify
from util import buildChartInfo
from charts import piechartlib, barchartlib, linechartlib


######################
# Configurations
######################
import conf

######################
# Helper Fucntions
######################

# this function creates a dictionary of hierachy of the content folder
# root
# - 2nd level
#  - 3rd level
#   - .....
def createTableContentDictionary():
    tableDict = {}
    tableDict['/'] = []
    pageList = []
    for page in pages:
        pageList.append(page)
    pageList.sort(key=lambda x: x.meta['order'])

    for orderPage in pageList:
        # split the page path 1/11/111 into list [1, 11, 111]
        path = orderPage.path.split('/')

        # file in root folder
        if len(path) == 1:
            tableDict['/'].append(path[0])
        else:
            # iterate the path and turn it into a dictionary [1, 2, 3, 4]
            # => {1: 2, 3: 4}
            i = iter(path)
            pathDict = dict(zip(i, i))
            index = 0
            update = False

            # if in the same path we add files to that path
            # otherwise it is a new path
            for resource in tableDict['/']:
                if type(resource) is dict and path[0] in resource.keys():
                    for k in pathDict.keys():
                        if k in resource.keys():
                            if type(resource[k]) is list:
                                resource[k].append(pathDict[k])
                            else:
                                tempList = [resource[k], pathDict[k]]
                                resource[k] = tempList
                        else:
                            resource[k] = pathDict[k]
                    update = True
                index += 1
            if not update:
                tableDict['/'].append(pathDict)
    return tableDict

# recursively turn the dictionary hierchy into html list elements
def concatTOC(resources, sublevelValues, currentLevel, fullPath):
    newString = "<li>" + currentLevel.upper() + "<ul>"

    for sublevels in sublevelValues:
        if type(sublevels) is not str:
            for sublevel in sublevels:
                if sublevel in resources.keys():
                    newString += concatTOC(resources, resources[sublevel], sublevel, fullPath+"/"+sublevel)
                else:
                    newString += "<li><a href='/%s/%s'>%s</a></li>" % (slugify(fullPath), slugify(sublevel), sublevel.upper())
        else:
            newString += "<li><a href='/%s/%s'>%s</a></li>" % (slugify(fullPath), slugify(sublevels), sublevels.upper())
    newString += "</ul></li>"
    return newString



######################
# Initialization
######################
app = Flask(__name__)
app.config.from_object(conf)
pages = FlatPages(app)

# generate the Table of content and page slugs from the title
# exclude the index page as its can be accessed by clicking on the page logo
TOC = createTableContentDictionary()
TOCString = "<ul class='nav' id='side-menu'>"
for resources in TOC.values():
    for resource in resources:
        if type(resource) is str:
            if resource != "index":
                TOCString += "<li><a href='/%s'>%s</a></li>" % (slugify(resource), resource.upper())
        else:
            for key in resource.keys():
                TOCString += concatTOC(resource, resource.values(), key, "/"+key)
TOCString += "</ul>"

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
    path = str(path).replace("-", " ").lower()
    page = pages.get_or_404(path)
    charts = buildChartInfo(page.html)
    chartdic = {}
    for chart in charts:
        if 'bar' in chart:
            chartdic[chart] = barchartlib.createBarChart(chart)
        elif 'line' in chart:
            chartdic[chart] = linechartlib.createLineChart(chart)
    return render_template('page.html', page=page, toc=TOCString, year=datetime.now().year, chartInfo=chartdic)


@app.route('/createPieChart', methods=['POST'])
def createPieChart():
    sentInData = request.get_json(force=True)
    chart = None
    for key in sentInData.keys():
        chart = key
    createPie = piechartlib.CreatePieChart(sentInData[chart]["label"], chart)
    return jsonify(createPie.createPieChart())

if __name__ == '__main__':
    app.run(debug=conf.DEBUG)