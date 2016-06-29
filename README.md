# VisualizationProject improved 

## Content Folder Description
The content folder is root folder for all the pages shown on our website.
Every page that you want to display should be added to under this folder in .md. 
You can also group several files and put them inside a subdirectory under content folder

For instance:
* Content
  * firstpage.md
  * secondpage.md
  * first subdirectory
    * firstnested.md
    * secondnested.md
    * thirdnested.md
  * thirdpage.md

All of these files and subdirectories name need to be lower case with **NO** special characters

Inside each .md files you will see a key word *order* followed by a colon and a number starting from 0.
This is how the program recognize where in the table of contents should should every page tab link appear.

The rest of these files are straight forward Markdown Language

## Chart Folder Description

The chart folder contains four different files including the library files and line chart library, pie chart library and chart config file.
Those library files indicate the type of chart could be created. Now there are three different types of charts including bar chart, line chart and pie chart.
When more types of charts are needed to be added, the library file of the new chart type should be added in the chart folder.

When adding a new chart, the config file should be modified. The template for adding a new chart is as follows.

"chart1-bar" (chartNumber-chartType): {
<br>&nbsp;&nbsp;&nbsp;"chart-type": "stackedColumn" [1],
<br>&nbsp;&nbsp;&nbsp;"chart-title": "chart title" ,
<br>&nbsp;&nbsp;&nbsp;"data-title": "tab name" [2],
<br>&nbsp;&nbsp;&nbsp;"x-axis": 0 [3],
<br>&nbsp;&nbsp;&nbsp;"y-axis": [{"VP GO": 1}, {"MVFT GO": 2}, {"Triple Pledge": 3}, {"GARVEEs": 4}, {"TIFIA": 5}, {"State COPs": 6}] [4],
<br>&nbsp;&nbsp;&nbsp;"y-axis-format": "$#,,,." [5],
<br>&nbsp;&nbsp;&nbsp;"row-offset": 3 [6],
<br>&nbsp;&nbsp;&nbsp;"color": ["#4F81BD", "#9BBB59", "#4BACC6", "#F79646", "#953735", "#8064A2"] [7]
<br>}

[1] different chart type options: "stackedColumn", "column", "pie", "line"
[2] tab name where the data will be read from in excel
[3] where data will start reading on x-axis
[4] a list of categories and their corresponding column positions in excel worksheet
[5] the format y-axis will be displayed in
[6] row offset where the data will be started reading
[7] hex color codes of all the categories


