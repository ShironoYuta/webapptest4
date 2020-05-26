from simulator_app import simulator_app
from app import app
from flask import render_template, request
from flask import Flask, render_template, request, jsonify, json, make_response
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import os.path
import pandas as pd
import codecs
import MyModules
import definition

@app.route('/')
def index():
    return render_template('calc.html')


@app.route('/simulate')
def simulate():
# This function read two parameters from web request
# Returns the sum of two parameters.

    Algo = request.args.get('input1')
    Term = request.args.get('input2')
    AitaiM = []
    AitaiN = []
    for i in range(12):
        key = "input"+str(i+3) 
        AitaiM.append(int(request.args.get(key)))
        key = "input"+str(i+15) 
        AitaiN.append(int(request.args.get(key)))
    # replace the next line with your simulator
    output1,output2 = definition.AnnualCost(Algo,Term,AitaiM,AitaiN)
    json_str = '{"output1":' + str(output1) +',"output2":' +str(output2) +'}'
    json_data = json.loads(json_str)
    # write your output to a file
    with open('./data/inputs.csv', 'r') as f:
        reader = csv.reader(f)
        testlist = list(reader)
        for row in reader:
            inputs = [row for row in reader]
    #inputnum = "input" + str(len(inputs) + 1)
    inputnum = "input" + str(len(testlist) + 1)
    li = [inputnum, json_data["output1"], json_data["output2"]]
    #inputs.append(li)
    testlist.append(li)
    with open('./data/inputs.csv', 'a') as f:
        writer = csv.writer(f,lineterminator='\n')
        writer.writerow(li)
    return  json_str

@app.route('/graph1.png',methods=["GET", "POST"])
def graph1():
    # データからグラフをプロットする
    #parame1 = request.form["param1"]
    #parame1 = 12345
    #x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    #y = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    Annual = request.args.get('input1')
    Scenario = request.args.get('input2')
    Simutype = request.args.get('input3')
    Month = request.args.get('input4')
    Algo = request.args.get('input5')
    Term = request.args.get('input6')

    aitaiM = []
    aitaiN = []
    for i in range(12):
        key = "input"+str(i+7) 
        aitaiM.append(int(request.args.get(key)))
        key = "input"+str(i+19) 
        aitaiN.append(int(request.args.get(key)))

    if Annual == "年間コスト":
        ans = definition.AnnualGraph()
        return ans
    elif Simutype == "月コ":
        if Scenario == "2019":
            ans = definition.OutputMonthlyCost_1(Algo,Term,aitaiM,aitaiN,Month)
            return ans
        else:
            ans = definition.OutputMonthlyCost(Algo,Term,aitaiM,aitaiN,Month)
            return ans
    elif Simutype == "日コ":
        if Scenario == "2019":
            ans = definition.OutputDailyCost_1(Algo,Term,aitaiM,aitaiN,Month)
            return ans
        else:
            ans = definition.OutputDailyCost(Algo,Term,aitaiM,aitaiN,Month)
            return ans
    elif Simutype == "月イ":
        if Scenario == "2019":
            ans = definition.OutputMonthlyInb(Algo,Term,aitaiM,aitaiN,Month)
            return ans
        else:
            ans = definition.OutputMonthlyInb_1(Algo,Term,aitaiM,aitaiN,Month)
            return ans
    elif Simutype == "日イ":
        if Scenario == "2019":
            ans = definition.OutputDailyInb(Algo,Term,aitaiM,aitaiN,Month)
            return ans
        else:
            ans = definition.OutputDailyInb_1(Algo,Term,aitaiM,aitaiN,Month)
            return ans


@app.route('/reset',methods=["GET", "POST"])
def reset():
    with open('./data/inputs.csv',"w") as f:
        pass
    return