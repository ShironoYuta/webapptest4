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
import MyModules


def AnnualCost(algo,term,aitaiM,aitaiN):#相対はリスト

    Sce1 = []
    Sce2 = []
    Sce3 = []
    Sce4 = []
    FileName_pre = term + "_" + algo + "_Tokyo_"
    for i in range(12):
        FileName = FileName_pre + str(i+1) + "_" + str(aitaiM[i])+"_M" + ".csv"
        FileDir = str(term) + "_" + str(algo) + "_Tokyo_M/"
        FilePath_soutai = 'scenarios/'+ FileDir + FileName
        base = os.path.dirname(os.path.abspath(__file__))
        FilePath = os.path.normpath(os.path.join(base, FilePath_soutai))
        #data = pd.read_csv(FilePath,header = None, encoding="shift-jis").values.tolist()
        data = pd.read_csv(FilePath_soutai,header = None, encoding="shift-jis").values.tolist()
        Sce1 += data[0]
        Sce2 += data[1]
        Sce3 += data[2]
        Sce4 += data[3]
    for i in range(12):
        FileName = FileName_pre + str(i+1) + "_" + str(aitaiN[i])+"_N" + ".csv"
        FileDir = str(term) + "_" + str(algo) + "_Tokyo_N/"
        FilePath_soutai = 'scenarios/'+ FileDir + FileName
        base = os.path.dirname(os.path.abspath(__file__))
        FilePath = os.path.normpath(os.path.join(base, FilePath_soutai))
        #data = pd.read_csv(FilePath,header = None, encoding="shift-jis").values.tolist()
        data = pd.read_csv(FilePath_soutai,header = None, encoding="shift-jis").values.tolist()
        Sce1 += data[0]
        Sce2 += data[1]
        Sce3 += data[2]
        Sce4 += data[3]
    AveCost1 = sum(Sce1)/len(Sce1)
    AveCost2 = sum(Sce2)/len(Sce2)
    AveCost3 = sum(Sce3)/len(Sce3)
    AveCost4 = sum(Sce4)/len(Sce4)
    Costs = [AveCost1,AveCost2,AveCost3,AveCost4]
    AveCost = sum(Costs)/len(Costs)
    StdCost = MyModules.calculate_variance(Costs) ** 0.5
    return AveCost, StdCost

def AnnualGraph():
    with open('./data/inputs.csv', 'r') as f:
        reader = csv.reader(f)
        inputs = list(reader)
        for row in reader:
            inputs = [row for row in reader]
    x = [i[2] for i in inputs]
    y = [float(i[1]) for i in inputs]
    data_name = [i[0] for i in inputs]
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.clear()
    plt.title("annual cost")
    plt.grid(which='both')
    #plt.legend()
    
    for (i,j,k) in zip(x,y,data_name):
        plt.plot(i,j,'o')
        plt.annotate(k, xy=(i, j))
    
        # canvasにプロットした画像を出力
    canvas = FigureCanvasAgg(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    data = png_output.getvalue()
    # HTML側に渡すレスポンスを生成する
    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Length'] = len(data)
    return response

#月次電力コストグラフ出力
def OutputMonthlyCost(Algo,Term,AitaiM,AitaiN,Month):
    fig_CostMonthly = plt.figure()
    plt.grid(which='both')
    ax_CostMonthly = fig_CostMonthly.add_subplot(111)
    ax_CostMonthly.clear()
    Input_CostMonthly = int(Month)

    #Mの分データ取得
    FileName_MC_pre = Term + "_" + Algo + "_Tokyo_"
    FileName_MC_M = FileName_MC_pre + str(Input_CostMonthly) + "_" + str(AitaiM[Input_CostMonthly - 1])+"_M" + ".csv"
    FileDir_MC_M = str(Term) + "_" + str(Algo) + "_Tokyo_M/"
    FilePath_soutai_MC_M = 'scenarios/'+ FileDir_MC_M + FileName_MC_M
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_MC_M = os.path.normpath(os.path.join(base, FilePath_soutai_MC_M))

    data1 = pd.read_csv(FilePath_soutai_MC_M,header = None, encoding="shift-jis").values.tolist()

    #Nの分データ
    FileName_MC_N = FileName_MC_pre + str(Input_CostMonthly) + "_" + str(AitaiN[Input_CostMonthly - 1])+"_N" + ".csv"
    FileDir_MC_N = str(Term) + "_" + str(Algo) + "_Tokyo_N/"
    FilePath_soutai_MC_N = 'scenarios/'+ FileDir_MC_N + FileName_MC_N
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_MC_N = os.path.normpath(os.path.join(base, FilePath_soutai_MC_N))

    data2 = pd.read_csv(FilePath_soutai_MC_N,header = None, encoding="shift-jis").values.tolist()

    SceMC= []

    
    for i in range(4):
        CurrentSceMC = []
        days = int(len(data1[i])/25)
        NumDays = [k+1 for k in range(days)]
        #NumDays = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
        for j in range(days):
            day = []
            StartM = j * 25
            StartN = j * 23                        
            MC_N1 = data2[i][StartN:(StartN + 15)]
            day.extend(MC_N1)
            MC_M = data1[i][StartM:(StartM + 25)]
            day.extend(MC_M)
            MC_N2 = data2[i][(StartN + 15):(StartN + 23)]
            day.extend(MC_N2)
            CurrentSceMC.append((sum(day)/48))
        SceMC.append(CurrentSceMC)
    for i in range(4):
        ax_CostMonthly.plot(NumDays,SceMC[i])
        
    ax_CostMonthly.set_xlabel("Day")
    ax_CostMonthly.set_ylabel("erectricity cost[yen/kwh]")
    ax_CostMonthly.set_ylim(8, 16)
    canvas_CostMonthly = FigureCanvasTkAgg(fig_CostMonthly)
    png_output = BytesIO()
    canvas_CostMonthly.print_png(png_output)
    data = png_output.getvalue()
    # HTML側に渡すレスポンスを生成する
    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Length'] = len(data)
    return response

def OutputMonthlyCost_1(Algo,Term,AitaiM,AitaiN,Month):
    fig_CostMonthly = plt.figure()
    plt.grid(which='both')
    ax_CostMonthly = fig_CostMonthly.add_subplot(111)
    ax_CostMonthly.clear()
    Input_CostMonthly = int(Month)


    #Mの分データ取得
    FileName_MC_pre = Term + "_" + Algo + "_Tokyo_"
    FileName_MC_M = FileName_MC_pre + str(Input_CostMonthly) + "_" + str(AitaiM[Input_CostMonthly - 1])+"_act_M" + ".csv"
    FileDir_MC_M = str(Term) + "_" + str(Algo) + "_Tokyo_act_M/"
    FilePath_soutai_MC_M = 'scenarios/'+ FileDir_MC_M + FileName_MC_M
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_MC_M = os.path.normpath(os.path.join(base, FilePath_soutai_MC_M))

    data1 = pd.read_csv(FilePath_soutai_MC_M,header = None, encoding="shift-jis").values.tolist()

    #Nの分データ
    FileName_MC_N = FileName_MC_pre + str(Input_CostMonthly) + "_" + str(AitaiN[Input_CostMonthly - 1])+"_act_N" + ".csv"
    FileDir_MC_N = str(Term) + "_" + str(Algo) + "_Tokyo_act_N/"
    FilePath_soutai_MC_N = 'scenarios/'+ FileDir_MC_N + FileName_MC_N
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_MC_N = os.path.normpath(os.path.join(base, FilePath_soutai_MC_N))

    data2 = pd.read_csv(FilePath_soutai_MC_N,header = None, encoding="shift-jis").values.tolist()

    SceMC= []
    days = int(len(data1[0])/25)
    NumDays = [k+1 for k in range(days)]
    #NumDays = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
    for j in range(days):
        day = []
        StartM = j * 25
        StartN = j * 23                        
        MC_N1 = data2[0][StartN:(StartN + 15)]
        day.extend(MC_N1)
        MC_M = data1[0][StartM:(StartM + 25)]
        day.extend(MC_M)
        MC_N2 = data2[0][(StartN + 15):(StartN + 23)]
        day.extend(MC_N2)
        SceMC.append((sum(day)/48))
 
    ax_CostMonthly.plot(NumDays,SceMC,marker='o')
    ax_CostMonthly.set_xlabel("Day")
    ax_CostMonthly.set_ylabel("erectricity cost[yen/kwh]")
    ax_CostMonthly.set_ylim(8, 16)
    canvas = FigureCanvasAgg(fig_CostMonthly)
    png_output = BytesIO()
    canvas.print_png(png_output)
    data = png_output.getvalue()
    # HTML側に渡すレスポンスを生成する
    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Length'] = len(data)
    return response

#日次電力コストグラフ出力
def OutputDailyCost(Algo,Term,AitaiM,AitaiN,Month):
    fig_CostDaily = plt.figure()
    plt.grid(which='both')
    ax_CostDaily = fig_CostDaily.add_subplot(111)
    ax_CostDaily.clear()
    Input_CostDaily = int(Month)

    #Mの分データ取得
    FileName_DC_pre = Term + "_" + Algo + "_Tokyo_"
    FileName_DC_M = FileName_DC_pre + str(Input_CostDaily) + "_" + str(AitaiM[Input_CostDaily - 1])+"_M" + ".csv"
    FileDir_DC_M = str(Term) + "_" + str(Algo) + "_Tokyo_M/"
    FilePath_soutai_DC_M = 'scenarios/'+ FileDir_DC_M + FileName_DC_M
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_DC_M = os.path.normpath(os.path.join(base, FilePath_soutai_DC_M))
    data1 = pd.read_csv(FilePath_soutai_DC_M,header = None, encoding="shift-jis").values.tolist()

    #Nの分データ
    FileName_DC_N = FileName_DC_pre + str(Input_CostDaily) + "_" + str(AitaiN[Input_CostDaily - 1])+"_N" + ".csv"
    FileDir_DC_N = str(Term) + "_" + str(Algo) + "_Tokyo_N/"
    FilePath_soutai_DC_N = 'scenarios/'+ FileDir_DC_N + FileName_DC_N
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_DC_N = os.path.normpath(os.path.join(base, FilePath_soutai_DC_N))
    data2 = pd.read_csv(FilePath_soutai_DC_N,header = None, encoding="shift-jis").values.tolist()

    SceDC= []

    
    for i in range(4):
        hours = 48
        Numhours = [i+1 for i in range(hours)]
        DateForC = 19
        #NumDays = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
        day = []
        StartM = DateForC * 25
        StartN = DateForC * 23              
        DC_N1 = data2[i][StartN:(StartN + 15)]
        day.extend(DC_N1)
        DC_M = data1[i][StartM:(StartM + 25)]
        day.extend(DC_M)
        DC_N2 = data2[i][(StartN + 15):(StartN + 23)]
        day.extend(DC_N2)
        SceDC.append(day)
    for i in range(4):
        ax_CostDaily.plot(Numhours,SceDC[i])
        
    ax_CostDaily.set_xlabel("timeslot")
    ax_CostDaily.set_ylabel("erectricity cost[yen/kwh]")
    ax_CostDaily.set_ylim(5, 20)
    canvas = FigureCanvasAgg(fig_CostDaily)
    png_output = BytesIO()
    canvas.print_png(png_output)
    data = png_output.getvalue()
    # HTML側に渡すレスポンスを生成する
    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Length'] = len(data)
    return response

def OutputDailyCost_1(Algo,Term,AitaiM,AitaiN,Month):
    fig_CostDaily = plt.figure()
    plt.grid(which='both')
    ax_CostDaily = fig_CostDaily.add_subplot(111)
    ax_CostDaily.clear()
    Input_CostDaily = int(Month)

    #Mの分データ取得
    FileName_DC_pre = Term + "_" + Algo + "_Tokyo_"
    FileName_DC_M = FileName_DC_pre + str(Input_CostDaily) + "_" + str(AitaiM[Input_CostDaily - 1])+"_act_M" + ".csv"
    FileDir_DC_M = str(Term) + "_" + str(Algo) + "_Tokyo_act_M/"
    FilePath_soutai_DC_M = 'scenarios/'+ FileDir_DC_M + FileName_DC_M
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_DC_M = os.path.normpath(os.path.join(base, FilePath_soutai_DC_M))
    data1 = pd.read_csv(FilePath_soutai_DC_M,header = None, encoding="shift-jis").values.tolist()

    #Nの分データ
    FileName_DC_N = FileName_DC_pre + str(Input_CostDaily) + "_" + str(AitaiN[Input_CostDaily - 1])+"_act_N" + ".csv"
    FileDir_DC_N = str(Term) + "_" + str(Algo) + "_Tokyo_act_N/"
    FilePath_soutai_DC_N = 'scenarios/'+ FileDir_DC_N + FileName_DC_N
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_DC_N = os.path.normpath(os.path.join(base, FilePath_soutai_DC_N))
    data2 = pd.read_csv(FilePath_soutai_DC_N,header = None, encoding="shift-jis").values.tolist()

    SceDC= []

    
    hours = 48
    Numhours = [i+1 for i in range(hours)]
    DateForC = 19
    #NumDays = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
    StartM = DateForC * 25
    StartN = DateForC * 23                        
    DC_N1 = data2[0][StartN:(StartN + 15)]
    SceDC.extend(DC_N1)
    DC_M = data1[0][StartM:(StartM + 25)]
    SceDC.extend(DC_M)
    DC_N2 = data2[0][(StartN + 15):(StartN + 23)]
    SceDC.extend(DC_N2)
    ax_CostDaily.plot(Numhours,SceDC,marker='o')    
    ax_CostDaily.set_xlabel("timeslot")
    ax_CostDaily.set_ylabel("erectricity cost[yen/kwh]")
    ax_CostDaily.set_ylim(5, 20)
    canvas = FigureCanvasAgg(fig_CostDaily)
    png_output = BytesIO()
    canvas.print_png(png_output)
    data = png_output.getvalue()
    # HTML側に渡すレスポンスを生成する
    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Length'] = len(data)
    return response

#月次インバランスグラフ出力
def OutputMonthlyInb(Algo,Term,AitaiM,AitaiN,Month):
    fig_InbMonthly = plt.figure()
    plt.grid(which='both')
    ax_InbMonthly = fig_InbMonthly.add_subplot(111)
    ax_InbMonthly.clear()
    Input_InbMonthly = int(Month)


    #Mの分データ取得
    FileName_MI_pre = "Inb_" + Term + "_" + Algo + "_Tokyo_"
    FileName_MI_M = FileName_MI_pre + str(Input_InbMonthly) + "_" + str(AitaiM[Input_InbMonthly - 1])+"_M" + ".csv"
    FileDir_MI_M = "inb_" + str(Term) + "_" + str(Algo) + "_Tokyo_M/"
    FilePath_soutai_MI_M = 'scenarios/'+ FileDir_MI_M + FileName_MI_M
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_MI_M = os.path.normpath(os.path.join(base, FilePath_soutai_MI_M))
    data1 = pd.read_csv(FilePath_soutai_MI_M,header = None, encoding="shift-jis").values.tolist()

    #Nの分データ
    FileName_MI_N = FileName_MI_pre + str(Input_InbMonthly) + "_" + str(AitaiN[Input_InbMonthly - 1])+"_N" + ".csv"
    FileDir_MI_N = "inb_" + str(Term) + "_" + str(Algo) + "_Tokyo_N/"
    FilePath_soutai_MI_N = 'scenarios/'+ FileDir_MI_N + FileName_MI_N
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_MI_N = os.path.normpath(os.path.join(base, FilePath_soutai_MI_N))
    data2 = pd.read_csv(FilePath_soutai_MI_N,header = None, encoding="shift-jis").values.tolist()

    SceMI= []

    
    for i in range(4):
        CurrentSceMI = []
        days = int(len(data1[i])/25)
        NumDays = [i+1 for i in range(days)]
        #NumDays = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
        for j in range(days):
            day = []
            StartM = j * 25
            StartN = j * 23                        
            MI_N1 = data2[i][StartN:(StartN + 15)]
            day.extend(MI_N1)
            MI_M = data1[i][StartM:(StartM + 25)]
            day.extend(MI_M)
            MI_N2 = data2[i][(StartN + 15):(StartN + 23)]
            day.extend(MI_N2)
            CurrentSceMI.append(sum(day))
        SceMI.append(CurrentSceMI)
    for i in range(4):
        ax_InbMonthly.plot(NumDays,SceMI[i])
        
    ax_InbMonthly.set_xlabel("Day")
    ax_InbMonthly.set_ylabel("Loss Anount[thousand yen]")
    ax_InbMonthly.set_ylim(0, 150000)
    canvas = FigureCanvasAgg(fig_InbMonthly)
    png_output = BytesIO()
    canvas.print_png(png_output)
    data = png_output.getvalue()
    # HTML側に渡すレスポンスを生成する
    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Length'] = len(data)
    return response

def OutputMonthlyInb_1(Algo,Term,AitaiM,AitaiN,Month):
    fig_InbMonthly = plt.figure()
    plt.grid(which='both')
    ax_InbMonthly = fig_InbMonthly.add_subplot(111)
    ax_InbMonthly.clear()
    Input_InbMonthly = int(Month)

    #Mの分データ取得
    FileName_MI_pre = "Inb_" + Term + "_" + Algo + "_Tokyo_"
    FileName_MI_M = FileName_MI_pre + str(Input_InbMonthly) + "_" + str(AitaiM[Input_InbMonthly - 1])+"_act_M" + ".csv"
    FileDir_MI_M = "inb_" + str(Term) + "_" + str(Algo) + "_Tokyo_act_M/"
    FilePath_soutai_MI_M = 'scenarios/'+ FileDir_MI_M + FileName_MI_M
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_MI_M = os.path.normpath(os.path.join(base, FilePath_soutai_MI_M))
    data1 = pd.read_csv(FilePath_soutai_MI_M,header = None, encoding="shift-jis").values.tolist()

    #Nの分データ
    FileName_MI_N = FileName_MI_pre + str(Input_InbMonthly) + "_" + str(AitaiN[Input_InbMonthly - 1])+"_act_N" + ".csv"
    FileDir_MI_N = "inb_" + str(Term) + "_" + str(Algo) + "_Tokyo_act_N/"
    FilePath_soutai_MI_N = 'scenarios/'+ FileDir_MI_N + FileName_MI_N
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_MI_N = os.path.normpath(os.path.join(base, FilePath_soutai_MI_N))
    data2 = pd.read_csv(FilePath_soutai_MI_N,header = None, encoding="shift-jis").values.tolist()

    SceMI= []

    days = int(len(data1[0])/25)
    NumDays = [i+1 for i in range(days)]
    #NumDays = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
    for j in range(days):
        day = []
        StartM = j * 25
        StartN = j * 23                        
        MI_N1 = data2[0][StartN:(StartN + 15)]
        day.extend(MI_N1)
        MI_M = data1[0][StartM:(StartM + 25)]
        day.extend(MI_M)
        MI_N2 = data2[0][(StartN + 15):(StartN + 23)]
        day.extend(MI_N2)
        SceMI.append(sum(day))
    ax_InbMonthly.plot(NumDays,SceMI,marker='o')
    ax_InbMonthly.set_xlabel("Day")
    ax_InbMonthly.set_ylabel("Loss Anount[thousand yen]")
    ax_InbMonthly.set_ylim(0, 150000)
    canvas = FigureCanvasAgg(fig_InbMonthly)
    png_output = BytesIO()
    canvas.print_png(png_output)
    data = png_output.getvalue()
    # HTML側に渡すレスポンスを生成する
    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Length'] = len(data)
    return response

#日次インバランスグラフ出力
def OutputDailyInb(Algo,Term,AitaiM,AitaiN,Month):
    fig_InbDaily = plt.figure()
    plt.grid(which='both')
    ax_InbDaily = fig_InbDaily.add_subplot(111)
    ax_InbDaily.clear()
    Input_InbDaily = int(Month)

    #Mの分データ取得
    FileName_DI_pre = "Inb_" + Term + "_" + Algo + "_Tokyo_"
    FileName_DI_M = FileName_DI_pre + str(Input_InbDaily) + "_" + str(AitaiM[Input_InbDaily - 1])+"_M" + ".csv"
    FileDir_DI_M = "inb_" + str(Term) + "_" + str(Algo) + "_Tokyo_M/"
    FilePath_soutai_DI_M = 'scenarios/'+ FileDir_DI_M + FileName_DI_M
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_DI_M = os.path.normpath(os.path.join(base, FilePath_soutai_DI_M))
    data1 = pd.read_csv(FilePath_soutai_DI_M,header = None, encoding="shift-jis").values.tolist()

    #Nの分データ
    FileName_DI_N = FileName_DI_pre + str(Input_InbDaily) + "_" + str(AitaiN[Input_InbDaily - 1])+"_N" + ".csv"
    FileDir_DI_N = "inb_" + str(Term) + "_" + str(Algo) + "_Tokyo_N/"
    FilePath_soutai_DI_N = 'scenarios/'+ FileDir_DI_N + FileName_DI_N
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_DI_N = os.path.normpath(os.path.join(base, FilePath_soutai_DI_N))
    data2 = pd.read_csv(FilePath_soutai_DI_N,header = None, encoding="shift-jis").values.tolist()

    SceDI= []

    
    for i in range(4):
        hours = 48
        Numhours = [i+1 for i in range(hours)]
        DateForC = 19
        day = []
        StartM = DateForC * 25
        StartN = DateForC * 23                        
        DI_N1 = data2[i][StartN:(StartN + 15)]
        day.extend(DI_N1)
        DI_M = data1[i][StartM:(StartM + 25)]
        day.extend(DI_M)
        DI_N2 = data2[i][(StartN + 15):(StartN + 23)]
        day.extend(DI_N2)
        SceDI.append(day)
    for i in range(4):
        ax_InbDaily.plot(Numhours,SceDI[i])
        
    ax_InbDaily.set_xlabel("Time")
    ax_InbDaily.set_ylabel("Loss Anount[thousand yen]")
    ax_InbDaily.set_ylim(0, 10000)
    canvas = FigureCanvasAgg(fig_InbDaily)
    png_output = BytesIO()
    canvas.print_png(png_output)
    data = png_output.getvalue()
    # HTML側に渡すレスポンスを生成する
    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Length'] = len(data)
    return response

def OutputDailyInb_1(Algo,Term,AitaiM,AitaiN,Month):
    fig_InbDaily = plt.figure()
    plt.grid(which='both')
    ax_InbDaily = fig_InbDaily.add_subplot(111)
    ax_InbDaily.clear()
    Input_InbDaily = int(Month)

    #Mの分データ取得
    FileName_DI_pre = "Inb_" + Term + "_" + Algo + "_Tokyo_"
    FileName_DI_M = FileName_DI_pre + str(Input_InbDaily) + "_" + str(AitaiM[Input_InbDaily - 1])+"_act_M" + ".csv"
    FileDir_DI_M = "inb_" + str(Term) + "_" + str(Algo) + "_Tokyo_act_M/"
    FilePath_soutai_DI_M = 'scenarios/'+ FileDir_DI_M + FileName_DI_M
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_DI_M = os.path.normpath(os.path.join(base, FilePath_soutai_DI_M))
    data1 = pd.read_csv(FilePath_soutai_DI_M,header = None, encoding="shift-jis").values.tolist()

    #Nの分データ
    FileName_DI_N = FileName_DI_pre + str(Input_InbDaily) + "_" + str(AitaiN[Input_InbDaily - 1])+"_act_N" + ".csv"
    FileDir_DI_N = "inb_" + str(Term) + "_" + str(Algo) + "_Tokyo_act_N/"
    FilePath_soutai_DI_N = 'scenarios/'+ FileDir_DI_N + FileName_DI_N
    base = os.path.dirname(os.path.abspath(__file__))
    FilePath_DI_N = os.path.normpath(os.path.join(base, FilePath_soutai_DI_N))
    data2 = pd.read_csv(FilePath_soutai_DI_N,header = None, encoding="shift-jis").values.tolist()

    SceDI= []

    hours = 48
    Numhours = [i+1 for i in range(hours)]
    DateForC = 19
    StartM = DateForC * 25
    StartN = DateForC * 23                        
    DI_N1 = data2[0][StartN:(StartN + 15)]
    SceDI.extend(DI_N1)
    DI_M = data1[0][StartM:(StartM + 25)]
    SceDI.extend(DI_M)
    DI_N2 = data2[0][(StartN + 15):(StartN + 23)]
    SceDI.extend(DI_N2)
    ax_InbDaily.plot(Numhours,SceDI,marker='o')    
    ax_InbDaily.set_xlabel("Time")
    ax_InbDaily.set_ylabel("Loss Anount[thousand yen]")
    ax_InbDaily.set_ylim(0, 10000)
    canvas = FigureCanvasAgg(fig_InbDaily)
    png_output = BytesIO()
    canvas.print_png(png_output)
    data = png_output.getvalue()
    # HTML側に渡すレスポンスを生成する
    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Length'] = len(data)
    return response
