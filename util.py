import json
import re
from htmldom import htmldom

from flask_flatpages.utils import pygmented_markdown

CUSTOM_CHART_RE = r'[--]{2}(?P<name>.+)[:](?P<footnote>.+)[|](?P<config>.+)[--]{2}'
CHART_DEFAULT_STYLE = '{"height":"300px", "width":"100%", "margin-bottom":"10px"}'
CHART_CONTAINER_TMPL = "<div id='parentChartContainer'>" \
                        "<div id='chartId' style='chartStyle' class='chartContainer'>" \
                        "</div>" \
                        "<div id='chartFootnote'>" \
                            "footnoteText" \
                        "</div>" \
                       "</div>"


def chart_renderer(text):
    '''
        This function matches the chart tag in the
        text and replaces it with the chart container
    '''
    matchedObject = re.finditer(CUSTOM_CHART_RE, text)
    if matchedObject is not None:
        for mo in matchedObject:
            print(mo.group('name'))
            chart_html = makeHtml(CHART_CONTAINER_TMPL, mo)
            text = re.sub(CUSTOM_CHART_RE, chart_html, text)
        return pygmented_markdown(text)
    return pygmented_markdown(text)


def makeHtml(tmpl, matchedObject):
    '''
    Extract and replace the values from text file into html template
    :param tmpl: Input template
    :param matchedObject: Regex object matching the chart tag
    :return: updated template with correct values
    '''
    name = matchedObject.group('name')
    footnote = matchedObject.group('footnote')
    config = parseConfig(matchedObject.group('config'))

    if len(config) == 0:
        config = parseConfig(CHART_DEFAULT_STYLE)


    html = re.sub(r'chartId', name, tmpl)
    html = re.sub(r'chartStyle', getChartStyle(config), html)
    html = re.sub(r'footnoteText', footnote, html)

    return html

def getChartStyle(config):
    styleAttr = []
    for key in config.keys():
        prop = key + ":" + config[key]
        styleAttr.append(prop)
    return ";".join(styleAttr)

def parseConfig(configStr):
    return json.loads(configStr)


def buildChartInfo(html_text):
    dom = htmldom.HtmlDom().createDom(html_text)
    charts = dom.find("div[class=chartContainer]")
    # for chart in charts:
    #     print(chart.attr('id'))