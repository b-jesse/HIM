'''
him - Hydrogen Investment Model
This script will take the results and create the figures for the paper

list of figures:
Fig. 3 - Hydrogen demand curve after BCG
Fig. 3a - Cases for electricity price
Fig. 4 - Installed capacity reference case
Fig. 5 - No. of agents reference case
Fig. 6 - Electricity production reference case
Fig. 7 - Hydrogen production reference case
Fig. 8 - Utilization rate Renewables & Electrolyzers reference case
Fig. 9 - Type of loads for Electrolyzers reference case
Fig. 10 - Median wallet for market reference case
Fig. 11 - ROI for Agents reference case
Fig. 12 - Expected profitability of new assets reference case
Fig. 13 - Invested money reference case
Fig. 14 - Weighted electricity price and hydrogen price reference case
Fig. 15 - Minimal electrolyzer production costs reference case
Fig. 16 - Electricity price and LCOE and Hydrogen price and LCOH reference case
Fig. 16a - Average electricity price of HP and LCOH and share of electricity of LCOH reference case
Fig. 16b - Investment threshold for all type of agents reference case
Fig. 17 - Installed capacities for obstacle cases
Fig. 18 - Electricity mix for obstacle cases
Fig. 19 - Hydrogen production for obstacle cases
Fig. 20 - Utilization rate for obstacle cases
Fig. 21 - ROI for obstacle cases
Fig. 22 - Electricity and hydrogen price for obstacle cases
Fig. 23 - Electrolyzer costs for obstacle cases
Fig. 24 - Invested money for obstacle cases
Fig. 25 - LCOE and weighted electricity price and LCOH and hydrogen price for obstacle cases
Fig. 25a - Average electricity price for HP and LCOH and share of electricity on LCOH for obstacle cases
Fig. 25b - Investment thresholds for all type of agents obstacle cases
Fig. 26 - Inst. RES vs Inst. ELC
Fig. 27 - Inst. ELC vs Inst. FAC
Fig. 28 - Inst. ELC vs cumulative Investment by HP
Fig. 29 - Share RES vs H2 Production
Fig. 30 - Price hydrogen vs weighted price electricity
Fig. 31 - Electrolyzer costs vs hydrogen price
Fig. 32 - No. of HP vs No. of EP
Fig. 33 - ROI of HP vs ROI of EP
Fig. 34 - LCOE vs LCOH
Fig. 35 - Average electricity price vs electrolyzer costs
Fig. 36 - Heatmap of installed electrolyzers capacity
Fig. 37 - Heatmap of weighted electricity price
Fig. 38 - Heatmap of cumulative investment


TODO
- Missing fig - Moneyflows
- combinded legend entry area and line together

version: 0.1.25.6.3
date: 2025-06-03
author: Jesse

changelog:
0.1.24.10.10 - start new script
0.1.25.5.8 - added figures for reference case
0.1.25.5.15 - added figures for obstacle cases and sensitivity analysis
0.1.25.5.20 - fixed missing cases in sensitivity analysis and added more figures
0.1.25.6.3 - changed the way sensitivity plots look, also comment not needed plots out
0.1.25.11.10 - added functions for sensitivity analysis for learning rate
'''

# import
import os, csv

import matplotlib.lines
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from matplotlib.legend_handler import HandlerTuple
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.cm import ScalarMappable
from matplotlib.lines import Line2D

global resultRefDir, resultW2PDir, resultStratDir, resultsWorsTDir
global resultSenseDir
global resultDir
global listFiles
global plotType, plotSettings
global blue, darkblue, green, black, grey, orange, purple, red
global x, year0, yearDelta
global dfHistoricalData

# Input
resultRefDir = '2025-07-17-17-19'
resultW2PDir = '2025-07-31-15-37'
resultStratDir = '2025-07-18-08-41'
resultWorstDir = '2025-07-31-15-28'
resultSensCsv = 'sensitivity.csv'
resultLearning = '2025-11-07-22-32'
resultValidation = '2025-11-12-00-11'

resultDir = 'D:\\USER\\ABM\\02_NetLogo\\02_Output' ## CHANGE THIS
listFiles = ['elc_year.csv', 'em_year.csv', 'ep_year.csv', 'hm_day.csv', 'hm_year.csv', 'hp_year.csv', 'man_year.csv',
             'pm_day.csv', 'pm_year.csv', 'pp_year.csv', 'res_year.csv', 'sale_year.csv']

# Time settings
year0 = 2024
yearEnd = 2050
yearDelta = yearEnd - year0 + 1
x = list(range(year0, yearEnd + 1))
yearSense = [2025, 2050]

# Plot settings
plotType = 'png'
plotSettings = {}
plotSettings['gridspec_kw'] = {'left': 0.1, 'bottom': 0.1, 'right': 0.9, 'top': 0.9}
plotSettings['dpi'] = 500
plotSettings['figsize_s'] = (2.87, 1.77)
plotSettings['figsize_l'] = (6.1, 3.54)
plotSettings['figsize_3t'] = (2.87, 5.37)
plotSettings['figsize_3t_l'] = (6.1, 5.37)
plotSettings['figsize_2t'] = (2.87, 3.54)
plotSettings['fontsize'] = 6
plotSettings['xticks'] = np.arange(2025, 2055, 10)
plotSettings['alpha'] = 0.5

plotSettings['xlim'] = (year0, year0 + yearDelta - 1)

plotSettings['ylim_res_cap'] = [-0.1, 700]
plotSettings['ylim_elc_cap'] = [-0.1, 80]
plotSettings['ylim_fac_cap'] = [-0.1, 30]
plotSettings['ylim_global_thres'] = [-1, 0.5]
plotSettings['ylim_profit'] = [-0.1, 5]
plotSettings['ylim_elc_mix'] = [0, 1.5]
plotSettings['ylim_lcoe'] = [0, 75]
plotSettings['ylim_lcoh-mwh'] = [0, 350]
plotSettings['ylim_lcoh-kg'] = [0, 350*0.0333]
plotSettings['ylim_p_elc'] = [0, 2500]
plotSettings['ylim_no_agents'] = [-0.1, 40]

# Colors
black = [0, 0, 0]
blue = [173/255, 189/255, 227/255]
darkblue = [2/255,  61/255, 107/255]
green = [185/255, 210/255, 95/255]
darkgreen = [0, 0.39, 0]
grey = [235/255, 235/255, 235/255]
darkgrey = [169/255, 169/255, 169/255]
orange = [250/255, 180/255, 90/255]
purple = [175/255, 130/255, 185/255]
darkpurple = [76/255, 0/255, 153/255]
red = [235/255, 95/255, 115/255]

# Hatches & Linestlyes
StratHatch = '///'
StratLinestyle = '--'
W2PHatch = 'ooo'
W2PLinestlye = ':'
WorstHatch = '+++'
WorstLinestyle = '-.'

# Symbol & Colors for sensitivity analysis
ColorMap = np.linspace(np.array(blue), np.array(red), 11)
SensMarker = {'ref': 'x',
              'strat': 'x',
              'w2p': 'x',
              3.: 'p',
              4.: '^',
              5.: 'o',
              6.: 's',
              7.: '*',
              8.: 'd'}
SensColor = {'ref': black,
             'strat': green,
             'w2p': purple,
             0.: ColorMap[0],
             -0.1: ColorMap[1],
             -0.2: ColorMap[2],
             -0.3: ColorMap[3],
             -0.4: ColorMap[4],
             -0.5: ColorMap[5],
             -0.6: ColorMap[6],
             -0.7: ColorMap[7],
             -0.8: ColorMap[8],
             -0.9: ColorMap[9],
             -0.99: ColorMap[10]}
SensCMap = LinearSegmentedColormap.from_list('custom_gradient', [blue, red])
HeatCMap = LinearSegmentedColormap.from_list('custom_gradient', [red, green])
HeatCMapReverse = LinearSegmentedColormap.from_list('custom_gradient', [green, red])

# Validation data - Wind Offshore, Onshore and PV only
dfHistoricalData = pd.DataFrame(data=[[2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012,
                                       2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
                                      [6.2, 8.9, 12.3, 14.8, 17.5, 20.3, 23.4, 26.3, 28.9, 36.3, 44.9, 54.6, 65.1, 70.2,
                                       76.5, 83.8, 90.1, 97.9, 103.9, 109.6, 116.5, 123.8, 133.8, 151.7, 172.6],
                                      [9.764, 10.797, 16.268, 19.407, 26.587, 29.082, 33.589, 43.644, 45.893, 46.135,
                                       50.51, 69.848, 78.424, 83.358, 93.945, 118.7, 117.48, 144.454, 154.281, 171.105,
                                       181.598, 164.781, 185.12, 203.319, 212.986],
                                      [1.4, 1.8, 2.4, 3.2, 3.5, 4.3, 4.8, 5.7, 7.4, 7.9, 8.2, 11.5, 12.9, 13.8, 15.8,
                                       19.7, 19.5, 24.0, 26.0, 29.6, 32.6, 28.8, 33.6, 38.7, 38.9],
                                      [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 4.49, 5.9, 7.19, 8.36, 8.1, 8.41,
                                       8.39, 8.34, 7.86, 7.57, 7.35, 6.42, 6.7, 7.61, 7.97, 8.59, 13.54, 18.10]],
                                index=['Year', 'Installed Capacity Renewables [GW]', 'Production Renewables [TWh]',
                                       'Share Renewables [%]', 'Electricity price [€/MWh]'])
dfHistoricalData = dfHistoricalData.T


def check_data(resultDir):
    '''
    Function that checks if all files exists in the given directory.
    :param:
        str resultDir: Name of the directory to check.
    :return:
    '''
    NoRuns = 0
    wkdir = os.getcwd()
    for i in os.listdir(os.path.join(wkdir, resultDir, 'Sensitivity_1')):
        if i.startswith('Run_'):
            for j in listFiles:
                if not os.path.isfile(os.path.join(wkdir, resultDir, 'Sensitivity_1', i, j)):
                    print('Error in check_data: ' + resultDir + '\\Sensitivity_1\\' + i + '\\' + j + ' not found.')
                    exit(200)
            NoRuns += 1
    print(str(NoRuns) + ' runs found.')


def check_sensitivity(resultCsv):
    '''
    Function that check if all files from the given result csv exists.
    :param:
        str resultCsv: Name of the csv with all information for the sensitivity analysis.
    :return:
    '''
    wkdir = os.getcwd()
    if not os.path.isfile(os.path.join(wkdir, resultCsv)):
        print('Error in check_sensitivity: ' + resultCsv + ' not found.')
        exit(300)

    # Find seperator
    with open(resultCsv, 'r') as file:
        tmpSample = file.read(1024)
    tmpSep = csv.Sniffer().sniff(tmpSample)
    tmpSep = tmpSep.delimiter

    # Read Sensitivity csv
    tmpDf = pd.read_csv(os.path.join(wkdir, resultCsv), sep=tmpSep)

    # Get the right runs
    sensDf = pd.DataFrame(data=np.nan, index=list(range(int(len(tmpDf) / 2 * 11))), columns=['run', 'w2p', 'strat'])
    tmpIndex = 0
    for i in tmpDf.index:
        if tmpDf.loc[i]['strat'] == 'sens':
            for j in range(10):
                sensDf.loc[tmpIndex, 'run'] = str(tmpDf.loc[i, 'run'] + '\\Sensitivity_' + str(j + 1))
                sensDf.loc[tmpIndex, 'w2p'] = tmpDf.loc[i, 'w2p']
                sensDf.loc[tmpIndex, 'strat'] = j * -0.1
                tmpIndex += 1
        else:
            sensDf.loc[tmpIndex, 'run'] = str(tmpDf.loc[i, 'run'] + '\\Sensitivity_1')
            sensDf.loc[tmpIndex, 'w2p'] = tmpDf.loc[i, 'w2p']
            sensDf.loc[tmpIndex, 'strat'] = tmpDf.loc[i, 'strat']
            tmpIndex += 1

    # Check data for each run
    for i in sensDf['run']:
        print('Check ' + str(i) + '...')
        NoRuns = 0
        wkdir = os.getcwd()
        for j in os.listdir(os.path.join(wkdir, i)):
            if j.startswith('Run_'):
                for k in listFiles:
                    if not os.path.isfile(os.path.join(wkdir, i, j, k)):
                        print('Error in check_sensitivity: ' + i + '\\' + j + '\\' + k + ' not found.')
                        exit(301)
                NoRuns += 1
        print(str(NoRuns) + ' runs found.')


def load_data(resultDir):
    '''
    Function that loads the data from the csv files.
    :param:
        string resultDir: Name of the folder
    :return:
        list tmp_list: List that contains the data from all file as an individual pd.Dataframe.
    '''
    wkdir = os.getcwd()

    # Get list of Runs
    listRuns = []
    for i in os.listdir(os.path.join(wkdir, resultDir, 'Sensitivity_1')):
        if i.startswith('Run_'):
            for j in listFiles:
                if not os.path.isfile(os.path.join(wkdir, resultDir, 'Sensitivity_1', i, j)):
                    print('Error in check_date: ' + resultDir + '\\Sensitivity_1\\' + i + '\\' + j + ' not found.')
                    exit(400)
            listRuns.append(i)

    # Load data for all runs
    tmpList = []
    for j in listFiles:
        listDf = []
        for i in listRuns:
            try:
                file = (os.path.join(wkdir, resultDir, 'Sensitivity_1', i, j))
                tmpDf = pd.read_csv(file, sep=';')
                tmpDf['Run'] = np.ones(len(tmpDf.index)) * int(i.split('_')[1])
                listDf.append(tmpDf)
            except FileNotFoundError:
                print('Error in load data: ' + resultDir + '\\Sensitivity_1\\' + i + '\\' + j + ' not found.')
                exit(401)
        tmpList.append(pd.concat(listDf))
    return(tmpList)


def load_data_sens(resultDir):
    '''
    Function that loads the data from the csv files.
    :param:
        string resultDir: Name of the folder
    :return:
        list tmp_list: List that contains the data from all file as an individual pd.Dataframe.
    '''
    wkdir = os.getcwd()

    # Get list of Runs
    listRuns = []
    for i in os.listdir(os.path.join(wkdir, resultDir)):
        if i.startswith('Run_'):
            for j in listFiles:
                if not os.path.isfile(os.path.join(wkdir, resultDir, i, j)):
                    print('Error in check_date: ' + resultDir + '\\' + i + '\\' + j + ' not found.')
                    exit(400)
            listRuns.append(i)

    # Load data for all runs
    tmpList = []
    for j in listFiles:
        listDf = []
        for i in listRuns:
            try:
                file = (os.path.join(wkdir, resultDir, i, j))
                tmpDf = pd.read_csv(file, sep=';')
                tmpDf['Run'] = np.ones(len(tmpDf.index)) * int(i.split('_')[1])
                listDf.append(tmpDf)
            except FileNotFoundError:
                print('Error in load data: ' + resultDir + '\\' + i + '\\' + j + ' not found.')
                exit(401)
        tmpList.append(pd.concat(listDf))
    return(tmpList)


def load_sensitivity(resultCsv):
    '''
    Function that loads the data for all runs from the given sensitivity csv file.
    :param
        str resultCsv: Name of the sensitivity csv file.
    :return:
    '''
    wkdir = os.getcwd()

    # Find seperator
    with open(resultCsv, 'r') as file:
        tmpSample = file.read(1024)
    tmpSep = csv.Sniffer().sniff(tmpSample)
    tmpSep = tmpSep.delimiter

    # Read Sensitivity csv
    tmpDf = pd.read_csv(os.path.join(wkdir, resultCsv), sep=tmpSep)

    # Get the right runs
    sensDf = pd.DataFrame(data=np.nan, index=list(range(int(len(tmpDf) / 2 * 11))), columns=['run', 'w2p', 'strat'])
    tmpIndex = 0
    for i in tmpDf.index:
        if tmpDf.loc[i]['strat'] == 'sens':
            for j in range(10):
                sensDf.loc[tmpIndex, 'run'] = str(tmpDf.loc[i, 'run'] + '\\Sensitivity_' + str(j + 1))
                sensDf.loc[tmpIndex, 'w2p'] = tmpDf.loc[i, 'w2p']
                sensDf.loc[tmpIndex, 'strat'] = j * -0.1
                tmpIndex += 1
        else:
            sensDf.loc[tmpIndex, 'run'] = str(tmpDf.loc[i, 'run'] + '\\Sensitivity_1')
            sensDf.loc[tmpIndex, 'w2p'] = tmpDf.loc[i, 'w2p']
            sensDf.loc[tmpIndex, 'strat'] = tmpDf.loc[i, 'strat']
            tmpIndex += 1

    noRuns = len(sensDf)

    # Load data for all runs
    dictRun = {}
    for i in sensDf.index:
        print('Load run: ' + str(sensDf.loc[i, 'run']) + '... ' + str(i + 1) + '/' + str(noRuns))
        tmpListResult = load_data_sens(sensDf.loc[i, 'run'])
        dictRun[i] = [sensDf.loc[i, 'run'], sensDf.loc[i, 'w2p'], sensDf.loc[i, 'strat'], tmpListResult]
    return(dictRun)


def check_learningrate(resultDir):
    '''
    Function that checks the data for the learning rate sensitivity analysis from the csv files.
    :param:
        string resultDir: Name of the folder with the learning rate sensitivity
    :return:
    '''
    NoRuns = 0
    wkdir = os.getcwd()
    for i in os.listdir(os.path.join(wkdir, resultDir)):
        if i.startswith('Sensitivity_'):
            for j in os.listdir(os.path.join(wkdir, resultDir, i)):
                if j.startswith('Run_'):
                    for k in listFiles:
                        if not os.path.isfile(os.path.join(wkdir, resultDir, i, j, k)):
                            print('Error in check_learningrate: ' + resultDir + '\\' + i + '\\' + j + '\\' + k + 'not found.')
                            exit(400)
                    NoRuns += 1
    print(str(NoRuns) + ' runs found.')


def load_learningrate(resultDir):
    '''
    Function that checks the data for the learning rate sensitivity analysis from the csv files.
    :param:
        string resultDir: Name of the folder with the learning rate sensitivity
    :return:
        list tmpList: List that contains the data from all file as an individual pd.Dataframe.
    '''
    wkdir = os.getcwd()

    # Get list of Sensitivity
    listSens = []
    listRuns = []
    listLearningRate = np.arange(0.08, 0.18, 0.01)
    for i in os.listdir(os.path.join(wkdir, resultDir)):
        if i.startswith('Sensitivity_'):
            for j in os.listdir(os.path.join(wkdir, resultDir, i)):
                if j.startswith('Run_'):
                    for k in listFiles:
                        if not os.path.isfile(os.path.join(wkdir, resultDir, i, j, k)):
                            print('Error in load_learningrate: ' + resultDir + '\\' + i + '\\' + j + '\\' + k + 'not found.')
                            exit(500)
                    if j not in listRuns:
                        listRuns.append(j)
            if i not in listSens:
                listSens.append(i)

    # Load data for all runs
    tmpList = []
    for k in listFiles:
        listDf = []
        for j in listRuns:
            for i in listSens:
                try:
                    file = (os.path.join(wkdir, resultDir, i, j, k))
                    tmpDf = pd.read_csv(file, sep=';')
                    tmpDf['Run'] = np.ones(len(tmpDf.index)) * int(j.split('_')[1])
                    tmpDf['Sensitivity'] = np.ones(len(tmpDf.index)) * int(i.split('_')[1])
                    tmpDf['LearningRate'] = np.ones(len(tmpDf.index)) * listLearningRate[int(int(i.split('_')[1]) - 1)]
                    listDf.append(tmpDf)
                except FileNotFoundError:
                    print('Error in load_learningrate: ' + resultDir + '\\' + i + '\\' + j + '\\' + k + 'not found.')
                    exit(501)
        tmpList.append(pd.concat(listDf))
    return(tmpList)


def figure_3():
    '''
    Function that will create Fig. 3. - Hydrogen demand curve after bcg
    :return:
    '''
    # Visualize CO2 tax
    CO2 = False

    # tmpW2P = [Type, Color, Hatch, Mt, MWh, €/kg, €/MWh, €/kg w/o CO2, €/MWh w/o CO2]
    tmpW2P = {1: ['Refineries', green, '///', 0.112, 3731897, 8.83, 265.29, 7.92, 237.88],
              2: ['Refineries',	green, '///', 0.095, 3157759, 7.52, 225.79, 6.61, 198.38],
              3: ['Ammonia', blue, '|||', 0.095, 3157759, 6.34, 190.32, 5.71, 171.46],
              4: ['Methanol', darkblue, '---', 0.052, 1722414, 6.23, 187.18, 5.53, 166.15],
              5: ['Refineries', green, '///', 0.078, 2583621, 6.23, 187.18, 5.32, 159.77],
              6: ['Steel', grey, '', 0.871, 28993966, 5.10, 153.07, 2.08, 62.58],
              7: ['Ammonia', blue, '|||', 0.302, 10047414, 4.29, 128.83, 3.66, 109.97],
              8: ['Power generation', orange, '+++', 0.190, 6315517, 3.95, 118.50, 3.31, 99.32],
              9: ['Ammonia', blue, '|||', 0.103, 3444828, 3.68, 110.42, 3.05, 91.56],
              10: ['Methanol', darkblue, '---', 0.138, 4593103, 3.68, 110.42, 2.98, 89.39],
              11: ['Aviation', purple, '...', 0.353, 11769828, 3.30, 99.20, 2.23, 66.92],
              12: ['Industrial heat', red, 'ooo', 0.509, 16937069, 2.93, 87.98, 2.29, 68.79],
              13: ['Industrial heat', red, 'ooo', 0.362, 12056897, 2.32, 69.58, 1.68, 50.39],
              14: ['Refineries', green, '///', 0.103, 3444828, 2.15, 64.64, 1.24, 37.23],
              15: ['Methanol', darkblue, '---', 0.069, 2296552, 2.14, 64.19, 1.44, 43.15],
              16: ['Power generation', orange, '+++', 0.422, 14066379, 2.03, 61.05, 1.39, 41.86],
              17: ['Steel', grey, '', 0.853, 28419828, 1.81, 54.31, -1.20, -36.18],
              18: ['Industrial heat', red, 'ooo', 5.897, 196355172, 1.73, 52.07, 1.10, 32.88],
              19: ['Aviation', purple, '...', 5.716, 190326724, 0.70, 21.10, -0.37, -11.18]
    }

    fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                            dpi=plotSettings['dpi'])
    ax2 = ax1.twinx()

    ax1.set_ylabel('Willingness to pay [€/kg]', fontsize=plotSettings['fontsize'])
    ax1.set_xlabel('Demand [Mt]', fontsize=plotSettings['fontsize'])
    ax1.spines['top'].set_visible(False)
    ax1.spines['bottom'].set_position(('data', 0))

    ax2.set_ylabel('Willingness to pay [€/MWh]', fontsize=plotSettings['fontsize'])
    ax2.spines['top'].set_visible(False)
    ax2.spines['bottom'].set_position(('data', 0))

    # DataFrame for writing out
    writeDf = pd.DataFrame(columns=['Demand [Mt]', 'W2P [€/MWh]', 'W2P [€/Mt]', 'W2P w/o CO2 [€/MWh]',
                                    'W2P w/o CO2 [€/Mt]'])

    # Areas and blocks
    tmpSum = 0
    if CO2:
        for i in tmpW2P.keys():
            tmpX = [tmpSum, tmpSum + tmpW2P[i][3]]
            tmpY1 = [tmpW2P[i][5], tmpW2P[i][5]] # €/Mt
            tmpY2 = [tmpW2P[i][6], tmpW2P[i][6]] # €/MWh
            tmpY3 = [tmpW2P[i][7], tmpW2P[i][7]] # €/Mt w/o CO2
            tmpY4 = [tmpW2P[i][8], tmpW2P[i][8]] # €/MWh w/o CO2

            # Plot areas
            ax1.fill_between(tmpX, tmpY1, tmpY3, alpha=0.25, color=tmpW2P[i][1], hatch=tmpW2P[i][2], edgecolor=None)
            ax1.fill_between(tmpX, tmpY3, [0, 0], alpha=0.75, color=tmpW2P[i][1], hatch=tmpW2P[i][2], edgecolor=None,
                             label=tmpW2P[i][0])

            ax2.fill_between(tmpX, tmpY2, tmpY4, alpha=0.25, color=tmpW2P[i][1], hatch=tmpW2P[i][2], edgecolor=None)
            ax2.fill_between(tmpX, tmpY4, [0, 0], alpha=0.75, color=tmpW2P[i][1], hatch=tmpW2P[i][2], edgecolor=None,
                             label=tmpW2P[i][0])

            # Writing data
            tmpDf = pd.DataFrame([tmpX, tmpY1, tmpY2, tmpY3, tmpY4],
                                 index=['Demand [Mt]', 'W2P [€/Mt]', 'W2P [€/MWh]', 'W2P w/o CO2 [€/Mt]',
                                        'W2P w/o CO2 [€/MWh]'],
                                 columns=[tmpW2P[i][0], tmpW2P[i][0]])
            writeDf = pd.concat([writeDf, tmpDf.T])

            # Next block
            tmpSum += tmpW2P[i][3]
    else:
        for i in tmpW2P.keys():
            tmpX = [tmpSum, tmpSum + tmpW2P[i][3]]
            tmpY1 = [tmpW2P[i][5], tmpW2P[i][5]] # €/Mt
            tmpY2 = [tmpW2P[i][6], tmpW2P[i][6]] # €/MWh

            # Plot areas
            ax1.fill_between(tmpX, tmpY1, [0, 0], alpha=0.75, color=tmpW2P[i][1], hatch=tmpW2P[i][2], edgecolor=None,
                             label=tmpW2P[i][0])

            ax2.fill_between(tmpX, tmpY2, [0, 0], alpha=0.75, color=tmpW2P[i][1], hatch=tmpW2P[i][2], edgecolor=None,
                             label=tmpW2P[i][0])

            # Writing data
            tmpDf = pd.DataFrame([tmpX, tmpY1, tmpY2],
                                 index=['Demand [Mt]', 'W2P [€/Mt]', 'W2P [€/MWh]'],
                                 columns=[tmpW2P[i][0], tmpW2P[i][0]])
            writeDf = pd.concat([writeDf, tmpDf.T])

            # Next block
            tmpSum += tmpW2P[i][3]

    # Adjust xlim
    ax1.set_xlim([0, tmpSum * 0.99])

    # Adjust ticks
    ticks = plt.xticks()[0]
    plt.xticks(ticks[1:-1])
    ax1.minorticks_on()
    ax2.minorticks_on()
    ax1.tick_params(which='major', axis='both', labelsize=plotSettings['fontsize'])
    ax1.xaxis.set_minor_locator(MultipleLocator(2.5))
    ax1.yaxis.set_minor_locator(MultipleLocator(1))
    ax1.tick_params(which='minor', axis='both', color='gray')
    ax2.tick_params(which='major', axis='both', labelsize=plotSettings['fontsize'])
    ax2.xaxis.set_minor_locator(MultipleLocator(2.5))
    ax2.yaxis.set_minor_locator(MultipleLocator(25))
    ax2.tick_params(which='minor', axis='both', color='gray')


    # Legend
    handles, labels = ax1.get_legend_handles_labels()
    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.55),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=3)

    # Save figure
    plt.savefig(os.getcwd() + '\\figure3.' + plotType, bbox_inches='tight')

    # Write out data
    writeDf.to_csv(os.getcwd() + '\\figure3.csv', sep=';')


def figure_3a():
    '''
    Function that will create Fig. 3a - Different electricity prices
    :return:
    '''

    # x - P_RES,max(t)/D_elc(t)
    tmpx = [0, 1, 1, 2, 2, 6]
    # y - p_elc
    tmpy = [3, 3, 2, 2, 0, 0]
    # y dashed 1 - p_gas/eta_GT
    tmpy_d1 = [3, 3, 3, 3, 3, 3]
    # y dashed 2 - p_H2 * eta_E
    tmpy_d2 = [2, 2, 2, 2, 2, 2]

    # Figure
    fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                            dpi=plotSettings['dpi'])
    ax1.set_ylabel('Electricity price [-]', fontsize=plotSettings['fontsize'])
    ax1.set_xlabel('$\\frac{Electricity \: production \: by \: renewables}{D_{elc}} \: [-]$',
                   fontsize=plotSettings['fontsize'])

    ax1.plot(tmpx, tmpy_d1, linestyle=':', color=grey, alpha=1)
    ax1.plot(tmpx, tmpy_d2, linestyle=':',  color=grey, alpha=1)
    ax1.plot(tmpx, tmpy, color=black, alpha=1)

    # Adjust xlim
    ax1.set_xlim([0, 3.5])
    ax1.set_ylim([0, 4])

    # Adjust ticks
    ax1.tick_params(which='major', axis='both', labelsize=plotSettings['fontsize'])
    ax1.minorticks_on()
    ax1.xaxis.set_minor_locator(MultipleLocator(0.5))
    ax1.yaxis.set_minor_locator(MultipleLocator(1))
    plt.xticks([0, 1, 2, 3], [0, 1, '$1+e$', ''])
    plt.xticks([0.5, 1.5, 2.5], ['', '', ''], minor=True, fontsize=plotSettings['fontsize'])
    plt.yticks([0, 2, 3], [0, '$\eta_{E} p_{H_{2}}$', '$\\frac{p_{gas}}{\eta_{GT}}$'])
    ax1.tick_params(which='minor', axis='both', color='gray')

    # Save figure
    plt.savefig(os.getcwd() + '\\figure3a.' + plotType, bbox_inches='tight')


def figure_4(dfPM, dfHM, dfEM):
    '''
    Function that will create Fig. 4 - Installed capacities reference case.
    :param:
        pd.DataFrame dfPM: Yearly data from the power market for the reference case.
        pd.DataFrame dfHM: Yearly data from the hydrogen market for the reference case.
        pd.DataFrame dfEM: Yearly data from the electrolyzer market for the reference case.
    :return:
    '''
    # Installed renewables
    tmpPM = dfPM.set_index(['Year', 'Run'])
    dfPlotRES = pd.DataFrame(data=np.nan, index=range(yearDelta), columns=['Median', '75%', '25%'])

    # Installed electrolyzers
    tmpHM = dfHM.set_index(['Year', 'Run'])
    dfPlotELC = pd.DataFrame(data=np.nan, index=range(yearDelta), columns=['Median', '75%', '25%'])

    # Installed factories
    tmpEM = dfEM.set_index(['Year', 'Run'])
    dfPlotFAC = pd.DataFrame(data=np.nan, index=range(yearDelta), columns=['Median', '75%', '25%'])

    for i in range(yearDelta):
        # Renewables
        if i in tmpPM.index.levels[0]:
            tmpDf = tmpPM.loc[i]['Installed capacity Renewables']
            dfPlotRES['Median'][i] = tmpDf.median()
            dfPlotRES['75%'][i] = tmpDf.quantile(q=0.75)
            dfPlotRES['25%'][i] = tmpDf.quantile(q=0.25)

        # Electorlyzers
        if i in tmpHM.index.levels[0]:
            tmpDf = tmpHM.loc[i]['Installed capacity Electrolyzers']
            dfPlotELC['Median'][i] = tmpDf.median()
            dfPlotELC['75%'][i] = tmpDf.quantile(q=0.75)
            dfPlotELC['25%'][i] = tmpDf.quantile(q=0.25)

        # Factories
        if i in tmpEM.index.levels[0]:
            tmpDf = tmpEM.loc[i]['Installed capacity Manufacturings']
            dfPlotFAC['Median'][i] = tmpDf.median()
            dfPlotFAC['75%'][i] = tmpDf.quantile(q=0.75)
            dfPlotFAC['25%'][i] = tmpDf.quantile(q=0.25)

    # Figure
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=plotSettings['figsize_3t'],
                                        gridspec_kw=plotSettings['gridspec_kw'], dpi=plotSettings['dpi'], sharex=True)

    # Renewables
    ax1.set_ylabel('Renewables [GW]', fontsize=plotSettings['fontsize'])

    # Phases
    ax1.plot([2028, 2028], [-1, 10000], linestyle=':', color=darkgrey)
    ax1.plot([2039, 2039], [-1, 10000], linestyle=':', color=darkgrey)
    ax1.annotate('I', xy=(2026, 100), xytext=(2026, 100),
                 bbox=dict(boxstyle='circle', facecolor='white', alpha=0.5, edgecolor=darkgrey),
                 fontsize=plotSettings['fontsize'])
    ax1.annotate('II', xy=(2033, 100), xytext=(2033, 100),
                 bbox=dict(boxstyle='circle', facecolor='white', alpha=0.5, edgecolor=darkgrey),
                 fontsize=plotSettings['fontsize'])
    ax1.annotate('III', xy=(2044, 100), xytext=(2044, 100),
                 bbox=dict(boxstyle='circle', facecolor='white', alpha=0.5, edgecolor=darkgrey),
                 fontsize=plotSettings['fontsize'])

    # Results data
    ax1.plot(x, dfPlotRES['Median']/1e3, label='Renewables (our work)', linestyle='-', color=green)
    ax1.fill_between(x, dfPlotRES['25%']/1e3, dfPlotRES['75%']/1e3, alpha=0.25, color=green, edgecolor=None)

    # Gov targets
    # https://www.bundeswirtschaftsministerium.de/Redaktion/DE/Dossier/erneuerbare-energien.html
    # https://www.bundeswirtschaftsministerium.de/Redaktion/DE/Publikationen/Energie/windenergie-an-land-strategie.pdf?__blob=publicationFile&v=11
    # https://www.bundeswirtschaftsministerium.de/Redaktion/DE/Publikationen/Energie/photovoltaik-stategie-2023.pdf?__blob=publicationFile&v=8
    # https://www.bundesregierung.de/breg-de/service/archiv-bundesregierung/windenergie-auf-see-gesetz-2022968
    ax1.scatter([2030, 2045], [360, 630], label='Gov. target', facecolor='none', edgecolor=darkgreen)

    # Results from other models
    ax1.plot([2025, 2030, 2035, 2040, 2045], [182, 316, 435, 533, 685], label='Schöb et al., 2023 [92]', linestyle='--',
             color=green, alpha=0.5)

    ax1.set_ylim(plotSettings['ylim_res_cap'])


    # Electrolyzers
    ax2.set_ylabel('Electrolyzers [GW]', fontsize=plotSettings['fontsize'])

    # Phases
    ax2.plot([2028, 2028], [-1, 10000], linestyle=':', color=darkgrey)
    ax2.plot([2039, 2039], [-1, 10000], linestyle=':', color=darkgrey)

    # Results data
    ax2.plot(x, dfPlotELC['Median']/1e3, label='Electrolyzers (our work)', linestyle='-', color=blue)
    ax2.fill_between(x, dfPlotELC['25%']/1e3, dfPlotELC['75%']/1e3, alpha=0.25, color=blue, edgecolor=None)
    # Gov targets
    # https://www.bundeswirtschaftsministerium.de/Redaktion/EN/Publikationen/Energie/national-hydrogen-strategy-update.pdf?__blob=publicationFile&v=2
    ax2.scatter([2030], [10], label='Gov. target', facecolor='none', edgecolor=darkblue)
    # Results from other models - Schöb et al., 2023
    ax2.plot([2025, 2030, 2035, 2040, 2045], [1.6, 4.9, 17.7, 34.6, 72.4], linestyle='--', color=blue, alpha=0.5)
    # Projections
    ax2.scatter([2025, 2026, 2027, 2028, 2029, 2030, 2031, 2035], [0.9, 2.1, 3.7, 5.6, 6.5, 10.0, 10.0, 16.5],
                label='IEA, 2024 [94]', facecolor='none', edgecolor=blue, alpha=0.5, marker='v')
    ax2.set_ylim(plotSettings['ylim_elc_cap'])

    # Factories
    ax3.set_ylabel('Electrolyzer manufacturing [GW/year]', fontsize=plotSettings['fontsize'])
    ax3.set_xlabel('Year', fontsize=plotSettings['fontsize'])

    # Phases
    ax3.plot([2028, 2028], [-1, 10000], linestyle=':', color=darkgrey)
    ax3.plot([2039, 2039], [-1, 10000], linestyle=':', color=darkgrey)

    # Results data
    ax3.plot(x, dfPlotFAC['Median']/1e3, label='Electrolyzer manufacturing (our work)', linestyle='-', color=purple)
    ax3.fill_between(x, dfPlotFAC['25%']/1e3, dfPlotFAC['75%']/1e3, alpha=0.25, color=purple, edgecolor=None)
    ax3.set_ylim(plotSettings['ylim_fac_cap'])

    fig.text(-0.1, 0.5, 'Installed capacities', va='center', rotation='vertical', fontsize=plotSettings['fontsize'])

    plt.xlim(plotSettings['xlim'])

    # Adjust ticks
    ax1.minorticks_on()
    ax2.minorticks_on()
    ax3.minorticks_on()
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(50))
    ax1.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax1.tick_params(which='minor', axis='both', color='gray')
    ax2.yaxis.set_minor_locator(MultipleLocator(10))
    ax2.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax2.tick_params(which='minor', axis='both', color='gray')
    ax3.yaxis.set_minor_locator(MultipleLocator(5))
    ax3.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax3.tick_params(which='minor', axis='both', color='gray')

    # Legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles3, labels3 = ax3.get_legend_handles_labels()

    handles = handles1 + handles2 + handles3
    labels = labels1 + labels2 + labels3

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.6),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save figure
    plt.savefig(os.getcwd() + '\\figure4.' + plotType, bbox_inches='tight')

    # Write out data
    writeDf = pd.DataFrame(data=[dfPlotRES['Median']/1e3, dfPlotRES['25%']/1e3, dfPlotRES['75%']/1e3,
                                 dfPlotELC['Median']/1e3, dfPlotELC['25%']/1e3, dfPlotELC['75%']/1e3,
                                 dfPlotFAC['Median']/1e3, dfPlotFAC['25%']/1e3, dfPlotFAC['75%']/1e3],
                           index=['Inst. cap. RES - median [GW]', 'Inst. cap. RES - 25% [GW]',
                                  'Inst. cap. RES - 75% [GW]', 'Inst. cap. ELC - median [GW]',
                                  'Inst. cap. ELC - 25% [GW]', 'Inst. cap. ELC - 75% [GW]',
                                  'Inst. cap. FAC - median [GW/year]', 'Inst. cap. FAC - 25% [GW/year]',
                                  'Inst. cap. FAC - 75% [GW/year]'])
    writeDf = writeDf.T
    writeDf.index = x

    tmpThomas = pd.DataFrame(data=[[182, 316, 435, 533, 685], [1.6, 4.9, 17.7, 34.6, 72.4]],
                             index=['Inst. cap. RES - Thomas [GW]', 'Inst. cap. ELC - Thomas [GW]'])
    tmpThomas = tmpThomas.T
    tmpThomas.index = [2025, 2030, 2035, 2040, 2045]

    tmpIEA = pd.DataFrame(data=[[0.9, 2.1, 3.7, 5.6, 6.5, 10.0, 10.0, 16.5]], index=['Inst. cap. ELC - IEA [GW]'])
    tmpIEA = tmpIEA.T
    tmpIEA.index = [2025, 2026, 2027, 2028, 2029, 2030, 2031, 2035]

    tmpGovRES = pd.DataFrame(data=[[360, 630]], index=['Gov. target RES [GW]'])
    tmpGovRES = tmpGovRES.T
    tmpGovRES.index = [2030, 2045]

    tmpGovELC = pd.DataFrame(data=[[10]], index=['Gov. target ELC [GW]'])
    tmpGovELC = tmpGovELC.T
    tmpGovELC.index = [2030]

    writeDf = pd.concat([writeDf, tmpThomas, tmpIEA, tmpGovRES, tmpGovELC])
    writeDf.to_csv(os.getcwd() + '\\figure4.csv', sep=';')


def figure_5(dfPM, dfHM, dfEM):
    '''
    Function that will create Fig. 5 - Number of agents reference case.
    :param:
        pd.DataFrame dfPM: Yearly data from the power market for the reference case.
        pd.DataFrame dfHM: Yearly data from the hydrogen market for the reference case.
        pd.DataFrame dfEM: Yearly data from the electrolyzer market for the reference case.
    :return:
    '''
    # No. of Power Producers
    tmpPM = dfPM.set_index(['Year', 'Run'])
    dfPlotPP = pd.DataFrame(data=np.nan, index=range(yearDelta), columns=['Median', '75%', '25%'])

    # No. of Hydrogen Producers
    tmpHM = dfHM.set_index(['Year', 'Run'])
    dfPlotHP = pd.DataFrame(data=np.nan, index=range(yearDelta), columns=['Median', '75%', '25%'])

    # No. of Electrolyzer Producers
    tmpEM = dfEM.set_index(['Year', 'Run'])
    dfPlotEP = pd.DataFrame(data=np.nan, index=range(yearDelta), columns=['Median', '75%', '25%'])

    for i in range(yearDelta):
        # Power Producers
        if i in tmpPM.index.levels[0]:
            tmpDf = tmpPM.loc[i]['No. of Powerproducers']
            dfPlotPP['Median'][i] = tmpDf.median()
            dfPlotPP['75%'][i] = tmpDf.quantile(q=0.75)
            dfPlotPP['25%'][i] = tmpDf.quantile(q=0.25)

        # Hydrogen Producers
        if i in tmpHM.index.levels[0]:
            tmpDf = tmpHM.loc[i]['No. of Hydrogenproducers']
            dfPlotHP['Median'][i] = tmpDf.median()
            dfPlotHP['75%'][i] = tmpDf.quantile(q=0.75)
            dfPlotHP['25%'][i] = tmpDf.quantile(q=0.25)

        # Electrolyzer Producers
        if i in tmpEM.index.levels[0]:
            tmpDf = tmpEM.loc[i]['No. of Electrolyzerproducers']
            dfPlotEP['Median'][i] = tmpDf.median()
            dfPlotEP['75%'][i] = tmpDf.quantile(q=0.75)
            dfPlotEP['25%'][i] = tmpDf.quantile(q=0.25)

    # Figure
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=plotSettings['figsize_3t'],
                                        gridspec_kw=plotSettings['gridspec_kw'], dpi=plotSettings['dpi'], sharex=True)

    # Power Producers
    ax1.set_ylabel('Power Producers', fontsize=plotSettings['fontsize'])
    # Results data
    ax1.plot(x, dfPlotPP['Median'], label='Power Producers', linestyle='-', color=green)
    ax1.fill_between(x, dfPlotPP['25%'], dfPlotPP['75%'], alpha=0.25, color=green, edgecolor=None)
    ax1.set_ylim(-0.1)

    # Hydrogen Producers
    ax2.set_ylabel('Hydrogen Producers', fontsize=plotSettings['fontsize'])
    # Results data
    ax2.plot(x, dfPlotHP['Median'], label='Hydrogen Producers', linestyle='-', color=blue)
    ax2.fill_between(x, dfPlotHP['25%'], dfPlotHP['75%'], alpha=0.25, color=blue, edgecolor=None)
    ax2.set_ylim(-0.1)

    # Electrolyzer Producers
    ax3.set_ylabel('Electrolyzer Producers', fontsize=plotSettings['fontsize'])
    ax3.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    # Results data
    ax3.plot(x, dfPlotEP['Median'], label='Electrolyzer Producers', linestyle='-', color=purple)
    ax3.fill_between(x, dfPlotEP['25%'], dfPlotEP['75%'], alpha=0.25, color=purple, edgecolor=None)
    ax3.set_ylim(-0.1)

    fig.text(-0.1, 0.5, 'No. of agents', va='center', rotation='vertical', fontsize=plotSettings['fontsize'])

    plt.xlim(plotSettings['xlim'])

    # Adjust ticks
    ax1.minorticks_on()
    ax2.minorticks_on()
    ax3.minorticks_on()
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(50))
    ax1.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax1.tick_params(which='minor', axis='both', color='gray')
    ax2.yaxis.set_minor_locator(MultipleLocator(10))
    ax2.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax2.tick_params(which='minor', axis='both', color='gray')
    ax3.yaxis.set_minor_locator(MultipleLocator(5))
    ax3.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax3.tick_params(which='minor', axis='both', color='gray')

    # Legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles3, labels3 = ax3.get_legend_handles_labels()

    handles = handles1 + handles2 + handles3
    labels = labels1 + labels2 + labels3

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.55),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=3)

    # Save figure
    plt.savefig(os.getcwd() + '\\figure5.' + plotType, bbox_inches='tight')

    # Single plot
    fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                            dpi=plotSettings['dpi'])

    # Power Producers
    ax1.set_ylabel('No. of Agents', fontsize=plotSettings['fontsize'])
    ax1.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    # Results data
    ax1.plot(x, dfPlotPP['Median'], label='Power Producers', linestyle='-', color=green)
    ax1.fill_between(x, dfPlotPP['25%'], dfPlotPP['75%'], alpha=0.25, color=green, edgecolor=None)

    # Hydrogen Producers
    # Results data
    ax1.plot(x, dfPlotHP['Median'], label='Hydrogen Producers', linestyle='-', color=blue)
    ax1.fill_between(x, dfPlotHP['25%'], dfPlotHP['75%'], alpha=0.25, color=blue, edgecolor=None)

    # Electrolyzer Producers
    # Results data
    ax1.plot(x, dfPlotEP['Median'], label='Electrolyzer Producers', linestyle='-', color=purple)
    ax1.fill_between(x, dfPlotEP['25%'], dfPlotEP['75%'], alpha=0.25, color=purple, edgecolor=None)
    ax1.set_ylim(-0.1)

    plt.xlim(plotSettings['xlim'])

    # Adjust ticks
    ax1.minorticks_on()
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(50))
    ax1.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax1.tick_params(which='minor', axis='both', color='gray')

    # Legend
    handles, labels = ax1.get_legend_handles_labels()
    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower left', bbox_to_anchor=(-0.15, -0.5),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save figure
    plt.savefig(os.getcwd() + '\\figure5a.' + plotType, bbox_inches='tight')


    # Write out Data
    writeDf = pd.DataFrame(data=[dfPlotPP['Median'], dfPlotPP['25%'], dfPlotPP['75%'], dfPlotHP['Median'],
                                 dfPlotHP['25%'], dfPlotHP['75%'], dfPlotEP['Median'], dfPlotEP['25%'], dfPlotEP['75%']],
                           index=['No. of Power Producers - Median', 'No. of Power Producers - 25%',
                                  'No. of Power Producers - 75%', 'No. of Hydrogen Producers - Median',
                                  'No. of Hydrogen Producers - 25%', 'No. of Hydrogen Producers - 75%',
                                  'No. of Electrolyzer Producers - Median', 'No. of Electrolyzer Producers - 25%',
                                  'No. of Electrolyzer Producers - 75%',])
    writeDf = writeDf.T
    writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure5.csv', sep=';')


def figure_6(dfPM):
    '''
    Function that will create Fig. 6 - Electricity production reference case.
    :param:
        pd.DataFrame dfPM: Daily data from the power market for the reference case.
    :return:
    '''
    # Power market
    tmpPM = dfPM.set_index(['Year', 'Day', 'Run'])
    dfPlotPM = pd.DataFrame(data=np.nan, index=range(yearDelta),
                            columns=['GT', 'GT - norm', 'Demand', 'Demand - norm', 'H2', 'H2 - norm', 'Curtailment',
                                     'Curtailment - Norm'])

    for i in range(yearDelta):
        if i in tmpPM.index.levels[0]:
            # Gas turbine production
            tmpGT = tmpPM.loc[i]['Electricity demand others'] - tmpPM.loc[i]['Actual production renewables']
            tmpGT = tmpGT.mask(tmpGT < 0, 0)
            tmpGT = tmpGT.groupby(level=1).sum().median()

            # Electricity demand
            tmpDemand = tmpPM.loc[i]['Electricity demand others'].groupby(level=1).sum().median()

            # Green hydrogen production
            tmpH2 = tmpGT + tmpPM.loc[i]['Actual production renewables'].groupby(level=1).sum().median()

            # Curtailment
            tmpCurtailment = tmpGT + tmpPM.loc[i]['Maximum production renewables'].groupby(level=1).sum().median()

            # Absolut values
            dfPlotPM.loc[i, 'GT'] = tmpGT / 1e6
            dfPlotPM.loc[i, 'Demand'] = tmpDemand / 1e6
            dfPlotPM.loc[i, 'H2'] = tmpH2 / 1e6
            dfPlotPM.loc[i, 'Curtailment'] = tmpCurtailment / 1e6

            # Normalize by the electricity demand
            dfPlotPM.loc[i, 'GT - norm'] = tmpGT / tmpDemand
            dfPlotPM.loc[i, 'Demand - norm'] = tmpDemand / tmpDemand
            dfPlotPM.loc[i, 'H2 - norm'] = tmpH2 / tmpDemand
            dfPlotPM.loc[i, 'Curtailment - norm'] = tmpCurtailment / tmpDemand

    # Figure
    fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                            dpi=plotSettings['dpi'])

    ax1.set_ylabel('Electricity mix [-]', fontsize=plotSettings['fontsize'])

    # Normalized
    # General electricity demand
    ax1.plot(x, dfPlotPM['Demand - norm'], label='General electricity demand', color=black)
    # Gas turbine production
    ax1.fill_between(x, 0, dfPlotPM['GT - norm'], alpha=0.5, color=grey, edgecolor=None, label='Production gas turbine')
    # Renewables production
    ax1.fill_between(x, dfPlotPM['GT - norm'], dfPlotPM['Demand - norm'], alpha=0.5, color=green, edgecolor=None,
                     label='Production renewables')
    # Green hydrogen production
    ax1.fill_between(x, dfPlotPM['Demand - norm'], dfPlotPM['H2 - norm'], label='Green hydrogen production', color=blue,
                     edgecolor=None, alpha=0.5)
    # Curtailment
    ax1.fill_between(x, dfPlotPM['H2 - norm'], dfPlotPM['Curtailment - norm'], label='Curtailment renewables',
                     color=purple, edgecolor=None, alpha=0.5)

    # Absolut
    ax2 = ax1.twinx()
    ax2.set_ylabel('Electricity mix [TWh]', fontsize=plotSettings['fontsize'])
    # General electricity demand
    ax2.plot(x, dfPlotPM['Demand'], color=black)
    # Gas turbine production
    ax2.fill_between(x, 0, dfPlotPM['GT'], alpha=0.5, color=grey, edgecolor=None)
    # Renewables production
    ax2.fill_between(x, dfPlotPM['GT'], dfPlotPM['Demand'], alpha=0.5, color=green, edgecolor=None)
    # Green hydrogen production
    ax2.fill_between(x, dfPlotPM['Demand'], dfPlotPM['H2'], color=blue, edgecolor=None, alpha=0.5)
    # Curtailment
    ax2.fill_between(x, dfPlotPM['H2'], dfPlotPM['Curtailment'], color=purple, edgecolor=None, alpha=0.5)

    # Gov. targets
    # https://www.umweltbundesamt.de/sites/default/files/medien/11850/publikationen/39_2023_cc_projektionsbericht_12_23.pdf
    #ax1.scatter([2030, 2035], [.2, 0], label='Gov. target', facecolor='none', edgecolor=darkgreen)

    # Adjust axis
    ax1.minorticks_on()
    ax1.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    ax1.set_xlim(plotSettings['xlim'])
    ax1.set_ylim(0)
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(5))
    ax2.minorticks_on()
    ax2.set_ylim(0)
    ax2.set_xticks(plotSettings['xticks'])
    ax2.xaxis.set_minor_locator(MultipleLocator(5))
    ax2.yaxis.set_minor_locator(MultipleLocator(50))

    ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax1.tick_params(axis='both', which='minor', color='gray')

    ax2.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax2.tick_params(axis='both', which='minor', color='gray')

    # Legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    handles = handles1 + handles2
    labels = labels1 + labels2

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.55),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save plot
    plt.savefig(os.getcwd() + '\\figure6.' + plotType, bbox_inches='tight')

    # Write data
    writeDf = pd.DataFrame(data=[dfPlotPM['GT - norm'], dfPlotPM['Demand - norm'], dfPlotPM['H2 - norm'],
                                 dfPlotPM['Curtailment - norm'], dfPlotPM['GT'], dfPlotPM['Demand'], dfPlotPM['H2'],
                                 dfPlotPM['Curtailment']],
                           index=['Production gas turbine [-]', 'General Electricity demand [-]',
                                  'Green hydrogen production [-]', 'Curtailment renewables [-]',
                                  'Production gas turbine [TWh]', 'General Electricity demand [TWh]',
                                  'Green hydrogen production [TWh]', 'Curtailment renewables [TWh]'])
    writeDf = writeDf.T
    writeDf.index = x

    tmpGov = pd.DataFrame(data=[[0.2, 0.0]], index=['Gov. target'])
    tmpGov = tmpGov.T
    tmpGov.index = [2030, 2035]

    writeDf = pd.concat([writeDf, tmpGov])
    writeDf.to_csv(os.getcwd() + '\\figure6.csv', sep=';')


def figure_7(dfHM):
    '''
    Function that will create Fig. 7 - Hydrogen production reference case.
    :param:
        pd.DataFrame dfHM: Daily data from the hydrogen market for the reference case.
    :return:
    '''

    # tmpDemand= [Type, Label, Color, Hatch, Mt, MWh]
    tmpDemand = {1: ['Refineries 1', 'Refineries', green, '///', 0.207, 6889656],
                 2: ['Ammonia 1', 'Ammonia', blue, '|||', 0.302, 10047415],
                 3: ['Methanol 1', 'Methanol', darkblue, '---', 0.354, 11769829],
                 4:	['Refineries 2', 'Refineries', green, '///', 0.432, 14353450],
                 5:	['Steel 1', 'Steel', grey, '', 1.303, 43347416],
                 6:	['Ammonia 2', 'Ammonia', blue, '|||', 1.605, 53394830],
                 7:	['Power 1', 'Power generation', orange, '+++', 1.795, 59710347],
                 8:	['Ammonia 3', 'Ammonia', blue, '|||', 1.898,	63155175],
                 9:	['Methanol 2', 'Methanol', darkblue, '---', 2.036, 67748278],
                 10: ['Aviation 1', 'Aviation', purple, '...', 2.389, 79518106],
                 11: ['Heat 1', 'Industrial heat', red, 'ooo', 3.26, 108512072],
                 12: ['Refineries 3', 'Refineries', green, '///', 3.363, 111956900],
                 13: ['Methanol 3', 'Methanol', darkblue, '---', 3.432, 114253452],
                 14: ['Power 2', 'Power generation', orange, '+++',	3.854, 128319831],
                 15: ['Steel 2', 'Steel', grey, '', 4.707, 156739659],
                 16: ['Heat 2', 'Industrial heat', red,	'ooo', 10.604, 353094831],
                 17: ['Aviation 2', 'Aviation', purple, '...', 16.32, 543421555]
    }
    tmpColumns = []
    for i in tmpDemand.keys():
        tmpColumns.append(tmpDemand[i][0])
    tmpColumns.append('Hydrogen Production - Median')
    tmpColumns.append('Hydrogen Production - 25%')
    tmpColumns.append('Hydrogen Production - 75%')

    # Power market
    tmpHM = dfHM.set_index(['Year', 'Day', 'Run'])
    dfPlotHM = pd.DataFrame(data=np.nan, index=range(yearDelta), columns=tmpColumns)

    for i in range(yearDelta):
        if i in tmpHM.index.levels[0]:
            # Hydrogen production
            tmpH2 = tmpHM.loc[i]['Actual production electrolyzers'].groupby(level=1).sum()
            dfPlotHM.loc[i, 'Hydrogen Production - Median'] = tmpH2.median()
            dfPlotHM.loc[i, 'Hydrogen Production - 25%'] = tmpH2.quantile(q=0.25)
            dfPlotHM.loc[i, 'Hydrogen Production - 75%'] = tmpH2.quantile(q=0.75)

            # Hydrogen demand
            for j in tmpDemand.keys():
                if tmpH2.median() < tmpDemand[j][-1]:
                    dfPlotHM.loc[i, tmpDemand[j][0]] = tmpH2.median()
                else:
                    dfPlotHM.loc[i, tmpDemand[j][0]] = tmpDemand[j][-1]

    # Figure
    fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                            dpi=plotSettings['dpi'])

    # Mt
    ax1.set_ylabel('Hydrogen production [Mt]', fontsize=plotSettings['fontsize'])
    ax1.set_xlabel('Year', fontsize=plotSettings['fontsize'])

    # BCG
    #ax1.scatter(2030, 16.319, marker='o', color='None', edgecolors=darkblue, label='Boston Consulting Group, 2022')

    # Hydrogen production
    ax1.plot(x, dfPlotHM['Hydrogen Production - Median']/(1e6*33.3), label='Hydrogen Production (our work)', color=blue,
             linestyle='-')
    ax1.fill_between(x, dfPlotHM['Hydrogen Production - 25%']/(1e6*33.3),
                     dfPlotHM['Hydrogen Production - 75%']/(1e6*33.3), color=blue, edgecolor=None, alpha=0.25)

    # Hydrogen demand - what sectors
    #oldKey = 'None'
    #lastKey = True
    #for i in tmpDemand.keys():
    #    if dfPlotHM['Hydrogen Production - Median'].max() > tmpDemand[i][-1]:
    #        if oldKey == 'None':
    #            ax1.fill_between(x, 0, dfPlotHM[tmpDemand[i][0]]/1e6*33.3, color=tmpDemand[i][2], alpha=0.25,
    #                             edgecolor=None, label=tmpDemand[i][1], hatch=tmpDemand[i][3])
    #        else:
    #            ax1.fill_between(x, dfPlotHM[tmpDemand[oldKey][0]]/1e6*33.3, dfPlotHM[tmpDemand[i][0]]/1e6*33.3,
    #                             color=tmpDemand[i][2], alpha=0.25, edgecolor=None, label=tmpDemand[i][1],
    #                             hatch=tmpDemand[i][3])
    #    else:
    #        if lastKey:
    #            ax1.fill_between(x, dfPlotHM[tmpDemand[oldKey][0]]/1e6*33.3, dfPlotHM[tmpDemand[i][0]]/1e6*33.3,
    #                             color=tmpDemand[i][2], alpha=0.25, edgecolor=None, label=tmpDemand[i][1],
    #                             hatch=tmpDemand[i][3])
    #            lastKey = False
    #    oldKey = i

    # Estimation
    # Nach meta studie fraunhofer
    # https://www.wasserstoffrat.de/fileadmin/wasserstoffrat/media/Dokumente/Metastudie_Wasserstoff-Abschlussbericht.pdf
    # Adjusted with import quotas to get to production Fig. 23
    tmpBoxData = [[0.0, 0.0, 3.7, 0.0, 5.5, 14.0, 15.4, 17.5, 8.8, 7.5, 15.5, 13.0, 21.2, 85.0, 335.0],
                  [15.3, 33.8, 56.3, 63.8, 25.4, 78.8, 0.0, 26.6, 25.3, 53.6, 39.3, 70.2],
                  [0.0, 26.7, 60.0, 71.3, 86.3, 86.3, 35.8, 35.8, 156.0, 156.0, 6.5, 78.2, 234.0, 133.7, 137.3, 63.3,
                   644.0]]
    tmpBoxData = [[value / 33.3 for value in sublist] for sublist in tmpBoxData]

    box = ax1.boxplot(tmpBoxData, positions=[2030, 2040, 2050], widths=2.0, showfliers=False)

    # Erstelle die schwarze Box als Patch
    black_box = mpatches.Rectangle((0, 0), 1, 1, edgecolor='black', facecolor='None')

    # Erstelle die orangene Linie als Line2D
    orange_line = Line2D([0, 1], [0.5, 0.5], color='orange', linewidth=1)

    dummy_handle = (black_box, orange_line)


    # In TWh
    ax2 = ax1.twinx()
    ax2.set_ylabel('Hydrogen production [TWh]', fontsize=plotSettings['fontsize'])

    # Estimation
    # Nach meta studie fraunhofer
    # https://www.wasserstoffrat.de/fileadmin/wasserstoffrat/media/Dokumente/Metastudie_Wasserstoff-Abschlussbericht.pdf
    # Adjusted with import quotas to get to production Fig. 23
    tmpBoxData = [[0.0, 0.0, 3.7, 0.0, 5.5, 14.0, 15.4, 17.5, 8.8, 7.5, 15.5, 13.0, 21.2, 85.0, 335.0],
                  [15.3, 33.8, 56.3, 63.8, 25.4, 78.8, 0.0, 26.6, 25.3, 53.6, 39.3, 70.2],
                  [0.0, 26.7, 60.0, 71.3, 86.3, 86.3, 35.8, 35.8, 156.0, 156.0, 6.5, 78.2, 234.0, 133.7, 137.3, 63.3,
                   644.0]]
    ax2.boxplot(tmpBoxData, positions=[2030, 2040, 2050], widths=2.0, showfliers=False)

    # BCG
    #ax2.scatter(2030, 16.319 * 33.3, marker='o', color='None', edgecolors=darkblue)

    # Hydrogen production
    #ax2.plot(x, dfPlotHM['Hydrogen Production - Median']/(33.3*1e6), color=blue, linestyle='-')
    #ax2.fill_between(x, dfPlotHM['Hydrogen Production - 25%']/(33.3*1e6),
    #                 dfPlotHM['Hydrogen Production - 75%']/(33.3*1e6), color=blue, edgecolor=None, alpha=0.25)

    # Adjust axis
    ax1.minorticks_on()
    ax1.set_xlim(plotSettings['xlim'])
    ax1.set_ylim(0)
    ax1.set_xticks(plotSettings['xticks'])
    ax1.set_xticklabels(['2025', '2035', '2045'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(1))
    ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax1.tick_params(axis='both', which='minor', color='gray')

    ax2.minorticks_on()
    ax2.set_xlim(plotSettings['xlim'])
    ax2.set_ylim(0)
    ax2.set_xticks(plotSettings['xticks'])
    ax2.xaxis.set_minor_locator(MultipleLocator(5))
    ax2.yaxis.set_minor_locator(MultipleLocator(50))
    ax2.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax2.tick_params(axis='both', which='minor', color='gray')

    # Adjust legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    handles = handles1 + handles2 + [dummy_handle]
    labels = labels1 + labels2 + ['Wietschel et al., 2021 [99]']

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.45),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save plot
    plt.savefig(os.getcwd() + '\\figure7.' + plotType, bbox_inches='tight')

    # Write out Data
    writeDf = dfPlotHM.copy(deep=True)
    writeDf.columns = [f"{col} [TWh]" for col in writeDf.columns]
    writeDf = writeDf/1e6
    writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure7.csv', sep=';')



class CombinedHandler:
    def __init__(self, patch, line):
        self.patch = patch
        self.line = line

    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        # Zeichnet das Rechteck (Box)
        patch_artist = mpatches.Rectangle((0, 0), 1, 1,
                                          facecolor='black',
                                          transform=handlebox.get_transform())
        handlebox.add_artist(patch_artist)
        # Zeichnet die orange Linie horizontal mittig
        line_artist = Line2D([0, 1], [0.5, 0.5],
                             color='orange',
                             linewidth=2,
                             transform=handlebox.get_transform())
        handlebox.add_artist(line_artist)
        return patch_artist



def figure_8(dfRES, dfELC):
    '''
    Function that will create Fig. 8 - Utilization of Renewables and Electrolyzers of the reference case.
    :param:
        pd.DataFrame dfRES: Yearly data from the renewables for the reference case.
        pd.DataFrame dfELC: Yearly data from the electrolyzers for the reference case.
    :return:
    '''
    # Renewables
    tmpRES = dfRES.set_index(['Year', 'Run', 'ID'])
    dfPlotRES = pd.DataFrame(data=np.nan, index=range(yearDelta), columns=['Median', '25%', '75%'])

    # Electrolyzers
    tmpELC = dfELC.set_index(['Year', 'Run', 'ID'])
    dfPlotELC = pd.DataFrame(data=np.nan, index=range(yearDelta), columns=['Median', '25%', '75%'])

    for i in range(yearDelta):
        # Renewables
        if i in tmpRES.index.levels[0]:
            tmpDf = tmpRES.loc[i]['Utilization rate'].groupby(level=0).max()
            dfPlotRES.loc[i, 'Median'] = tmpDf.median()*100
            dfPlotRES.loc[i, '25%'] = tmpDf.quantile(q=0.25)*100
            dfPlotRES.loc[i, '75%'] = tmpDf.quantile(q=0.75)*100

        # Electrolyzers
        if i in  tmpELC.index.levels[0]:
            tmpDf = tmpELC.loc[i]['Utilization rate'].groupby(level=0).max()
            dfPlotELC.loc[i, 'Median'] = tmpDf.median()*100
            dfPlotELC.loc[i, '25%'] = tmpDf.quantile(q=0.25)*100
            dfPlotELC.loc[i, '75%'] = tmpDf.quantile(q=0.75)*100

    # Figure
    fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                            dpi=plotSettings['dpi'])

    ax1.set_ylabel('Utilization rate [%]', fontsize=plotSettings['fontsize'])
    ax1.set_xlabel('Year', fontsize=plotSettings['fontsize'])

    # In %
    # Renewables
    ax1.plot(x, dfPlotRES['Median'], label='Renewables', color=green, linestyle='-')
    ax1.fill_between(x, dfPlotRES['25%'], dfPlotRES['75%'], color=green, edgecolor=None, alpha=0.25)

    # Electrolyzers
    ax1.plot(x, dfPlotELC['Median'], label='Electrolyzers', color=blue, linestyle='-')
    ax1.fill_between(x, dfPlotELC['25%'], dfPlotELC['75%'], color=blue, edgecolor=None, alpha=0.25)

    # In full load hours
    ax2 = ax1.twinx()
    ax2.set_ylabel('Full load hours [h]', fontsize=plotSettings['fontsize'])

    # Renewables
    ax2.plot(x, dfPlotRES['Median']*87.6, label='Renewables', color=green, linestyle='-')
    ax2.fill_between(x, dfPlotRES['25%']*87.6, dfPlotRES['75%']*87.6, color=green, edgecolor=None, alpha=0.25)

    # Electrolyzers
    ax2.plot(x, dfPlotELC['Median']*87.6, label='Electrolyzers', color=blue, linestyle='-')
    ax2.fill_between(x, dfPlotELC['25%']*87.6, dfPlotELC['75%']*87.6, color=blue, edgecolor=None, alpha=0.25)

    # Adjust axis
    ax1.minorticks_on()
    ax1.set_xlim(plotSettings['xlim'])
    ax1.set_ylim([0, 100])
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(10))
    ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax1.tick_params(axis='both', which='minor', color='gray')

    ax2.minorticks_on()
    ax2.set_xlim(plotSettings['xlim'])
    ax2.set_ylim([0, 8760])
    ax2.set_xticks(plotSettings['xticks'])
    ax2.xaxis.set_minor_locator(MultipleLocator(5))
    ax2.yaxis.set_minor_locator(MultipleLocator(1000))
    ax2.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax2.tick_params(axis='both', which='minor', color='gray')

    # Adjust legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    handles = handles1 + handles2
    labels = labels1 + labels2

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.45),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save plot
    plt.savefig(os.getcwd() + '\\figure8.' + plotType, bbox_inches='tight')

    # Write data
    writeDf = pd.DataFrame(data=[dfPlotRES['Median'], dfPlotRES['25%'], dfPlotRES['75%'], dfPlotRES['Median']*87.6,
                                 dfPlotRES['25%']*87.6, dfPlotRES['75%']*87.6, dfPlotELC['Median'], dfPlotELC['25%'],
                                 dfPlotELC['75%'], dfPlotELC['Median']*87.6, dfPlotELC['25%']*87.6,
                                 dfPlotELC['75%']*87.6],
                           index=['Renewables - median [%]','Renewables - 25% [%]','Renewables - 75% [%]',
                                  'Renewables - median [h]','Renewables - 25% [h]','Renewables - 75% [h]',
                                  'Electrolyzers - median [%]', 'Electrolyzers - 25% [%]', 'Electrolyzers - 75% [%]',
                                  'Electrolyzers - median [h]', 'Electrolyzers - 25% [h]', 'Electrolyzers - 75% [h]'])
    writeDf = writeDf.T
    writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure8.csv', sep=';')


def figure_9(dfPM):
    '''
    Function that will create Fig. 9 - Load types for the Electrolyzers of the reference case.
    :param:
        pd.DataFrame dfPM: Yearly data from the power market for the reference case.
    :return:
    '''
    # Electrolyzers
    tmpPM = dfPM.set_index(['Year', 'Run'])
    dfPlotPM = pd.DataFrame(data=np.NaN, index=range(yearDelta), columns=['No load', 'Partial load', 'Full load'])

    for i in range(yearDelta):
        # Electrolyzers
        if i in tmpPM.index.levels[0]:
            tmpDf = tmpPM.loc[i]['Cost share']
            tmpNL = pd.Series()
            tmpPL = pd.Series()
            tmpFL = pd.Series()
            k = 0
            for j in tmpDf:
                tmpNL[k] = float(j[1:-1].split(' ')[0])
                tmpPL[k] = float(j[1:-1].split(' ')[1])
                tmpFL[k] = float(j[1:-1].split(' ')[2])
                k += 1
            dfPlotPM.loc[i, 'No load'] = tmpNL.median() / (tmpNL.median() + tmpPL.median() + tmpFL.median()) * 100
            dfPlotPM.loc[i, 'Partial load'] = tmpPL.median() / (tmpNL.median() + tmpPL.median() + tmpFL.median()) * 100
            dfPlotPM.loc[i, 'Full load'] = tmpFL.median() / (tmpNL.median() + tmpPL.median() + tmpFL.median()) * 100

    # Figure
    fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                            dpi=plotSettings['dpi'])

    # In %
    ax1.set_ylabel('Type of load [%]', fontsize=plotSettings['fontsize'])
    ax1.set_xlabel('Year', fontsize=plotSettings['fontsize'])

    # Load type
    ax1.fill_between(x, 0, dfPlotPM['No load'], label='No load', color=grey, alpha=0.5, edgecolor=None)
    ax1.fill_between(x, dfPlotPM['No load'], dfPlotPM['No load'] + dfPlotPM['Partial load'],
                     label='Partial load', color=blue, alpha=0.5, edgecolor=None)
    ax1.fill_between(x, dfPlotPM['No load'] + dfPlotPM['Partial load'],
                     dfPlotPM['No load'] + dfPlotPM['Partial load'] + dfPlotPM['Full load'],
                     label='Full load', color=green, alpha=0.5, edgecolor=None)

    # In hours
    ax2 = ax1.twinx()
    ax2.set_ylabel('Type of load [h]', fontsize=plotSettings['fontsize'])

    # Load type
    ax2.fill_between(x, 0, dfPlotPM['No load']*87.6, label='No load', color=grey, alpha=0.5, edgecolor=None)
    ax2.fill_between(x, dfPlotPM['No load']*87.6, dfPlotPM['No load']*87.6 + dfPlotPM['Partial load']*87.6,
                     label='Partial load', color=blue, alpha=0.5, edgecolor=None)
    ax2.fill_between(x, dfPlotPM['No load']*87.6 + dfPlotPM['Partial load']*87.6,
                     dfPlotPM['No load']*87.6 + dfPlotPM['Partial load']*87.6 + dfPlotPM['Full load']*87.6,
                     label='Full load', color=green, alpha=0.5, edgecolor=None)

    # Adjust axis
    ax1.minorticks_on()
    ax1.set_xlim(plotSettings['xlim'])
    ax1.set_ylim([0, 100])
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(10))
    ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax1.tick_params(axis='both', which='minor', color='gray')

    ax2.minorticks_on()
    ax2.set_xlim(plotSettings['xlim'])
    ax2.set_ylim([0, 8760])
    ax2.set_xticks(plotSettings['xticks'])
    ax2.xaxis.set_minor_locator(MultipleLocator(5))
    ax2.yaxis.set_minor_locator(MultipleLocator(1000))
    ax2.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax2.tick_params(axis='both', which='minor', color='gray')

    # Adjust legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    handles = handles1 + handles2
    labels = labels1 + labels2

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.45),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save plot
    plt.savefig(os.getcwd() + '\\figure9.' + plotType, bbox_inches='tight')

    # Write data
    writeDf = pd.DataFrame(data=[dfPlotPM['No load'], dfPlotPM['Partial load'], dfPlotPM['Full load'],
                                 dfPlotPM['No load']*87.6, dfPlotPM['Partial load']*87.6, dfPlotPM['Full load']*87.6],
                           index=['No load [%]', 'Partial load [%]', 'Full load [%]', 'No load [h]', 'Partial load [h]',
                                  'Full load [h]'])
    writeDf = writeDf.T
    writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure9.csv', sep=';')


def figure_10(dfPP, dfHP, dfEP):
    '''
    Function that will create Fig. 10 - Wallet for PP, HP & EP of the reference case.
    :param:
        pd.DataFrame dfPP: Yearly data from the power producers for the reference case.
        pd.DataFrame dfHP: Yearly data from the hydrogen producers for the reference case.
        pd.DataFrame dfEP: Yearly data from the electrolyzer producers for the reference case.
    :return:
    '''
    # Power producers
    tmpPP = dfPP.set_index(['Year', 'Run', 'ID'])
    dfPlotPP = pd.DataFrame(data=np.NaN, index=range(yearDelta), columns=['median', '25%', '75%'])

    # Hydrogen producers
    tmpHP = dfHP.set_index(['Year', 'Run', 'ID'])
    dfPlotHP = pd.DataFrame(data=np.NaN, index=range(yearDelta), columns=['median', '25%', '75%'])

    # Electrolyzer producers
    tmpEP = dfEP.set_index(['Year', 'Run', 'ID'])
    dfPlotEP = pd.DataFrame(data=np.NaN, index=range(yearDelta), columns=['median', '25%', '75%'])

    for i in range(yearDelta):
        # Power producers
        if i in tmpPP.index.levels[0]:
            tmpDf = tmpPP.loc[i].groupby(level=0).sum()
            tmpDf = tmpDf['Wallet']
            dfPlotPP.loc[i, 'median'] = tmpDf.median()/1e9
            dfPlotPP.loc[i, '25%'] = tmpDf.quantile(q=0.25)/1e9
            dfPlotPP.loc[i, '75%'] = tmpDf.quantile(q=0.75)/1e9

        # Hydrogen producers
        if i in tmpHP.index.levels[0]:
            tmpDf = tmpHP.loc[i].groupby(level=0).sum()
            tmpDf = tmpDf['Wallet']
            dfPlotHP.loc[i, 'median'] = tmpDf.median()/1e9
            dfPlotHP.loc[i, '25%'] = tmpDf.quantile(q=0.25)/1e9
            dfPlotHP.loc[i, '75%'] = tmpDf.quantile(q=0.75)/1e9

        # Electrolyzer producers
        if i in tmpEP.index.levels[0]:
            tmpDf = tmpEP.loc[i].groupby(level=0).sum()
            tmpDf = tmpDf['Wallet']
            dfPlotEP.loc[i, 'median'] = tmpDf.median()/1e9
            dfPlotEP.loc[i, '25%'] = tmpDf.quantile(q=0.25)/1e9
            dfPlotEP.loc[i, '75%'] = tmpDf.quantile(q=0.75)/1e9

    # Figure
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=plotSettings['figsize_3t'],
                                        gridspec_kw=plotSettings['gridspec_kw'], dpi=plotSettings['dpi'], sharex=True)

    # Power producers
    ax1.plot([0, 3000], [0, 0], color=black, linewidth=1)
    ax1.plot(x, dfPlotPP['median'], label='Power producers', linestyle='-', color=green)
    ax1.fill_between(x, dfPlotPP['25%'], dfPlotPP['75%'], color=green, alpha=0.25, edgecolor=None)
    #ax1.set_ylim([-5, 10])

    # Hydrogen producers
    ax2.set_ylabel('Liquidity [Bn. €]', fontsize=plotSettings['fontsize'])
    ax2.plot([0, 3000], [0, 0], color=black, linewidth=1)
    ax2.plot(x, dfPlotHP['median'], label='Hydrogen producers', linestyle='-', color=blue)
    ax2.fill_between(x, dfPlotHP['25%'], dfPlotHP['75%'], color=blue, alpha=0.25, edgecolor=None)
    #ax2.set_ylim([-5, 10])

    # Electrolyzer producers
    ax3.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    ax3.plot([0, 3000], [0, 0], color=black, linewidth=1)
    ax3.plot(x, dfPlotEP['median'], label='Electrolyzer producers', linestyle='-', color=purple)
    ax3.fill_between(x, dfPlotEP['25%'], dfPlotEP['75%'], color=purple, alpha=0.25, edgecolor=None)
    #ax3.set_ylim([-5, 10])

    #fig.text(-0.1, 0.5, 'Liquidity [Bn. €]', va='center', rotation='vertical', fontsize=plotSettings['fontsize'])

    plt.xlim(plotSettings['xlim'])

    # Adjust ticks
    ax1.minorticks_on()
    ax2.minorticks_on()
    ax3.minorticks_on()
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(125))
    ax1.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax1.tick_params(which='minor', axis='both', color='gray')
    ax2.yaxis.set_minor_locator(MultipleLocator(125))
    ax2.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax2.tick_params(which='minor', axis='both', color='gray')
    ax3.yaxis.set_minor_locator(MultipleLocator(125))
    ax3.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax3.tick_params(which='minor', axis='both', color='gray')

    # Legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles3, labels3 = ax3.get_legend_handles_labels()

    handles = handles1 + handles2 + handles3
    labels = labels1 + labels2 + labels3

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.45),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save figure
    plt.savefig(os.getcwd() + '\\figure10.' + plotType, bbox_inches='tight')

    # Write data
    writeDf = pd.DataFrame(data=[dfPlotPP['median'], dfPlotPP['25%'], dfPlotPP['75%'], dfPlotHP['median'],
                                 dfPlotHP['25%'], dfPlotHP['75%'], dfPlotEP['median'], dfPlotEP['25%'], dfPlotEP['75%']],
                           index=['Power producers - median [Mio. €]', 'Power producers - 25% [Mio. €]',
                                  'Power producers - 75 [Mio. €]', 'Hydrogen producers - median [Mio. €]',
                                  'Hydrogen producers - 25% [Mio. €]', 'Hydrogen producers - 75 [Mio. €]',
                                  'Electrolyzer producers - median [Mio. €]', 'Electrolyzer producers - 25% [Mio. €]',
                                  'Electrolyzer producers - 75 [Mio. €]'])
    writeDf = writeDf.T
    writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure10.csv', sep=';')


def figure_11(dfPP, dfHP, dfEP):
    '''
    Function that will create Fig. 11 - ROI for PP, HP & EP of the reference case.
    :param:
        pd.DataFrame dfPP: Yearly data from the power producers for the reference case.
        pd.DataFrame dfHP: Yearly data from the hydrogen producers for the reference case.
        pd.DataFrame dfEP: Yearly data from the electrolyzer producers for the reference case.
    :return:
    '''
    # Power producers
    tmpPP = dfPP.set_index(['Year', 'Run', 'ID'])
    dfPlotPP = pd.DataFrame(data=np.NaN, index=range(yearDelta), columns=['median', '25%', '75%'])

    # Hydrogen producers
    tmpHP = dfHP.set_index(['Year', 'Run', 'ID'])
    dfPlotHP = pd.DataFrame(data=np.NaN, index=range(yearDelta), columns=['median', '25%', '75%'])

    # Electrolyzer producers
    tmpEP = dfEP.set_index(['Year', 'Run', 'ID'])
    dfPlotEP = pd.DataFrame(data=np.NaN, index=range(yearDelta), columns=['median', '25%', '75%'])

    for i in range(yearDelta):
        # Power producers
        if i in tmpPP.index.levels[0]:
            tmpDf = tmpPP.loc[i]['Return on Investment']
            dfPlotPP.loc[i, 'median'] = tmpDf.median() * 100
            dfPlotPP.loc[i, '25%'] = tmpDf.quantile(q=0.25) * 100
            dfPlotPP.loc[i, '75%'] = tmpDf.quantile(q=0.75) * 100

        # Hydrogen producers
        if i in tmpHP.index.levels[0]:
            tmpDf = tmpHP.loc[i]['Return on Investment']
            dfPlotHP.loc[i, 'median'] = tmpDf.median() * 100
            dfPlotHP.loc[i, '25%'] = tmpDf.quantile(q=0.25) * 100
            dfPlotHP.loc[i, '75%'] = tmpDf.quantile(q=0.75) * 100

        # Electrolyzer producers
        if i in tmpEP.index.levels[0]:
            tmpDf = tmpEP.loc[i]['Return on Investment']
            dfPlotEP.loc[i, 'median'] = tmpDf.median() * 100
            dfPlotEP.loc[i, '25%'] = tmpDf.quantile(q=0.25) * 100
            dfPlotEP.loc[i, '75%'] = tmpDf.quantile(q=0.75) * 100

    # Figure
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=plotSettings['figsize_3t'],
                                        gridspec_kw=plotSettings['gridspec_kw'], dpi=plotSettings['dpi'], sharex=True)

    # Power producers
    ax1.plot(x, dfPlotPP['median'], label='Power producers', linestyle='-', color=green)
    ax1.fill_between(x, dfPlotPP['25%'], dfPlotPP['75%'], color=green, alpha=0.25, edgecolor=None)
    #ax1.set_ylim([-0.1, 55])

    # Hydrogen producers
    ax2.plot(x, dfPlotHP['median'], label='Hydrogen producers', linestyle='-', color=blue)
    ax2.fill_between(x, dfPlotHP['25%'], dfPlotHP['75%'], color=blue, alpha=0.25, edgecolor=None)
    #ax2.set_ylim([-0.1, 55])

    # Electrolyzer producers
    ax3.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    ax3.plot(x, dfPlotEP['median'], label='Electrolyzer producers', linestyle='-', color=purple)
    ax3.fill_between(x, dfPlotEP['25%'], dfPlotEP['75%'], color=purple, alpha=0.25, edgecolor=None)
    #ax3.set_ylim([-0.1, 55])

    fig.text(-0.1, 0.5, 'Return on Investment [%]', va='center', rotation='vertical', fontsize=plotSettings['fontsize'])

    plt.xlim(plotSettings['xlim'])

    # Adjust ticks
    ax1.minorticks_on()
    ax2.minorticks_on()
    ax3.minorticks_on()
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(5))
    ax1.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax1.tick_params(which='minor', axis='both', color='gray')
    ax2.yaxis.set_minor_locator(MultipleLocator(5))
    ax2.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax2.tick_params(which='minor', axis='both', color='gray')
    ax3.yaxis.set_minor_locator(MultipleLocator(5))
    ax3.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax3.tick_params(which='minor', axis='both', color='gray')

    # Legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles3, labels3 = ax3.get_legend_handles_labels()

    handles = handles1 + handles2 + handles3
    labels = labels1 + labels2 + labels3

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.55),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save figure
    plt.savefig(os.getcwd() + '\\figure11.' + plotType, bbox_inches='tight')

    # Write data
    writeDf = pd.DataFrame(data=[dfPlotPP['median'], dfPlotPP['25%'], dfPlotPP['75%'], dfPlotHP['median'],
                                 dfPlotHP['25%'], dfPlotHP['75%'], dfPlotEP['median'], dfPlotEP['25%'],
                                 dfPlotEP['75%']],
                           index=['Power producers - median [%]', 'Power producers - 25% [%]',
                                  'Power producers - 75 [%]','Hydrogen producers - median [%]',
                                  'Hydrogen producers - 25% [%]', 'Hydrogen producers - 75 [%]',
                                  'Electrolyzer producers - median [%]', 'Electrolyzer producers - 25% [%]',
                                  'Electrolyzer producers - 75 [%]'])
    writeDf = writeDf.T
    writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure11.csv', sep=';')


def figure_12(dfPP, dfHP, dfEP):
    '''
    Function that will create Fig. 12 - Expected profitability for a new asset in the reference case.
    :param:
        pd.DataFrame dfPP: Yearly data from the power producers for the reference case.
        pd.DataFrame dfHP: Yearly data from the hydrogen producers for the reference case.
        pd.DataFrame dfEP: Yearly data from the electrolyzer producers for the reference case.
    :return:
    '''
    # Fixed calues
    tmpInvestRES = 1250000.
    tmpInvestFAC = 500000.
    tmpCRFRES = 0.05 / (1 - (1 + 0.05) ** -20)
    tmpCRFELC = 0.05 / (1 - (1 + 0.05) ** -15)
    tmpCRFFAC = 0.05 / (1 - (1 + 0.05) ** -20)

    # Renewables
    tmpRES = dfPP.set_index(['Year', 'Run', 'ID'])
    dfPlotRES = pd.DataFrame(data=np.NaN, index=range(yearDelta), columns=['median', '25%', '75%'])

    # Electrolyzers
    tmpELC = dfHP.set_index(['Year', 'Run', 'ID'])
    dfPlotELC = pd.DataFrame(data=np.NaN, index=range(yearDelta), columns=['median', '25%', '75%'])

    # Factories
    tmpFAC = dfEP.set_index(['Year', 'Run', 'ID'])
    dfPlotFAC = pd.DataFrame(data=np.NaN, index=range(yearDelta), columns=['median', '25%', '75%'])

    for i in range(yearDelta):
        # Renewables
        if i in tmpRES.index.levels[0]:
            tmpDf = ((tmpRES.loc[i]['Income'] / tmpRES.loc[i]['Installed capacity Renewables']) /
                     (tmpCRFRES * tmpInvestRES))
            dfPlotRES.loc[i, 'median'] = tmpDf.median()
            dfPlotRES.loc[i, '25%'] = tmpDf.quantile(q=0.25)
            dfPlotRES.loc[i, '75%'] = tmpDf.quantile(q=0.75)

        # Electrolyzers
        if i in tmpELC.index.levels[0]:
            tmpDf = ((tmpELC.loc[i]['Income'] / tmpELC.loc[i]['Installed capacity Electrolyzers']) /
                     ((tmpELC.loc[i]['Expense'] / tmpELC.loc[i]['Installed capacity Electrolyzers']) +
                      (tmpCRFELC * tmpFAC.loc[i]['Minimal costs Electrolyzers'].min())))
            dfPlotELC.loc[i, 'median'] = tmpDf.median()
            dfPlotELC.loc[i, '25%'] = tmpDf.quantile(q=0.25)
            dfPlotELC.loc[i, '75%'] = tmpDf.quantile(q=0.75)

        # Factories
        if i in tmpFAC.index.levels[0]:
            tmpDf = ((tmpFAC.loc[i]['Income'] / tmpFAC.loc[i]['Installed capacity Manufacturings']) /
                     ((tmpFAC.loc[i]['Expense'] / tmpFAC.loc[i]['Installed capacity Manufacturings']) +
                      (tmpCRFFAC * tmpInvestFAC)))
            dfPlotFAC.loc[i, 'median'] = tmpDf.median()
            dfPlotFAC.loc[i, '25%'] = tmpDf.quantile(q=0.25)
            dfPlotFAC.loc[i, '75%'] = tmpDf.quantile(q=0.75)

    # Figure
    fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                            dpi=plotSettings['dpi'])

    ax1.set_ylabel('Profitability Index [-]', fontsize=plotSettings['fontsize'])
    ax1.set_xlabel('Year', fontsize=plotSettings['fontsize'])

    # Threshold
    ax1.plot([0, 3000], [1, 1], label='Profitability threshold', color=black, linestyle='--')

    # New Renewables
    ax1.plot(x, dfPlotRES['median'], label='Renewables', color=green, linestyle='-')
    ax1.fill_between(x, dfPlotRES['25%'], dfPlotRES['75%'], color=green, alpha=0.25, edgecolor=None)

    # New Electrolyzer
    ax1.plot(x, dfPlotELC['median'], label='Electrolyzers', color=blue, linestyle='-')
    ax1.fill_between(x, dfPlotELC['25%'], dfPlotELC['75%'], color=blue, alpha=0.25, edgecolor=None)

    # New Factories
    ax1.plot(x, dfPlotFAC['median'], label='Factory', color=purple, linestyle='-')
    ax1.fill_between(x, dfPlotFAC['25%'], dfPlotFAC['75%'], color=purple, alpha=0.25, edgecolor=None)

    plt.ylim(0)
    plt.xlim(plotSettings['xlim'])

    # Adjust ticks
    ax1.minorticks_on()
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(5))
    ax1.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax1.tick_params(which='minor', axis='both', color='gray')

    # Legend
    handles1, labels1 = ax1.get_legend_handles_labels()

    handles = handles1
    labels = labels1

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.45),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save figure
    plt.savefig(os.getcwd() + '\\figure12.' + plotType, bbox_inches='tight')

    # Write data
    writeDf = pd.DataFrame(data=[dfPlotRES['median'], dfPlotRES['25%'], dfPlotRES['75%'], dfPlotELC['median'],
                                 dfPlotELC['25%'], dfPlotELC['75%'], dfPlotFAC['median'], dfPlotFAC['25%'],
                                 dfPlotFAC['75%']],
                           index=['Profitability Index new Renewable - median [-]',
                                  'Profitability Index new Renewable - 25% [-]',
                                  'Profitability Index new Renewable - 75 [-]',
                                  'Profitability Index new Electrolyzer - median [-]',
                                  'Profitability Index new Electrolyzer - 25% [-]',
                                  'Profitability Index new Electrolyzer - 75 [-]',
                                  'Profitability Index new Factory - median [-]',
                                  'Profitability Index new Factory - 25% [-]',
                                  'Profitability Index new Factory - 75 [-]'])
    writeDf = writeDf.T
    writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure12.csv', sep=';')


def figure_13(dfPM, dfHM, dfEM):
    '''
    Function that will create Fig. 13 - Invested money over time in the reference case.
    :param:
        pd.DataFrame dfPM: Yearly data from the power market for the reference case.
        pd.DataFrame dfHM: Yearly data from the electrolyzer sales for the reference case.
        pd.DataFrame dfEM: Yearly data from the electrolyzer market for the reference case.
    :return:
    '''
    # Fixed values
    tmpInvestRES = 1250000.
    tmpInvestFAC = 500000.

    # Power market
    tmpPM = dfPM.set_index(['Year', 'Run'])
    dfPlotPM = pd.DataFrame(data=np.NaN, index=range(yearDelta), columns=['year - median', 'year - 25%', 'year - 75%',
                                                                          'cum - median', 'cum - 25%', 'cum - 75%'])
    tmpPMCum = pd.Series(data=0, index=tmpPM.loc[0].index)


    # Hydrogen market
    tmpHM = dfHM.set_index(['Year', 'Run'])
    dfPlotHM = pd.DataFrame(data=np.NaN, index=range(yearDelta), columns=['year - median', 'year - 25%', 'year - 75%',
                                                                          'cum - median', 'cum - 25%', 'cum - 75%'])
    tmpHMCum = pd.Series(data=0, index=tmpPM.loc[0].index)

    # Electrolyzer market
    tmpEM = dfEM.set_index(['Year', 'Run'])
    dfPlotEM = pd.DataFrame(data=np.NaN, index=range(yearDelta), columns=['year - median', 'year - 25%', 'year - 75%',
                                                                          'cum - median', 'cum - 25%', 'cum - 75%'])
    tmpEMCum = pd.Series(data=0, index=tmpPM.loc[0].index)

    for i in range(yearDelta):
        # Power market
        if i in tmpPM.index.levels[0]:
            # Per Year
            tmpDf = tmpPM.loc[i]['Added capacity Renewables'] * tmpInvestRES / 1e9
            dfPlotPM.loc[i, 'year - median'] = tmpDf.median()
            dfPlotPM.loc[i, 'year - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotPM.loc[i, 'year - 75%'] = tmpDf.quantile(q=0.75)
            # Cumulative
            tmpPMCum = tmpPMCum + tmpDf
        dfPlotPM.loc[i, 'cum - median'] = tmpPMCum.median()
        dfPlotPM.loc[i, 'cum - 25%'] = tmpPMCum.quantile(q=0.25)
        dfPlotPM.loc[i, 'cum - 75%'] = tmpPMCum.quantile(q=0.75)

        # Hydrogen market
        if i in tmpHM.index.levels[0]:
            # Per Year
            tmpHMAbs = pd.Series(data=0, index=tmpHM.loc[0].index)
            tmpDf = tmpHM.loc[i]['Price'] * tmpHM.loc[i]['Capacity']
            tmpDf = tmpDf.groupby(level=0).sum() / 1e9
            tmpHMAbs = tmpHMAbs.add(tmpDf, fill_value=0)
            dfPlotHM.loc[i, 'year - median'] = tmpHMAbs.median()
            dfPlotHM.loc[i, 'year - 25%'] = tmpHMAbs.quantile(q=0.25)
            dfPlotHM.loc[i, 'year - 75%'] = tmpHMAbs.quantile(q=0.75)
            # Cumulative
            tmpHMCum = tmpHMCum.add(tmpDf, fill_value=0)
        dfPlotHM.loc[i, 'cum - median'] = tmpHMCum.median()
        dfPlotHM.loc[i, 'cum - 25%'] = tmpHMCum.quantile(q=0.25)
        dfPlotHM.loc[i, 'cum - 75%'] = tmpHMCum.quantile(q=0.75)

        # Electrolyzer market
        if i in tmpEM.index.levels[0]:
            # Per Year
            tmpDf = tmpEM.loc[i]['Added capacity Manufacturings'] * tmpInvestFAC / 1e9
            dfPlotEM.loc[i, 'year - median'] = tmpDf.median()
            dfPlotEM.loc[i, 'year - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotEM.loc[i, 'year - 75%'] = tmpDf.quantile(q=0.75)
            # Cumulative
            tmpEMCum = tmpEMCum + tmpDf
        dfPlotEM.loc[i, 'cum - median'] = tmpEMCum.median()
        dfPlotEM.loc[i, 'cum - 25%'] = tmpEMCum.quantile(q=0.25)
        dfPlotEM.loc[i, 'cum - 75%'] = tmpEMCum.quantile(q=0.75)

    # Figure
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=plotSettings['figsize_3t'],
                                        gridspec_kw=plotSettings['gridspec_kw'], dpi=plotSettings['dpi'], sharex=True)

    # Power market
    ax1.set_ylabel('Renewables', fontsize=plotSettings['fontsize'])
    # Results data
    # Per year
    ax1.plot(x, dfPlotPM['year - median'], label='Power producer', linestyle='-', color=green)
    ax1.fill_between(x, dfPlotPM['year - 25%'], dfPlotPM['year - 75%'], alpha=0.25, color=green, edgecolor=None)
    ax1.set_ylim(-0.01)
    # Cumulative
    ax12 = ax1.twinx()
    ax12.set_ylabel('Renewables', fontsize=plotSettings['fontsize'])
    ax12.plot(x, dfPlotPM['cum - median'], label='Power producer - cumulative', linestyle='--', color=green)
    ax12.fill_between(x, dfPlotPM['cum - 25%'], dfPlotPM['cum - 75%'], alpha=0.25, color=green, edgecolor=None,
                      hatch='///')
    ax12.set_ylim(-0.01)

    # Hydrogen market
    ax2.set_ylabel('Electrolyzers', fontsize=plotSettings['fontsize'])
    # Results data
    # Per year
    ax2.plot(x, dfPlotHM['year - median'], label='Hydrogen producer', linestyle='-', color=blue)
    ax2.fill_between(x, dfPlotHM['year - 25%'], dfPlotHM['year - 75%'], alpha=0.25, color=blue, edgecolor=None)
    ax2.set_ylim(-0.1)
    # Cumulative
    ax22 = ax2.twinx()
    ax22.set_ylabel('Electrolyzers', fontsize=plotSettings['fontsize'])
    ax22.plot(x, dfPlotHM['cum - median'], label='Hydrogen producer - cumulative', linestyle='--', color=blue)
    ax22.fill_between(x, dfPlotHM['cum - 25%'], dfPlotHM['cum - 75%'], alpha=0.25, color=blue, edgecolor=None,
                      hatch='///')
    ax22.set_ylim(-0.01)

    # Electrolyzer market
    ax3.set_ylabel('Factories', fontsize=plotSettings['fontsize'])
    ax3.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    # Results data
    # Per year
    ax3.plot(x, dfPlotEM['year - median'], label='Electrolyzer producer', linestyle='-', color=purple)
    ax3.fill_between(x, dfPlotEM['year - 25%'], dfPlotEM['year - 75%'], alpha=0.25, color=purple, edgecolor=None)
    ax3.set_ylim(-0.01)
    # Cumulative
    ax32 = ax3.twinx()
    ax32.set_ylabel('Factories', fontsize=plotSettings['fontsize'])
    ax32.plot(x, dfPlotEM['cum - median'], label='Electrolyzer producer - cumulative', linestyle='--', color=purple)
    ax32.fill_between(x, dfPlotEM['cum - 25%'], dfPlotEM['cum - 75%'], alpha=0.25, color=purple, edgecolor=None,
                      hatch='///')
    ax32.set_ylim(-0.01)

    fig.text(-0.1, 0.5, 'Yearly Investment [Bn. €]', va='center', rotation='vertical', fontsize=plotSettings['fontsize'])
    fig.text(1.1, 0.5, 'Cumulative investment [Bn. €]', va='center', rotation='vertical',
             fontsize=plotSettings['fontsize'])

    plt.xlim(plotSettings['xlim'])

    # Adjust ticks
    ax1.minorticks_on()
    ax12.minorticks_on()
    ax2.minorticks_on()
    ax22.minorticks_on()
    ax3.minorticks_on()
    ax32.minorticks_on()
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(10))
    ax1.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax1.tick_params(which='minor', axis='both', color='gray')
    ax12.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax12.yaxis.set_minor_locator(MultipleLocator(100))
    ax12.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax12.tick_params(which='minor', axis='both', color='gray')
    ax2.yaxis.set_minor_locator(MultipleLocator(1))
    ax2.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax2.tick_params(which='minor', axis='both', color='gray')
    ax22.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax22.yaxis.set_minor_locator(MultipleLocator(10))
    ax22.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax22.tick_params(which='minor', axis='both', color='gray')
    ax3.yaxis.set_minor_locator(MultipleLocator(0.25))
    ax3.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax3.tick_params(which='minor', axis='both', color='gray')
    ax32.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax32.yaxis.set_minor_locator(MultipleLocator(5))
    ax32.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax32.tick_params(which='minor', axis='both', color='gray')

    # Legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles12, labels12 = ax12.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles22, labels22 = ax22.get_legend_handles_labels()
    handles3, labels3 = ax3.get_legend_handles_labels()
    handles32, labels32 = ax32.get_legend_handles_labels()

    handles = handles1 + handles2 + handles3 + handles12 + handles22 + handles32
    labels = labels1 + labels2 + labels3 + labels12 + labels22 + labels32

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.5),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save figure
    plt.savefig(os.getcwd() + '\\figure13.' + plotType, bbox_inches='tight')

    # Write Data
    writeDf = pd.DataFrame(data=[dfPlotPM['year - median'], dfPlotPM['year - 25%'], dfPlotPM['year - 75%'],
                                 dfPlotPM['cum - median'], dfPlotPM['cum - 25%'], dfPlotPM['cum - 75%'],
                                 dfPlotHM['year - median'], dfPlotHM['year - 25%'], dfPlotHM['year - 75%'],
                                 dfPlotHM['cum - median'], dfPlotHM['cum - 25%'], dfPlotHM['cum - 75%'],
                                 dfPlotEM['year - median'], dfPlotEM['year - 25%'], dfPlotEM['year - 75%'],
                                 dfPlotEM['cum - median'], dfPlotEM['cum - 25%'], dfPlotEM['cum - 75%']],
                           index=['Renewables - median [Bn. €]', 'Renewables - 25% [Bn. €]', 'Renewables - 75% [Bn. €]',
                                  'Renewables cum. - median [Bn. €]', 'Renewables cum. - 25% [Bn. €]',
                                  'Renewables cum. - 75% [Bn. €]', 'Electrolyzers - median [Bn. €]',
                                  'Electrolyzers - 25% [Bn. €]', 'Electrolyzers - 75% [Bn. €]',
                                  'Electrolyzers cum. - median [Bn. €]', 'Electrolyzers cum. - 25% [Bn. €]',
                                  'Electrolyzers cum. - 75% [Bn. €]', 'Factories - median [Bn. €]',
                                  'Factories - 25% [Bn. €]', 'Factories - 75% [Bn. €]',
                                  'Factories cum. - median [Bn. €]', 'Factories cum. - 25% [Bn. €]',
                                  'Factories cum. - 75% [Bn. €]'])
    writeDf = writeDf.T
    writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure13.csv', sep=';')


def figure_14(dfPM, dfHM):
    '''
    Function that will create Fig. 14 - Weighted electricity and hydrogen price in the reference case.
    :param:
        pd.DataFrame dfPM: Yearly data from the power market for the reference case.
        pd.DataFrame dfHM: Yearly data from the hydrogen market for the reference case.
    :return:
    '''
    # Power market
    tmpPM = dfPM.set_index(['Year', 'Run'])
    dfPlotPM = pd.DataFrame(data=np.NaN, index=range(yearDelta), columns=['median', '25%', '75%'])

    # Hydrogen market
    tmpHM = dfHM.set_index(['Year', 'Run'])
    dfPlotHM = pd.DataFrame(data=np.NaN, index=range(yearDelta), columns=['median', '25%', '75%'])

    for i in range(yearDelta):
        # Power market
        if i in tmpPM.index.levels[0]:
            tmpDf = tmpPM.loc[i]['Weighted Price Electricity']
            dfPlotPM.loc[i, 'median'] = tmpDf.median()
            dfPlotPM.loc[i, '25%'] = tmpDf.quantile(q=0.25)
            dfPlotPM.loc[i, '75%'] = tmpDf.quantile(q=0.75)

        # Hydrogen market
        if i in tmpHM.index.levels[0]:
            tmpDf = tmpHM.loc[i]['Price Hydrogen']
            dfPlotHM.loc[i, 'median'] = tmpDf.median()
            dfPlotHM.loc[i, '25%'] = tmpDf.quantile(q=0.25)
            dfPlotHM.loc[i, '75%'] = tmpDf.quantile(q=0.75)

    # Figure
    fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                            dpi=plotSettings['dpi'])

    # Electricity price
    ax1.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    ax1.set_ylabel('Price [€/MWh]', fontsize=plotSettings['fontsize'])
    ax1.plot(x, dfPlotPM['median'], label='Electricity', linestyle='-', color=green)
    ax1.fill_between(x, dfPlotPM['25%'], dfPlotPM['75%'], color=green, alpha=0.25, edgecolor=None)

    # Hydrogen price
    # In €/MWh
    ax1.plot(x, dfPlotHM['median'], label='Hydrogen', linestyle='-', color=blue)
    ax1.fill_between(x, dfPlotHM['25%'], dfPlotHM['75%'], color=blue, alpha=0.25, edgecolor=None)

    # In €/kg
    ax2 = ax1.twinx()
    ax2.set_ylabel('Price [€/kg]', fontsize=plotSettings['fontsize'])
    ax2.plot(x, dfPlotHM['median']*33.3/1e3, linestyle='-', color=blue)

    # Adjust axis
    ax1.minorticks_on()
    ax1.set_xlim(plotSettings['xlim'])
    ax1.set_ylim([0, 275])
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(25))
    ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax1.tick_params(axis='both', which='minor', color='gray')

    ax2.minorticks_on()
    ax2.set_xlim(plotSettings['xlim'])
    ax2.set_ylim([0, 275*33.3/1e3])
    ax2.set_xticks(plotSettings['xticks'])
    ax2.xaxis.set_minor_locator(MultipleLocator(5))
    ax2.yaxis.set_minor_locator(MultipleLocator(1))
    ax2.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax2.tick_params(axis='both', which='minor', color='gray')

    # Adjust legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    handles = handles1 + handles2
    labels = labels1 + labels2

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.45),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save plot
    plt.savefig(os.getcwd() + '\\figure14.' + plotType, bbox_inches='tight')

    # Write Data
    writeDf = pd.DataFrame(data=[dfPlotPM['median'], dfPlotPM['25%'], dfPlotPM['75%'], dfPlotHM['median'],
                                 dfPlotHM['25%'], dfPlotHM['75%'], dfPlotHM['median']*33.3/1e3, dfPlotHM['25%']*33.3/1e3,
                                 dfPlotHM['75%']*33.3/1e3],
                           index=['Weighted electricity price - median [€/MWh]',
                                  'Weighted electricity price - 25% [€/MWh]',
                                  'Weighted electricity price - 75% [€/MWh]',
                                  'Hydrogen price - median [€/MWh]', 'Hydrogen price - 25% [€/MWh]',
                                  'Hydrogen price - 75% [€/MWh]', 'Hydrogen price - median [€/kg]',
                                  'Hydrogen price - 25% [€/kg]', 'Hydrogen price - 75% [€/kg]'])
    writeDf = writeDf.T
    writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure14.csv', sep=';')


def figure_15(dfEP):
    '''
    Function that will create Fig. 15 - Minimal electrolyzer production costs reference case.
    :param:
        pd.DataFrame dfEP: Yearly data from the electrolyzer producers for the reference case.
    :return:
    '''
    # Electroylzer producers
    tmpEP = dfEP.set_index(['Year', 'Run', 'ID'])
    dfPlotEP = pd.DataFrame(data=np.NaN, index=range(yearDelta), columns=['median', '25%', '75%'])

    for i in range(yearDelta):
        # Electrolyzer Producers
        if i in tmpEP.index.levels[0]:
            tmpDf = tmpEP.loc[i]['Minimal costs Electrolyzers'].groupby(level=0).min()
            dfPlotEP.loc[i, 'median'] = tmpDf.median() / 1e3
            dfPlotEP.loc[i, '25%'] = tmpDf.quantile(q=0.25) / 1e3
            dfPlotEP.loc[i, '75%'] = tmpDf.quantile(q=0.75) / 1e3

    # Figure
    fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                            dpi=plotSettings['dpi'])

    # Electrolyzer cost
    ax1.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    ax1.set_ylabel('Production costs [€/kW]', fontsize=plotSettings['fontsize'])
    ax1.plot(x, dfPlotEP['median'], label='Electrolyzer', linestyle='-', color=purple)
    ax1.fill_between(x, dfPlotEP['25%'], dfPlotEP['75%'], color=purple, alpha=0.25, edgecolor=None)

    # Adjust axis
    ax1.minorticks_on()
    ax1.set_xlim(plotSettings['xlim'])
    ax1.set_ylim(0)
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(500))
    ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax1.tick_params(axis='both', which='minor', color='gray')

    # Adjust legend
    handles1, labels1 = ax1.get_legend_handles_labels()

    handles = handles1
    labels = labels1

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.45),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=1)

    # Save plot
    plt.savefig(os.getcwd() + '\\figure15.' + plotType, bbox_inches='tight')

    # Write Data
    writeDf = pd.DataFrame(data=[dfPlotEP['median'], dfPlotEP['25%'], dfPlotEP['75%']],
                           index=['Min. Electrolyzer costs - median [€/kW]', 'Min. Electrolyzer costs - 25% [€/kW]',
                                  'Min. Electrolyzer costs - 75% [€/kW]'])
    writeDf = writeDf.T
    writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure15.csv', sep=';')


def figure_16(dfPM, dfHM):
    '''
    Function that will create Fig. 16 - Weighted electricity and LCOE and hydrogen price and LCOH in the reference case.
    :param:
        pd.DataFrame dfPM: Yearly data from the power market for the reference case.
        pd.DataFrame dfHM: Yearly data from the hydrogen market for the reference case.
    :return:
    '''
    # Power market
    tmpPM = dfPM.set_index(['Year', 'Run'])
    dfPlotPM = pd.DataFrame(data=np.NaN, index=range(yearDelta), columns=['lcoe - median', 'lcoe - 25%', 'lcoe - 75%',
                                                                          'elc - median', 'elc - 25%', 'elc - 75%'])

    # Hydrogen market
    tmpHM = dfHM.set_index(['Year', 'Run'])
    dfPlotHM = pd.DataFrame(data=np.NaN, index=range(yearDelta), columns=['lcoh - median', 'lcoh - 25%', 'lcoh - 75%',
                                                                          'h2 - median', 'h2 - 25%', 'h2 - 75%'])

    for i in range(yearDelta):
        # Power market
        if i in tmpPM.index.levels[0]:
            tmpDf = tmpPM.loc[i]['LCOE']
            dfPlotPM.loc[i, 'lcoe - median'] = tmpDf.median()
            dfPlotPM.loc[i, 'lcoe - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotPM.loc[i, 'lcoe - 75%'] = tmpDf.quantile(q=0.75)
            tmpDf = tmpPM.loc[i]['Weighted Price Electricity']
            dfPlotPM.loc[i, 'elc - median'] = tmpDf.median()
            dfPlotPM.loc[i, 'elc - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotPM.loc[i, 'elc - 75%'] = tmpDf.quantile(q=0.75)
        # Hydrogen market
        if i in tmpHM.index.levels[0]:
            tmpDf = tmpHM.loc[i]['LCOH']
            dfPlotHM.loc[i, 'lcoh - median'] = tmpDf.median()
            dfPlotHM.loc[i, 'lcoh - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotHM.loc[i, 'lcoh - 75%'] = tmpDf.quantile(q=0.75)
            tmpDf = tmpHM.loc[i]['Price Hydrogen']
            dfPlotHM.loc[i, 'h2 - median'] = tmpDf.median()
            dfPlotHM.loc[i, 'h2 - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotHM.loc[i, 'h2 - 75%'] = tmpDf.quantile(q=0.75)

    # Figure
    fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=plotSettings['figsize_2t'], gridspec_kw=plotSettings['gridspec_kw'],
                                   dpi=plotSettings['dpi'], sharex=True)

    # Electricity price
    ax1.set_ylabel('Electricity price/LCOE [€/MWh]', fontsize=plotSettings['fontsize'])
    ax1.plot(x, dfPlotPM['elc - median'], label='Electricity price', linestyle='-', color=green)
    ax1.plot(x, dfPlotPM['lcoe - median'], label='Levelized costs of electricity', linestyle=':', color=darkgreen)
    ax1.fill_between(x, dfPlotPM['elc - 25%'], dfPlotPM['elc - 75%'], color=green, alpha=0.25, edgecolor=None)
    ax1.fill_between(x, dfPlotPM['lcoe - 25%'], dfPlotPM['lcoe - 75%'], color=darkgreen, alpha=0.1, edgecolor=None,
                     hatch='///')

    # Hydrogen price
    # In €/MWh
    ax2.set_ylabel('Hydrogen price/LCOH [€/MWh]', fontsize=plotSettings['fontsize'])
    ax2.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    ax2.plot(x, dfPlotHM['h2 - median'], label='Hydrogen price', linestyle='-', color=blue)
    ax2.plot(x, dfPlotHM['lcoh - median'], label='Levelized costs of hydrogen', linestyle=':', color=darkblue)
    ax2.fill_between(x, dfPlotHM['h2 - 25%'], dfPlotHM['h2 - 75%'], color=blue, alpha=0.25, edgecolor=None)
    ax2.fill_between(x, dfPlotHM['lcoh - 25%'], dfPlotHM['lcoh - 75%'], color=darkblue, alpha=0.1, edgecolor=None,
                     hatch='///')

    # In €/kg
    ax22 = ax2.twinx()
    ax22.set_ylabel('Hydrogen price/LCOH [€/kg]', fontsize=plotSettings['fontsize'])
    ax22.plot(x, dfPlotHM['h2 - median']*33.3/1e3, linestyle='-', color=blue)
    ax22.plot(x, dfPlotHM['lcoh - median']*33.3/1e3, linestyle=':', color=darkblue)

    # Adjust axis
    ax1.minorticks_on()
    ax1.set_xlim(plotSettings['xlim'])
    ax1.set_ylim([0, 100])
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(10))
    ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax1.tick_params(axis='both', which='minor', color='gray')

    ax2.minorticks_on()
    ax2.set_xlim(plotSettings['xlim'])
    ax2.set_ylim([0, 500])
    ax2.set_xticks(plotSettings['xticks'])
    ax2.xaxis.set_minor_locator(MultipleLocator(5))
    ax2.yaxis.set_minor_locator(MultipleLocator(50))
    ax2.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax2.tick_params(axis='both', which='minor', color='gray')

    ax22.minorticks_on()
    ax22.set_xlim(plotSettings['xlim'])
    ax22.set_ylim([0, 500*33.3/1e3])
    ax22.set_xticks(plotSettings['xticks'])
    ax22.xaxis.set_minor_locator(MultipleLocator(5))
    ax22.yaxis.set_minor_locator(MultipleLocator(2.5))
    ax22.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax22.tick_params(axis='both', which='minor', color='gray')

    # Adjust legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    handles = handles1 + handles2
    labels = labels1 + labels2

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.45),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save plot
    plt.savefig(os.getcwd() + '\\figure16.' + plotType, bbox_inches='tight')

    # Write Data
    writeDf = pd.DataFrame(data=[dfPlotPM['elc - median'], dfPlotPM['elc - 25%'], dfPlotPM['elc - 75%'],
                                 dfPlotPM['lcoe - median'], dfPlotPM['lcoe - 25%'], dfPlotPM['lcoe - 75%'],
                                 dfPlotHM['h2 - median'], dfPlotHM['h2 - 25%'], dfPlotHM['h2 - 75%'],
                                 dfPlotHM['lcoh - median'], dfPlotHM['lcoh - 25%'], dfPlotHM['lcoh - 75%'],
                                 dfPlotHM['h2 - median']*33.3/1e3, dfPlotHM['h2 - 25%']*33.3/1e3,
                                 dfPlotHM['h2 - 75%']*33.3/1e3, dfPlotHM['lcoh - median']*33.3/1e3,
                                 dfPlotHM['lcoh - 25%']*33.3/1e3, dfPlotHM['lcoh - 75%']*33.3/1e3],
                           index=['Weighted electricity price - median [€/MWh]',
                                  'Weighted electricity price - 25% [€/MWh]',
                                  'Weighted electricity price - 75% [€/MWh]',
                                  'Levelized costs of electricity - median [€/MWh]',
                                  'Levelized costs of electricity - 25% [€/MWh]',
                                  'Levelized costs of electricity - 75% [€/MWh]',
                                  'Hydrogen price - median [€/MWh]', 'Hydrogen price - 25% [€/MWh]',
                                  'Hydrogen price - 75% [€/MWh]', 'Levelized costs of hydrogen - median [€/MWh]',
                                  'Levelized costs of hydrogen - 25% [€/MWh]',
                                  'Levelized costs of hydrogen - 75% [€/MWh]', 'Hydrogen price - median [€/kg]',
                                  'Hydrogen price - 25% [€/kg]', 'Hydrogen price - 75% [€/kg]',
                                  'Levelized costs of hydrogen - median [€/kg]',
                                  'Levelized costs of hydrogen - 25% [€/kg]',
                                  'Levelized costs of hydrogen - 75% [€/kg]'])
    writeDf = writeDf.T
    writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure16.csv', sep=';')


def figure_16a(dfPM, dfHM):
    '''
    Function that will create Fig. 16a - LCOH and the average electricity price for HP and its ratio in the reference
    case.
    :param:
        pd.DataFrame dfPM: Daily data from the power market for the reference case.
        pd.DataFrame dfHM: Yearly data from the hydrogen market for the reference case.
    :return:
    '''
    # Power market
    tmpPM = dfPM.set_index(['Year', 'Day', 'Run'])

    # Hydrogen market
    tmpHM = dfHM.set_index(['Year', 'Run'])
    dfPlot = pd.DataFrame(data=np.nan, index=range(yearDelta), columns=['elc - median', 'elc - 25%', 'elc - 75%',
                                                                        'lcoh - median', 'lcoh - 25%', 'lcoh - 75%'])

    for i in range(yearDelta):
        # Power market
        if i in tmpPM.index.levels[0]:
            tmpDf = tmpPM.loc[i]['Electricity demand electrolyzers'] * tmpPM.loc[i]['Price Electricity']
            tmpDf = (tmpDf.groupby(level=1).sum() /
                     tmpPM.loc[i]['Electricity demand electrolyzers'].groupby(level=1).sum())
            dfPlot.loc[i, 'elc - median'] = tmpDf.median()
            dfPlot.loc[i, 'elc - 25%'] = tmpDf.quantile(q=0.25)
            dfPlot.loc[i, 'elc - 75%'] = tmpDf.quantile(q=0.75)
        # Hydrogen market
        if i in tmpHM.index.levels[0]:
            tmpDf = tmpHM.loc[i]['LCOH']
            dfPlot.loc[i, 'lcoh - median'] = tmpDf.median()
            dfPlot.loc[i, 'lcoh - 25%'] = tmpDf.quantile(q=0.25)
            dfPlot.loc[i, 'lcoh - 75%'] = tmpDf.quantile(q=0.75)

    # Figure
    fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                            dpi=plotSettings['dpi'])

    # Electricity price
    ax1.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    #ax1.set_ylabel('Average electricty price [€/${MWh_{elc}}$]\nLevelized costs of hydrogen [€/${MWh_{{H}_{2}}}]$',
    #               fontsize=plotSettings['fontsize'])
    ax1.set_ylabel('Average electricity price [€/MWh]', fontsize=plotSettings['fontsize'], color=green)
    ax1.plot(x, dfPlot['elc - median'], label='Electricity price', linestyle='-', color=green)
    ax1.fill_between(x, dfPlot['elc - 25%'], dfPlot['elc - 75%'], color=green, alpha=0.25, edgecolor=None)

    # Hydrogen price
    # In €/MWh
    ax1.plot(x, dfPlot['lcoh - median'], label='Levelized costs of hydrogen', linestyle='-', color=blue)
    ax1.fill_between(x, dfPlot['lcoh - 25%'], dfPlot['lcoh - 75%'], color=blue, alpha=0.25, edgecolor=None)

    # Hydrogen price
    # In €/kg
    ax2 = ax1.twinx()
    ax2.set_ylabel('Levelized costs of hydrogen [€/kg]', fontsize=plotSettings['fontsize'], color=blue)
    ax2.plot(x, dfPlot['lcoh - median']*33.3/1000, linestyle='-', color=blue)

    # In €/kg
    ax3 = ax1.twinx()
    ax3.set_ylabel('Share of electricity costs at LCOH [%]', fontsize=plotSettings['fontsize'], color=darkblue)
    ax3.plot(x, dfPlot['elc - median']/0.7/dfPlot['lcoh - median']*100, label='Share of LCOH', linestyle='--',
             color=darkblue)
    ax3.fill_between(x, dfPlot['elc - 25%']/0.7/dfPlot['lcoh - 25%']*100,
                     dfPlot['elc - 75%']/0.7/dfPlot['lcoh - 75%']*100, color=darkblue, alpha=0.1, edgecolor=None)

    # Adjust axis
    ax1.minorticks_on()
    ax1.yaxis.set_label_position('left')
    ax1.set_xlim(plotSettings['xlim'])
    ax1.set_ylim([0, 500])
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(25))
    ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax1.tick_params(axis='both', which='minor', color='gray')

    ax2.spines['left'].set_position(('axes', -.2))
    ax2.spines['left'].set_visible(True)
    ax2.yaxis.set_label_position('left')
    ax2.yaxis.set_ticks_position('left')
    ax2.minorticks_on()
    ax2.set_xlim(plotSettings['xlim'])
    ax2.set_ylim([0, 500*33.3/1000])
    ax2.set_xticks(plotSettings['xticks'])
    ax2.yaxis.set_minor_locator(MultipleLocator(1.25))
    ax2.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax2.tick_params(axis='both', which='minor', color='gray')

    ax3.minorticks_on()
    ax3.set_xlim(plotSettings['xlim'])
    ax3.set_ylim([0, 55])
    ax3.set_xticks(plotSettings['xticks'])
    ax3.xaxis.set_minor_locator(MultipleLocator(5))
    ax3.yaxis.set_minor_locator(MultipleLocator(5))
    ax3.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax3.tick_params(axis='both', which='minor', color='gray')

    ax1.set_zorder(1)
    ax2.set_zorder(2)
    ax3.set_zorder(3)

    # Adjust legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles3, labels3 = ax3.get_legend_handles_labels()

    handles = handles1 + handles3
    labels = labels1 + labels3

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.45),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save plot
    plt.savefig(os.getcwd() + '\\figure16a.' + plotType, bbox_inches='tight')

    # Write Datadd
    writeDf = pd.DataFrame(data=[dfPlot['elc - median'], dfPlot['elc - 25%'], dfPlot['elc - 75%'],
                                 dfPlot['lcoh - median'], dfPlot['lcoh - 25%'], dfPlot['lcoh - 75%'],
                                 dfPlot['elc - median']/0.7/dfPlot['lcoh - median']*100,
                                 dfPlot['elc - 25%'] / 0.7 / dfPlot['lcoh - 25%'] * 100,
                                 dfPlot['elc - 75%'] / 0.7 / dfPlot['lcoh - 75%'] * 100],
                           index=['Average electricity price - median [€/MWh_elc]',
                                  'Average electricity price - 25% [€/MWh_elc]',
                                  'Average electricity price - 75% [€/MWh_elc]',
                                  'Levelized costs of hydrogen - median [€/MWh_H2]',
                                  'Levelized costs of hydrogen - 25% [€/MWh_H2]',
                                  'Levelized costs of hydrogen - 75% [€/MWh_H2]',
                                  'Share of electricity costs at LCOH - median [%]',
                                  'Share of electricity costs at LCOH - 25% [%]',
                                  'Share of electricity costs at LCOH - 75% [%]'])
    writeDf = writeDf.T
    writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure16a.csv', sep=';')


def figure_16b(dfPP, dfHP, dfEP):
    '''
    Function that will create Fig. 16b - Investment thresholds for all type of agents in the reference case.
    :param:
        pd.DataFrame dfPP: Year data from the power producers for the reference case.
        pd.DataFrame dfHP: Year data from the hydrogen producers for the reference case.
        pd.DataFrame dfEP: Year data from the electrolyzer producers for the reference case.
    :return:
    '''
    # Power producer
    tmpPP = dfPP.set_index(['Year', 'Run', 'ID'])
    dfPlotPP = pd.DataFrame(data=np.nan, index=range(yearDelta), columns=['median', 'min', 'max'])
    # Hydrogen producer
    tmpHP = dfHP.set_index(['Year', 'Run', 'ID'])
    dfPlotHP = pd.DataFrame(data=np.nan, index=range(yearDelta), columns=['median', 'min', 'max'])
    # Electroyzer producer
    tmpEP = dfEP.set_index(['Year', 'Run', 'ID'])
    dfPlotEP = pd.DataFrame(data=np.nan, index=range(yearDelta), columns=['median', 'min', 'max'])

    for i in range(yearDelta):
        # Power producers
        if i in tmpPP.index.levels[0]:
            tmpDf = tmpPP.loc[i]['Investment threshold']
            dfPlotPP.loc[i, 'median'] = tmpDf.median()
            dfPlotPP.loc[i, 'min'] = tmpDf.min()
            dfPlotPP.loc[i, 'max'] = tmpDf.max()
        # Hydrogen producers
        if i in tmpHP.index.levels[0]:
            tmpDf = tmpHP.loc[i]['Investment threshold']
            dfPlotHP.loc[i, 'median'] = tmpDf.median()
            dfPlotHP.loc[i, 'min'] = tmpDf.min()
            dfPlotHP.loc[i, 'max'] = tmpDf.max()
        # Electrolyzer producers
        if i in tmpEP.index.levels[0]:
            tmpDf = tmpEP.loc[i]['Investment threshold']
            dfPlotEP.loc[i, 'median'] = tmpDf.median()
            dfPlotEP.loc[i, 'min'] = tmpDf.min()
            dfPlotEP.loc[i, 'max'] = tmpDf.max()

    # Figure
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=plotSettings['figsize_3t'],
                                        gridspec_kw=plotSettings['gridspec_kw'], dpi=plotSettings['dpi'], sharex=True)

    # Power producers
    ax1.plot(x, dfPlotPP['median'], label='Power producers', linestyle='-', color=green)
    ax1.fill_between(x, dfPlotPP['min'], dfPlotPP['max'], color=green, alpha=0.25, edgecolor=None)
    ax1.set_ylim(-1)
    # Hydrogen producers
    ax2.set_ylabel('Investment threshold [-]', fontsize=plotSettings['fontsize'])
    ax2.plot(x, dfPlotHP['median'], label='Hydrogen producers', linestyle='-', color=blue)
    ax2.fill_between(x, dfPlotHP['min'], dfPlotHP['max'], color=blue, alpha=0.25, edgecolor=None)
    ax2.set_ylim(-1)
    # Electrolyzer producers
    ax3.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    ax3.plot(x, dfPlotEP['median'], label='Electrolyzer producers', linestyle='-', color=purple)
    ax3.fill_between(x, dfPlotEP['min'], dfPlotEP['max'], color=purple, alpha=0.25, edgecolor=None)
    ax3.set_ylim(-1)

    # Adjust axis
    ax1.minorticks_on()
    ax1.set_xlim(plotSettings['xlim'])
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(0.1))
    ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax1.tick_params(axis='both', which='minor', color='gray')

    ax2.minorticks_on()
    ax2.set_xlim(plotSettings['xlim'])
    ax2.set_xticks(plotSettings['xticks'])
    ax2.xaxis.set_minor_locator(MultipleLocator(5))
    ax2.yaxis.set_minor_locator(MultipleLocator(0.1))
    ax2.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax2.tick_params(axis='both', which='minor', color='gray')

    ax3.minorticks_on()
    ax3.set_xlim(plotSettings['xlim'])
    ax3.set_xticks(plotSettings['xticks'])
    ax3.xaxis.set_minor_locator(MultipleLocator(5))
    ax3.yaxis.set_minor_locator(MultipleLocator(0.1))
    ax3.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax3.tick_params(axis='both', which='minor', color='gray')

    # Adjust legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles3, labels3 = ax3.get_legend_handles_labels()

    handles = handles1 + handles2 + handles3
    labels = labels1 + labels2 + labels3

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.45),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save plot
    plt.savefig(os.getcwd() + '\\figure16b.' + plotType, bbox_inches='tight')

    # Write Data
    writeDf = pd.DataFrame(data=[dfPlotPP['median'], dfPlotPP['min'], dfPlotPP['max'],
                                 dfPlotHP['median'], dfPlotHP['min'], dfPlotHP['max'],
                                 dfPlotEP['median'], dfPlotEP['min'], dfPlotEP['max']],
                           index=['Investment threshold PP - median [-]', 'Investment threshold PP - min [-]',
                                  'Investment threshold PP - max [-]', 'Investment threshold HP - median [-]',
                                  'Investment threshold HP - min [-]', 'Investment threshold HP - max [-]',
                                  'Investment threshold EP - median [-]', 'Investment threshold EP - min [-]',
                                  'Investment threshold EP - max [-]'])
    writeDf = writeDf.T
    writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure16b.csv', sep=';')


def figure_17(dfPMRef, dfHMRef, dfEMRef, dfPMStrat, dfHMStrat, dfEMStrat, dfPMW2P, dfHMW2P, dfEMW2P, dfPMWorst,
              dfHMWorst, dfEMWorst):
    '''
    Function that will create Fig. 17 - Installed capacities obstacle cases.
    :param:
        pd.DataFrame dfPMRef: Yearly data from the power market for the reference case.
        pd.DataFrame dfHMRef: Yearly data from the hydrogen market for the reference case.
        pd.DataFrame dfEMRef: Yearly data from the electrolyzer market for the reference case.
        pd.DataFrame dfPMStrat: Yearly data from the power market for the strategic investment case.
        pd.DataFrame dfHMStrat: Yearly data from the hydrogen market for the strategic investment case.
        pd.DataFrame dfEMStrat: Yearly data from the electrolyzer market for the strategic investment case.
        pd.DataFrame dfPMW2P: Yearly data from the power market for the willingness to pay case.
        pd.DataFrame dfHMW2P: Yearly data from the hydrogen market for the willingness to pay case.
        pd.DataFrame dfEMW2p: Yearly data from the electrolyzer market for the willingness to pay case.
        pd.DataFrame dfPMWorst: Yearly data from the power market for the worst case.
        pd.DataFrame dfHMWorst: Yearly data from the hydrogen market for the worst case.
        pd.DataFrame dfEMWorst: Yearly data from the electrolyzer market for the worst case.
    :return:
    '''
    # Installed renewables
    tmpPMRef = dfPMRef.set_index(['Year', 'Run'])
    tmpPMStrat = dfPMStrat.set_index(['Year', 'Run'])
    tmpPMW2P = dfPMW2P.set_index(['Year', 'Run'])
    tmpPMWorst = dfPMWorst.set_index(['Year', 'Run'])
    dfPlotRES = pd.DataFrame(data=np.NaN, index=range(yearDelta),
                             columns=['Ref - median', 'Ref - 25%', 'Ref - 75%', 'Strat - median', 'Strat - 25%',
                                      'Strat - 75%', 'W2P - median', 'W2P - 25%', 'W2P - 75%', 'Worst - median',
                                      'Worst - 25%', 'Worst - 75%'])

    # Installed electrolyzers
    tmpHMRef = dfHMRef.set_index(['Year', 'Run'])
    tmpHMStrat = dfHMStrat.set_index(['Year', 'Run'])
    tmpHMW2P = dfHMW2P.set_index(['Year', 'Run'])
    tmpHMWorst = dfHMWorst.set_index(['Year', 'Run'])
    dfPlotELC = pd.DataFrame(data=np.NaN, index=range(yearDelta),
                             columns=['Ref - median', 'Ref - 25%', 'Ref - 75%', 'Strat - median', 'Strat - 25%',
                                      'Strat - 75%', 'W2P - median', 'W2P - 25%', 'W2P - 75%', 'Worst - median',
                                      'Worst - 25%', 'Worst - 75%'])

    # Installed factories
    tmpEMRef = dfEMRef.set_index(['Year', 'Run'])
    tmpEMStrat = dfEMStrat.set_index(['Year', 'Run'])
    tmpEMW2P = dfEMW2P.set_index(['Year', 'Run'])
    tmpEMWorst = dfEMWorst.set_index(['Year', 'Run'])
    dfPlotFAC = pd.DataFrame(data=np.NaN, index=range(yearDelta),
                             columns=['Ref - median', 'Ref - 25%', 'Ref - 75%', 'Strat - median', 'Strat - 25%',
                                      'Strat - 75%', 'W2P - median', 'W2P - 25%', 'W2P - 75%', 'Worst - median',
                                      'Worst - 25%', 'Worst - 75%'])

    for i in range(yearDelta):
        # Renewables
        # Reference case
        if i in tmpPMRef.index.levels[0]:
            tmpDf = tmpPMRef.loc[i]['Installed capacity Renewables']
            dfPlotRES.loc[i, 'Ref - median'] = tmpDf.median()
            dfPlotRES.loc[i, 'Ref - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotRES.loc[i, 'Ref - 75%'] = tmpDf.quantile(q=0.75)
        # Strategic investment case
        if i in tmpPMStrat.index.levels[0]:
            tmpDf = tmpPMStrat.loc[i]['Installed capacity Renewables']
            dfPlotRES.loc[i, 'Strat - median'] = tmpDf.median()
            dfPlotRES.loc[i, 'Strat - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotRES.loc[i, 'Strat - 75%'] = tmpDf.quantile(q=0.75)
        # Willingness to pay case
        if i in tmpPMW2P.index.levels[0]:
            tmpDf = tmpPMW2P.loc[i]['Installed capacity Renewables']
            dfPlotRES.loc[i, 'W2P - median'] = tmpDf.median()
            dfPlotRES.loc[i, 'W2P - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotRES.loc[i, 'W2P - 75%'] = tmpDf.quantile(q=0.75)
        # Worst case
        if i in tmpPMWorst.index.levels[0]:
            tmpDf = tmpPMWorst.loc[i]['Installed capacity Renewables']
            dfPlotRES.loc[i, 'Worst - median'] = tmpDf.median()
            dfPlotRES.loc[i, 'Worst - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotRES.loc[i, 'Worst - 75%'] = tmpDf.quantile(q=0.75)

        # Electrolyzers
        # Reference case
        if i in tmpHMRef.index.levels[0]:
            tmpDf = tmpHMRef.loc[i]['Installed capacity Electrolyzers']
            dfPlotELC.loc[i, 'Ref - median'] = tmpDf.median()
            dfPlotELC.loc[i, 'Ref - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotELC.loc[i, 'Ref - 75%'] = tmpDf.quantile(q=0.75)
        # Strategic investment case
        if i in tmpHMStrat.index.levels[0]:
            tmpDf = tmpHMStrat.loc[i]['Installed capacity Electrolyzers']
            dfPlotELC.loc[i, 'Strat - median'] = tmpDf.median()
            dfPlotELC.loc[i, 'Strat - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotELC.loc[i, 'Strat - 75%'] = tmpDf.quantile(q=0.75)
        # Willingness to pay case
        if i in tmpHMW2P.index.levels[0]:
            tmpDf = tmpHMW2P.loc[i]['Installed capacity Electrolyzers']
            dfPlotELC.loc[i, 'W2P - median'] = tmpDf.median()
            dfPlotELC.loc[i, 'W2P - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotELC.loc[i, 'W2P - 75%'] = tmpDf.quantile(q=0.75)
        # Worst case
        if i in tmpHMWorst.index.levels[0]:
            tmpDf = tmpHMWorst.loc[i]['Installed capacity Electrolyzers']
            dfPlotELC.loc[i, 'Worst - median'] = tmpDf.median()
            dfPlotELC.loc[i, 'Worst - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotELC.loc[i, 'Worst - 75%'] = tmpDf.quantile(q=0.75)

        # Factories
        # Reference case
        if i in tmpEMRef.index.levels[0]:
            tmpDf = tmpEMRef.loc[i]['Installed capacity Manufacturings']
            dfPlotFAC.loc[i, 'Ref - median'] = tmpDf.median()
            dfPlotFAC.loc[i, 'Ref - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotFAC.loc[i, 'Ref - 75%'] = tmpDf.quantile(q=0.75)
        # Strategic investment case
        if i in tmpEMStrat.index.levels[0]:
            tmpDf = tmpEMStrat.loc[i]['Installed capacity Manufacturings']
            dfPlotFAC.loc[i, 'Strat - median'] = tmpDf.median()
            dfPlotFAC.loc[i, 'Strat - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotFAC.loc[i, 'Strat - 75%'] = tmpDf.quantile(q=0.75)
        # Willingness to pay case
        if i in tmpEMW2P.index.levels[0]:
            tmpDf = tmpEMW2P.loc[i]['Installed capacity Manufacturings']
            dfPlotFAC.loc[i, 'W2P - median'] = tmpDf.median()
            dfPlotFAC.loc[i, 'W2P - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotFAC.loc[i, 'W2P - 75%'] = tmpDf.quantile(q=0.75)
        # Worst case
        if i in tmpEMWorst.index.levels[0]:
            tmpDf = tmpEMWorst.loc[i]['Installed capacity Manufacturings']
            dfPlotFAC.loc[i, 'Worst - median'] = tmpDf.median()
            dfPlotFAC.loc[i, 'Worst - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotFAC.loc[i, 'Worst - 75%'] = tmpDf.quantile(q=0.75)

    # Figure
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=plotSettings['figsize_3t_l'],
                                        gridspec_kw=plotSettings['gridspec_kw'], dpi=plotSettings['dpi'], sharex=True)

    # Renewables
    ax1.set_ylabel('Renewables [GW]', fontsize=plotSettings['fontsize'])
    # Results data
    ax1.plot(x, dfPlotRES['Ref - median']/1e3, label='Renewables - best case', linestyle='-', color=green)
    ax1.plot(x, dfPlotRES['Strat - median']/1e3, label='Renewables - non-strategic', linestyle=StratLinestyle,
             color=darkgreen)
    ax1.plot(x, dfPlotRES['W2P - median']/1e3, label='Renewables - grey hydrogen', linestyle=W2PLinestlye,
             color=darkgreen)
    ax1.plot(x, dfPlotRES['Worst - median']/1e3, label='Renewables - worst case', linestyle=WorstLinestyle,
            color=darkgreen)

    ax1.fill_between(x, dfPlotRES['Strat - 25%']/1e3, dfPlotRES['Strat - 75%']/1e3, alpha=0.1, color=darkgreen,
                     edgecolor=None, hatch=StratHatch)
    ax1.fill_between(x, dfPlotRES['W2P - 25%']/1e3, dfPlotRES['W2P - 75%']/1e3, alpha=0.1, color=darkgreen,
                     edgecolor=None, hatch=W2PHatch)
    ax1.fill_between(x, dfPlotRES['Worst - 25%']/1e3, dfPlotRES['Worst - 75%']/1e3, alpha=0.1, color=darkgreen,
                     edgecolor=None, hatch=WorstHatch)

    ax1.set_ylim(plotSettings['ylim_res_cap'])

    # Electrolyzers
    ax2.set_ylabel('Electrolyzers [GW]', fontsize=plotSettings['fontsize'])
    # Results data
    ax2.plot(x, dfPlotELC['Ref - median']/1e3, label='Electrolyzers - best case', linestyle='-', color=blue)
    ax2.plot(x, dfPlotELC['Strat - median']/1e3, label='Electrolyzers - non-strategic', linestyle=StratLinestyle,
             color=darkblue)
    ax2.plot(x, dfPlotELC['W2P - median']/1e3, label='Electrolyzers - grey hydrogen', linestyle=W2PLinestlye,
             color=darkblue)
    ax2.plot(x, dfPlotELC['Worst - median']/1e3, label='Electrolyzers - worst case', linestyle=WorstLinestyle,
             color=darkblue)

    ax2.fill_between(x, dfPlotELC['Strat - 25%']/1e3, dfPlotELC['Strat - 75%']/1e3, alpha=0.1, color=darkblue,
                     edgecolor=None, hatch=StratHatch)
    ax2.fill_between(x, dfPlotELC['W2P - 25%']/1e3, dfPlotELC['W2P - 75%']/1e3, alpha=0.1, color=darkblue,
                     edgecolor=None, hatch=W2PHatch)
    ax2.fill_between(x, dfPlotELC['Worst - 25%']/1e3, dfPlotELC['Worst - 75%']/1e3, alpha=0.1, color=darkblue,
                     edgecolor=None, hatch=WorstHatch)

    ax2.set_ylim(plotSettings['ylim_elc_cap'])

    # Factories
    ax3.set_ylabel('Electrolyzer manufacturing [GW/year]', fontsize=plotSettings['fontsize'])
    ax3.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    # Results data
    ax3.plot(x, dfPlotFAC['Ref - median'] / 1e3, label='Electrolyzer manufacturing - best case', linestyle='-',
             color=purple)
    ax3.plot(x, dfPlotFAC['Strat - median']/1e3, label='Electrolyzer manufacturing - non-strategic',
             linestyle=StratLinestyle, color=darkpurple)
    ax3.plot(x, dfPlotFAC['W2P - median']/1e3, label='Electrolyzer manufacturing - grey hydrogen',
             linestyle=W2PLinestlye, color=darkpurple)
    ax3.plot(x, dfPlotFAC['Worst - median']/1e3, label='Electrolyzer manufacturing - worst case',
             linestyle=WorstLinestyle, color=darkpurple)

    ax3.fill_between(x, dfPlotFAC['Strat - 25%']/1e3, dfPlotFAC['Strat - 75%']/1e3, alpha=0.1, color=darkpurple,
                     edgecolor=None, hatch=StratHatch)
    ax3.fill_between(x, dfPlotFAC['W2P - 25%']/1e3, dfPlotFAC['W2P - 75%']/1e3, alpha=0.1, color=darkpurple,
                     edgecolor=None, hatch=W2PHatch)
    ax3.fill_between(x, dfPlotFAC['Worst - 25%']/1e3, dfPlotFAC['Worst - 75%']/1e3, alpha=0.1, color=darkpurple,
                     edgecolor=None, hatch=WorstHatch)

    ax3.set_ylim(plotSettings['ylim_fac_cap'])

    fig.text(-0.02, 0.5, 'Installed capacities', va='center', rotation='vertical', fontsize=plotSettings['fontsize'])

    plt.xlim(plotSettings['xlim'])

    # Adjust ticks
    ax1.minorticks_on()
    ax2.minorticks_on()
    ax3.minorticks_on()
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(50))
    ax1.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax1.tick_params(which='minor', axis='both', color='gray')
    ax2.yaxis.set_minor_locator(MultipleLocator(10))
    ax2.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax2.tick_params(which='minor', axis='both', color='gray')
    ax3.yaxis.set_minor_locator(MultipleLocator(5))
    ax3.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax3.tick_params(which='minor', axis='both', color='gray')

    # Legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles3, labels3 = ax3.get_legend_handles_labels()

    handles = handles1 + handles2 + handles3
    labels = labels1 + labels2 + labels3

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.4, -0.7),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=3)

    # Save figure
    plt.savefig(os.getcwd() + '\\figure17.' + plotType, bbox_inches='tight')

    # Write Data
    writeDf = pd.DataFrame(data=[dfPlotRES['Ref - median']/1e3, dfPlotRES['Strat - median']/1e3,
                                 dfPlotRES['Strat - 25%']/1e3, dfPlotRES['Strat - 75%']/1e3,
                                 dfPlotRES['W2P - median']/1e3, dfPlotRES['W2P - 25%']/1e3,
                                 dfPlotRES['W2P - 75%']/1e3, dfPlotRES['Worst - median']/1e3,
                                 dfPlotRES['Worst - 25%']/1e3, dfPlotRES['Worst - 75%']/1e3,
                                 dfPlotELC['Ref - median']/1e3, dfPlotELC['Strat - median']/1e3,
                                 dfPlotELC['Strat - 25%']/1e3, dfPlotELC['Strat - 75%']/1e3,
                                 dfPlotELC['W2P - median']/1e3, dfPlotELC['W2P - 25%']/1e3,
                                 dfPlotELC['W2P - 75%']/1e3, dfPlotELC['Worst - median']/1e3,
                                 dfPlotELC['Worst - 25%']/1e3, dfPlotELC['Worst - 75%']/1e3,
                                 dfPlotFAC['Ref - median']/1e3, dfPlotFAC['Strat - median']/1e3,
                                 dfPlotFAC['Strat - 25%']/1e3, dfPlotFAC['Strat - 75%']/1e3,
                                 dfPlotFAC['W2P - median']/1e3, dfPlotFAC['W2P - 25%']/1e3,
                                 dfPlotFAC['W2P - 75%']/1e3, dfPlotFAC['Worst - median']/1e3,
                                 dfPlotFAC['Worst - 25%']/1e3, dfPlotFAC['Worst - 75%']/1e3],
                           index=['Inst. Renewables Ref. - median [GW]', 'Inst. Renewables Strat. - median [GW]',
                                  'Inst. Renewables Strat. - 25% [GW]', 'Inst. Renewables Strat. - 75% [GW]',
                                  'Inst. Renewables W2P - median [GW]', 'Inst. Renewables W2P - 25% [GW]',
                                  'Inst. Renewables W2P - 75% [GW]', 'Inst. Renewables Worst - median [GW]',
                                  'Inst. Renewables Worst - 25% [GW]', 'Inst. Renewables Worst - 75% [GW]',
                                  'Inst. Electrolyzers Ref. - median [GW]', 'Inst. Electrolyzers Strat. - median [GW]',
                                  'Inst. Electrolyzers Strat. - 25% [GW]', 'Inst. Electrolyzers Strat. - 75% [GW]',
                                  'Inst. Electrolyzers W2P - median [GW]', 'Inst. Electrolyzers W2P - 25% [GW]',
                                  'Inst. Electrolyzers W2P - 75% [GW]', 'Inst. ELectrolyzers Worst - median [GW]',
                                  'Inst. Electrolyzers Worst - 25% [GW]', 'Inst. Electrolyzers Worst - 75% [GW]',
                                  'Inst. Factories Ref. - median [GW/year]', 'Inst. Factories Strat. - median [GW/year]',
                                  'Inst. Factories Strat. - 25% [GW/year]', 'Inst. Factories Strat. - 75% [GW/year]',
                                  'Inst. Factories W2P - median [GW/year]', 'Inst. Factories W2P - 25% [GW/year]',
                                  'Inst. Factories W2P - 75% [GW/year]', 'Inst. Factories Worst - median [GW/year]',
                                  'Inst. Factoires Worst - 25% [GW/year]', 'Inst. Factoires Worst - 75% [GW/year]'])
    writeDf = writeDf.T
    writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure17.csv', sep=';')

def figure_17b(dfPMRef, dfHMRef, dfEMRef, dfPMStrat, dfHMStrat, dfEMStrat, dfPMW2P, dfHMW2P, dfEMW2P, dfPMWorst,
              dfHMWorst, dfEMWorst):
    '''
    Function that will create Fig. 17b - Installed capacities obstacle cases until 2100.
    :param:
        pd.DataFrame dfPMRef: Yearly data from the power market for the reference case.
        pd.DataFrame dfHMRef: Yearly data from the hydrogen market for the reference case.
        pd.DataFrame dfEMRef: Yearly data from the electrolyzer market for the reference case.
        pd.DataFrame dfPMStrat: Yearly data from the power market for the strategic investment case.
        pd.DataFrame dfHMStrat: Yearly data from the hydrogen market for the strategic investment case.
        pd.DataFrame dfEMStrat: Yearly data from the electrolyzer market for the strategic investment case.
        pd.DataFrame dfPMW2P: Yearly data from the power market for the willingness to pay case.
        pd.DataFrame dfHMW2P: Yearly data from the hydrogen market for the willingness to pay case.
        pd.DataFrame dfEMW2p: Yearly data from the electrolyzer market for the willingness to pay case.
        pd.DataFrame dfPMWorst: Yearly data from the power market for the worst case.
        pd.DataFrame dfHMWorst: Yearly data from the hydrogen market for the worst case.
        pd.DataFrame dfEMWorst: Yearly data from the electrolyzer market for the worst case.
    :return:
    '''
    # Since this is until 2100
    tmpyearEnd = 2100
    tmpyearDelta = tmpyearEnd - year0 + 1
    x = list(range(year0, tmpyearEnd + 1))


    # Installed renewables
    tmpPMRef = dfPMRef.set_index(['Year', 'Run'])
    tmpPMStrat = dfPMStrat.set_index(['Year', 'Run'])
    tmpPMW2P = dfPMW2P.set_index(['Year', 'Run'])
    tmpPMWorst = dfPMWorst.set_index(['Year', 'Run'])
    dfPlotRES = pd.DataFrame(data=np.NaN, index=range(tmpyearDelta),
                             columns=['Ref - median', 'Ref - 25%', 'Ref - 75%', 'Strat - median', 'Strat - 25%',
                                      'Strat - 75%', 'W2P - median', 'W2P - 25%', 'W2P - 75%', 'Worst - median',
                                      'Worst - 25%', 'Worst - 75%'])

    # Installed electrolyzers
    tmpHMRef = dfHMRef.set_index(['Year', 'Run'])
    tmpHMStrat = dfHMStrat.set_index(['Year', 'Run'])
    tmpHMW2P = dfHMW2P.set_index(['Year', 'Run'])
    tmpHMWorst = dfHMWorst.set_index(['Year', 'Run'])
    dfPlotELC = pd.DataFrame(data=np.NaN, index=range(tmpyearDelta),
                             columns=['Ref - median', 'Ref - 25%', 'Ref - 75%', 'Strat - median', 'Strat - 25%',
                                      'Strat - 75%', 'W2P - median', 'W2P - 25%', 'W2P - 75%', 'Worst - median',
                                      'Worst - 25%', 'Worst - 75%'])

    # Installed factories
    tmpEMRef = dfEMRef.set_index(['Year', 'Run'])
    tmpEMStrat = dfEMStrat.set_index(['Year', 'Run'])
    tmpEMW2P = dfEMW2P.set_index(['Year', 'Run'])
    tmpEMWorst = dfEMWorst.set_index(['Year', 'Run'])
    dfPlotFAC = pd.DataFrame(data=np.NaN, index=range(tmpyearDelta),
                             columns=['Ref - median', 'Ref - 25%', 'Ref - 75%', 'Strat - median', 'Strat - 25%',
                                      'Strat - 75%', 'W2P - median', 'W2P - 25%', 'W2P - 75%', 'Worst - median',
                                      'Worst - 25%', 'Worst - 75%'])

    for i in range(tmpyearDelta):
        # Renewables
        # Reference case
        if i in tmpPMRef.index.levels[0]:
            tmpDf = tmpPMRef.loc[i]['Installed capacity Renewables']
            dfPlotRES.loc[i, 'Ref - median'] = tmpDf.median()
            dfPlotRES.loc[i, 'Ref - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotRES.loc[i, 'Ref - 75%'] = tmpDf.quantile(q=0.75)
        # Strategic investment case
        if i in tmpPMStrat.index.levels[0]:
            tmpDf = tmpPMStrat.loc[i]['Installed capacity Renewables']
            dfPlotRES.loc[i, 'Strat - median'] = tmpDf.median()
            dfPlotRES.loc[i, 'Strat - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotRES.loc[i, 'Strat - 75%'] = tmpDf.quantile(q=0.75)
        # Willingness to pay case
        if i in tmpPMW2P.index.levels[0]:
            tmpDf = tmpPMW2P.loc[i]['Installed capacity Renewables']
            dfPlotRES.loc[i, 'W2P - median'] = tmpDf.median()
            dfPlotRES.loc[i, 'W2P - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotRES.loc[i, 'W2P - 75%'] = tmpDf.quantile(q=0.75)
        # Worst case
        if i in tmpPMWorst.index.levels[0]:
            tmpDf = tmpPMWorst.loc[i]['Installed capacity Renewables']
            dfPlotRES.loc[i, 'Worst - median'] = tmpDf.median()
            dfPlotRES.loc[i, 'Worst - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotRES.loc[i, 'Worst - 75%'] = tmpDf.quantile(q=0.75)

        # Electrolyzers
        # Reference case
        if i in tmpHMRef.index.levels[0]:
            tmpDf = tmpHMRef.loc[i]['Installed capacity Electrolyzers']
            dfPlotELC.loc[i, 'Ref - median'] = tmpDf.median()
            dfPlotELC.loc[i, 'Ref - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotELC.loc[i, 'Ref - 75%'] = tmpDf.quantile(q=0.75)
        # Strategic investment case
        if i in tmpHMStrat.index.levels[0]:
            tmpDf = tmpHMStrat.loc[i]['Installed capacity Electrolyzers']
            dfPlotELC.loc[i, 'Strat - median'] = tmpDf.median()
            dfPlotELC.loc[i, 'Strat - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotELC.loc[i, 'Strat - 75%'] = tmpDf.quantile(q=0.75)
        # Willingness to pay case
        if i in tmpHMW2P.index.levels[0]:
            tmpDf = tmpHMW2P.loc[i]['Installed capacity Electrolyzers']
            dfPlotELC.loc[i, 'W2P - median'] = tmpDf.median()
            dfPlotELC.loc[i, 'W2P - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotELC.loc[i, 'W2P - 75%'] = tmpDf.quantile(q=0.75)
        # Worst case
        if i in tmpHMWorst.index.levels[0]:
            tmpDf = tmpHMWorst.loc[i]['Installed capacity Electrolyzers']
            dfPlotELC.loc[i, 'Worst - median'] = tmpDf.median()
            dfPlotELC.loc[i, 'Worst - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotELC.loc[i, 'Worst - 75%'] = tmpDf.quantile(q=0.75)

        # Factories
        # Reference case
        if i in tmpEMRef.index.levels[0]:
            tmpDf = tmpEMRef.loc[i]['Installed capacity Manufacturings']
            dfPlotFAC.loc[i, 'Ref - median'] = tmpDf.median()
            dfPlotFAC.loc[i, 'Ref - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotFAC.loc[i, 'Ref - 75%'] = tmpDf.quantile(q=0.75)
        # Strategic investment case
        if i in tmpEMStrat.index.levels[0]:
            tmpDf = tmpEMStrat.loc[i]['Installed capacity Manufacturings']
            dfPlotFAC.loc[i, 'Strat - median'] = tmpDf.median()
            dfPlotFAC.loc[i, 'Strat - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotFAC.loc[i, 'Strat - 75%'] = tmpDf.quantile(q=0.75)
        # Willingness to pay case
        if i in tmpEMW2P.index.levels[0]:
            tmpDf = tmpEMW2P.loc[i]['Installed capacity Manufacturings']
            dfPlotFAC.loc[i, 'W2P - median'] = tmpDf.median()
            dfPlotFAC.loc[i, 'W2P - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotFAC.loc[i, 'W2P - 75%'] = tmpDf.quantile(q=0.75)
        # Worst case
        if i in tmpEMWorst.index.levels[0]:
            tmpDf = tmpEMWorst.loc[i]['Installed capacity Manufacturings']
            dfPlotFAC.loc[i, 'Worst - median'] = tmpDf.median()
            dfPlotFAC.loc[i, 'Worst - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotFAC.loc[i, 'Worst - 75%'] = tmpDf.quantile(q=0.75)

    # Figure
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=plotSettings['figsize_3t_l'],
                                        gridspec_kw=plotSettings['gridspec_kw'], dpi=plotSettings['dpi'], sharex=True)

    # Renewables
    ax1.set_ylabel('Renewables [GW]', fontsize=plotSettings['fontsize'])
    # Results data
    ax1.plot(x, dfPlotRES['Ref - median']/1e3, label='Renewables - best case', linestyle='-', color=green)
    #ax1.plot(x, dfPlotRES['Strat - median']/1e3, label='Renewables - non-strategic', linestyle=StratLinestyle,
    #         color=darkgreen)
    ax1.plot(x, dfPlotRES['W2P - median']/1e3, label='Renewables - grey hydrogen', linestyle=W2PLinestlye,
             color=darkgreen)
    #ax1.plot(x, dfPlotRES['Worst - median']/1e3, label='Renewables - worst case', linestyle=WorstLinestyle,
    #        color=darkgreen)

    #ax1.fill_between(x, dfPlotRES['Strat - 25%']/1e3, dfPlotRES['Strat - 75%']/1e3, alpha=0.1, color=darkgreen,
    #                 edgecolor=None, hatch=StratHatch)
    ax1.fill_between(x, dfPlotRES['W2P - 25%']/1e3, dfPlotRES['W2P - 75%']/1e3, alpha=0.1, color=darkgreen,
                     edgecolor=None, hatch=W2PHatch)
    #ax1.fill_between(x, dfPlotRES['Worst - 25%']/1e3, dfPlotRES['Worst - 75%']/1e3, alpha=0.1, color=darkgreen,
    #                 edgecolor=None, hatch=WorstHatch)

    ax1.set_ylim(plotSettings['ylim_res_cap'])

    # Electrolyzers
    ax2.set_ylabel('Electrolyzers [GW]', fontsize=plotSettings['fontsize'])
    # Results data
    ax2.plot(x, dfPlotELC['Ref - median']/1e3, label='Electrolyzers - best case', linestyle='-', color=blue)
    #ax2.plot(x, dfPlotELC['Strat - median']/1e3, label='Electrolyzers - non-strategic', linestyle=StratLinestyle,
    #         color=darkblue)
    ax2.plot(x, dfPlotELC['W2P - median']/1e3, label='Electrolyzers - grey hydrogen', linestyle=W2PLinestlye,
             color=darkblue)
    #ax2.plot(x, dfPlotELC['Worst - median']/1e3, label='Electrolyzers - worst case', linestyle=WorstLinestyle,
    #         color=darkblue)

    #ax2.fill_between(x, dfPlotELC['Strat - 25%']/1e3, dfPlotELC['Strat - 75%']/1e3, alpha=0.1, color=darkblue,
    #                 edgecolor=None, hatch=StratHatch)
    ax2.fill_between(x, dfPlotELC['W2P - 25%']/1e3, dfPlotELC['W2P - 75%']/1e3, alpha=0.1, color=darkblue,
                     edgecolor=None, hatch=W2PHatch)
    #ax2.fill_between(x, dfPlotELC['Worst - 25%']/1e3, dfPlotELC['Worst - 75%']/1e3, alpha=0.1, color=darkblue,
    #                 edgecolor=None, hatch=WorstHatch)

    ax2.set_ylim(plotSettings['ylim_elc_cap'])

    # Factories
    ax3.set_ylabel('Electrolyzer manufacturing [GW/year]', fontsize=plotSettings['fontsize'])
    ax3.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    # Results data
    ax3.plot(x, dfPlotFAC['Ref - median'] / 1e3, label='Electrolyzer manufacturing - best case', linestyle='-', color=purple)
    #ax3.plot(x, dfPlotFAC['Strat - median']/1e3, label='Factories - non-strategic', linestyle=StratLinestyle,
    #         color=darkpurple)
    ax3.plot(x, dfPlotFAC['W2P - median']/1e3, label='Electrolyzer manufacturing - grey hydrogen', linestyle=W2PLinestlye,
             color=darkpurple)
    #ax3.plot(x, dfPlotFAC['Worst - median']/1e3, label='Factories - worst case', linestyle=WorstLinestyle,
    #         color=darkpurple)

    #ax3.fill_between(x, dfPlotFAC['Strat - 25%']/1e3, dfPlotFAC['Strat - 75%']/1e3, alpha=0.1, color=darkpurple,
    #                 edgecolor=None, hatch=StratHatch)
    ax3.fill_between(x, dfPlotFAC['W2P - 25%']/1e3, dfPlotFAC['W2P - 75%']/1e3, alpha=0.1, color=darkpurple,
                     edgecolor=None, hatch=W2PHatch)
    #ax3.fill_between(x, dfPlotFAC['Worst - 25%']/1e3, dfPlotFAC['Worst - 75%']/1e3, alpha=0.1, color=darkpurple,
    #                 edgecolor=None, hatch=WorstHatch)

    ax3.set_ylim(plotSettings['ylim_fac_cap'])

    fig.text(-0.02, 0.5, 'Installed capacities', va='center', rotation='vertical', fontsize=plotSettings['fontsize'])

    tmpxlim = (year0, year0 + tmpyearDelta - 1)
    plt.xlim(tmpxlim)

    # Adjust ticks
    ax1.minorticks_on()
    ax2.minorticks_on()
    ax3.minorticks_on()
    ax1.set_xticks(np.arange(2025, 2105, 10))
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(50))
    ax1.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax1.tick_params(which='minor', axis='both', color='gray')
    ax2.yaxis.set_minor_locator(MultipleLocator(10))
    ax2.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax2.tick_params(which='minor', axis='both', color='gray')
    ax3.yaxis.set_minor_locator(MultipleLocator(5))
    ax3.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax3.tick_params(which='minor', axis='both', color='gray')

    # Legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles3, labels3 = ax3.get_legend_handles_labels()

    handles = handles1 + handles2 + handles3
    labels = labels1 + labels2 + labels3

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.4, -0.55),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=3)

    # Save figure
    plt.savefig(os.getcwd() + '\\figure17b.' + plotType, bbox_inches='tight')

    # Write Data
    writeDf = pd.DataFrame(data=[dfPlotRES['Ref - median']/1e3, dfPlotRES['Strat - median']/1e3,
                                 dfPlotRES['Strat - 25%']/1e3, dfPlotRES['Strat - 75%']/1e3,
                                 dfPlotRES['W2P - median']/1e3, dfPlotRES['W2P - 25%']/1e3,
                                 dfPlotRES['W2P - 75%']/1e3, dfPlotRES['Worst - median']/1e3,
                                 dfPlotRES['Worst - 25%']/1e3, dfPlotRES['Worst - 75%']/1e3,
                                 dfPlotELC['Ref - median']/1e3, dfPlotELC['Strat - median']/1e3,
                                 dfPlotELC['Strat - 25%']/1e3, dfPlotELC['Strat - 75%']/1e3,
                                 dfPlotELC['W2P - median']/1e3, dfPlotELC['W2P - 25%']/1e3,
                                 dfPlotELC['W2P - 75%']/1e3, dfPlotELC['Worst - median']/1e3,
                                 dfPlotELC['Worst - 25%']/1e3, dfPlotELC['Worst - 75%']/1e3,
                                 dfPlotFAC['Ref - median']/1e3, dfPlotFAC['Strat - median']/1e3,
                                 dfPlotFAC['Strat - 25%']/1e3, dfPlotFAC['Strat - 75%']/1e3,
                                 dfPlotFAC['W2P - median']/1e3, dfPlotFAC['W2P - 25%']/1e3,
                                 dfPlotFAC['W2P - 75%']/1e3, dfPlotFAC['Worst - median']/1e3,
                                 dfPlotFAC['Worst - 25%']/1e3, dfPlotFAC['Worst - 75%']/1e3],
                           index=['Inst. Renewables Ref. - median [GW]', 'Inst. Renewables Strat. - median [GW]',
                                  'Inst. Renewables Strat. - 25% [GW]', 'Inst. Renewables Strat. - 75% [GW]',
                                  'Inst. Renewables W2P - median [GW]', 'Inst. Renewables W2P - 25% [GW]',
                                  'Inst. Renewables W2P - 75% [GW]', 'Inst. Renewables Worst - median [GW]',
                                  'Inst. Renewables Worst - 25% [GW]', 'Inst. Renewables Worst - 75% [GW]',
                                  'Inst. Electrolyzers Ref. - median [GW]', 'Inst. Electrolyzers Strat. - median [GW]',
                                  'Inst. Electrolyzers Strat. - 25% [GW]', 'Inst. Electrolyzers Strat. - 75% [GW]',
                                  'Inst. Electrolyzers W2P - median [GW]', 'Inst. Electrolyzers W2P - 25% [GW]',
                                  'Inst. Electrolyzers W2P - 75% [GW]', 'Inst. ELectrolyzers Worst - median [GW]',
                                  'Inst. Electrolyzers Worst - 25% [GW]', 'Inst. Electrolyzers Worst - 75% [GW]',
                                  'Inst. Factories Ref. - median [GW/year]', 'Inst. Factories Strat. - median [GW/year]',
                                  'Inst. Factories Strat. - 25% [GW/year]', 'Inst. Factories Strat. - 75% [GW/year]',
                                  'Inst. Factories W2P - median [GW/year]', 'Inst. Factories W2P - 25% [GW/year]',
                                  'Inst. Factories W2P - 75% [GW/year]', 'Inst. Factories Worst - median [GW/year]',
                                  'Inst. Factoires Worst - 25% [GW/year]', 'Inst. Factoires Worst - 75% [GW/year]'])
    writeDf = writeDf.T
    writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure17b.csv', sep=';')

def figure_18(dfPMRef, dfPMStrat, dfPMW2P, dfPMWorst):
    '''
    Function that will create Fig. 18 - Electricity production obstacle cases.
    :param:
        pd.DataFrame dfPMRef: Daily data from the power market for the reference case.
        pd.DataFrame dfPMStrat: Daily data from the power market for the non-strategic case.
        pd.DataFrame dfPMW2P: Daily data from the power market for the grey hydrogen case.
        pd.DataFrame dfPMWorst: Daily data from the power market for the worst case.
    :return:
    '''
    # Power market
    tmpPMRef = dfPMRef.set_index(['Year', 'Day', 'Run'])
    tmpPMStrat = dfPMStrat.set_index(['Year', 'Day', 'Run'])
    tmpPMW2P = dfPMW2P.set_index(['Year', 'Day', 'Run'])
    tmpPMWorst = dfPMWorst.set_index(['Year', 'Day', 'Run'])
    dfPlotPM = pd.DataFrame(data=np.nan, index=range(yearDelta),
                            columns=['GT - ref', 'GT norm. - ref', 'Demand - ref', 'Demand norm. - ref', 'H2 - ref',
                                     'H2 norm. - ref', 'Curt - ref', 'Curt norm. - ref', 'GT - strat',
                                     'GT norm. - strat', 'Demand - strat', 'Demand norm. - strat', 'H2 - strat',
                                     'H2 norm. - strat', 'Curt - strat', 'Curt norm. - strat', 'GT - W2P',
                                     'GT norm. - W2P', 'Demand - W2P', 'Demand norm. - W2P', 'H2 - W2P',
                                     'H2 norm. - W2P', 'Curt - W2P', 'Curt norm. - W2P', 'GT - worst',
                                     'GT norm. - worst', 'Demand - worst', 'Demand norm. - worst', 'H2 - worst',
                                     'H2 norm. - worst', 'Curt - worst', 'Curt norm. - worst'])

    for i in range(yearDelta):
        # Reference case
        if i in tmpPMRef.index.levels[0]:
            # GT
            tmpGT = tmpPMRef.loc[i]['Electricity demand others'] - tmpPMRef.loc[i]['Actual production renewables']
            tmpGT = tmpGT.mask(tmpGT < 0, 0)
            tmpGT = tmpGT.groupby(level=1).sum().median()
            # Demand
            tmpDemand = tmpPMRef.loc[i]['Electricity demand others'].groupby(level=1).sum().median()
            # H2
            tmpH2 = tmpGT + tmpPMRef.loc[i]['Actual production renewables'].groupby(level=1).sum().median()
            # Curtailment
            tmpCurt = tmpGT + tmpPMRef.loc[i]['Maximum production renewables'].groupby(level=1).sum().median()
            # Absolut values
            dfPlotPM.loc[i, 'GT - ref'] = tmpGT/1e6
            dfPlotPM.loc[i, 'Demand - ref'] = tmpDemand/1e6
            dfPlotPM.loc[i, 'H2 - ref'] = tmpH2/1e6
            dfPlotPM.loc[i, 'Curt - ref'] = tmpCurt/1e6
            # Normalized values
            dfPlotPM.loc[i, 'GT norm. - ref'] = tmpGT/tmpDemand
            dfPlotPM.loc[i, 'Demand norm. - ref'] = tmpDemand/tmpDemand
            dfPlotPM.loc[i, 'H2 norm. - ref'] = tmpH2/tmpDemand
            dfPlotPM.loc[i, 'Curt norm. - ref'] = tmpCurt/tmpDemand

        # Strategic case
        if i in tmpPMStrat.index.levels[0]:
            # GT
            tmpGT = tmpPMStrat.loc[i]['Electricity demand others'] - tmpPMStrat.loc[i]['Actual production renewables']
            tmpGT = tmpGT.mask(tmpGT < 0, 0)
            tmpGT = tmpGT.groupby(level=1).sum().median()
            # Demand
            tmpDemand = tmpPMStrat.loc[i]['Electricity demand others'].groupby(level=1).sum().median()
            # H2
            tmpH2 = tmpGT + tmpPMStrat.loc[i]['Actual production renewables'].groupby(level=1).sum().median()
            # Curtailment
            tmpCurt = tmpGT + tmpPMStrat.loc[i]['Maximum production renewables'].groupby(level=1).sum().median()
            # Absolut values
            dfPlotPM.loc[i, 'GT - strat'] = tmpGT/1e6
            dfPlotPM.loc[i, 'Demand - strat'] = tmpDemand/1e6
            dfPlotPM.loc[i, 'H2 - strat'] = tmpH2/1e6
            dfPlotPM.loc[i, 'Curt - strat'] = tmpCurt/1e6
            # Normalized values
            dfPlotPM.loc[i, 'GT norm. - strat'] = tmpGT/tmpDemand
            dfPlotPM.loc[i, 'Demand norm. - strat'] = tmpDemand/tmpDemand
            dfPlotPM.loc[i, 'H2 norm. - strat'] = tmpH2/tmpDemand
            dfPlotPM.loc[i, 'Curt norm. - strat'] = tmpCurt/tmpDemand

        # Willingness to pay case
        if i in tmpPMW2P.index.levels[0]:
            # GT
            tmpGT = tmpPMW2P.loc[i]['Electricity demand others'] - tmpPMW2P.loc[i]['Actual production renewables']
            tmpGT = tmpGT.mask(tmpGT < 0, 0)
            tmpGT = tmpGT.groupby(level=1).sum().median()
            # Demand
            tmpDemand = tmpPMW2P.loc[i]['Electricity demand others'].groupby(level=1).sum().median()
            # H2
            tmpH2 = tmpGT + tmpPMW2P.loc[i]['Actual production renewables'].groupby(level=1).sum().median()
            # Curtailment
            tmpCurt = tmpGT + tmpPMW2P.loc[i]['Maximum production renewables'].groupby(level=1).sum().median()
            # Absolut values
            dfPlotPM.loc[i, 'GT - W2P'] = tmpGT/1e6
            dfPlotPM.loc[i, 'Demand - W2P'] = tmpDemand/1e6
            dfPlotPM.loc[i, 'H2 - W2P'] = tmpH2/1e6
            dfPlotPM.loc[i, 'Curt - W2P'] = tmpCurt/1e6
            # Normalized values
            dfPlotPM.loc[i, 'GT norm. - W2P'] = tmpGT/tmpDemand
            dfPlotPM.loc[i, 'Demand norm. - W2P'] = tmpDemand/tmpDemand
            dfPlotPM.loc[i, 'H2 norm. - W2P'] = tmpH2/tmpDemand
            dfPlotPM.loc[i, 'Curt norm. - W2P'] = tmpCurt/tmpDemand

        # Worst case
        if i in tmpPMWorst.index.levels[0]:
            # GT
            tmpGT = tmpPMWorst.loc[i]['Electricity demand others'] - tmpPMWorst.loc[i]['Actual production renewables']
            tmpGT = tmpGT.mask(tmpGT < 0, 0)
            tmpGT = tmpGT.groupby(level=1).sum().median()
            # Demand
            tmpDemand = tmpPMWorst.loc[i]['Electricity demand others'].groupby(level=1).sum().median()
            # H2
            tmpH2 = tmpGT + tmpPMWorst.loc[i]['Actual production renewables'].groupby(level=1).sum().median()
            # Curtailment
            tmpCurt = tmpGT + tmpPMWorst.loc[i]['Maximum production renewables'].groupby(level=1).sum().median()
            # Absolut values
            dfPlotPM.loc[i, 'GT - worst'] = tmpGT/1e6
            dfPlotPM.loc[i, 'Demand - worst'] = tmpDemand/1e6
            dfPlotPM.loc[i, 'H2 - worst'] = tmpH2/1e6
            dfPlotPM.loc[i, 'Curt - worst'] = tmpCurt/1e6
            # Normalized values
            dfPlotPM.loc[i, 'GT norm. - worst'] = tmpGT/tmpDemand
            dfPlotPM.loc[i, 'Demand norm. - worst'] = tmpDemand/tmpDemand
            dfPlotPM.loc[i, 'H2 norm. - worst'] = tmpH2/tmpDemand
            dfPlotPM.loc[i, 'Curt norm. - worst'] = tmpCurt/tmpDemand

    # Figure
    fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                            dpi=plotSettings['dpi'])

    ax1.set_ylabel('Electricity mix [-]', fontsize=plotSettings['fontsize'])
    ax1.set_xlabel('Year', fontsize=plotSettings['fontsize'])

    # Reference case
    # Normalized
    ax1.plot(x, dfPlotPM['Demand norm. - ref'], label='General electricity demand - reference', color=black)
    ax1.fill_between(x, 0, dfPlotPM['GT norm. - ref'], label='Production gas turbine - reference', color=grey,
                     alpha=0.25, edgecolor=None)
    ax1.fill_between(x, dfPlotPM['GT norm. - ref'], dfPlotPM['Demand norm. - ref'],
                     label='Production renewables - reference', color=green, alpha=0.25, edgecolor=None)
    ax1.fill_between(x, dfPlotPM['Demand norm. - ref'], dfPlotPM['H2 norm. - ref'],
                     label='Green hydrogen production - reference', color=blue, alpha=0.25, edgecolor=None)
    ax1.fill_between(x, dfPlotPM['H2 norm. - ref'], dfPlotPM['Curt norm. - ref'], label='Curtailment - reference',
                     color=purple, alpha=0.25, edgecolor=None)
    # Absolut
    ax2 = ax1.twinx()
    ax2.set_ylabel('Electricity mix [TWh]', fontsize=plotSettings['fontsize'])
    ax2.plot(x,dfPlotPM['Demand - ref'], color=black)
    ax2.fill_between(x, 0, dfPlotPM['GT - ref'], color=grey, alpha=0.25, edgecolor=None)
    ax2.fill_between(x, dfPlotPM['GT - ref'], dfPlotPM['Demand - ref'], color=green, alpha=0.25, edgecolor=None)
    ax2.fill_between(x, dfPlotPM['Demand - ref'], dfPlotPM['H2 - ref'], color=blue, alpha=0.25, edgecolor=None)
    ax2.fill_between(x, dfPlotPM['H2 - ref'], dfPlotPM['Curt - ref'], color=purple, alpha=0.25, edgecolor=None)

    # Strategic case
    # Normalized
    ax1.plot(x, dfPlotPM['GT norm. - strat'], label='Production gas turbine - non-strategic', color=darkgreen,
             linestyle=StratLinestyle)
    ax1.plot(x, dfPlotPM['H2 norm. - strat'], label='Green hydrogen production - non-strategic', color=darkblue,
             linestyle=StratLinestyle)
    ax1.plot(x, dfPlotPM['Curt norm. - strat'], label='Curtailment - non-strategic', color=darkpurple,
             linestyle=StratLinestyle)
    # Absolut
    ax2.plot(x, dfPlotPM['GT - strat'], color=darkgreen, linestyle=StratLinestyle)
    ax2.plot(x, dfPlotPM['H2 - strat'], color=darkblue, linestyle=StratLinestyle)
    ax2.plot(x, dfPlotPM['Curt - strat'], color=darkpurple, linestyle=StratLinestyle)

    # Willingness to pay case
    # Normalized
    ax1.plot(x, dfPlotPM['GT norm. - W2P'], label='Production gas turbine - grey hydrogen', color=darkgreen,
             linestyle=W2PLinestlye)
    ax1.plot(x, dfPlotPM['H2 norm. - W2P'], label='Green hydrogen production - grey hydrogen', color=darkblue,
             linestyle=W2PLinestlye)
    ax1.plot(x, dfPlotPM['Curt norm. - W2P'], label='Curtailment - grey hydrogen', color=darkpurple,
             linestyle=W2PLinestlye)
    # Absolut
    ax2.plot(x, dfPlotPM['GT - W2P'], color=darkgreen, linestyle=W2PLinestlye)
    ax2.plot(x, dfPlotPM['H2 - W2P'], color=darkblue, linestyle=W2PLinestlye)
    ax2.plot(x, dfPlotPM['Curt - W2P'], color=darkpurple, linestyle=W2PLinestlye)

    # Worst case
    # Normalized
    ax1.plot(x, dfPlotPM['GT norm. - worst'], label='Production gas turbine - worst case', color=darkgreen,
             linestyle=WorstLinestyle)
    ax1.plot(x, dfPlotPM['H2 norm. - worst'], label='Green hydrogen production - worst case', color=darkblue,
             linestyle=WorstLinestyle)
    ax1.plot(x, dfPlotPM['Curt norm. - worst'], label='Curtailment - worst case', color=darkpurple,
             linestyle=WorstLinestyle)
    # Absolut
    ax2.plot(x, dfPlotPM['GT - worst'], color=darkgreen, linestyle=WorstLinestyle)
    ax2.plot(x, dfPlotPM['H2 - worst'], color=darkblue, linestyle=WorstLinestyle)
    ax2.plot(x, dfPlotPM['Curt - worst'], color=darkpurple, linestyle=WorstLinestyle)


    # Adjust axis
    ax1.minorticks_on()
    ax1.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    ax1.set_xlim(plotSettings['xlim'])
    ax1.set_ylim(0)
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(5))
    ax2.minorticks_on()
    ax2.set_ylim(0)
    ax2.set_xticks(plotSettings['xticks'])
    ax2.xaxis.set_minor_locator(MultipleLocator(5))
    ax2.yaxis.set_minor_locator(MultipleLocator(50))

    ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax1.tick_params(axis='both', which='minor', color='gray')

    ax2.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax2.tick_params(axis='both', which='minor', color='gray')

    # Legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    handles = handles1 + handles2
    labels = labels1 + labels2

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.85),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save plot
    plt.savefig(os.getcwd() + '\\figure18.' + plotType, bbox_inches='tight')

    # Write data
    writeDf = pd.DataFrame(data=[dfPlotPM['GT - ref'], dfPlotPM['Demand - ref'], dfPlotPM['H2 - ref'],
                                 dfPlotPM['Curt - ref'],
                                 dfPlotPM['GT norm. - ref'], dfPlotPM['Demand norm. - ref'], dfPlotPM['H2 norm. - ref'],
                                 dfPlotPM['Curt norm. - ref'],
                                 dfPlotPM['GT - strat'], dfPlotPM['H2 - strat'], dfPlotPM['Curt - strat'],
                                 dfPlotPM['GT norm. - strat'], dfPlotPM['H2 norm. - strat'], dfPlotPM['Curt norm. - strat'],
                                 dfPlotPM['GT - W2P'],  dfPlotPM['H2 - W2P'], dfPlotPM['Curt - W2P'],
                                 dfPlotPM['GT norm. - W2P'], dfPlotPM['H2 norm. - W2P'], dfPlotPM['Curt norm. - W2P'],
                                 dfPlotPM['GT - worst'], dfPlotPM['H2 - worst'], dfPlotPM['Curt - worst'],
                                 dfPlotPM['GT norm. - worst'], dfPlotPM['H2 norm. - worst'], dfPlotPM['Curt norm. - worst']],
                           index=['Production GT - ref [TWh]', 'Demand - ref [TWh]', 'H2 - ref [TWh]',
                                  'Curtailment - ref [TWh]',
                                  'Production GT - ref [-]', 'Demand - ref [-]', 'H2 - ref [-]',
                                  'Curtailment - ref [-]',
                                  'Production GT - strat [TWh]', 'H2 - strat [TWh]', 'Curtailment - strat [TWh]',
                                  'Production GT - strat [-]', 'H2 - strat [-]', 'Curtailment - strat [-]',
                                  'Production GT - W2P [TWh]', 'H2 - W2P [TWh]', 'Curtailment - W2P [TWh]',
                                  'Production GT - W2P [-]', 'H2 - W2P [-]', 'Curtailment - W2P [-]',
                                  'Production GT - Worst [TWh]', 'H2 - Worst [TWh]', 'Curtailment - Worst [TWh]',
                                  'Production GT - Worst [-]', 'H2 - Worst [-]', 'Curtailment - Worst [-]'])
    writeDf = writeDf.T
    writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure18.csv', sep=';')


def figure_19(dfHMRef, dfHMStrat, dfHMW2P, dfHMWorst):
    '''
    Function that will create Fig. 19 - Hydrogen production obstacle cases.
    :param:
        pd.DataFrame dfHMRef: Daily data from the hydrogen market for the reference case.
        pd.DataFrame dfHMStrat: Daily data from the hydrogen market for the strategic investment case.
        pd.DataFrame dfHMW2P: Daily data from the hydrogen market for the willingness to pay case.
        pd.DataFrame dfHMWorst: Daily data from the hydrogen market for the worst case.
    :return:
    '''
    # tmpDemand= [Type, Label, Color, Hatch, Mt, MWh]
    tmpDemand = {1: ['Refineries 1', 'Refineries', green, '///', 0.207, 6889656],
                 2: ['Ammonia 1', 'Ammonia', blue, '|||', 0.302, 10047415],
                 3: ['Methanol 1', 'Methanol', darkblue, '---', 0.354, 11769829],
                 4:	['Refineries 2', 'Refineries', green, '///', 0.432, 14353450],
                 5:	['Steel 1', 'Steel', grey, '', 1.303, 43347416],
                 6:	['Ammonia 2', 'Ammonia', blue, '|||', 1.605, 53394830],
                 7:	['Power 1', 'Power generation', orange, '+++', 1.795, 59710347],
                 8:	['Ammonia 3', 'Ammonia', blue, '|||', 1.898,	63155175],
                 9:	['Methanol 2', 'Methanol', darkblue, '---', 2.036, 67748278],
                 10: ['Aviation 1', 'Aviation', purple, '...', 2.389, 79518106],
                 11: ['Heat 1', 'Industrial heat', red, 'ooo', 3.26, 108512072],
                 12: ['Refineries 3', 'Refineries', green, '///', 3.363, 111956900],
                 13: ['Methanol 3', 'Methanol', darkblue, '---', 3.432, 114253452],
                 14: ['Power 2', 'Power generation', orange, '+++',	3.854, 128319831],
                 15: ['Steel 2', 'Steel', grey, '', 4.707, 156739659],
                 16: ['Heat 2', 'Industrial heat', red,	'ooo', 10.604, 353094831],
                 17: ['Aviation 2', 'Aviation', purple, '...', 16.32, 543421555]
                 }

    tmpColumns = []
    for i in tmpDemand.keys():
        tmpColumns.append(tmpDemand[i][0])
    tmpColumns.append('H2 ref - median')
    tmpColumns.append('H2 strat - median')
    tmpColumns.append('H2 strat - 25%')
    tmpColumns.append('H2 strat - 75%')
    tmpColumns.append('H2 w2p - median')
    tmpColumns.append('H2 w2p - 25%')
    tmpColumns.append('H2 w2p - 75%')
    tmpColumns.append('H2 worst - median')
    tmpColumns.append('H2 worst - 25%')
    tmpColumns.append('H2 worst - 75%')

    # Hydrogen market
    tmpHMRef = dfHMRef.set_index(['Year', 'Day', 'Run'])
    tmpHMStrat = dfHMStrat.set_index(['Year', 'Day', 'Run'])
    tmpHMW2P = dfHMW2P.set_index(['Year', 'Day', 'Run'])
    tmpHMWorst = dfHMWorst.set_index(['Year', 'Day', 'Run'])
    dfPlotHM = pd.DataFrame(data=np.nan, index=range(yearDelta), columns=tmpColumns)

    for i in range(yearDelta):
        # Reference case
        if i in tmpHMRef.index.levels[0]:
            # Hydrogen production
            tmpH2 = tmpHMRef.loc[i]['Actual production electrolyzers'].groupby(level=1).sum()
            dfPlotHM.loc[i, 'H2 ref - median'] = tmpH2.median()
            # Hydrogen demand
            for j in tmpDemand.keys():
                if tmpH2.median() < tmpDemand[j][-1]:
                    dfPlotHM.loc[i, tmpDemand[j][0]] = tmpH2.median()
                else:
                    dfPlotHM.loc[i, tmpDemand[j][0]] = tmpDemand[j][-1]

        # Strategic case
        if i in tmpHMStrat.index.levels[0]:
            tmpH2 = tmpHMStrat.loc[i]['Actual production electrolyzers'].groupby(level=1).sum()
            dfPlotHM.loc[i, 'H2 strat - median'] = tmpH2.median()
            dfPlotHM.loc[i, 'H2 strat - 25%'] = tmpH2.quantile(q=0.25)
            dfPlotHM.loc[i, 'H2 strat - 75%'] = tmpH2.quantile(q=0.75)

        # Willingness to pay case
        if i in tmpHMW2P.index.levels[0]:
            tmpH2 = tmpHMW2P.loc[i]['Actual production electrolyzers'].groupby(level=1).sum()
            dfPlotHM.loc[i, 'H2 w2p - median'] = tmpH2.median()
            dfPlotHM.loc[i, 'H2 w2p - 25%'] = tmpH2.quantile(q=0.25)
            dfPlotHM.loc[i, 'H2 w2p - 75%'] = tmpH2.quantile(q=0.75)

        # Worst case
        if i in tmpHMWorst.index.levels[0]:
            tmpH2 = tmpHMWorst.loc[i]['Actual production electrolyzers'].groupby(level=1).sum()
            dfPlotHM.loc[i, 'H2 worst - median'] = tmpH2.median()
            dfPlotHM.loc[i, 'H2 worst - 25%'] = tmpH2.quantile(q=0.25)
            dfPlotHM.loc[i, 'H2 worst - 75%'] = tmpH2.quantile(q=0.75)

    # Figure
    fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                            dpi=plotSettings['dpi'])

    ax1.set_ylabel('Hydrogen production [TWh/year]', fontsize=plotSettings['fontsize'])
    ax1.set_xlabel('Year', fontsize=plotSettings['fontsize'])

    # Hydrogen production
    # Reference
    ax1.plot(x, dfPlotHM['H2 ref - median']/1e6, label='Hydrogen production - best case', color=blue,
             linestyle='-')
    # Strategic
    ax1.plot(x, dfPlotHM['H2 strat - median']/1e6, label='Hydrogen production - non-strategic', color=darkblue,
             linestyle=StratLinestyle)
    ax1.fill_between(x, dfPlotHM['H2 strat - 25%']/1e6, dfPlotHM['H2 strat - 75%']/1e6, color=darkblue, edgecolor=None,
                     alpha=0.1, hatch=StratHatch)
    # W2P
    ax1.plot(x, dfPlotHM['H2 w2p - median']/1e6, label='Hydrogen production - grey hydrogen', color=darkblue,
             linestyle=W2PLinestlye)
    ax1.fill_between(x, dfPlotHM['H2 w2p - 25%']/1e6, dfPlotHM['H2 w2p - 75%']/1e6, color=darkblue, edgecolor=None,
                     alpha=0.1, hatch=W2PHatch)
    # Worst
    ax1.plot(x, dfPlotHM['H2 worst - median']/1e6, label='Hydrogen production - worst case', color=darkblue,
             linestyle=WorstLinestyle)
    ax1.fill_between(x, dfPlotHM['H2 worst - 25%']/1e6, dfPlotHM['H2 worst - 75%']/1e6, color=darkblue, edgecolor=None,
                     alpha=0.1, hatch=WorstHatch)

    # Hydrogen demand
    oldKey = 'None'
    lastKey = True
    for i in tmpDemand.keys():
        if dfPlotHM['H2 ref - median'].max() > tmpDemand[i][-1]:
            if oldKey == 'None':
                ax1.fill_between(x, 0, dfPlotHM[tmpDemand[i][0]] / 1e6, color=tmpDemand[i][2], alpha=0.25,
                                 edgecolor=None,
                                 label=tmpDemand[i][1], hatch=tmpDemand[i][3])
            else:
                ax1.fill_between(x, dfPlotHM[tmpDemand[oldKey][0]] / 1e6, dfPlotHM[tmpDemand[i][0]] / 1e6,
                                 color=tmpDemand[i][2], alpha=0.25, edgecolor=None, label=tmpDemand[i][1],
                                 hatch=tmpDemand[i][3])
        else:
            if lastKey:
                ax1.fill_between(x, dfPlotHM[tmpDemand[oldKey][0]] / 1e6, dfPlotHM[tmpDemand[i][0]] / 1e6,
                                 color=tmpDemand[i][2], alpha=0.25, edgecolor=None, label=tmpDemand[i][1],
                                 hatch=tmpDemand[i][3])
                lastKey = False
        oldKey = i

    # In Mt
    ax2 = ax1.twinx()
    ax2.set_ylabel('Hydrogen production [Mio. t/year]', fontsize=plotSettings['fontsize'])
    ax2.plot(x, dfPlotHM['H2 ref - median']/(33.3*1e6), color=blue, linestyle='-')
    ax2.plot(x, dfPlotHM['H2 strat - median']/(33.3*1e6), color=darkblue, linestyle=StratLinestyle)
    ax2.fill_between(x, dfPlotHM['H2 strat - 25%']/(33.3*1e6), dfPlotHM['H2 strat - 75%']/(33.3*1e6), color=darkblue,
                     edgecolor=None, alpha=0.1, hatch=StratHatch)

    # Adjust axis
    ax1.minorticks_on()
    ax1.set_xlim(plotSettings['xlim'])
    ax1.set_ylim(0)
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(10))
    ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax1.tick_params(axis='both', which='minor', color='gray')

    ax2.minorticks_on()
    ax2.set_xlim(plotSettings['xlim'])
    ax2.set_ylim(0)
    ax2.set_xticks(plotSettings['xticks'])
    ax2.xaxis.set_minor_locator(MultipleLocator(5))
    ax2.yaxis.set_minor_locator(MultipleLocator(10))
    ax2.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax2.tick_params(axis='both', which='minor', color='gray')

    # Adjust legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    handles = handles1 + handles2
    labels = labels1 + labels2

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.8),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save plot
    plt.savefig(os.getcwd() + '\\figure19.' + plotType, bbox_inches='tight')

    # Write data
    writeDf = pd.DataFrame(data=[dfPlotHM['H2 ref - median'], dfPlotHM['H2 strat - median'], dfPlotHM['H2 strat - 25%'],
                                 dfPlotHM['H2 strat - 75%'], dfPlotHM['H2 w2p - median'], dfPlotHM['H2 w2p - 25%'],
                                 dfPlotHM['H2 w2p - 75%'], dfPlotHM['H2 worst - median'], dfPlotHM['H2 worst - 25%'],
                                 dfPlotHM['H2 worst - 75%']],
                           index=['Hydrogen production reference - median [TWh]',
                                  'Hydrogen production strategic - median [TWh]',
                                  'Hydrogen production strategic - 25% [TWh]',
                                  'Hydrogen production strategic - 75% [TWh]', 'Hydrogen production W2P - median [TWh]',
                                  'Hydrogen production W2P - 25% [TWh]', 'Hydrogen production W2P - 75% [TWh]',
                                  'Hydrogen production Worst - median [TWh]',
                                  'Hydrogen production Worst - 25% [TWh]', 'Hydrogen production Worst - 75% [TWh]'])
    writeDf = writeDf.T
    writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure19.csv', sep=';')


def figure_20(dfRESRef, dfRESStrat, dfRESW2P, dfRESWorst, dfELCRef, dfELCStrat, dfELCW2P, dfELCWorst):
    '''
    Function that will create Fig. 20 - Utilization of Renewables and Electrolyzers of the obstacle cases.
    :param:
        pd.DataFrame dfRESRef: Yearly data from the renewables for the reference case.
        pd.DataFrame dfRESStrat: Yearly data from the renewables for the strategic case.
        pd.DataFrame dfRESW2P: Yearly data from the renewables for the willingness to pay case.
        pd.DataFrame dfRESWorst: Yearly data from the renewables for the worst case.
        pd.DataFrame dfELCRef: Yearly data from the electrolyzers for the reference case.
        pd.DataFrame dfELCStrat: Yearly data from the electrolyzers for the non-strategic case.
        pd.DataFrame dfELCW2P: Yearly data from the electrolyzers for the grey hydrogen case.
        pd.DataFrame dfELCWorst: Yearly data from the electrolyzers for the worste case.
    :return:
    '''
    # Renewables
    tmpRESRef = dfRESRef.set_index(['Year', 'Run', 'ID'])
    tmpRESStrat = dfRESStrat.set_index(['Year', 'Run', 'ID'])
    tmpRESW2P = dfRESW2P.set_index(['Year', 'Run', 'ID'])
    tmpRESWorst = dfRESWorst.set_index(['Year', 'Run', 'ID'])
    dfPlotRES = pd.DataFrame(data=np.nan, index=range(yearDelta),
                             columns=['Util ref - median', 'Util strat - median', 'Util strat - 25%',
                                      'Util strat - 75%', 'Util w2p - median', 'Util w2p - 25%', 'Util w2p - 75%',
                                      'Util worst - median', 'Util worst - 25%', 'Util worst - 75%'])

    # Electrolyzers
    tmpELCRef = dfELCRef.set_index(['Year', 'Run', 'ID'])
    tmpELCStrat = dfELCStrat.set_index(['Year', 'Run', 'ID'])
    tmpELCW2P = dfELCW2P.set_index(['Year', 'Run', 'ID'])
    tmpELCWorst = dfELCWorst.set_index(['Year','Run', 'ID'])
    dfPlotELC = pd.DataFrame(data=np.nan, index=range(yearDelta),
                             columns=['Util ref - median', 'Util strat - median', 'Util strat - 25%',
                                      'Util strat - 75%', 'Util w2p - median', 'Util w2p - 25%', 'Util w2p - 75%',
                                      'Util worst - median', 'Util worst - 25%', 'Util worst - 75%'])

    for i in range(yearDelta):
        # Renewables
        # Reference case
        if i in tmpRESRef.index.levels[0]:
            tmpDf = tmpRESRef.loc[i]['Utilization rate'].groupby(level=0).max()
            dfPlotRES.loc[i, 'Util ref - median'] = tmpDf.median()*100
        # Strategic case
        if i in tmpRESStrat.index.levels[0]:
            tmpDf = tmpRESStrat.loc[i]['Utilization rate'].groupby(level=0).max()
            dfPlotRES.loc[i, 'Util strat - median'] = tmpDf.median()*100
            dfPlotRES.loc[i, 'Util strat - 25%'] = tmpDf.quantile(q=0.25)*100
            dfPlotRES.loc[i, 'Util strat - 75%'] = tmpDf.quantile(q=0.75)*100
        # Willingness to pay case
        if i in tmpRESW2P.index.levels[0]:
            tmpDf = tmpRESW2P.loc[i]['Utilization rate'].groupby(level=0).max()
            dfPlotRES.loc[i, 'Util w2p - median'] = tmpDf.median()*100
            dfPlotRES.loc[i, 'Util w2p - 25%'] = tmpDf.quantile(q=0.25)*100
            dfPlotRES.loc[i, 'Util w2p - 75%'] = tmpDf.quantile(q=0.75)*100
        # Worst case
        if i in tmpRESWorst.index.levels[0]:
            tmpDf = tmpRESWorst.loc[i]['Utilization rate'].groupby(level=0).max()
            dfPlotRES.loc[i, 'Util worst - median'] = tmpDf.median()*100
            dfPlotRES.loc[i, 'Util worst - 25%'] = tmpDf.quantile(q=0.25)*100
            dfPlotRES.loc[i, 'Util worst - 75%'] = tmpDf.quantile(q=0.75)*100

        # Electrolyzers
        # Reference case
        if i in tmpELCRef.index.levels[0]:
            tmpDf = tmpELCRef.loc[i]['Utilization rate'].groupby(level=0).max()
            dfPlotELC.loc[i, 'Util ref - median'] = tmpDf.median()*100
        # Strategic case
        if i in tmpELCStrat.index.levels[0]:
            tmpDf = tmpELCStrat.loc[i]['Utilization rate'].groupby(level=0).max()
            dfPlotELC.loc[i, 'Util strat - median'] = tmpDf.median()*100
            dfPlotELC.loc[i, 'Util strat - 25%'] = tmpDf.quantile(q=0.25)*100
            dfPlotELC.loc[i, 'Util strat - 75%'] = tmpDf.quantile(q=0.75)*100
        # Willingness to pay case
        if i in tmpELCW2P.index.levels[0]:
            tmpDf = tmpELCW2P.loc[i]['Utilization rate'].groupby(level=0).max()
            dfPlotELC.loc[i, 'Util w2p - median'] = tmpDf.median()*100
            dfPlotELC.loc[i, 'Util w2p - 25%'] = tmpDf.quantile(q=0.25)*100
            dfPlotELC.loc[i, 'Util w2p - 75%'] = tmpDf.quantile(q=0.75)*100
        # Worst case
        if i in tmpELCWorst.index.levels[0]:
            tmpDf = tmpELCWorst.loc[i]['Utilization rate'].groupby(level=0).max()
            dfPlotELC.loc[i, 'Util worst - median'] = tmpDf.median()*100
            dfPlotELC.loc[i, 'Util worst - 25%'] = tmpDf.quantile(q=0.25)*100
            dfPlotELC.loc[i, 'Util worst - 75%'] = tmpDf.quantile(q=0.75)*100

    # Figure
    fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                            dpi=plotSettings['dpi'])

    ax1.set_ylabel('Utilization rate [%]', fontsize=plotSettings['fontsize'])
    ax1.set_xlabel('Year', fontsize=plotSettings['fontsize'])

    # In %
    # Renewables
    ax1.plot(x, dfPlotRES['Util ref - median'], label='Renewables - best case', color=green, linestyle='-')
    ax1.plot(x, dfPlotRES['Util strat - median'], label='Renewables - non-strategic', color=darkgreen,
             linestyle=StratLinestyle)
    ax1.fill_between(x, dfPlotRES['Util strat - 25%'], dfPlotRES['Util strat - 75%'], color=darkgreen, edgecolor=None,
                     hatch=StratHatch, alpha=0.1)
    ax1.plot(x, dfPlotRES['Util w2p - median'], label='Renewables - grey hydrogen', color=darkgreen,
             linestyle=W2PLinestlye)
    ax1.fill_between(x, dfPlotRES['Util w2p - 25%'], dfPlotRES['Util w2p - 75%'], color=darkgreen, edgecolor=None,
                     hatch=W2PHatch, alpha=0.1)
    ax1.plot(x, dfPlotRES['Util worst - median'], label='Renewables - worst case', color=darkgreen,
             linestyle=WorstLinestyle)
    ax1.fill_between(x, dfPlotRES['Util worst - 25%'], dfPlotRES['Util worst - 75%'], color=darkgreen, edgecolor=None,
                     hatch=WorstHatch, alpha=0.1)

    # Electrolyzers
    ax1.plot(x, dfPlotELC['Util ref - median'], label='Electrolyzers - best case', color=blue, linestyle='-')
    ax1.plot(x, dfPlotELC['Util strat - median'], label='Electrolyzers - non-strategic', color=darkblue,
             linestyle=StratLinestyle)
    ax1.fill_between(x, dfPlotELC['Util strat - 25%'], dfPlotELC['Util strat - 75%'], color=darkblue, edgecolor=None,
                     hatch=StratHatch, alpha=0.1)
    ax1.plot(x, dfPlotELC['Util w2p - median'], label='Electrolyzers - grey hydrogen', color=darkblue,
             linestyle=W2PLinestlye)
    ax1.fill_between(x, dfPlotELC['Util w2p - 25%'], dfPlotELC['Util w2p - 75%'], color=darkblue, edgecolor=None,
                     hatch=W2PHatch, alpha=0.1)
    ax1.plot(x, dfPlotELC['Util worst - median'], label='Electrolyzers - worst case', color=darkblue,
             linestyle=WorstLinestyle)
    ax1.fill_between(x, dfPlotELC['Util worst - 25%'], dfPlotELC['Util worst - 75%'], color=darkblue, edgecolor=None,
                     hatch=WorstHatch, alpha=0.1)

    # In full load hours
    ax2 = ax1.twinx()
    ax2.set_ylabel('Full load hours [h]', fontsize=plotSettings['fontsize'])
    # Renewables
    ax2.plot(x, dfPlotRES['Util ref - median']*87.6, label='Renewables - best case', color=green, linestyle='-')
    ax2.plot(x, dfPlotRES['Util strat - median']*87.6, label='Renewables - non-strategic', color=darkgreen,
             linestyle=StratLinestyle)
    ax2.fill_between(x, dfPlotRES['Util strat - 25%']*87.6, dfPlotRES['Util strat - 75%']*87.6, color=darkgreen,
                     edgecolor=None, hatch=StratHatch, alpha=0.1)
    ax2.plot(x, dfPlotRES['Util w2p - median']*87.6, label='Renewables - grey hydrogen', color=darkgreen,
             linestyle=W2PLinestlye)
    ax2.fill_between(x, dfPlotRES['Util w2p - 25%']*87.6, dfPlotRES['Util w2p - 75%']*87.6, color=darkgreen,
                     edgecolor=None, hatch=W2PHatch, alpha=0.1)
    ax2.plot(x, dfPlotRES['Util worst - median']*87.6, label='Renewables - worst case', color=darkgreen,
             linestyle=WorstLinestyle)
    ax2.fill_between(x, dfPlotRES['Util worst - 25%']*87.6, dfPlotRES['Util worst - 75%']*87.6, color=darkgreen,
                     edgecolor=None, hatch=WorstHatch, alpha=0.1)

    # Electrolyzers
    ax2.plot(x, dfPlotELC['Util ref - median']*87.6, label='Electrolyzers - best case', color=blue, linestyle='-')
    ax2.plot(x, dfPlotELC['Util strat - median']*87.6, label='Electrolyzers - non-strategic', color=darkblue,
             linestyle=StratLinestyle)
    ax2.fill_between(x, dfPlotELC['Util strat - 25%']*87.6, dfPlotELC['Util strat - 75%']*87.6, color=darkblue,
                     edgecolor=None, hatch=StratHatch, alpha=0.1)
    ax2.plot(x, dfPlotELC['Util w2p - median']*87.6, label='Electrolyzers - grey hydrogen', color=darkblue,
             linestyle=W2PLinestlye)
    ax2.fill_between(x, dfPlotELC['Util w2p - 25%']*87.6, dfPlotELC['Util w2p - 75%']*87.6, color=darkblue,
                     edgecolor=None, hatch=W2PHatch, alpha=0.1)
    ax2.plot(x, dfPlotELC['Util worst - median']*87.6, label='Electrolyzers - worst case', color=darkblue,
             linestyle=WorstLinestyle)
    ax2.fill_between(x, dfPlotELC['Util worst - 25%']*87.6, dfPlotELC['Util worst - 75%']*87.6, color=darkblue,
                     edgecolor=None, hatch=WorstHatch, alpha=0.1)

    # Adjust axis
    ax1.minorticks_on()
    ax1.set_xlim(plotSettings['xlim'])
    ax1.set_ylim([0, 100])
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(10))
    ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax1.tick_params(axis='both', which='minor', color='gray')

    ax2.minorticks_on()
    ax2.set_xlim(plotSettings['xlim'])
    ax2.set_ylim([0, 8760])
    ax2.set_xticks(plotSettings['xticks'])
    ax2.xaxis.set_minor_locator(MultipleLocator(5))
    ax2.yaxis.set_minor_locator(MultipleLocator(1000))
    ax2.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax2.tick_params(axis='both', which='minor', color='gray')

    # Adjust legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    handles = handles1 + handles2
    labels = labels1 + labels2

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.8),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save plot
    plt.savefig(os.getcwd() + '\\figure20.' + plotType, bbox_inches='tight')

    # Write data
    writeDf = pd.DataFrame(data=[dfPlotRES['Util ref - median'], dfPlotRES['Util strat - median'],
                                 dfPlotRES['Util strat - 25%'], dfPlotRES['Util strat - 75%'],
                                 dfPlotRES['Util w2p - median'], dfPlotRES['Util w2p - 25%'],
                                 dfPlotRES['Util w2p - 75%'], dfPlotRES['Util worst - median'],
                                 dfPlotRES['Util worst - 25%'], dfPlotRES['Util worst - 75%'],
                                 dfPlotELC['Util ref - median'], dfPlotELC['Util strat - median'],
                                 dfPlotELC['Util strat - 25%'], dfPlotELC['Util strat - 75%'],
                                 dfPlotELC['Util w2p - median'], dfPlotELC['Util w2p - 25%'],
                                 dfPlotELC['Util w2p - 75%'], dfPlotELC['Util worst - median'],
                                 dfPlotELC['Util worst - 25%'], dfPlotELC['Util worst - 75%'],
                                 dfPlotRES['Util ref - median']*87.6, dfPlotRES['Util strat - median']*87.6,
                                 dfPlotRES['Util strat - 25%']*87.6, dfPlotRES['Util strat - 75%']*87.6,
                                 dfPlotRES['Util w2p - median']*87.6, dfPlotRES['Util w2p - 25%']*87.6,
                                 dfPlotRES['Util w2p - 75%']*87.6, dfPlotRES['Util worst - median']*87.6,
                                 dfPlotRES['Util worst - 25%']*87.6, dfPlotRES['Util w2p - 75%']*87.6,
                                 dfPlotELC['Util ref - median']*87.6, dfPlotELC['Util strat - median']*87.6,
                                 dfPlotELC['Util strat - 25%']*87.6, dfPlotELC['Util strat - 75%']*87.6,
                                 dfPlotELC['Util w2p - median']*87.6, dfPlotELC['Util w2p - 25%']*87.6,
                                 dfPlotELC['Util w2p - 75%']*87.6, dfPlotELC['Util worst - median']*87.6,
                                 dfPlotELC['Util worst - 25%']*87.6, dfPlotELC['Util worst - 75%']*87.6],
                           index=['Utilization Renewables reference - median [%]',
                                  'Utilization Renewables strat - median [%]', 'Utilization Renewables strat - 25% [%]',
                                  'Utilization Renewables strat - 75% [%]', 'Utilization Renewables W2P - median [%]',
                                  'Utilization Renewables W2P - 25% [%]', 'Utilization Renewables W2P - 75% [%]',
                                  'Utilization Renewables worst - median [%]',
                                  'Utilization Renewables worst - 25% [%]', 'Utilization Renewables worst - 75% [%]',
                                  'Utilization Electrolyzers reference - median [%]',
                                  'Utilization Electrolyzers strat - median [%]',
                                  'Utilization Electrolyzers strat - 25% [%]',
                                  'Utilization Electrolyzers strat - 75% [%]',
                                  'Utilization Electrolyzers W2P - median [%]',
                                  'Utilization Electrolyzers W2P - 25% [%]',
                                  'Utilization Electrolyzers W2P - 75% [%]',
                                  'Utilization Electrolyzers worst - median [%]',
                                  'Utilization Electrolyzers worst - 25% [%]',
                                  'Utilization Electrolyzers worst - 75% [%]',
                                  'Utilization Renewables reference - median [h]',
                                  'Utilization Renewables strat - median [h]', 'Utilization Renewables strat - 25% [h]',
                                  'Utilization Renewables strat - 75% [h]', 'Utilization Renewables W2P - median [h]',
                                  'Utilization Renewables W2P - 25% [h]', 'Utilization Renewables W2P - 75% [h]',
                                  'Utilization Renewables worst - median [h]',
                                  'Utilization Renewables worst - 25% [h]', 'Utilization Renewables worst - 75% [h]',
                                  'Utilization Electrolyzers reference - median [h]',
                                  'Utilization Electrolyzers strat - median [h]',
                                  'Utilization Electrolyzers strat - 25% [h]',
                                  'Utilization Electrolyzers strat - 75% [h]',
                                  'Utilization Electrolyzers W2P - median [h]',
                                  'Utilization Electrolyzers W2P - 25% [h]',
                                  'Utilization Electrolyzers W2P - 75% [h]',
                                  'Utilization Electrolyzers worst - median [h]',
                                  'Utilization Electrolyzers worst - 25% [h]',
                                  'Utilization Electrolyzers worst - 75% [h]'])

    writeDf = writeDf.T
    writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure20.csv', sep=';')


def figure_21(dfPPRef, dfPPStrat, dfPPW2P, dfPPWorst, dfHPRef, dfHPStrat, dfHPW2P, dfHPWorst, dfEPRef, dfEPStrat,
              dfEPW2P, dfEPWorst):
    '''
    Function that will create Fig. 21 - ROI for PP, HP & EP of the obstacle cases.
    :param:
        pd.DataFrame dfPPRef: Yearly data from the power producers for the reference case.
        pd.DataFrame dfPPStrat: Yearly data from the power producers for the strategic case.
        pd.DataFrame dfPPW2P: Yearly data from the power producers for the willingness to pay case.
        pd.DataFrame dfPPWorst: Yearly data from the power producers for the worst case.
        pd.DataFrame dfHPRef: Yearly data from the hydrogen producers for the reference case.
        pd.DataFrame dfHPStrat: Yearly data from the hydrogen producers for the strategic case.
        pd.DataFrame dfHPW2P: Yearly data from the hydrogen producers for the willingness to pay case.
        pd.DataFrame dfHPWorst: Yearly data from the hydrogen producers for the worst case.
        pd.DataFrame dfHPRef: Yearly data from the hydrogen producers for the reference case.
        pd.DataFrame dfHPStrat: Yearly data from the hydrogen producers for the strategic case.
        pd.DataFrame dfHPW2P: Yearly data from the hydrogen producers for the willingness to pay case.
        pd.DataFrame dfHPWorst: Yearly data from the hydrogen producers for the worst case.
    :return:
    '''
    # Power producers
    tmpPPRef = dfPPRef.set_index(['Year', 'Run', 'ID'])
    tmpPPStrat = dfPPStrat.set_index(['Year', 'Run', 'ID'])
    tmpPPW2P = dfPPW2P.set_index(['Year', 'Run', 'ID'])
    tmpPPWorst = dfPPWorst.set_index(['Year', 'Run', 'ID'])
    dfPlotPP = pd.DataFrame(data=np.NaN, index=range(yearDelta),
                            columns=['ref - median', 'strat - median', 'strat - 25%', 'strat - 75%', 'w2p - median',
                                     'w2p - 25%', 'w2p - 75%', 'worst - median', 'worst - 25%', 'worst - 75%'])

    # Hydrogen producers
    tmpHPRef = dfHPRef.set_index(['Year', 'Run', 'ID'])
    tmpHPStrat = dfHPStrat.set_index(['Year', 'Run', 'ID'])
    tmpHPW2P = dfHPW2P.set_index(['Year', 'Run', 'ID'])
    tmpHPWorst = dfHPWorst.set_index(['Year', 'Run', 'ID'])
    dfPlotHP = pd.DataFrame(data=np.nan, index=range(yearDelta),
                            columns=['ref - median', 'strat - median', 'strat - 25%', 'strat - 75%', 'w2p - median',
                                     'w2p - 25%', 'w2p - 75%', 'worst - median', 'worst - 25%', 'worst - 75%'])

    # Electrolyzer producers
    tmpEPRef = dfEPRef.set_index(['Year', 'Run', 'ID'])
    tmpEPStrat = dfEPStrat.set_index(['Year', 'Run', 'ID'])
    tmpEPW2P = dfEPW2P.set_index(['Year', 'Run', 'ID'])
    tmpEPWorst = dfEPWorst.set_index(['Year', 'Run', 'ID'])
    dfPlotEP = pd.DataFrame(data=np.nan, index=range(yearDelta),
                            columns=['ref - median', 'strat - median', 'strat - 25%', 'strat - 75%', 'w2p - median',
                                     'w2p - 25%', 'w2p - 75%', 'worst - median', 'worst - 25%', 'worst - 75%'])

    for i in range(yearDelta):
        # Power producers
        # Reference case
        if i in tmpPPRef.index.levels[0]:
            tmpDf = tmpPPRef.loc[i]['Return on Investment']
            dfPlotPP.loc[i, 'ref - median'] = tmpDf.median()*100
        # Strategic case
        if i in tmpPPStrat.index.levels[0]:
            tmpDf = tmpPPStrat.loc[i]['Return on Investment']
            dfPlotPP.loc[i, 'strat - median'] = tmpDf.median()*100
            dfPlotPP.loc[i, 'strat - 25%'] = tmpDf.quantile(q=0.25)*100
            dfPlotPP.loc[i, 'strat - 75%'] = tmpDf.quantile(q=0.75)*100
        # Willingness to pay case
        if i in tmpPPW2P.index.levels[0]:
            tmpDf = tmpPPW2P.loc[i]['Return on Investment']
            dfPlotPP.loc[i, 'w2p - median'] = tmpDf.median()*100
            dfPlotPP.loc[i, 'w2p - 25%'] = tmpDf.quantile(q=0.25)*100
            dfPlotPP.loc[i, 'w2p - 75%'] = tmpDf.quantile(q=0.75)*100
        # Worst case
        if i in tmpPPWorst.index.levels[0]:
            tmpDf = tmpPPWorst.loc[i]['Return on Investment']
            dfPlotPP.loc[i, 'worst - median'] = tmpDf.median()*100
            dfPlotPP.loc[i, 'worst - 25%'] = tmpDf.quantile(q=0.25)*100
            dfPlotPP.loc[i, 'worst - 75%'] = tmpDf.quantile(q=0.75)*100

        # Hydrogen producers
        # Reference case
        if i in tmpHPRef.index.levels[0]:
            tmpDf = tmpHPRef.loc[i]['Return on Investment']
            dfPlotHP.loc[i, 'ref - median'] = tmpDf.median()*100
        # Strategic case
        if i in tmpHPStrat.index.levels[0]:
            tmpDf = tmpHPStrat.loc[i]['Return on Investment']
            dfPlotHP.loc[i, 'strat - median'] = tmpDf.median()*100
            dfPlotHP.loc[i, 'strat - 25%'] = tmpDf.quantile(q=0.25)*100
            dfPlotHP.loc[i, 'strat - 75%'] = tmpDf.quantile(q=0.75)*100
        # Willingness to pay case
        if i in tmpHPW2P.index.levels[0]:
            tmpDf = tmpHPW2P.loc[i]['Return on Investment']
            dfPlotHP.loc[i, 'w2p - median'] = tmpDf.median()*100
            dfPlotHP.loc[i, 'w2p - 25%'] = tmpDf.quantile(q=0.25)*100
            dfPlotHP.loc[i, 'w2p - 75%'] = tmpDf.quantile(q=0.75)*100
        # Worst case
        if i in tmpHPWorst.index.levels[0]:
            tmpDf = tmpHPWorst.loc[i]['Return on Investment']
            dfPlotHP.loc[i, 'worst - median'] = tmpDf.median()*100
            dfPlotHP.loc[i, 'worst - 25%'] = tmpDf.quantile(q=0.25)*100
            dfPlotHP.loc[i, 'worst - 75%'] = tmpDf.quantile(q=0.75)*100

        # Electrolyzer producers
        # Reference case
        if i in tmpEPRef.index.levels[0]:
            tmpDf = tmpEPRef.loc[i]['Return on Investment']
            dfPlotEP.loc[i, 'ref - median'] = tmpDf.median()*100
        # Strategic case
        if i in tmpEPStrat.index.levels[0]:
            tmpDf = tmpEPStrat.loc[i]['Return on Investment']
            dfPlotEP.loc[i, 'strat - median'] = tmpDf.median()*100
            dfPlotEP.loc[i, 'strat - 25%'] = tmpDf.quantile(q=0.25)*100
            dfPlotEP.loc[i, 'strat - 75%'] = tmpDf.quantile(q=0.75)*100
        # Willingness to pay case
        if i in tmpEPW2P.index.levels[0]:
            tmpDf = tmpEPW2P.loc[i]['Return on Investment']
            dfPlotEP.loc[i, 'w2p - median'] = tmpDf.median()*100
            dfPlotEP.loc[i, 'w2p - 25%'] = tmpDf.quantile(q=0.25)*100
            dfPlotEP.loc[i, 'w2p - 75%'] = tmpDf.quantile(q=0.75)*100
        # Worst case
        if i in tmpEPWorst.index.levels[0]:
            tmpDf = tmpEPWorst.loc[i]['Return on Investment']
            dfPlotEP.loc[i, 'worst - median'] = tmpDf.median()*100
            dfPlotEP.loc[i, 'worst - 25%'] = tmpDf.quantile(q=0.25)*100
            dfPlotEP.loc[i, 'worst - 75%'] = tmpDf.quantile(q=0.75)*100

    # Figure
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=plotSettings['figsize_3t'],
                                        gridspec_kw=plotSettings['gridspec_kw'], dpi=plotSettings['dpi'], sharex=True)

    # Power producers
    ax1.plot(x, dfPlotPP['ref - median'], label='Power producers - best case', linestyle='-', color=green)
    ax1.plot(x, dfPlotPP['strat - median'], label='Power producers - non-strategic', linestyle=StratLinestyle,
             color=darkgreen)
    ax1.fill_between(x, dfPlotPP['strat - 25%'], dfPlotPP['strat - 75%'], color=darkgreen, alpha=0.1, edgecolor=None,
                     hatch=StratHatch)
    ax1.plot(x, dfPlotPP['w2p - median'], label='Power producers - grey hydrogen', linestyle=W2PLinestlye,
             color=darkgreen)
    ax1.fill_between(x, dfPlotPP['w2p - 25%'], dfPlotPP['w2p - 75%'], color=darkgreen, alpha=0.1, edgecolor=None,
                     hatch=W2PHatch)
    ax1.plot(x, dfPlotPP['worst - median'], label='Power producers - worst case', linestyle=WorstLinestyle,
             color=darkgreen)
    ax1.fill_between(x, dfPlotPP['worst - 25%'], dfPlotPP['worst - 75%'], color=darkgreen, alpha=0.1, edgecolor=None,
                     hatch=WorstHatch)

    # Hydrogen producers
    ax2.plot(x, dfPlotHP['ref - median'], label='Hydrogen producers - best case', linestyle='-', color=blue)
    ax2.plot(x, dfPlotHP['strat - median'], label='Hydrogen producers - non-strategic', linestyle=StratLinestyle,
             color=darkblue)
    ax2.fill_between(x, dfPlotHP['strat - 25%'], dfPlotHP['strat - 75%'], color=darkblue, alpha=0.1, edgecolor=None,
                     hatch=StratHatch)
    ax2.plot(x, dfPlotHP['w2p - median'], label='Hydrogen producers - grey hydrogen', linestyle=W2PLinestlye,
             color=darkblue)
    ax2.fill_between(x, dfPlotHP['w2p - 25%'], dfPlotHP['w2p - 75%'], color=darkblue, alpha=0.1, edgecolor=None,
                     hatch=W2PHatch)
    ax2.plot(x, dfPlotHP['worst - median'], label='Hydrogen producers - worst case', linestyle=WorstLinestyle,
             color=darkblue)
    ax2.fill_between(x, dfPlotHP['worst - 25%'], dfPlotHP['worst - 75%'], color=darkblue, alpha=0.1, edgecolor=None,
                     hatch=WorstHatch)

    # Electrolyzer producers
    ax3.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    ax3.plot(x, dfPlotEP['ref - median'], label='Electrolyzer producers - worst case', linestyle='-', color=purple)
    ax3.plot(x, dfPlotEP['strat - median'], label='Electrolyzer producers - non-strategic', linestyle=StratLinestyle,
             color=darkpurple)
    ax3.fill_between(x, dfPlotEP['strat - 25%'], dfPlotEP['strat - 75%'], color=darkpurple, alpha=0.1, edgecolor=None,
                     hatch=StratHatch)
    ax3.plot(x, dfPlotEP['w2p - median'], label='Electrolyzer producers - grey hydrogen', linestyle=W2PLinestlye,
             color=darkpurple)
    ax3.fill_between(x, dfPlotEP['w2p - 25%'], dfPlotEP['w2p - 75%'], color=darkpurple, alpha=0.1, edgecolor=None,
                     hatch=W2PHatch)
    ax3.plot(x, dfPlotEP['worst - median'], label='Electrolyzer producers - worst case', linestyle=WorstLinestyle,
             color=darkpurple)
    ax3.fill_between(x, dfPlotEP['worst - 25%'], dfPlotEP['worst - 75%'], color=darkpurple, alpha=0.1, edgecolor=None,
                     hatch=WorstHatch)

    fig.text(-0.1, 0.5, 'Return on Investment [%]', va='center', rotation='vertical', fontsize=plotSettings['fontsize'])

    plt.xlim(plotSettings['xlim'])

    # Adjust ticks
    ax1.minorticks_on()
    ax2.minorticks_on()
    ax3.minorticks_on()
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(5))
    ax1.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax1.tick_params(which='minor', axis='both', color='gray')
    ax2.yaxis.set_minor_locator(MultipleLocator(5))
    ax2.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax2.tick_params(which='minor', axis='both', color='gray')
    ax3.yaxis.set_minor_locator(MultipleLocator(5))
    ax3.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax3.tick_params(which='minor', axis='both', color='gray')

    # Legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles3, labels3 = ax3.get_legend_handles_labels()

    handles = handles1 + handles2 + handles3
    labels = labels1 + labels2 + labels3

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.8),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save figure
    plt.savefig(os.getcwd() + '\\figure21.' + plotType, bbox_inches='tight')

    # Write data
    writeDf = pd.DataFrame(data=[dfPlotPP['ref - median'],
                                 dfPlotPP['strat - median'], dfPlotPP['strat - 25%'], dfPlotPP['strat - 75%'],
                                 dfPlotPP['w2p - median'], dfPlotPP['w2p - 25%'], dfPlotPP['w2p - 75%'],
                                 dfPlotPP['worst - median'], dfPlotPP['worst - 25%'], dfPlotPP['worst - 75%'],
                                 dfPlotHP['ref - median'],
                                 dfPlotHP['strat - median'], dfPlotHP['strat - 25%'], dfPlotHP['strat - 75%'],
                                 dfPlotHP['w2p - median'], dfPlotHP['w2p - 25%'], dfPlotHP['w2p - 75%'],
                                 dfPlotHP['worst - median'], dfPlotHP['worst - 25%'], dfPlotHP['worst - 75%'],
                                 dfPlotEP['ref - median'],
                                 dfPlotEP['strat - median'], dfPlotEP['strat - 25%'], dfPlotEP['strat - 75%'],
                                 dfPlotEP['w2p - median'], dfPlotEP['w2p - 25%'], dfPlotEP['w2p - 75%'],
                                 dfPlotEP['worst - median'], dfPlotEP['worst - 25%'], dfPlotEP['worst - 75%']],
                           index=['ROI PP reference - median [%]',
                                  'ROI PP strategic - median [%]', 'ROI PP strategic - 25% [%]', 'ROI PP strategic - 75% [%]',
                                  'ROI PP W2P - median [%]', 'ROI PP W2P - 25% [%]', 'ROI PP W2P - 75% [%]',
                                  'ROI PP worst - median [%]', 'ROI PP worst - 25% [%]', 'ROI PP worst - 75% [%]',
                                  'ROI HP reference - median [%]',
                                  'ROI HP strategic - median [%]', 'ROI HP strategic - 25% [%]', 'ROI HP strategic - 75% [%]',
                                  'ROI HP W2P - median [%]', 'ROI HP W2P - 25% [%]', 'ROI HP W2P - 75% [%]',
                                  'ROI HP worst - median [%]', 'ROI HP worst - 25% [%]', 'ROI HP worst - 75% [%]',
                                  'ROI EP reference - median [%]',
                                  'ROI EP strategic - median [%]', 'ROI EP strategic - 25% [%]', 'ROI EP strategic - 75% [%]',
                                  'ROI EP W2P - median [%]', 'ROI EP W2P - 25% [%]', 'ROI EP W2P - 75% [%]',
                                  'ROI EP worst - median [%]', 'ROI EP worst - 25% [%]', 'ROI EP worst - 75% [%]'])
    writeDf = writeDf.T
    #writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure21.csv', sep=';')


def figure_22(dfPMRef, dfPMStrat, dfPMW2P, dfPMWorst, dfHMRef, dfHMStrat, dfHMW2P, dfHMWorst):
    '''
    Function that will create Fig. 22 - Weighted electricity and hydrogen price in the obstacle cases.
    :param:
        pd.DataFrame dfPMRef: Yearly data from the power market for the reference case.
        pd.DataFrame dfPMStrat: Yearly data from the power market for the strategic case.
        pd.DataFrame dfPMW2P: Yearly data from the power market for the willingness to pay case.
        pd.DataFrame dfPMWorst: Yearly data from the power market for the worst case.
        pd.DataFrame dfHMRef: Yearly data from the hydrogen market for the reference case.
        pd.DataFrame dfHMStrat: Yearly data from the hydrogen market for the strategic case.
        pd.DataFrame dfHMW2P: Yearly data from the hydrogen market for the willingness to pay case.
        pd.DataFrame dfHMWorst: Yearly data from the hydrogen market for the worst case.
    :return:
    '''
    # Power market
    tmpPMRef = dfPMRef.set_index(['Year', 'Run'])
    tmpPMStrat = dfPMStrat.set_index(['Year', 'Run'])
    tmpPMW2P = dfPMW2P.set_index(['Year', 'Run'])
    tmpPMWorst = dfPMWorst.set_index(['Year', 'Run'])
    dfPlotPM = pd.DataFrame(data=np.nan, index=range(yearDelta),
                            columns=['ref - median', 'strat - median', 'strat - 25%', 'strat - 75%', 'w2p - median',
                                     'w2p - 25%', 'w2p - 75%', 'worst - median', 'worst - 25%', 'worst - 75%'])
    # Hydrogen market
    tmpHMRef = dfHMRef.set_index(['Year', 'Run'])
    tmpHMStrat = dfHMStrat.set_index(['Year', 'Run'])
    tmpHMW2P = dfHMW2P.set_index(['Year', 'Run'])
    tmpHMWorst = dfHMWorst.set_index(['Year', 'Run'])
    dfPlotHM = pd.DataFrame(data=np.nan, index=range(yearDelta),
                            columns=['ref - median', 'strat - median', 'strat - 25%', 'strat - 75%', 'w2p - median',
                                     'w2p - 25%', 'w2p - 75%', 'worst - median', 'worst - 25%', 'worst - 75%'])

    for i in range(yearDelta):
        # Electricity price
        # Reference case
        if i in tmpPMRef.index.levels[0]:
            tmpDf = tmpPMRef.loc[i]['Weighted Price Electricity']
            dfPlotPM.loc[i, 'ref - median'] = tmpDf.median()
        # Strategic case
        if i in tmpPMStrat.index.levels[0]:
            tmpDf = tmpPMStrat.loc[i]['Weighted Price Electricity']
            dfPlotPM.loc[i, 'strat - median'] = tmpDf.median()
            dfPlotPM.loc[i, 'strat - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotPM.loc[i, 'strat - 75%'] = tmpDf.quantile(q=0.75)
        # Willingness to pay case
        if i in tmpPMW2P.index.levels[0]:
            tmpDf = tmpPMW2P.loc[i]['Weighted Price Electricity']
            dfPlotPM.loc[i, 'w2p - median'] = tmpDf.median()
            dfPlotPM.loc[i, 'w2p - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotPM.loc[i, 'w2p - 75%'] = tmpDf.quantile(q=0.75)
        # Worst case
        if i in tmpPMWorst.index.levels[0]:
            tmpDf = tmpPMWorst.loc[i]['Weighted Price Electricity']
            dfPlotPM.loc[i, 'worst - median'] = tmpDf.median()
            dfPlotPM.loc[i, 'worst - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotPM.loc[i, 'worst - 75%'] = tmpDf.quantile(q=0.75)

        # Hydrogen price
        # Reference case
        if i in tmpHMRef.index.levels[0]:
            tmpDf = tmpHMRef.loc[i]['Price Hydrogen']
            dfPlotHM.loc[i, 'ref - median'] = tmpDf.median()
        # Strategic case
        if i in tmpHMStrat.index.levels[0]:
            tmpDf = tmpHMStrat.loc[i]['Price Hydrogen']
            dfPlotHM.loc[i, 'strat - median'] = tmpDf.median()
            dfPlotHM.loc[i, 'strat - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotHM.loc[i, 'strat - 75%'] = tmpDf.quantile(q=0.75)
        # Willingness to pay case
        if i in tmpHMW2P.index.levels[0]:
            tmpDf = tmpHMW2P.loc[i]['Price Hydrogen']
            dfPlotHM.loc[i, 'w2p - median'] = tmpDf.median()
            dfPlotHM.loc[i, 'w2p - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotHM.loc[i, 'w2p - 75%'] = tmpDf.quantile(q=0.75)
        # Worst case
        if i in tmpHMWorst.index.levels[0]:
            tmpDf = tmpHMWorst.loc[i]['Price Hydrogen']
            dfPlotHM.loc[i, 'worst - median'] = tmpDf.median()
            dfPlotHM.loc[i, 'worst - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotHM.loc[i, 'worst - 75%'] = tmpDf.quantile(q=0.75)

    # Figure
    fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                            dpi=plotSettings['dpi'])

    # Electricity price
    ax1.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    ax1.set_ylabel('Price [€/MWh]', fontsize=plotSettings['fontsize'])
    ax1.plot(x, dfPlotPM['ref - median'], label='Electricity - best case', linestyle='-', color=green)
    ax1.plot(x, dfPlotPM['strat - median'], label='Electricity - non-strategic', linestyle=StratLinestyle,
             color=darkgreen)
    ax1.fill_between(x, dfPlotPM['strat - 25%'], dfPlotPM['strat - 75%'], color=darkgreen, alpha=0.1, edgecolor=None,
                     hatch=StratHatch)
    ax1.plot(x, dfPlotPM['w2p - median'], label='Electricity - grey hydrogen', linestyle=W2PLinestlye, color=darkgreen)
    ax1.fill_between(x, dfPlotPM['w2p - 25%'], dfPlotPM['w2p - 75%'], color=darkgreen, alpha=0.1, edgecolor=None,
                     hatch=W2PHatch)
    ax1.plot(x, dfPlotPM['worst - median'], label='Electricity - worst case', linestyle=WorstLinestyle, color=darkgreen)
    ax1.fill_between(x, dfPlotPM['worst - 25%'], dfPlotPM['worst - 75%'], color=darkgreen, alpha=0.1, edgecolor=None,
                     hatch=WorstHatch)

    # Hydrogen price
    # In €/MWh
    ax1.plot(x, dfPlotHM['ref - median'], label='Hydrogen - best case', linestyle='-', color=blue)
    ax1.plot(x, dfPlotHM['strat - median'], label='Hydrogen - non-strategic', linestyle=StratLinestyle, color=darkblue)
    ax1.fill_between(x, dfPlotHM['strat - 25%'], dfPlotHM['strat - 75%'], color=darkblue, alpha=0.1, edgecolor=None,
                     hatch=StratHatch)
    ax1.plot(x, dfPlotHM['w2p - median'], label='Hydrogen - grey hydrogen', linestyle=W2PLinestlye, color=darkblue)
    ax1.fill_between(x, dfPlotHM['w2p - 25%'], dfPlotHM['w2p - 75%'], color=darkblue, alpha=0.1, edgecolor=None,
                     hatch=W2PHatch)
    ax1.plot(x, dfPlotHM['worst - median'], label='Hydrogen - worst case', linestyle=WorstLinestyle, color=darkblue)
    ax1.fill_between(x, dfPlotHM['worst - 25%'], dfPlotHM['worst - 75%'], color=darkblue, alpha=0.1, edgecolor=None,
                     hatch=WorstHatch)

    # In €/kg
    ax2 = ax1.twinx()
    ax2.set_ylabel('Price [€/kg]', fontsize=plotSettings['fontsize'])
    ax2.plot(x, dfPlotHM['ref - median']*33.3/1e3, linestyle='-', color=blue)

    # Adjust axis
    ax1.minorticks_on()
    ax1.set_xlim(plotSettings['xlim'])
    ax1.set_ylim([0, 275])
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(25))
    ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax1.tick_params(axis='both', which='minor', color='gray')

    ax2.minorticks_on()
    ax2.set_xlim(plotSettings['xlim'])
    ax2.set_ylim([0, 275*33.3/1e3])
    ax2.set_xticks(plotSettings['xticks'])
    ax2.xaxis.set_minor_locator(MultipleLocator(5))
    ax2.yaxis.set_minor_locator(MultipleLocator(1))
    ax2.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax2.tick_params(axis='both', which='minor', color='gray')

    # Adjust legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    handles = handles1 + handles2
    labels = labels1 + labels2

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.6),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save plot
    plt.savefig(os.getcwd() + '\\figure22.' + plotType, bbox_inches='tight')

    # Write data
    writeDf = pd.DataFrame(data=[dfPlotPM['ref - median'], dfPlotPM['strat - median'], dfPlotPM['strat - 25%'],
                                 dfPlotPM['strat - 75%'], dfPlotPM['w2p - median'], dfPlotPM['w2p - 25%'],
                                 dfPlotPM['w2p - 75%'], dfPlotPM['worst - median'], dfPlotPM['worst - 25%'],
                                 dfPlotPM['worst - 75%'], dfPlotHM['ref - median'], dfPlotHM['strat - median'],
                                 dfPlotHM['strat - 25%'], dfPlotHM['strat - 75%'], dfPlotHM['w2p - median'],
                                 dfPlotHM['w2p - 25%'], dfPlotHM['w2p - 75%'], dfPlotHM['worst - median'],
                                 dfPlotHM['worst - 25%'], dfPlotHM['worst - 75%'], dfPlotHM['ref - median']*33.3/1e3,
                                 dfPlotHM['strat - median']*33.3/1e3, dfPlotHM['strat - 25%']*33.3/1e3,
                                 dfPlotHM['strat - 75%']*33.3/1e3, dfPlotHM['w2p - median']*33.3/1e3,
                                 dfPlotHM['w2p - 25%']*33.3/1e3, dfPlotHM['w2p - 75%']*33.3/1e3,
                                 dfPlotHM['worst - median']*33.3/1e3, dfPlotHM['worst - 25%']*33.3/1e3,
                                 dfPlotHM['worst - 75%']*33.3/1e3],
                           index=['Weighted electricity price reference - median [€/MWh]',
                                  'Weighted electricity price strategic - median [€/MWh]',
                                  'Weighted electricity price strategic - 25% [€/MWh]',
                                  'Weighted electricity price strategic - 75% [€/MWh]',
                                  'Weighted electricity price W2P - median [€/MWh]',
                                  'Weighted electricity price W2P - 25% [€/MWh]',
                                  'Weighted electricity price W2P - 75% [€/MWh]',
                                  'Weighted electricity price worst - median [€/MWh]',
                                  'Weighted electricity price worst - 25% [€/MWh]',
                                  'Weighted electricity price worst - 75% [€/MWh]',
                                  'Hydrogen price reference - median [€/MWh]',
                                  'Hydrogen price strategic - median [€/MWh]', 'Hydrogen price reference - 25% [€/MWh]',
                                  'Hydrogen price reference - 75% [€/MWh]', 'Hydrogen price W2P - median [€/MWh]',
                                  'Hydrogen price W2P - 25% [€/MWh]', 'Hydrogen price W2P - 75% [€/MWh]',
                                  'Hydrogen price worst - median [€/MWh]', 'Hydrogen price worst - 25% [€/MWh]',
                                  'Hydrogen price worst - 75% [€/MWh]',
                                  'Hydrogen price reference - median [€/kg]',
                                  'Hydrogen price strategic - median [€/kg]', 'Hydrogen price reference - 25% [€/kg]',
                                  'Hydrogen price reference - 75% [€/kg]', 'Hydrogen price W2P - median [€/kg]',
                                  'Hydrogen price W2P - 25% [€/kg]', 'Hydrogen price W2P - 75% [€/kg]',
                                  'Hydrogen price worst - median [€/kg]',
                                  'Hydrogen price worst - 25% [€/kg]', 'Hydrogen price worst - 75% [€/kg]',
                                  ])
    writeDf = writeDf.T
    writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure22.csv', sep=';')


def figure_23(dfEPRef, dfEPStrat, dfEPW2P, dfEPWorst):
    '''
    Function that will create Fig. 23 - Minimal electrolyzer production costs obstracle cases.
    :param:
        pd.DataFrame dfEPRef: Yearly data from the electrolyzer producers for the reference case.
        pd.DataFrame dfEPStrat: Yearly data from the electrolyzer producers for the strategic case.
        pd.DataFrame dfEPW2P: Yearly data from the electrolyzer producers for the willingness to pay case.
        pd.DataFrame dfEPWorst: Yearly data from the electrolyzer producers for the worst case.
    :return:
    '''
    # Electrolyzer producers
    tmpEPRef = dfEPRef.set_index(['Year', 'Run', 'ID'])
    tmpEPStrat = dfEPStrat.set_index(['Year', 'Run', 'ID'])
    tmpEPW2P = dfEPW2P.set_index(['Year', 'Run', 'ID'])
    tmpEPWorst = dfEPWorst.set_index(['Year', 'Run', 'ID'])
    dfPlotEP = pd.DataFrame(data=np.nan, index=range(yearDelta),
                            columns=['ref - median', 'strat - median', 'strat - 25%', 'strat - 75%', 'w2p - median',
                                     'w2p - 25%', 'w2p - 75%', 'worst - median', 'worst - 25%', 'worst - 75%'])

    for i in range(yearDelta):
        # Electrolyzer producers
        # Reference case
        if i in tmpEPRef.index.levels[0]:
            tmpDf = tmpEPRef.loc[i]['Minimal costs Electrolyzers'].groupby(level=0).min()
            dfPlotEP.loc[i, 'ref - median'] = tmpDf.median()/1e3
        # Strategic case
        if i in tmpEPStrat.index.levels[0]:
            tmpDf = tmpEPStrat.loc[i]['Minimal costs Electrolyzers'].groupby(level=0).min()
            dfPlotEP.loc[i, 'strat - median'] = tmpDf.median()/1e3
            dfPlotEP.loc[i, 'strat - 25%'] = tmpDf.quantile(q=0.25)/1e3
            dfPlotEP.loc[i, 'strat - 75%'] = tmpDf.quantile(q=0.75)/1e3
        # Willingness to pay case
        if i in tmpEPW2P.index.levels[0]:
            tmpDf = tmpEPW2P.loc[i]['Minimal costs Electrolyzers'].groupby(level=0).min()
            dfPlotEP.loc[i, 'w2p - median'] = tmpDf.median()/1e3
            dfPlotEP.loc[i, 'w2p - 25%'] = tmpDf.quantile(q=0.25)/1e3
            dfPlotEP.loc[i, 'w2p - 75%'] = tmpDf.quantile(q=0.75)/1e3
        # Worst case
        if i in tmpEPWorst.index.levels[0]:
            tmpDf = tmpEPWorst.loc[i]['Minimal costs Electrolyzers'].groupby(level=0).min()
            dfPlotEP.loc[i, 'worst - median'] = tmpDf.median()/1e3
            dfPlotEP.loc[i, 'worst - 25%'] = tmpDf.quantile(q=0.25)/1e3
            dfPlotEP.loc[i, 'worst - 75%'] = tmpDf.quantile(q=0.75)/1e3

    # Figure
    fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                            dpi=plotSettings['dpi'])

    # Electrolyzer cost
    ax1.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    ax1.set_ylabel('Production costs [€/kW]', fontsize=plotSettings['fontsize'])
    ax1.plot(x, dfPlotEP['ref - median'], label='Electrolyzer - best case', linestyle='-', color=purple)
    ax1.plot(x, dfPlotEP['strat - median'], label='Electrolyzer - non-strategic', linestyle=StratLinestyle,
             color=darkpurple)
    ax1.fill_between(x, dfPlotEP['strat - 25%'], dfPlotEP['strat - 75%'], color=darkpurple, alpha=0.1, edgecolor=None,
                     hatch=StratHatch)
    ax1.plot(x, dfPlotEP['w2p - median'], label='Electrolyzer - grey hydrogen', linestyle=W2PLinestlye, color=darkpurple)
    ax1.fill_between(x, dfPlotEP['w2p - 25%'], dfPlotEP['w2p - 75%'], color=darkpurple, alpha=0.1, edgecolor=None,
                     hatch=W2PHatch)
    ax1.plot(x, dfPlotEP['worst - median'], label='Electrolyzer - worst case', linestyle=WorstLinestyle, color=darkpurple)
    ax1.fill_between(x, dfPlotEP['worst - 25%'], dfPlotEP['worst - 75%'], color=darkpurple, alpha=0.1, edgecolor=None,
                     hatch=WorstHatch)

    # Adjust axis
    ax1.minorticks_on()
    ax1.set_xlim(plotSettings['xlim'])
    ax1.set_ylim(0)
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(500))
    ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax1.tick_params(axis='both', which='minor', color='gray')

    # Adjust legend
    handles1, labels1 = ax1.get_legend_handles_labels()

    handles = handles1
    labels = labels1

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.55),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save plot
    plt.savefig(os.getcwd() + '\\figure23.' + plotType, bbox_inches='tight')

    # Write data
    writeDf = pd.DataFrame(data=[dfPlotEP['ref - median'], dfPlotEP['strat - median'], dfPlotEP['strat - 25%'],
                                 dfPlotEP['strat - 75%'], dfPlotEP['w2p - median'], dfPlotEP['w2p - 25%'],
                                 dfPlotEP['w2p - 75%'], dfPlotEP['worst - median'], dfPlotEP['worst - 25%'],
                                 dfPlotEP['worst - 75%']],
                           index=['Min. Electrolyzer costs reference - median [€/kw]',
                                  'Min. Electrolyzer costs strategic - median [€/kw]',
                                  'Min. Electrolyzer costs strategic - 25% [€/kw]',
                                  'Min. Electrolyzer costs strategic - 75% [€/kw]',
                                  'Min. Electrolyzer costs W2P - median [€/kw]',
                                  'Min. Electrolyzer costs W2P - 25% [€/kw]',
                                  'Min. Electrolyzer costs W2P - 75% [€/kw]',
                                  'Min. Electrolyzer costs worst - median [€/kw]',
                                  'Min. Electrolyzer costs worst - 25% [€/kw]',
                                  'Min. Electrolyzer costs worst - 75% [€/kw]'])
    writeDf = writeDf.T
    writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure23.csv', sep=';')


def figure_24(dfPMRef, dfPMStrat, dfPMW2P, dfPMWorst, dfHMRef, dfHMStrat, dfHMW2P, dfHMWorst, dfEMRef, dfEMStrat,
              dfEMW2P, dfEMWorst):
    '''
    Function that will create Fig. 24 - Invested money over time in the obstacle case.
    :param:
        pd.DataFrame dfPMRef: Yearly data from the power market for the reference case.
        pd.DataFrame dfPMStrat: Yearly data from the power market for the strategic case.
        pd.DataFrame dfPMW2P: Yearly data from the power market for the willingness to pay case.
        pd.DataFrame dfPMWorst: Yearly data from the power market for the worst case.
        pd.DataFrame dfHMRef: Yearly data from the electrolyzer sales for the reference case.
        pd.DataFrame dfHMStrat: Yearly data from the electrolyzer sales for the strategic case.
        pd.DataFrame dfHMW2P: Yearly data from the electrolyzer sales for the willingness to pay case.
        pd.DataFrame dfHMWorst: Yearly data from the electrolyzer sales for the worst case.
        pd.DataFrame dfEMRef: Yearly data from the electrolyzer market for the reference case.
        pd.DataFrame dfEMStrat: Yearly data from the electrolyzer market for the strategic case.
        pd.DataFrame dfEMW2P: Yearly data from the electrolyzer market for the willingness to pay case.
        pd.DataFrame dfEMWorst: Yearly data from the electrolyzer market for the worst case.
    :return:
    '''
    # Fixed values
    tmpInvestRES = 1250000.
    tmpInvestFAC = 500000.

    # Power market
    tmpPMRef = dfPMRef.set_index(['Year', 'Run'])
    tmpPMStrat = dfPMStrat.set_index(['Year', 'Run'])
    tmpPMW2P = dfPMW2P.set_index(['Year', 'Run'])
    tmpPMWorst = dfPMWorst.set_index(['Year', 'Run'])
    dfPlotPM = pd.DataFrame(data=np.nan, index=range(yearDelta),
                            columns=['ref - median', 'ref cum - median', 'strat - median', 'strat - 25%', 'strat - 75%',
                                     'strat cum - median', 'strat cum - 25%', 'strat cum - 75%', 'w2p - median',
                                     'w2p - 25%', 'w2p - 75%', 'w2p cum - median', 'w2p cum - 25%', 'w2p cum - 75%',
                                     'worst - median', 'worst - 25%', 'worst - 75%', 'worst cum - median',
                                     'worst cum - 25%', 'worst cum - 75%'])
    tmpPMRefCum = pd.Series(data=0, index=tmpPMRef.loc[0].index)
    tmpPMStratCum = pd.Series(data=0, index=tmpPMStrat.loc[0].index)
    tmpPMW2PCum = pd.Series(data=0, index=tmpPMW2P.loc[0].index)
    tmpPMWorstCum = pd.Series(data=0, index=tmpPMWorst.loc[0].index)

    # Hydrogen market
    tmpHMRef = dfHMRef.set_index(['Year', 'Run'])
    tmpHMStrat = dfHMStrat.set_index(['Year', 'Run'])
    tmpHMW2P = dfHMW2P.set_index(['Year', 'Run'])
    tmpHMWorst = dfHMWorst.set_index(['Year', 'Run'])
    dfPlotHM = pd.DataFrame(data=np.nan, index=range(yearDelta),
                            columns=['ref - median', 'ref cum - median', 'strat - median', 'strat - 25%', 'strat - 75%',
                                     'strat cum - median', 'strat cum - 25%', 'strat cum - 75%', 'w2p - median',
                                     'w2p - 25%', 'w2p - 75%', 'w2p cum - median', 'w2p cum - 25%', 'w2p cum - 75%',
                                     'worst - median', 'worst - 25%', 'worst - 75%', 'worst cum - median',
                                     'worst cum - 25%', 'worst cum - 75%'])
    tmpHMRefCum = pd.Series(data=0, index=tmpPMRef.loc[0].index)
    tmpHMStratCum = pd.Series(data=0, index=tmpPMStrat.loc[0].index)
    tmpHMW2PCum = pd.Series(data=0, index=tmpPMW2P.loc[0].index)
    tmpHMWorstCum = pd.Series(data=0, index=tmpPMWorst.loc[0].index)

    # Electrolyzer market
    tmpEMRef = dfEMRef.set_index(['Year', 'Run'])
    tmpEMStrat = dfEMStrat.set_index(['Year', 'Run'])
    tmpEMW2P = dfEMW2P.set_index(['Year', 'Run'])
    tmpEMWorst = dfEMWorst.set_index(['Year', 'Run'])
    dfPlotEM = pd.DataFrame(data=np.nan, index=range(yearDelta),
                            columns=['ref - median', 'ref cum - median', 'strat - median', 'strat - 25%', 'strat - 75%',
                                     'strat cum - median', 'strat cum - 25%', 'strat cum - 75%', 'w2p - median',
                                     'w2p - 25%', 'w2p - 75%', 'w2p cum - median', 'w2p cum - 25%', 'w2p cum - 75%',
                                     'worst - median', 'worst - 25%', 'worst - 75%', 'worst cum - median',
                                     'worst cum - 25%', 'worst cum - 75%'])
    tmpEMRefCum = pd.Series(data=0, index=tmpEMRef.loc[0].index)
    tmpEMStratCum = pd.Series(data=0, index=tmpEMStrat.loc[0].index)
    tmpEMW2PCum = pd.Series(data=0, index=tmpEMW2P.loc[0].index)
    tmpEMWorstCum = pd.Series(data=0, index=tmpEMWorst.loc[0].index)

    for i in range(yearDelta):
        # Power market
        # Reference case
        if i in tmpPMRef.index.levels[0]:
            # Per year
            tmpDf = tmpPMRef.loc[i]['Added capacity Renewables'] * tmpInvestRES / 1e9
            dfPlotPM.loc[i, 'ref - median'] = tmpDf.median()
            # Cumulative
            tmpPMRefCum = tmpPMRefCum + tmpDf
            dfPlotPM.loc[i, 'ref cum - median'] = tmpPMRefCum.median()
        # Strategic case
        if i in tmpPMStrat.index.levels[0]:
            # Per year
            tmpDf = tmpPMStrat.loc[i]['Added capacity Renewables'] * tmpInvestRES / 1e9
            dfPlotPM.loc[i, 'strat - median'] = tmpDf.median()
            dfPlotPM.loc[i, 'strat - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotPM.loc[i, 'strat - 75%'] = tmpDf.quantile(q=0.75)
            # Cumulative
            tmpPMStratCum = tmpPMStratCum + tmpDf
        dfPlotPM.loc[i, 'strat cum - median'] = tmpPMStratCum.median()
        dfPlotPM.loc[i, 'strat cum - 25%'] = tmpPMStratCum.quantile(q=0.25)
        dfPlotPM.loc[i, 'strat cum - 75%'] = tmpPMStratCum.quantile(q=0.75)
        # Willingness to pay case
        if i in tmpPMW2P.index.levels[0]:
            # Per year
            tmpDf = tmpPMW2P.loc[i]['Added capacity Renewables'] * tmpInvestRES / 1e9
            dfPlotPM.loc[i, 'w2p - median'] = tmpDf.median()
            dfPlotPM.loc[i, 'w2p - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotPM.loc[i, 'w2p - 75%'] = tmpDf.quantile(q=0.75)
            # Cumulative
            tmpPMW2PCum = tmpPMW2PCum + tmpDf
        dfPlotPM.loc[i, 'w2p cum - median'] = tmpPMW2PCum.median()
        dfPlotPM.loc[i, 'w2p cum - 25%'] = tmpPMW2PCum.quantile(q=0.25)
        dfPlotPM.loc[i, 'w2p cum - 75%'] = tmpPMW2PCum.quantile(q=0.75)
        # Worst case
        if i in tmpPMWorst.index.levels[0]:
            # Per year
            tmpDf = tmpPMWorst.loc[i]['Added capacity Renewables'] * tmpInvestRES / 1e9
            dfPlotPM.loc[i, 'worst - median'] = tmpDf.median()
            dfPlotPM.loc[i, 'worst - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotPM.loc[i, 'worst - 75%'] = tmpDf.quantile(q=0.75)
            # Cumulative
            tmpPMWorstCum = tmpPMWorstCum + tmpDf
        dfPlotPM.loc[i, 'worst cum - median'] = tmpPMWorstCum.median()
        dfPlotPM.loc[i, 'worst cum - 25%'] = tmpPMWorstCum.quantile(q=0.25)
        dfPlotPM.loc[i, 'worst cum - 75%'] = tmpPMWorstCum.quantile(q=0.75)

        # Hydrogen market
        # Reference case
        if i in tmpHMRef.index.levels[0]:
            # Per year
            tmpHMAbs = pd.Series(data=0, index=tmpPMRef.loc[0].index)
            tmpDf = tmpHMRef.loc[i]['Price'] * tmpHMRef.loc[i]['Capacity']
            tmpDf = tmpDf.groupby(level=0).sum() / 1e9
            tmpHMAbs = tmpHMAbs.add(tmpDf, fill_value=0)
            dfPlotHM.loc[i, 'ref - median'] = tmpHMAbs.median()
            # Cumulative
            tmpHMRefCum = tmpHMRefCum.add(tmpDf, fill_value=0)
        dfPlotHM.loc[i, 'ref cum - median'] = tmpHMRefCum.median()
        # Strat case
        if i in tmpHMStrat.index.levels[0]:
            # Per year
            tmpHMAbs = pd.Series(data=0, index=tmpPMStrat.loc[0].index)
            tmpDf = tmpHMStrat.loc[i]['Price'] * tmpHMStrat.loc[i]['Capacity']
            tmpDf = tmpDf.groupby(level=0).sum() / 1e9
            tmpHMAbs = tmpHMAbs.add(tmpDf, fill_value=0)
            dfPlotHM.loc[i, 'strat - median'] = tmpHMAbs.median()
            dfPlotHM.loc[i, 'strat - 25%'] = tmpHMAbs.quantile(q=0.25)
            dfPlotHM.loc[i, 'strat - 75%'] = tmpHMAbs.quantile(q=0.75)
            # Cumulative
            tmpHMStratCum = tmpHMStratCum.add(tmpDf, fill_value=0)
        dfPlotHM.loc[i, 'strat cum - median'] = tmpHMStratCum.median()
        dfPlotHM.loc[i, 'strat cum - 25%'] = tmpHMStratCum.quantile(q=0.25)
        dfPlotHM.loc[i, 'strat cum - 75%'] = tmpHMStratCum.quantile(q=0.75)
        # W2P case
        if i in tmpHMW2P.index.levels[0]:
            # Per year
            tmpHMAbs = pd.Series(data=0, index=tmpPMW2P.loc[0].index)
            tmpDf = tmpHMW2P.loc[i]['Price'] * tmpHMW2P.loc[i]['Capacity']
            tmpDf = tmpDf.groupby(level=0).sum() / 1e9
            tmpHMAbs = tmpHMAbs.add(tmpDf, fill_value=0)
            dfPlotHM.loc[i, 'w2p - median'] = tmpHMAbs.median()
            dfPlotHM.loc[i, 'w2p - 25%'] = tmpHMAbs.quantile(q=0.25)
            dfPlotHM.loc[i, 'w2p - 75%'] = tmpHMAbs.quantile(q=0.75)
            # Cumulative
            tmpHMW2PCum = tmpHMW2PCum.add(tmpDf, fill_value=0)
        dfPlotHM.loc[i, 'w2p cum - median'] = tmpHMW2PCum.median()
        dfPlotHM.loc[i, 'w2p cum - 25%'] = tmpHMW2PCum.quantile(q=0.25)
        dfPlotHM.loc[i, 'w2p cum - 75%'] = tmpHMW2PCum.quantile(q=0.75)
        # Worst case
        if i in tmpHMWorst.index.levels[0]:
            # Per year
            tmpHMAbs = pd.Series(data=0, index=tmpPMWorst.loc[0].index)
            tmpDf = tmpHMWorst.loc[i]['Price'] * tmpHMWorst.loc[i]['Capacity']
            tmpDf = tmpDf.groupby(level=0).sum() / 1e9
            tmpHMAbs = tmpHMAbs.add(tmpDf, fill_value=0)
            dfPlotHM.loc[i, 'worst - median'] = tmpHMAbs.median()
            dfPlotHM.loc[i, 'worst - 25%'] = tmpHMAbs.quantile(q=0.25)
            dfPlotHM.loc[i, 'worst - 75%'] = tmpHMAbs.quantile(q=0.75)
            # Cumulative
            tmpHMWorstCum = tmpHMWorstCum.add(tmpDf, fill_value=0)
        dfPlotHM.loc[i, 'worst cum - median'] = tmpHMWorstCum.median()
        dfPlotHM.loc[i, 'worst cum - 25%'] = tmpHMWorstCum.quantile(q=0.25)
        dfPlotHM.loc[i, 'worst cum - 75%'] = tmpHMWorstCum.quantile(q=0.75)

        # Electrolyzer market
        # Reference case
        if i in tmpEMRef.index.levels[0]:
            # Per year
            tmpDf = tmpEMRef.loc[i]['Added capacity Manufacturings'] * tmpInvestFAC / 1e9
            dfPlotEM.loc[i, 'ref - median'] = tmpDf.median()
            # Cumulative
            tmpEMRefCum = tmpEMRefCum + tmpDf
        dfPlotEM.loc[i, 'ref cum - median'] = tmpEMRefCum.median()
        # Strat case
        if i in tmpEMStrat.index.levels[0]:
            # Per year
            tmpDf = tmpEMStrat.loc[i]['Added capacity Manufacturings'] * tmpInvestFAC / 1e9
            dfPlotEM.loc[i, 'strat - median'] = tmpDf.median()
            dfPlotEM.loc[i, 'strat - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotEM.loc[i, 'strat - 75%'] = tmpDf.quantile(q=0.75)
            # Cumulative
            tmpEMStratCum = tmpEMStratCum + tmpDf
        dfPlotEM.loc[i, 'strat cum - median'] = tmpEMStratCum.median()
        dfPlotEM.loc[i, 'strat cum - 25%'] = tmpEMStratCum.quantile(q=0.25)
        dfPlotEM.loc[i, 'strat cum - 75%'] = tmpEMStratCum.quantile(q=0.75)
        # W2P case
        if i in tmpEMW2P.index.levels[0]:
            # Per year
            tmpDf = tmpEMW2P.loc[i]['Added capacity Manufacturings'] * tmpInvestFAC / 1e9
            dfPlotEM.loc[i, 'w2p - median'] = tmpDf.median()
            dfPlotEM.loc[i, 'w2p - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotEM.loc[i, 'w2p - 75%'] = tmpDf.quantile(q=0.75)
            # Cumulative
            tmpEMW2PCum = tmpEMW2PCum + tmpDf
        dfPlotEM.loc[i, 'w2p cum - median'] = tmpEMW2PCum.median()
        dfPlotEM.loc[i, 'w2p cum - 25%'] = tmpEMW2PCum.quantile(q=0.25)
        dfPlotEM.loc[i, 'w2p cum - 75%'] = tmpEMW2PCum.quantile(q=0.75)
        # Worst case
        if i in tmpEMWorst.index.levels[0]:
            # Per year
            tmpDf = tmpEMWorst.loc[i]['Added capacity Manufacturings'] * tmpInvestFAC / 1e9
            dfPlotEM.loc[i, 'worst - median'] = tmpDf.median()
            dfPlotEM.loc[i, 'worst - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotEM.loc[i, 'worst - 75%'] = tmpDf.quantile(q=0.75)
            # Cumulative
            tmpEMWorstCum = tmpEMWorstCum + tmpDf
        dfPlotEM.loc[i, 'worst cum - median'] = tmpEMWorstCum.median()
        dfPlotEM.loc[i, 'worst cum - 25%'] = tmpEMWorstCum.quantile(q=0.25)
        dfPlotEM.loc[i, 'worst cum - 75%'] = tmpEMWorstCum.quantile(q=0.75)

    # Figure
    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=plotSettings['figsize_3t'],
                             gridspec_kw=plotSettings['gridspec_kw'], dpi=plotSettings['dpi'], sharex=True)

    # Power market
    ax1 = axes[0, 0]
    ax1.set_ylabel('Renewables', fontsize=plotSettings['fontsize'])
    # Results data
    # Per year
    ax1.plot(x, dfPlotPM['ref - median'], label='Power producer - best case', linestyle='-', color=green)
    ax1.plot(x, dfPlotPM['strat - median'], label='Power producer - non-strategic', linestyle=StratLinestyle,
             color=darkgreen)
    ax1.fill_between(x, dfPlotPM['strat - 25%'], dfPlotPM['strat - 75%'], color=darkgreen, edgecolor=None, alpha=0.1,
                     hatch=StratHatch)
    ax1.plot(x, dfPlotPM['w2p - median'], label='Power producer - grey hydrogen', linestyle=W2PLinestlye, color=darkgreen)
    ax1.fill_between(x, dfPlotPM['w2p - 25%'], dfPlotPM['w2p - 75%'], color=darkgreen, edgecolor=None, alpha=0.1,
                     hatch=W2PHatch)
    ax1.plot(x, dfPlotPM['worst - median'], label='Power producer - worst case', linestyle=WorstLinestyle, color=darkgreen)
    ax1.fill_between(x, dfPlotPM['worst - 25%'], dfPlotPM['worst - 75%'], color=darkgreen, edgecolor=None, alpha=0.1,
                     hatch=WorstHatch)
    ax1.set_ylim(-0.01)
    # Cumulative
    ax12 = axes[0, 1]
    ax12.plot(x, dfPlotPM['ref cum - median'], label='Power producer cumulative - best case', linestyle='-', color=green)
    ax12.plot(x, dfPlotPM['strat cum - median'], label='Power producer cumulative - non-strategic',
              linestyle=StratLinestyle, color=darkgreen)
    ax12.fill_between(x, dfPlotPM['strat cum - 25%'], dfPlotPM['strat cum - 75%'], color=darkgreen, edgecolor=None,
                      alpha=0.1, hatch=StratHatch)
    ax12.plot(x, dfPlotPM['w2p cum - median'], label='Power producer cumulative - grey hydrogen', linestyle=W2PLinestlye,
              color=darkgreen)
    ax12.fill_between(x, dfPlotPM['w2p cum - 25%'], dfPlotPM['w2p cum - 75%'], color=darkgreen, edgecolor=None,
                      alpha=0.1, hatch=W2PHatch)
    ax12.plot(x, dfPlotPM['worst cum - median'], label='Power producer cumulative - worst case', linestyle=WorstLinestyle,
              color=darkgreen)
    ax12.fill_between(x, dfPlotPM['worst cum - 25%'], dfPlotPM['worst cum - 75%'], color=darkgreen, edgecolor=None,
                      alpha=0.1, hatch=WorstHatch)

    # Hydrogen market
    ax2 = axes[1, 0]
    ax2.set_ylabel('Electrolyzers', fontsize=plotSettings['fontsize'])
    # Results data
    # Per year
    ax2.plot(x, dfPlotHM['ref - median'], label='Hydrogen producer - best case', linestyle='-', color=blue)
    ax2.plot(x, dfPlotHM['strat - median'], label='Hydrogen producer - non-strategic', linestyle=StratLinestyle,
             color=darkblue)
    ax2.fill_between(x, dfPlotHM['strat - 25%'], dfPlotHM['strat - 75%'], color=darkblue, edgecolor=None, alpha=0.1,
                     hatch=StratHatch)
    ax2.plot(x, dfPlotHM['w2p - median'], label='Hydrogen producer - grey hydrogen', linestyle=W2PLinestlye,
             color=darkblue)
    ax2.fill_between(x, dfPlotHM['w2p - 25%'], dfPlotHM['w2p - 75%'], color=darkblue, edgecolor=None, alpha=0.1,
                     hatch=W2PHatch)
    ax2.plot(x, dfPlotHM['worst - median'], label='Hydrogen producer - worst case', linestyle=WorstLinestyle,
             color=darkblue)
    ax2.fill_between(x, dfPlotHM['worst - 25%'], dfPlotHM['worst - 75%'], color=darkblue, edgecolor=None, alpha=0.1,
                     hatch=WorstHatch)
    ax2.set_ylim(-0.01)
    # Cumulative
    ax22 = axes[1, 1]
    ax22.plot(x, dfPlotHM['ref cum - median'], label='Hydrogen producer cumulative - best case', linestyle='-',
              color=blue)
    ax22.plot(x, dfPlotHM['strat cum - median'], label='Hydrogen producer cumulative - non-strategic',
              linestyle=StratLinestyle, color=darkblue)
    ax22.fill_between(x, dfPlotHM['strat cum - 25%'], dfPlotHM['strat cum - 75%'], color=darkblue, edgecolor=None,
                      alpha=0.1, hatch=StratHatch)
    ax22.plot(x, dfPlotHM['w2p cum - median'], label='Power producer cumulative - grey hydrogen', linestyle=W2PLinestlye,
              color=darkblue)
    ax22.fill_between(x, dfPlotHM['w2p cum - 25%'], dfPlotHM['w2p cum - 75%'], color=darkblue, edgecolor=None,
                      alpha=0.1, hatch=W2PHatch)
    ax22.plot(x, dfPlotHM['worst cum - median'], label='Power producer cumulative - worst case', linestyle=WorstLinestyle,
              color=darkblue)
    ax22.fill_between(x, dfPlotHM['worst cum - 25%'], dfPlotHM['worst cum - 75%'], color=darkblue, edgecolor=None,
                      alpha=0.1, hatch=WorstHatch)
    ax22.set_ylim(-0.01)

    # Electrolyzer market
    ax3 = axes[2, 0]
    ax3.set_ylabel('Factories', fontsize=plotSettings['fontsize'])
    # Results data
    # Per year
    ax3.plot(x, dfPlotEM['ref - median'], label='Electrolyzer producer - best case', linestyle='-', color=purple)
    ax3.plot(x, dfPlotEM['strat - median'], label='Electrolyzer producer - non-strategic', linestyle=StratLinestyle,
             color=darkpurple)
    ax3.fill_between(x, dfPlotEM['strat - 25%'], dfPlotEM['strat - 75%'], color=darkpurple, edgecolor=None, alpha=0.1,
                     hatch=StratHatch)
    ax3.plot(x, dfPlotEM['w2p - median'], label='Electrolyzer producer - grey hydrogen', linestyle=W2PLinestlye,
             color=darkpurple)
    ax3.fill_between(x, dfPlotEM['w2p - 25%'], dfPlotEM['w2p - 75%'], color=darkpurple, edgecolor=None, alpha=0.1,
                     hatch=W2PHatch)
    ax3.plot(x, dfPlotEM['worst - median'], label='Electrolyzer producer - worst case', linestyle=WorstLinestyle,
             color=darkpurple)
    ax3.fill_between(x, dfPlotEM['worst - 25%'], dfPlotEM['worst - 75%'], color=darkpurple, edgecolor=None, alpha=0.1,
                     hatch=WorstHatch)
    ax3.set_ylim(-0.01)
    # Cumulative
    ax32 = axes[2, 1]
    ax32.plot(x, dfPlotEM['ref cum - median'], label='Electrolyzer producer cumulative - best case', linestyle='-',
              color=purple)
    ax32.plot(x, dfPlotEM['strat cum - median'], label='Electrolyzer producer cumulative - non-strategic',
              linestyle=StratLinestyle, color=darkpurple)
    ax32.fill_between(x, dfPlotEM['strat cum - 25%'], dfPlotEM['strat cum - 75%'], color=darkpurple, edgecolor=None,
                      alpha=0.1, hatch=StratHatch)
    ax32.plot(x, dfPlotEM['w2p cum - median'], label='Electrolyzer producer cumulative - grey hydrogen',
              linestyle=W2PLinestlye, color=darkpurple)
    ax32.fill_between(x, dfPlotEM['w2p cum - 25%'], dfPlotEM['w2p cum - 75%'], color=darkpurple, edgecolor=None,
                      alpha=0.1, hatch=W2PHatch)
    ax32.plot(x, dfPlotEM['worst cum - median'], label='Electrolyzer producer cumulative - worst case',
              linestyle=WorstLinestyle, color=darkpurple)
    ax32.fill_between(x, dfPlotEM['worst cum - 25%'], dfPlotEM['worst cum - 75%'], color=darkpurple, edgecolor=None,
                      alpha=0.1, hatch=WorstHatch)
    ax32.set_ylim(-0.01)

    fig.text(-0.1, 0.5, 'Yearly Investment [Bn. €]', va='center', rotation='vertical', fontsize=plotSettings['fontsize'])
    fig.text(1.1, 0.5, 'Cumulative investment [Bn. €]', va='center', rotation='vertical',
             fontsize=plotSettings['fontsize'])

    plt.xlim(plotSettings['xlim'])

    # Adjust ticks
    ax1.minorticks_on()
    ax12.minorticks_on()
    ax2.minorticks_on()
    ax22.minorticks_on()
    ax3.minorticks_on()
    ax32.minorticks_on()
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(10))
    ax1.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax1.tick_params(which='minor', axis='both', color='gray')
    ax12.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax12.tick_params(axis='y', which='both', left=False, right=True, labelleft=False, labelright=True)
    ax12.yaxis.set_minor_locator(MultipleLocator(100))
    ax12.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax12.tick_params(which='minor', axis='both', color='gray')
    ax2.yaxis.set_minor_locator(MultipleLocator(1))
    ax2.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax2.tick_params(which='minor', axis='both', color='gray')
    ax22.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax22.yaxis.set_minor_locator(MultipleLocator(10))
    ax22.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax22.tick_params(which='minor', axis='both', color='gray')
    ax22.tick_params(axis='y', which='both', left=False, right=True, labelleft=False, labelright=True)
    ax3.yaxis.set_minor_locator(MultipleLocator(0.25))
    ax3.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax3.tick_params(which='minor', axis='both', color='gray')
    ax32.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax32.yaxis.set_minor_locator(MultipleLocator(5))
    ax32.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax32.tick_params(which='minor', axis='both', color='gray')
    ax32.tick_params(axis='y', which='both', left=False, right=True, labelleft=False, labelright=True)

    # Legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles12, labels12 = ax12.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles22, labels22 = ax22.get_legend_handles_labels()
    handles3, labels3 = ax3.get_legend_handles_labels()
    handles32, labels32 = ax32.get_legend_handles_labels()

    handles = handles1 + handles2 + handles3 + handles12 + handles22 + handles32
    labels = labels1 + labels2 + labels3 + labels12 + labels22 + labels32

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.99),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save figure
    plt.savefig(os.getcwd() + '\\figure24.' + plotType, bbox_inches='tight')

    # Write data
    writeDf = pd.DataFrame(data=[dfPlotPM['ref - median'],
                                 dfPlotPM['strat - median'], dfPlotPM['strat - 25%'],dfPlotPM['strat - 75%'],
                                 dfPlotPM['w2p - median'], dfPlotPM['w2p - 25%'], dfPlotPM['w2p - 75%'],
                                 dfPlotPM['worst - median'], dfPlotPM['worst - 25%'], dfPlotPM['worst - 75%'],
                                 dfPlotPM['ref cum - median'],
                                 dfPlotPM['strat cum - median'], dfPlotPM['strat cum - 25%'], dfPlotPM['strat cum - 75%'],
                                 dfPlotPM['w2p cum - median'], dfPlotPM['w2p cum - 25%'], dfPlotPM['w2p cum - 75%'],
                                 dfPlotPM['worst cum - median'], dfPlotPM['worst cum - 25%'], dfPlotPM['worst cum - 75%'],
                                 dfPlotHM['ref - median'],
                                 dfPlotHM['strat - median'], dfPlotHM['strat - 25%'], dfPlotHM['strat - 75%'],
                                 dfPlotHM['w2p - median'], dfPlotHM['w2p - 25%'], dfPlotHM['w2p - 75%'],
                                 dfPlotHM['worst - median'], dfPlotHM['worst - 25%'], dfPlotHM['worst - 75%'],
                                 dfPlotHM['ref cum - median'],
                                 dfPlotHM['strat cum - median'], dfPlotHM['strat cum - 25%'], dfPlotHM['strat cum - 75%'],
                                 dfPlotHM['w2p cum - median'], dfPlotHM['w2p cum - 25%'], dfPlotHM['w2p cum - 75%'],
                                 dfPlotHM['worst cum - median'], dfPlotHM['worst cum - 25%'], dfPlotHM['worst cum - 75%'],
                                 dfPlotEM['ref - median'],
                                 dfPlotEM['strat - median'], dfPlotEM['strat - 25%'], dfPlotEM['strat - 75%'],
                                 dfPlotEM['w2p - median'], dfPlotEM['w2p - 25%'], dfPlotEM['w2p - 75%'],
                                 dfPlotEM['worst - median'], dfPlotEM['worst - 25%'], dfPlotEM['worst - 75%'],
                                 dfPlotEM['ref cum - median'],
                                 dfPlotEM['strat cum - median'], dfPlotEM['strat cum - 25%'], dfPlotEM['strat cum - 75%'],
                                 dfPlotEM['w2p cum - median'], dfPlotEM['w2p cum - 25%'], dfPlotEM['w2p cum - 75%'],
                                 dfPlotEM['worst cum - median'], dfPlotEM['worst cum - 25%'], dfPlotEM['worst cum - 75%']],
                           index=['Renewables reference - median [Bn. €]',
                                  'Renewables strategic - median [Bn. €]',
                                  'Renewables strategic - 25% [Bn. €]', 'Renewables strategic - 75% [Bn. €]',
                                  'Renewables W2P - median [Bn. €]',
                                  'Renewables W2P - 25% [Bn. €]', 'Renewables W2P - 75% [Bn. €]',
                                  'Renewables worst - median [Bn. €]',
                                  'Renewables worst - 25% [Bn. €]', 'Renewables worst - 75% [Bn. €]',
                                  'Renewables reference cum. - median [Bn. €]',
                                  'Renewables strategic cum. - median [Bn. €]',
                                  'Renewables strategic cum. - 25% [Bn. €]', 'Renewables strategic cum. - 75% [Bn. €]',
                                  'Renewables W2P cum. - median [Bn. €]',
                                  'Renewables W2P cum. - 25% [Bn. €]', 'Renewables W2P cum. - 75% [Bn. €]',
                                  'Renewables worst cum. - median [Bn. €]',
                                  'Renewables worst cum. - 25% [Bn. €]', 'Renewables worst cum. - 75% [Bn. €]',
                                  'Electrolyzers reference - median [Bn. €]',
                                  'Electrolyzers strategic - median [Bn. €]',
                                  'Electrolyzers strategic - 25% [Bn. €]', 'Electrolyzers strategic - 75% [Bn. €]',
                                  'Electrolyzers W2P - median [Bn. €]',
                                  'Electrolyzers W2P - 25% [Bn. €]', 'Electrolyzers W2P - 75% [Bn. €]',
                                  'Electrolyzers worst - median [Bn. €]',
                                  'Electrolyzers worst - 25% [Bn. €]', 'Electrolyzers worst - 75% [Bn. €]',
                                  'Electrolyzers reference cum. - median [Bn. €]',
                                  'Electrolyzers strategic cum. - median [Bn. €]',
                                  'Electrolyzers strategic cum. - 25% [Bn. €]', 'Electrolyzers strategic cum. - 75% [Bn. €]',
                                  'Electrolyzers W2P cum. - median [Bn. €]',
                                  'Electrolyzers W2P cum. - 25% [Bn. €]', 'Electrolyzers W2P cum. - 75% [Bn. €]',
                                  'Electrolyzers worst cum. - median [Bn. €]',
                                  'Electrolyzers worst cum. - 25% [Bn. €]', 'Electrolyzers worst cum. - 75% [Bn. €]',
                                  'Factories reference - median [Bn. €]',
                                  'Factories strategic - median [Bn. €]',
                                  'Factories strategic - 25% [Bn. €]', 'Factories strategic - 75% [Bn. €]',
                                  'Factories W2P - median [Bn. €]',
                                  'Factories W2P - 25% [Bn. €]', 'Factories W2P - 75% [Bn. €]',
                                  'Factories worst - median [Bn. €]',
                                  'Factories worst - 25% [Bn. €]', 'Factories worst - 75% [Bn. €]',
                                  'Factories reference cum. - median [Bn. €]',
                                  'Factories strategic cum. - median [Bn. €]',
                                  'Factories strategic cum. - 25% [Bn. €]', 'Factories strategic cum. - 75% [Bn. €]',
                                  'Factories W2P cum. - median [Bn. €]',
                                  'Factories W2P cum. - 25% [Bn. €]', 'Factories W2P cum. - 75% [Bn. €]',
                                  'Factories worst cum. - median [Bn. €]',
                                  'Factories worst cum. - 25% [Bn. €]', 'Factories worst cum. - 75% [Bn. €]'])
    writeDf = writeDf.T
    writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure24.csv', sep=';')


def figure_25(dfPMRef, dfPMStrat, dfPMW2P, dfHMRef, dfHMStrat, dfHMW2P):
    '''
    Function that will create Fig. 25 - Weighted electricity price and LCOE and hydrogen price and LCOH for the obstalce
    case.
    :param:
        pd.DataFrame dfPMRef: Yearly data from the power market for the reference case.
        pd.DataFrame dfPMStrat: Yearly data from the power market for the strategic case.
        pd.DataFrame dfPMW2P: Yearly data from the power market for the willingness to pay case.
        pd.DataFrame dfHMRef: Yearly data from the electrolyzer sales for the reference case.
        pd.DataFrame dfHMStrat: Yearly data from the electrolyzer sales for the strategic case.
        pd.DataFrame dfHMW2P: Yearly data from the electrolyzer sales for the willingness to pay case.
    :return:
    '''
    # Power market
    tmpPMRef = dfPMRef.set_index(['Year', 'Run'])
    tmpPMStrat = dfPMStrat.set_index(['Year', 'Run'])
    tmpPMW2P = dfPMW2P.set_index(['Year', 'Run'])
    dfPlotPM = pd.DataFrame(data=np.nan, index=range(yearDelta),
                            columns=['lcoe ref - median',
                                     'lcoe strat - median', 'lcoe strat - 25%', 'lcoe strat - 75%',
                                     'lcoe w2p - median', 'lcoe w2p - 25%', 'lcoe w2p - 75%',
                                     'elc ref - median',
                                     'elc strat - median', 'elc strat - 25%', 'elc strat 75%',
                                     'elc w2p - median', 'elc w2p - 25%', 'elc w2p -75%'])

    # Hydrogen market
    tmpHMRef = dfHMRef.set_index(['Year', 'Run'])
    tmpHMStrat = dfHMStrat.set_index(['Year', 'Run'])
    tmpHMW2P = dfHMW2P.set_index(['Year', 'Run'])
    dfPlotHM = pd.DataFrame(data=np.nan, index=range(yearDelta),
                            columns=['lcoh ref - median',
                                     'lcoh strat - median', 'lcoh strat - 25%', 'lcoh strat - 75%',
                                     'lcoh w2p - median', 'lcoh w2p - 25%', 'lcoh w2p - 75%',
                                     'h2 ref - median',
                                     'h2 strat - median', 'h2 strat - 25%', 'h2 strat 75%',
                                     'h2 w2p - median', 'h2 w2p - 25%', 'h2 w2p -75%'])

    for i in range(yearDelta):
        # Power market
        # Reference case
        if i in tmpPMRef.index.levels[0]:
            tmpDf = tmpPMRef.loc[i]['LCOE']
            dfPlotPM.loc[i, 'lcoe ref - median'] = tmpDf.median()
            tmpDf = tmpPMRef.loc[i]['Weighted Price Electricity']
            dfPlotPM.loc[i, 'elc ref - median'] = tmpDf.median()
        # Strategic case
        if i in tmpPMStrat.index.levels[0]:
            tmpDf = tmpPMStrat.loc[i]['LCOE']
            dfPlotPM.loc[i, 'lcoe strat - median'] = tmpDf.median()
            dfPlotPM.loc[i, 'lcoe strat - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotPM.loc[i, 'lcoe strat - 75%'] = tmpDf.quantile(q=0.75)
            tmpDf = tmpPMStrat.loc[i]['Weighted Price Electricity']
            dfPlotPM.loc[i, 'elc strat - median'] = tmpDf.median()
            dfPlotPM.loc[i, 'elc strat - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotPM.loc[i, 'elc strat - 75%'] = tmpDf.quantile(q=0.75)
        # Willingness to pay case
        if i in tmpPMW2P.index.levels[0]:
            tmpDf = tmpPMW2P.loc[i]['LCOE']
            dfPlotPM.loc[i, 'lcoe w2p - median'] = tmpDf.median()
            dfPlotPM.loc[i, 'lcoe w2p - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotPM.loc[i, 'lcoe w2p - 75%'] = tmpDf.quantile(q=0.75)
            tmpDf = tmpPMW2P.loc[i]['Weighted Price Electricity']
            dfPlotPM.loc[i, 'elc w2p - median'] = tmpDf.median()
            dfPlotPM.loc[i, 'elc w2p - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotPM.loc[i, 'elc w2p - 75%'] = tmpDf.quantile(q=0.75)
        # Hydrogen market
        # Reference case
        if i in tmpHMRef.index.levels[0]:
            tmpDf = tmpHMRef.loc[i]['LCOH']
            dfPlotHM.loc[i, 'lcoh ref - median'] = tmpDf.median()
            tmpDf = tmpHMRef.loc[i]['Price Hydrogen']
            dfPlotHM.loc[i, 'h2 ref -median'] = tmpDf.median()
        # Strategic case
        if i in tmpHMStrat.index.levels[0]:
            tmpDf = tmpHMStrat.loc[i]['LCOH']
            dfPlotHM.loc[i, 'lcoh strat - median'] = tmpDf.median()
            dfPlotHM.loc[i, 'lcoh strat - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotHM.loc[i, 'lcoh strat - 75%'] = tmpDf.quantile(q=0.75)
            tmpDf = tmpHMStrat.loc[i]['Price Hydrogen']
            dfPlotHM.loc[i, 'h2 strat - median'] = tmpDf.median()
            dfPlotHM.loc[i, 'h2 strat - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotHM.loc[i, 'h2 strat - 75%'] = tmpDf.quantile(q=0.75)
        # W2P cacse
        if i in tmpHMW2P.index.levels[0]:
            tmpDf = tmpHMW2P.loc[i]['LCOH']
            dfPlotHM.loc[i, 'lcoh w2p - median'] = tmpDf.median()
            dfPlotHM.loc[i, 'lcoh w2p - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotHM.loc[i, 'lcoh w2p - 75%'] = tmpDf.quantile(q=0.75)
            tmpDf = tmpHMW2P.loc[i]['Price Hydrogen']
            dfPlotHM.loc[i, 'h2 w2p - median'] = tmpDf.median()
            dfPlotHM.loc[i, 'h2 w2p - 25%'] = tmpDf.quantile(q=0.25)
            dfPlotHM.loc[i, 'h2 w2p - 75%'] = tmpDf.quantile(q=0.75)

    # Figure
    fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=plotSettings['figsize_2t'], gridspec_kw=plotSettings['gridspec_kw'],
                                   dpi=plotSettings['dpi'], sharex=True)

    # Electricity price
    ax1.set_ylabel('Electricity price/LCOE [€/MWh]', fontsize=plotSettings['fontsize'])
    ax1.plot(x, dfPlotPM['elc ref - median'], label='Electricity price - reference', linestyle='-', color=green)
    ax1.plot(x, dfPlotPM['elc strat - median'], label='Electricity price - non-strategic', linestyle=StratLinestyle,
             color=green)
    ax1.fill_between(x, dfPlotPM['elc strat - 25%'], dfPlotPM['elc strat - 75%'], color=green, edgecolor=None,
                     hatch=StratHatch, alpha=0.1)
    ax1.plot(x, dfPlotPM['elc w2p - median'], label='Electricity price - grey hydrogen', linestyle=W2PLinestlye,
             color=green)
    ax1.fill_between(x, dfPlotPM['elc w2p - 25%'], dfPlotPM['elc w2p - 75%'], color=green, edgecolor=None,
                     hatch=W2PHatch, alpha=0.1)

    ax1.plot(x, dfPlotPM['lcoe ref - median'], label='Levelized costs of electricity case - reference', linestyle='-',
             color=darkgreen, marker='x', markersize=3)
    ax1.plot(x, dfPlotPM['lcoe strat - median'], label='Levelized costs of electricity case - non-strategic',
             linestyle=StratLinestyle, color=darkgreen, marker='o', markersize=3)
    ax1.plot(x, dfPlotPM['lcoe w2p - median'], label='Levelized costs of electricity case - grey hydrogen',
             linestyle=W2PLinestlye, color=darkgreen, marker='^', markersize=3)
    ax1.fill_between(x, dfPlotPM['lcoe strat - 25%'], dfPlotPM['lcoe strat - 75%'], color=darkgreen, edgecolor=None,
                     hatch='...', alpha=0.05)
    ax1.fill_between(x, dfPlotPM['lcoe w2p - 25%'], dfPlotPM['lcoe w2p - 75%'], color=darkgreen, edgecolor=None,
                     hatch='***', alpha=0.05)


    # Hydrogen price
    ax2.set_ylabel('Hydrogen price/LCOH [€/MWh]', fontsize=plotSettings['fontsize'])
    ax2.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    ax2.plot(x, dfPlotHM['h2 ref - median'], label='Hydrogen price - reference', linestyle='-', color=blue)
    ax2.plot(x, dfPlotHM['h2 strat - median'], label='Hydrogen price - non-strategic', linestyle=StratLinestyle,
             color=blue)
    ax2.plot(x, dfPlotHM['h2 w2p - median'], label='Hydrogen price - grey hydrogen', linestyle=W2PLinestlye, color=blue)
    ax2.fill_between(x, dfPlotHM['h2 strat - 25%'], dfPlotHM['h2 strat - 75%'], color=blue, edgecolor=None,
                     hatch=StratHatch, alpha=0.1)
    ax2.fill_between(x, dfPlotHM['h2 w2p - 25%'], dfPlotHM['h2 w2p - 75%'], color=blue, edgecolor=None,
                     hatch=W2PHatch, alpha=0.1)

    ax2.plot(x, dfPlotHM['lcoh ref - median'], label='Levelized costs of hydrogen - reference', linestyle='-',
             color=darkblue, marker='x', markersize=3)
    ax2.plot(x, dfPlotHM['lcoh strat - median'], label='Levelized costs of hydrogen - non-strategic',
             linestyle=StratLinestyle, color=darkblue, marker='o', markersize=3)
    ax2.plot(x, dfPlotHM['lcoh w2p - median'], label='Levelized costs of hydrogen - grey hydrogen',
             linestyle=W2PLinestlye, color=darkblue, marker='^', markersize=3)
    ax2.fill_between(x, dfPlotHM['lcoh strat - 25%'], dfPlotHM['lcoh strat - 75%'], color=darkblue, edgecolor=None,
                     hatch='...', alpha=0.05)
    ax2.fill_between(x, dfPlotHM['lcoh w2p - 25%'], dfPlotHM['lcoh w2p - 75%'], color=darkblue, edgecolor=None,
                     hatch='***', alpha=0.05)

    # in €/kg
    ax22 = ax2.twinx()
    ax22.set_ylabel('Hydrogen price/LCOH [€/kg]', fontsize=plotSettings['fontsize'])
    ax22.plot(x, dfPlotHM['h2 ref - median']*33.3/1e3, linestyle='-', color=blue)
    ax22.plot(x, dfPlotHM['h2 strat - median']*33.3/1e3, linestyle=StratLinestyle, color=darkblue, marker='x',
              markersize=6)

    # Adjust axis
    ax1.minorticks_on()
    ax1.set_xlim(plotSettings['xlim'])
    ax1.set_ylim([0, 100])
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(10))
    ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax1.tick_params(axis='both', which='minor', color='gray')

    ax2.minorticks_on()
    ax2.set_xlim(plotSettings['xlim'])
    ax2.set_ylim([0, 500])
    ax2.set_xticks(plotSettings['xticks'])
    ax2.xaxis.set_minor_locator(MultipleLocator(5))
    ax2.yaxis.set_minor_locator(MultipleLocator(50))
    ax2.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax2.tick_params(axis='both', which='minor', color='gray')

    ax22.minorticks_on()
    ax22.set_xlim(plotSettings['xlim'])
    ax22.set_ylim([0, 500*33.3/1e3])
    ax22.set_xticks(plotSettings['xticks'])
    ax22.xaxis.set_minor_locator(MultipleLocator(5))
    ax22.yaxis.set_minor_locator(MultipleLocator(2.5))
    ax22.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax22.tick_params(axis='both', which='minor', color='gray')

    # Adjust legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    handles = handles1 + handles2
    labels = labels1 + labels2

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.8),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save plot
    plt.savefig(os.getcwd() + '\\figure25.' + plotType, bbox_inches='tight')

    # Write Data
    writeDf = pd.DataFrame(data=[dfPlotPM['elc ref - median'],
                                 dfPlotPM['elc strat - median'], dfPlotPM['elc strat - 25%'], dfPlotPM['elc strat - 75%'],
                                 dfPlotPM['elc w2p - median'], dfPlotPM['elc w2p - 25%'], dfPlotPM['elc w2p - 75%'],
                                 dfPlotPM['lcoe ref - median'],
                                 dfPlotPM['lcoe strat - median'], dfPlotPM['lcoe strat - 25%'], dfPlotPM['lcoe strat - 75%'],
                                 dfPlotPM['lcoe w2p - median'], dfPlotPM['lcoe w2p - 25%'], dfPlotPM['lcoe w2p - 75%'],
                                 dfPlotHM['h2 ref - median'],
                                 dfPlotHM['h2 strat - median'], dfPlotHM['h2 strat - 25%'], dfPlotHM['h2 strat - 75%'],
                                 dfPlotHM['h2 w2p - median'], dfPlotHM['h2 w2p - 25%'], dfPlotHM['h2 w2p - 75%'],
                                 dfPlotHM['lcoh ref - median'],
                                 dfPlotHM['lcoh strat - median'], dfPlotHM['lcoh strat - 25%'], dfPlotHM['lcoh strat - 75%'],
                                 dfPlotHM['lcoh w2p - median'], dfPlotHM['lcoh w2p - 25%'], dfPlotHM['lcoh w2p - 75%'],
                                 dfPlotHM['h2 ref - median']*33.3/1e3,
                                 dfPlotHM['h2 strat - median']*33.3/1e3, dfPlotHM['h2 strat - 25%']*33.3/1e3,
                                 dfPlotHM['h2 strat - 75%']*33.3/1e3,
                                 dfPlotHM['h2 w2p - median']*33.3/1e3, dfPlotHM['h2 w2p - 25%']*33.3/1e3,
                                 dfPlotHM['h2 w2p - 75%']*33.3/1e3,
                                 dfPlotHM['lcoh ref - median']*33.3/1e3,
                                 dfPlotHM['lcoh strat - median']*33.3/1e3, dfPlotHM['lcoh strat - 25%']*33.3/1e3,
                                 dfPlotHM['lcoh strat - 75%']*33.3/1e3,
                                 dfPlotHM['lcoh w2p - median']*33.3/1e3, dfPlotHM['lcoh w2p - 25%']*33.3/1e3,
                                 dfPlotHM['lcoh w2p - 75%']*33.3/1e3,],
                           index=['Weighted electricity price ref - median [€/MWh]',
                                  'Weighted electricity price strat - median [€/MWh]',
                                  'Weighted electricity price strat - 25% [€/MWh]',
                                  'Weighted electricity price strat - 75% [€/MWh]',
                                  'Weighted electricity price w2p - median [€/MWh]',
                                  'Weighted electricity price w2p - 25% [€/MWh]',
                                  'Weighted electricity price w2p - 75% [€/MWh]',
                                  'Levelized costs of electricity ref - median [€/MWh]',
                                  'Levelized costs of electricity strat - median [€/MWh]',
                                  'Levelized costs of electricity strat - 25% [€/MWh]',
                                  'Levelized costs of electricity strat - 75% [€/MWh]',
                                  'Levelized costs of electricity w2p - median [€/MWh]',
                                  'Levelized costs of electricity w2p - 25% [€/MWh]',
                                  'Levelized costs of electricity w2p - 75% [€/MWh]',
                                  'Hydrogen price ref - median [€/MWh]',
                                  'Hydrogen price strat - median [€/MWh]',
                                  'Hydrogen price strat - 25% [€/MWh]',
                                  'Hydrogen price strat - 75% [€/MWh]',
                                  'Hydrogen price w2p - median [€/MWh]',
                                  'Hydrogen price w2p - 25% [€/MWh]',
                                  'Hydrogen price w2p - 75% [€/MWh]',
                                  'Levelized costs of hydrogen ref - median [€/MWh]',
                                  'Levelized costs of hydrogen strat - median [€/MWh]',
                                  'Levelized costs of hydrogen strat - 25% [€/MWh]',
                                  'Levelized costs of hydrogen strat - 75% [€/MWh]',
                                  'Levelized costs of hydrogen w2p - median [€/MWh]',
                                  'Levelized costs of hydrogen w2p - 25% [€/MWh]',
                                  'Levelized costs of hydrogen w2p - 75% [€/MWh]',
                                  'Hydrogen price ref - median [€/kg]',
                                  'Hydrogen price strat - median [€/kg]',
                                  'Hydrogen price strat - 25% [€/kg]',
                                  'Hydrogen price strat - 75% [€/kg]',
                                  'Hydrogen price w2p - median [€/kg]',
                                  'Hydrogen price w2p - 25% [€/kg]',
                                  'Hydrogen price w2p - 75% [€/kg]',
                                  'Levelized costs of hydrogen ref - median [€/kg]',
                                  'Levelized costs of hydrogen strat - median [€/kg]',
                                  'Levelized costs of hydrogen strat - 25% [€/kg]',
                                  'Levelized costs of hydrogen strat - 75% [€/kg]',
                                  'Levelized costs of hydrogen w2p - median [€/kg]',
                                  'Levelized costs of hydrogen w2p - 25% [€/kg]',
                                  'Levelized costs of hydrogen w2p - 75% [€/kg]'])
    writeDf = writeDf.T
    writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure25.csv', sep=';')


def figure_25a(dfPMRef, dfPMStrat, dfPMW2P, dfHMRef, dfHMStrat, dfHMW2P):
    '''
    Function that will create Fig. 25a - LCOH and the average electricity price for HP and its ratio in the obstacle
    case.
    :param:
        pd.DataFrame dfPMRef: Daily data from the power market for the reference case.
        pd.DataFrame dfPMStrat: Daily data from the power market for the nonstrategic case.
        pd.DataFrame dfPMW2P: Daily data from the power market for the w2p case.
        pd.DataFrame dfHMRef: Yearly data from the hydrogen market for the reference case.
        pd.DataFrame dfHMStrat: Yearly data from the hydrogen market for the nonstrategic case.
        pd.DataFrame dfHMW2P: Yearly data from the hydrogen market for the w2p case.
    :return:
    '''
    # Power market
    tmpPMRef = dfPMRef.set_index(['Year', 'Day', 'Run'])
    tmpPMStrat = dfPMStrat.set_index(['Year', 'Day', 'Run'])
    tmpPMW2P = dfPMW2P.set_index(['Year', 'Day', 'Run'])

    # Hydrogen market
    tmpHMRef = dfHMRef.set_index(['Year', 'Run'])
    tmpHMStrat = dfHMStrat.set_index(['Year', 'Run'])
    tmpHMW2P = dfHMW2P.set_index(['Year', 'Run'])
    dfPlot = pd.DataFrame(data=np.nan, index=range(yearDelta),
                          columns=['elc ref - median',
                                   'elc strat - median', 'elc strat - 25%', 'elc strat - 75%',
                                   'elc w2p - median', 'elc w2p - 25%', 'elc w2p - 75%',
                                   'lcoh ref - median',
                                   'lcoh strat - median', 'lcoh strat - 25%', 'lcoh strat - 75%',
                                   'lcoh w2p - median', 'lcoh w2p - 25%', 'lcoh w2p - 75%'])


    for i in range(yearDelta):
        # Power market
        # Reference case
        if i in tmpPMRef.index.levels[0]:
            tmpDf = tmpPMRef.loc[i]['Electricity demand electrolyzers'] * tmpPMRef.loc[i]['Price Electricity']
            tmpDf = (tmpDf.groupby(level=1).sum() /
                     tmpPMRef.loc[i]['Electricity demand electrolyzers'].groupby(level=1).sum())
            dfPlot.loc[i, 'elc ref - median'] = tmpDf.median()
        # Non strategic case
        if i in tmpPMStrat.index.levels[0]:
            tmpDf = tmpPMStrat.loc[i]['Electricity demand electrolyzers'] * tmpPMStrat.loc[i]['Price Electricity']
            tmpDf = (tmpDf.groupby(level=1).sum() /
                     tmpPMStrat.loc[i]['Electricity demand electrolyzers'].groupby(level=1).sum())
            dfPlot.loc[i, 'elc strat - median'] = tmpDf.median()
            dfPlot.loc[i, 'elc strat - 25%'] = tmpDf.quantile(q=0.25)
            dfPlot.loc[i, 'elc strat - 75%'] = tmpDf.quantile(q=0.75)
        # W2P case
        if i in tmpPMW2P.index.levels[0]:
            tmpDf = tmpPMW2P.loc[i]['Electricity demand electrolyzers'] * tmpPMW2P.loc[i]['Price Electricity']
            tmpDf = (tmpDf.groupby(level=1).sum() /
                     tmpPMW2P.loc[i]['Electricity demand electrolyzers'].groupby(level=1).sum())
            dfPlot.loc[i, 'elc w2p - median'] = tmpDf.median()
            dfPlot.loc[i, 'elc w2p - 25%'] = tmpDf.quantile(q=0.25)
            dfPlot.loc[i, 'elc w2p - 75%'] = tmpDf.quantile(q=0.75)
        # Hydrogen market
        # Reference case
        if i in tmpHMRef.index.levels[0]:
            tmpDf = tmpHMRef.loc[i]['LCOH']
            dfPlot.loc[i, 'lcoh ref - median'] = tmpDf.median()
        # Non strategic case
        if i in tmpHMStrat.index.levels[0]:
            tmpDf = tmpHMStrat.loc[i]['LCOH']
            dfPlot.loc[i, 'lcoh strat - median'] = tmpDf.median()
            dfPlot.loc[i, 'lcoh strat - 25%'] = tmpDf.quantile(q=0.25)
            dfPlot.loc[i, 'lcoh strat - 75%'] = tmpDf.quantile(q=0.75)
        # W2P case
        if i in tmpHMW2P.index.levels[0]:
            tmpDf = tmpHMW2P.loc[i]['LCOH']
            dfPlot.loc[i, 'lcoh w2p - median'] = tmpDf.median()
            dfPlot.loc[i, 'lcoh w2p - 25%'] = tmpDf.quantile(q=0.25)
            dfPlot.loc[i, 'lcoh w2p - 75%'] = tmpDf.quantile(q=0.75)



    # Figure
    fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                            dpi=plotSettings['dpi'])

    # Electricity price
    ax1.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    ax1.set_ylabel('Average electricty price [€/${MWh_{elc}}$]/\nLevelized costs of hydrogen [€/${MWh_{{H}_{2}}}]$',
                   fontsize=plotSettings['fontsize'])
    ax1.plot(x, dfPlot['elc ref - median'], label='Electricity price - reference', linestyle='-', color=green)
    ax1.plot(x, dfPlot['elc strat - median'], label='Electricity price - non-strategic', linestyle=StratLinestyle,
             color=darkgreen)
    ax1.plot(x, dfPlot['elc w2p - median'], label='Electricity price - grey hydrogen', linestyle=W2PLinestlye,
             color=darkgreen)
    ax1.fill_between(x, dfPlot['elc strat - 25%'], dfPlot['elc strat - 75%'], color=darkgreen, alpha=0.1, edgecolor=None,
                     hatch=StratHatch)
    ax1.fill_between(x, dfPlot['elc w2p - 25%'], dfPlot['elc w2p - 75%'], color=darkgreen, alpha=0.1, edgecolor=None,
                     hatch=W2PHatch)

    # Hydrogen price
    # In €/MWh
    ax1.plot(x, dfPlot['lcoh ref - median'], label='LCOH - reference', linestyle='-', color=blue)
    ax1.plot(x, dfPlot['lcoh strat - median'], label='LCOH - non-strategic', linestyle=StratLinestyle, color=darkblue)
    ax1.plot(x, dfPlot['lcoh w2p - median'], label='LCOH - grey hydrogen', linestyle=W2PLinestlye, color=darkblue)
    ax1.fill_between(x, dfPlot['lcoh strat - 25%'], dfPlot['lcoh strat - 75%'], color=darkblue, alpha=0.1,
                     edgecolor=None, hatch=StratHatch)
    ax1.fill_between(x, dfPlot['lcoh w2p - 25%'], dfPlot['lcoh w2p - 75%'], color=darkblue, alpha=0.1, edgecolor=None,
                     hatch=W2PHatch)

    # Share of LCOE
    ax2 = ax1.twinx()
    ax2.set_ylabel('Share of electricity csots at LCOH [%]', fontsize=plotSettings['fontsize'])
    ax2.plot(x, dfPlot['elc ref - median']/0.7/dfPlot['lcoh ref - median']*100, label='Share of LCOH - reference',
             linestyle='--', color=darkblue)
    ax2.plot(x, dfPlot['elc strat - median']/0.7/dfPlot['lcoh strat - median']*100,
             label='Share of LCOH - non-strategic', linestyle='--', color=darkblue, marker='o', markersize=3)
    ax2.plot(x, dfPlot['elc w2p - median']/0.7/dfPlot['lcoh w2p - median']*100, label='Share of LCOH - grey hydrogen',
             linestyle='--', color=darkblue, marker='^', markersize=3)
    ax2.fill_between(x, dfPlot['elc strat - 25%']/0.7/dfPlot['lcoh strat - 75%']*100,
                     dfPlot['elc strat - 75%']/0.7/dfPlot['lcoh strat - 75%']*100, color=darkblue, alpha=0.05,
                     edgecolor=None, hatch='...')
    ax2.fill_between(x, dfPlot['elc w2p - 25%']/0.7/dfPlot['lcoh w2p - 75%']*100,
                     dfPlot['elc w2p - 75%']/0.7/dfPlot['lcoh w2p - 75%']*100, color=darkblue, alpha=0.05,
                     edgecolor=None, hatch='***')


    # Adjust axis
    ax1.minorticks_on()
    ax1.set_xlim(plotSettings['xlim'])
    ax1.set_ylim([0, 500])
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(25))
    ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax1.tick_params(axis='both', which='minor', color='gray')

    ax2.minorticks_on()
    ax2.set_xlim(plotSettings['xlim'])
    ax2.set_ylim([0, 50])
    ax2.set_xticks(plotSettings['xticks'])
    ax2.xaxis.set_minor_locator(MultipleLocator(5))
    ax2.yaxis.set_minor_locator(MultipleLocator(5))
    ax2.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax2.tick_params(axis='both', which='minor', color='gray')

    # Adjust legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    handles = handles1 + handles2
    labels = labels1 + labels2

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.45),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save plot
    plt.savefig(os.getcwd() + '\\figure25a.' + plotType, bbox_inches='tight')

    # Write data
    writeDf = pd.DataFrame(data=[dfPlot['elc ref - median'],
                                 dfPlot['elc strat - median'], dfPlot['elc strat - 25%'], dfPlot['elc strat - 75%'],
                                 dfPlot['elc w2p - median'], dfPlot['elc w2p - 25%'], dfPlot['elc w2p - 75%'],
                                 dfPlot['lcoh ref - median'],
                                 dfPlot['lcoh strat - median'], dfPlot['lcoh strat - 25%'], dfPlot['lcoh strat - 75%'],
                                 dfPlot['lcoh w2p - median'], dfPlot['lcoh w2p - 25%'], dfPlot['lcoh w2p - 75%'],
                                 dfPlot['elc ref - median']/0.7/dfPlot['lcoh ref - median']*100,
                                 dfPlot['elc strat - median']/0.7/dfPlot['lcoh strat - median']*100,
                                 dfPlot['elc strat - 25%']/0.7/dfPlot['lcoh strat - 25%']*100,
                                 dfPlot['elc strat - 75%']/0.7/dfPlot['lcoh strat - 75%']*100,
                                 dfPlot['elc w2p - median']/0.7/dfPlot['lcoh w2p - median']*100,
                                 dfPlot['elc w2p - 25%']/0.7/dfPlot['lcoh w2p - 25%']*100,
                                 dfPlot['elc w2p - 75%']/0.7/dfPlot['lcoh w2p - 75%']*100],
                           index=['Average electricity price for HP reference - median [€/MWh]',
                                  'Average electricity price for HP non strategic - median [€/MWh]',
                                  'Average electricity price for HP non strategic - 25% [€/MWh]',
                                  'Average electricity price for HP non strategic - 75% [€/MWh]',
                                  'Average electricity price for HP w2p - median [€/MWh]',
                                  'Average electricity price for HP w2p - 25% [€/MWh]',
                                  'Average electricity price for HP w2p - 75% [€/MWh]',
                                  'LCOH reference - median [€/MWh]',
                                  'LCOH non strategic - median [€/MWh]',
                                  'LCOH non strategic - 25% [€/MWh]',
                                  'LCOH non strategic - 75% [€/MWh]',
                                  'LCOH w2p - median [€/MWh]',
                                  'LCOH w2p - 25% [€/MWh]',
                                  'LCOH w2p - 75% [€/MWh]',
                                  'Share of electricity costs on LOCH reference case - median',
                                  'Share of electricity costs on LOCH non strategic case - median',
                                  'Share of electricity costs on LOCH non strategic case - 25%',
                                  'Share of electricity costs on LOCH non strategic case - 75%',
                                  'Share of electricity costs on LOCH w2p case - median',
                                  'Share of electricity costs on LOCH w2p case - 25%',
                                  'Share of electricity costs on LOCH w2p case - 75%'])
    writeDf = writeDf.T
    writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure25a.csv', sep=';')


def figure_25b(dfPPRef, dfPPStrat, dfPPW2P, dfHPRef, dfHPStrat, dfHPW2P, dfEPRef, dfEPStrat, dfEPW2P):
    '''
    Function that will create Fig. 25b - Investment thresholds for all type of agents in the obstacle cases.
    :param:
        pd.DataFrame dfPPRef: Daily data from the power producers for the reference case.
        pd.DataFrame dfPPStrat: Daily data from the power producers for the nonstrategic case.
        pd.DataFrame dfPPW2P: Daily data from the power producers for the w2p case.
        pd.DataFrame dfHPRef: Yearly data from the hydrogen producers for the reference case.
        pd.DataFrame dfHPStrat: Yearly data from the hydrogen producers for the nonstrategic case.
        pd.DataFrame dfHPW2P: Yearly data from the hydrogen producers for the w2p case.
        pd.DataFrame dfÉPRef: Yearly data from the electrolyzer producers for the reference case.
        pd.DataFrame dfEPStrat: Yearly data from the electrolyzer producers for the nonstrategic case.
        pd.DataFrame dfEPW2P: Yearly data from the electrolyzer producers for the w2p case.
    :return:
    '''
    # Power producers
    tmpPPRef = dfPPRef.set_index(['Year', 'Run', 'ID'])
    tmpPPStrat = dfPPStrat.set_index(['Year', 'Run', 'ID'])
    tmpPPW2P = dfPPW2P.set_index(['Year', 'Run', 'ID'])
    dfPlotPP = pd.DataFrame(data=np.nan, index=range(yearDelta),
                            columns=['ref - median', 'strat - median', 'strat - max', 'strat - min', 'w2p - median',
                                     'w2p - max', 'w2p - min'])

    # Hydrogen producers
    tmpHPRef = dfHPRef.set_index(['Year', 'Run', 'ID'])
    tmpHPStrat = dfHPStrat.set_index(['Year', 'Run', 'ID'])
    tmpHPW2P = dfHPW2P.set_index(['Year', 'Run', 'ID'])
    dfPlotHP = pd.DataFrame(data=np.nan, index=range(yearDelta),
                            columns=['ref - median', 'strat - median', 'strat - max', 'strat - min', 'w2p - median',
                                     'w2p - max', 'w2p - min'])

    # Electrolyzer producers
    tmpEPRef = dfEPRef.set_index(['Year', 'Run', 'ID'])
    tmpEPStrat = dfEPStrat.set_index(['Year', 'Run', 'ID'])
    tmpEPW2P = dfEPW2P.set_index(['Year', 'Run', 'ID'])
    dfPlotEP = pd.DataFrame(data=np.nan, index=range(yearDelta),
                            columns=['ref - median', 'strat - median', 'strat - max', 'strat - min', 'w2p - median',
                                     'w2p - max', 'w2p - min'])

    for i in range(yearDelta):
        # Power producers
        # Reference case
        if i in tmpPPRef.index.levels[0]:
            tmpDf = tmpPPRef.loc[i]['Investment threshold']
            dfPlotPP.loc[i, 'ref - median'] = tmpDf.median()
        # Non strategic case
        if i in tmpPPStrat.index.levels[0]:
            tmpDf = tmpPPStrat.loc[i]['Investment threshold']
            dfPlotPP.loc[i, 'strat - median'] = tmpDf.median()
            dfPlotPP.loc[i, 'strat - max'] = tmpDf.max()
            dfPlotPP.loc[i, 'strat - min'] = tmpDf.min()
        # W2P case
        if i in tmpPPW2P.index.levels[0]:
            tmpDf = tmpPPW2P.loc[i]['Investment threshold']
            dfPlotPP.loc[i, 'w2p - median'] = tmpDf.median()
            dfPlotPP.loc[i, 'w2p - max'] = tmpDf.max()
            dfPlotPP.loc[i, 'w2p - min'] = tmpDf.min()
        # Hydrogen producers
        # Reference case
        if i in tmpHPRef.index.levels[0]:
            tmpDf = tmpHPRef.loc[i]['Investment threshold']
            dfPlotHP.loc[i, 'ref - median'] = tmpDf.median()
        # Non strategic case
        if i in tmpHPStrat.index.levels[0]:
            tmpDf = tmpHPStrat.loc[i]['Investment threshold']
            dfPlotHP.loc[i, 'strat - median'] = tmpDf.median()
            dfPlotHP.loc[i, 'strat - max'] = tmpDf.max()
            dfPlotHP.loc[i, 'strat - min'] = tmpDf.min()
        # W2P case
        if i in tmpHPW2P.index.levels[0]:
            tmpDf = tmpHPW2P.loc[i]['Investment threshold']
            dfPlotHP.loc[i, 'w2p - median'] = tmpDf.median()
            dfPlotHP.loc[i, 'w2p - max'] = tmpDf.max()
            dfPlotHP.loc[i, 'w2p - min'] = tmpDf.min()
        # Electrolyzer producers
        # Reference case
        if i in tmpEPRef.index.levels[0]:
            tmpDf = tmpEPRef.loc[i]['Investment threshold']
            dfPlotEP.loc[i, 'ref - median'] = tmpDf.median()
        # Non strategic case
        if i in tmpEPStrat.index.levels[0]:
            tmpDf = tmpEPStrat.loc[i]['Investment threshold']
            dfPlotEP.loc[i, 'strat - median'] = tmpDf.median()
            dfPlotEP.loc[i, 'strat - max'] = tmpDf.max()
            dfPlotEP.loc[i, 'strat - min'] = tmpDf.min()
        # W2P case
        if i in tmpEPW2P.index.levels[0]:
            tmpDf = tmpEPW2P.loc[i]['Investment threshold']
            dfPlotEP.loc[i, 'w2p - median'] = tmpDf.median()
            dfPlotEP.loc[i, 'w2p - max'] = tmpDf.max()
            dfPlotEP.loc[i, 'w2p - min'] = tmpDf.min()

    # Figure
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=plotSettings['figsize_3t'],
                                        gridspec_kw=plotSettings['gridspec_kw'], dpi=plotSettings['dpi'], sharex=True)

    # Power producers
    ax1.plot(x, dfPlotPP['ref - median'], label='Power producers - reference', linestyle='-', color=green)
    ax1.plot(x, dfPlotPP['strat - median'], label='Power producers - non-strategic', linestyle=StratLinestyle,
             color=darkgreen)
    ax1.fill_between(x, dfPlotPP['strat - min'], dfPlotPP['strat - max'], color=darkgreen, alpha=0.1, edgecolor=None,
                     hatch=StratHatch)
    ax1.plot(x, dfPlotPP['w2p - median'], label='Power producers - grey hydrogen', linestyle=W2PLinestlye,
             color=darkgreen)
    ax1.fill_between(x, dfPlotPP['w2p - min'], dfPlotPP['w2p - max'], color=darkgreen, alpha=0.1, edgecolor=None,
                    hatch=W2PHatch)
    ax1.set_ylim(-1)
    # Hydrogen producers
    ax2.set_ylabel('Investment threshold [-]', fontsize=plotSettings['fontsize'])
    ax2.plot(x, dfPlotHP['ref - median'], label='Hydrogen producers - reference', linestyle='-', color=blue)
    ax2.plot(x, dfPlotHP['strat - median'], label='Hydrogen producers - non-strategic', linestyle=StratLinestyle,
             color=darkblue)
    ax2.fill_between(x, dfPlotHP['strat - min'], dfPlotHP['strat - max'], color=darkblue, alpha=0.1, edgecolor=None,
                     hatch=StratHatch)
    ax2.plot(x, dfPlotHP['w2p - median'], label='Hydrogen producers - grey hydrogen', linestyle=W2PLinestlye,
             color=darkblue)
    ax2.fill_between(x, dfPlotHP['w2p - min'], dfPlotHP['w2p - max'], color=darkblue, alpha=0.1, edgecolor=None,
                     hatch=W2PHatch)
    ax2.set_ylim(-1)
    # Electrolyzer producers
    ax3.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    ax3.plot(x, dfPlotEP['ref - median'], label='Electrolyzer producers - reference', linestyle='-', color=purple)
    ax3.plot(x, dfPlotEP['strat - median'], label='Electrolyzer producers - non-strategic', linestyle=StratLinestyle,
             color=darkpurple)
    ax3.fill_between(x, dfPlotEP['strat - min'], dfPlotEP['strat - max'], color=darkpurple, alpha=0.1, edgecolor=None,
                     hatch=StratHatch)
    ax3.plot(x, dfPlotEP['w2p - median'], label='Electrolyzer producers - grey hydrogen', linestyle=W2PLinestlye,
             color=darkpurple)
    ax3.fill_between(x, dfPlotEP['w2p - min'], dfPlotEP['w2p - max'], color=darkpurple, alpha=0.1, edgecolor=None,
                     hatch=W2PHatch)
    ax3.set_ylim(-1)

    # Adjust axis
    ax1.minorticks_on()
    ax1.set_xlim(plotSettings['xlim'])
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(0.1))
    ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax1.tick_params(axis='both', which='minor', color='gray')

    ax2.minorticks_on()
    ax2.set_xlim(plotSettings['xlim'])
    ax2.set_xticks(plotSettings['xticks'])
    ax2.xaxis.set_minor_locator(MultipleLocator(5))
    ax2.yaxis.set_minor_locator(MultipleLocator(0.1))
    ax2.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax2.tick_params(axis='both', which='minor', color='gray')

    ax3.minorticks_on()
    ax3.set_xlim(plotSettings['xlim'])
    ax3.set_xticks(plotSettings['xticks'])
    ax3.xaxis.set_minor_locator(MultipleLocator(5))
    ax3.yaxis.set_minor_locator(MultipleLocator(0.1))
    ax3.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax3.tick_params(axis='both', which='minor', color='gray')

    # Adjust legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles3, labels3 = ax3.get_legend_handles_labels()

    handles = handles1 + handles2 + handles3
    labels = labels1 + labels2 + labels3

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.45),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save plot
    plt.savefig(os.getcwd() + '\\figure25b.' + plotType, bbox_inches='tight')

    # Write data
    writeDf = pd.DataFrame(data=[dfPlotPP['ref - median'],
                                 dfPlotPP['strat - median'], dfPlotPP['strat - min'], dfPlotPP['strat - max'],
                                 dfPlotPP['w2p - median'], dfPlotPP['w2p - min'], dfPlotPP['w2p - max'],
                                 dfPlotHP['ref - median'],
                                 dfPlotHP['strat - median'], dfPlotHP['strat - min'], dfPlotHP['strat - max'],
                                 dfPlotHP['w2p - median'], dfPlotHP['w2p - min'], dfPlotHP['w2p - max'],
                                 dfPlotEP['ref - median'],
                                 dfPlotEP['strat - median'], dfPlotEP['strat - min'], dfPlotEP['strat - max'],
                                 dfPlotEP['w2p - median'], dfPlotEP['w2p - min'], dfPlotEP['w2p - max']],
                           index=['Investment threshold PP reference - median [-]',
                                  'Investment threshold PP non strategic - median [-]',
                                  'Investment threshold PP non strategic - min [-]',
                                  'Investment threshold PP non strategic - max [-]',
                                  'Investment threshold PP w2p - median [-]',
                                  'Investment threshold PP w2p - min [-]',
                                  'Investment threshold PP w2p - max [-]',
                                  'Investment threshold HP reference - median [-]',
                                  'Investment threshold HP non strategic - median [-]',
                                  'Investment threshold HP non strategic - min [-]',
                                  'Investment threshold HP non strategic - max [-]',
                                  'Investment threshold HP w2p - median [-]',
                                  'Investment threshold HP w2p - min [-]',
                                  'Investment threshold HP w2p - max [-]',
                                  'Investment threshold EP reference - median [-]',
                                  'Investment threshold EP non strategic - median [-]',
                                  'Investment threshold EP non strategic - min [-]',
                                  'Investment threshold EP non strategic - max [-]',
                                  'Investment threshold EP w2p - median [-]',
                                  'Investment threshold EP w2p - min [-]',
                                  'Investment threshold EP w2p - max [-]'])
    writeDf = writeDf.T
    writeDf.index = x
    writeDf.to_csv(os.getcwd() + '\\figure25b.csv', sep=';')


def figure_26(dfPMRef, dfPMStrat, dfPMW2P, dfHMRef, dfHMStrat, dfHMW2P, dictSens, lstIndex):
    '''
    Function that will create Fig. 26 - Installed Renewables vs installed Electrolyzers for the sensitivity analysis.
    :param:
        pd.DataFrame dfPMRef: Yearly data from the power market for the reference case.
        pd.DataFrame dfPMStrat: Yearly data from the power market for the strategic case.
        pd.DataFrame dfPMW2P: Yearly data from the power market for the willingness to pay case.
        pd.DataFrame dfHMRef: Yearly data from the hydrogen market for the reference case.
        pd.DataFrame dfHMStrat: Yearly data from the hydrogen market sales for the strategic case.
        pd.DataFrame dfHMW2P: Yearly data from the hydrogen market for the willingness to pay case.
        dict dictSens: Dictionary with all Results of the sensitivity analysis (index: [name, w2p, strat, listResults])
        lst lstIndex: List with Index for all cases for the notations in the plots.
    :return:
    '''
    # Write df
    writeDf = pd.DataFrame()

    # Go through years
    for year in yearSense:
        tmpYear = year - year0
        tmpData = []
        # Reference case
        tmpRES, tmpELC = np.nan, np.nan
        tmpDf = dfPMRef.set_index(['Year', 'Run'])
        if tmpYear in tmpDf.index.levels[0]:
            tmpRES = tmpDf.loc[tmpYear, 'Installed capacity Renewables'].median()/1e3
        tmpDf = dfHMRef.set_index(['Year', 'Run'])
        if tmpYear in tmpDf.index.levels[0]:
            tmpELC = tmpDf.loc[tmpYear, 'Installed capacity Electrolyzers'].median()/1e3
        tmpData.append([tmpRES, tmpELC])
        # Strategic case
        tmpRES, tmpELC = np.nan, np.nan
        tmpDf = dfPMStrat.set_index(['Year', 'Run'])
        if tmpYear in tmpDf.index.levels[0]:
            tmpRES = tmpDf.loc[tmpYear, 'Installed capacity Renewables'].median()/1e3
        tmpDf = dfHMStrat.set_index(['Year', 'Run'])
        if tmpYear in tmpDf.index.levels[0]:
            tmpELC = tmpDf.loc[tmpYear, 'Installed capacity Electrolyzers'].median()/1e3
        tmpData.append([tmpRES, tmpELC])
        # W2P case
        tmpRES, tmpELC = np.nan, np.nan
        tmpDf = dfPMW2P.set_index(['Year', 'Run'])
        if tmpYear in tmpDf.index.levels[0]:
            tmpRES = tmpDf.loc[tmpYear, 'Installed capacity Renewables'].median()/1e3
        tmpDf = dfHMW2P.set_index(['Year', 'Run'])
        if tmpYear in tmpDf.index.levels[0]:
            tmpELC = tmpDf.loc[tmpYear, 'Installed capacity Electrolyzers'].median()/1e3
        tmpData.append([tmpRES, tmpELC])
        # Sensitivity analysis
        for i in dictSens:
            tmpRES, tmpELC = np.nan, np.nan
            tmpDf = dictSens[i][-1][8].set_index(['Year', 'Run'])
            if tmpYear in tmpDf.index.levels[0]:
                tmpRES = tmpDf.loc[tmpYear, 'Installed capacity Renewables'].median()/1e3
            tmpDf = dictSens[i][-1][4].set_index(['Year', 'Run'])
            if tmpYear in tmpDf.index.levels[0]:
                tmpELC = tmpDf.loc[tmpYear, 'Installed capacity Electrolyzers'].median()/1e3
            tmpData.append([tmpRES, tmpELC])

        # Plot
        dfPlot = pd.DataFrame(data=tmpData, index=lstIndex, columns=['Renewables', 'Electrolyzers'])

        # Figure
        fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                                dpi=plotSettings['dpi'])

        # Scatter plot
        for index in dfPlot.index:
            if index == 'Ref.':
                tmpMarker = 'ref'
                tmpColor = 'ref'
            elif index == 'Non-strat.':
                tmpMarker = 'strat'
                tmpColor = 'strat'
            elif index == 'Grey H2':
                tmpMarker = 'w2p'
                tmpColor = 'w2p'
            else:
                tmpMarker = round(float(index.split(sep=';')[0].split(sep=':')[1]), 3)
                tmpColor = round(float(index.split(sep=';')[1].split(sep=':')[1]), 3)

            ax1.scatter(dfPlot.loc[index, 'Renewables'], dfPlot.loc[index, 'Electrolyzers'], color=SensColor[tmpColor],
                        edgecolor=None, s=20, marker=SensMarker[tmpMarker])

        # Notation
        #ax1.text(dfPlot.loc['Ref.', 'Renewables'], dfPlot.loc['Ref.', 'Electrolyzers'], 'Ref.',
        #         fontsize=plotSettings['fontsize'], ha='right', va='bottom')
        #ax1.text(dfPlot.loc['Non-strat.', 'Renewables'], dfPlot.loc['Non-strat.', 'Electrolyzers'], 'Non-strat.',
        #         fontsize=plotSettings['fontsize'], ha='right', va='bottom')
        #ax1.text(dfPlot.loc['Grey H2', 'Renewables'], dfPlot.loc['Grey H2', 'Electrolyzers'], 'Grey H2',
        #         fontsize=plotSettings['fontsize'], ha='right', va='bottom')


        # Add box with year
        tmpStr = f'Year:{year}'
        ax1.text(0.05, 0.95, tmpStr, transform=ax1.transAxes, fontsize=plotSettings['fontsize'], va='top', ha='left',
                 bbox=dict(facecolor='white', edgecolor='white'))

        # Adjust axis
        ax1.set_xlabel('Installed Renewables capacity [GW]', fontsize=plotSettings['fontsize'])
        ax1.set_ylabel('Installed Electrolyzers capacity [GW]', fontsize=plotSettings['fontsize'])
        ax1.minorticks_on()
        ax1.xaxis.set_minor_locator(MultipleLocator(25))
        ax1.yaxis.set_minor_locator(MultipleLocator(5))
        ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
        ax1.tick_params(axis='both', which='minor', color='gray')

        # Legend
        for i in SensMarker.keys():
            if i == 'ref':
                tmpLabel = 'Reference'
                tmpColor = black
            elif i == 'strat':
                tmpLabel = 'Non-strategic'
                tmpColor = green
            elif i =='w2p':
                tmpLabel = 'Grey hydrogen'
                tmpColor = purple
            else:
                tmpLabel = str(str(i) + ' €/kg')
                tmpColor = darkgrey
            ax1.scatter(-10, -10, color=tmpColor, edgecolor=None, s=20, marker=SensMarker[i], label=tmpLabel)

        plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.65), fontsize=plotSettings['fontsize'], frameon=False,
                   ncol=3)

        # Color map
        cbar = plt.colorbar(ScalarMappable(cmap=SensCMap), ax=ax1)
        cbar.ax.tick_params(labelsize=plotSettings['fontsize'])
        cbar.set_label('Investment threshold [-]', fontsize=plotSettings['fontsize'])

        ax1.set_xlim([0, 400])
        ax1.set_ylim([0, 50])

        # Save plot
        plt.savefig(os.getcwd() + '\\figure26_' + str(year) + '.' + plotType, bbox_inches='tight')

        # Add to writeDf
        dfPlot.columns = [str('Installed capacity Renewables - ' + str(year) + ' [GW]'),
                          str('Installed capacity Electrolyzers - ' + str(year) + ' [GW]')]
        writeDf = pd.concat([writeDf, dfPlot], axis=1)

    # Write data
    writeDf.to_csv(os.getcwd() + '\\figure26.csv', sep=';')


def figure_27(dfHMRef, dfHMStrat, dfHMW2P, dfEMRef, dfEMStrat, dfEMW2P, dictSens, lstIndex):
    '''
    Function that will create Fig. 27 - Installed Electrolyzers vs installed Factories for the sensitivity analysis.
    :param:
        pd.DataFrame dfHMRef: Yearly data from the hydrogen market for the reference case.
        pd.DataFrame dfHMStrat: Yearly data from the hydrogen market sales for the strategic case.
        pd.DataFrame dfHMW2P: Yearly data from the hydrogen market for the willingness to pay case.
        pd.DataFrame dfEMRef: Yearly data from the electrolyzer market for the reference case.
        pd.DataFrame dfEMStrat: Yearly data from the electrolyzer market for the strategic case.
        pd.DataFrame dfEMW2P: Yearly data from the electrolyzer market for the willingness to pay case.
        dict dictSens: Dictionary with all Results of the sensitivity analysis (index: [name, w2p, strat, listResults])
        lst lstIndex: List with Index for all cases for the notations in the plots.
    :return:
    '''
    # Write df
    writeDf = pd.DataFrame()

    # Go through years
    for year in yearSense:
        tmpYear = year - year0
        tmpData = []
        # Reference case
        tmpELC, tmpFAC = np.nan, np.nan
        tmpDf = dfHMRef.set_index(['Year', 'Run'])
        if tmpYear in tmpDf.index.levels[0]:
            tmpELC = tmpDf.loc[tmpYear, 'Installed capacity Electrolyzers'].median()/1e3
        tmpDf = dfEMRef.set_index(['Year', 'Run'])
        if tmpYear in tmpDf.index.levels[0]:
            tmpFAC = tmpDf.loc[tmpYear, 'Installed capacity Manufacturings'].median()/1e3
        tmpData.append([tmpELC, tmpFAC])
        # Strategic case
        tmpELC, tmpFAC = np.nan, np.nan
        tmpDf = dfHMStrat.set_index(['Year', 'Run'])
        if tmpYear in tmpDf.index.levels[0]:
            tmpELC = tmpDf.loc[tmpYear, 'Installed capacity Electrolyzers'].median()/1e3
        tmpDf = dfEMStrat.set_index(['Year', 'Run'])
        if tmpYear in tmpDf.index.levels[0]:
            tmpFAC = tmpDf.loc[tmpYear, 'Installed capacity Manufacturings'].median()/1e3
        tmpData.append([tmpELC, tmpFAC])
        # W2P case
        tmpELC, tmpFAC = np.nan, np.nan
        tmpDf = dfHMW2P.set_index(['Year', 'Run'])
        if tmpYear in tmpDf.index.levels[0]:
            tmpELC = tmpDf.loc[tmpYear, 'Installed capacity Electrolyzers'].median()/1e3
        tmpDf = dfEMW2P.set_index(['Year', 'Run'])
        if tmpYear in tmpDf.index.levels[0]:
            tmpFAC = tmpDf.loc[tmpYear, 'Installed capacity Manufacturings'].median()/1e3
        tmpData.append([tmpELC, tmpFAC])
        # Sensitivity analysis
        for i in dictSens:
            tmpELC, tmpFAC = np.nan, np.nan
            tmpDf = dictSens[i][-1][4].set_index(['Year', 'Run'])
            if tmpYear in tmpDf.index.levels[0]:
                tmpELC = tmpDf.loc[tmpYear, 'Installed capacity Electrolyzers'].median()/1e3
            tmpDf = dictSens[i][-1][1].set_index(['Year', 'Run'])
            if tmpYear in tmpDf.index.levels[0]:
                tmpFAC = tmpDf.loc[tmpYear, 'Installed capacity Manufacturings'].median()/1e3
            tmpData.append([tmpELC, tmpFAC])

        # Plot
        dfPlot = pd.DataFrame(data=tmpData, index=lstIndex, columns=['Electrolyzers', 'Factories'])

        # Figure
        fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                                dpi=plotSettings['dpi'])

        # Scatter plot
        for index in dfPlot.index:
            if index == 'Ref.':
                tmpMarker = 'ref'
                tmpColor = 'ref'
            elif index == 'Non-strat.':
                tmpMarker = 'strat'
                tmpColor = 'strat'
            elif index == 'Grey H2':
                tmpMarker = 'w2p'
                tmpColor = 'w2p'
            else:
                tmpMarker = round(float(index.split(sep=';')[0].split(sep=':')[1]), 3)
                tmpColor = round(float(index.split(sep=';')[1].split(sep=':')[1]), 3)

            ax1.scatter(dfPlot.loc[index, 'Electrolyzers'], dfPlot.loc[index, 'Factories'], color=SensColor[tmpColor],
                        edgecolor=None, s=20, marker=SensMarker[tmpMarker])

        # Notation
        #ax1.text(dfPlot.loc['Ref.', 'Electrolyzers'], dfPlot.loc['Ref.', 'Factories'], 'Ref.',
        #         fontsize=plotSettings['fontsize'], ha='right', va='bottom')
        #ax1.text(dfPlot.loc['Non-strat.', 'Electrolyzers'], dfPlot.loc['Non-strat.', 'Factories'], 'Non-strat.',
        #         fontsize=plotSettings['fontsize'], ha='right', va='bottom')
        #ax1.text(dfPlot.loc['Grey H2', 'Electrolyzers'], dfPlot.loc['Grey H2', 'Factories'], 'Grey H2',
        #         fontsize=plotSettings['fontsize'], ha='right', va='bottom')

        # Add box with year
        tmpStr = f'Year:{year}'
        ax1.text(0.05, 0.95, tmpStr, transform=ax1.transAxes, fontsize=plotSettings['fontsize'],
                 va='top', ha='left', bbox=dict(facecolor='white', edgecolor='white'))

        # Adjust axis
        ax1.set_xlabel('Installed Electrolyzers capacity [GW]', fontsize=plotSettings['fontsize'])
        ax1.set_ylabel('Installed Factories capacity [GW/year]', fontsize=plotSettings['fontsize'])
        ax1.minorticks_on()
        ax1.xaxis.set_minor_locator(MultipleLocator(5))
        #ax1.yaxis.set_minor_locator(MultipleLocator(1))
        ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
        ax1.tick_params(axis='both', which='minor', color='gray')

        # Legend
        for i in SensMarker.keys():
            if i == 'ref':
                tmpLabel = 'Reference'
                tmpColor = black
            elif i == 'strat':
                tmpLabel = 'Non-strategic'
                tmpColor = green
            elif i == 'w2p':
                tmpLabel = 'Grey hydrogen'
                tmpColor = purple
            else:
                tmpLabel = str(str(i) + ' €/kg')
                tmpColor = darkgrey
            ax1.scatter(-10, -10, color=tmpColor, edgecolor=None, s=20, marker=SensMarker[i], label=tmpLabel)

        plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.65), fontsize=plotSettings['fontsize'], frameon=False,
                   ncol=3)

        # Color map
        cbar = plt.colorbar(ScalarMappable(cmap=SensCMap), ax=ax1)
        cbar.ax.tick_params(labelsize=plotSettings['fontsize'])
        cbar.set_label('Investment threshold [-]', fontsize=plotSettings['fontsize'])
        ax1.set_xlim([0, 50])
        ax1.set_ylim([0, 20])

        # Save plot
        plt.savefig(os.getcwd() + '\\figure27_' + str(year) + '.' + plotType, bbox_inches='tight')

        # Add to writeDf
        dfPlot.columns = [str('Installed capacity Electrolyzers - ' + str(year) + ' [GW]'),
                          str('Installed capacity Factories - ' + str(year) + ' [GW/year]')]
        writeDf = pd.concat([writeDf, dfPlot], axis=1)

    # Write data
    writeDf.to_csv(os.getcwd() + '\\figure27.csv', sep=';')


def figure_28(dfHMRef, dfHMStrat, dfHMW2P, dfSaleRef, dfSaleStrat, dfSaleW2P, dictSens, lstIndex):
    '''
    Function that will create Fig. 28 - Installed Electrolyzers vs cumulative invested money into Electrolyzers for the
    sensitivity analysis.
    :param:
        pd.DataFrame dfHMRef: Yearly data from the hydrogen market for the reference case.
        pd.DataFrame dfHMStrat: Yearly data from the hydrogen market for the strategic investment case.
        pd.DataFrame dfHMW2P: Yearly data from the hydrogen market for the willingness to pay case.
        pd.DataFrame dfSaleRef: Yearly data from the electrolyzer sales for the reference case.
        pd.DataFrame dfSaleStrat: Yearly data from the electrolyzer sales for the strategic case.
        pd.DataFrame dfSaleW2P: Yearly data from the electrolyzer sales for the willingness to pay case.
        dict dictSens: Dictionary with all Results of the sensitivity analysis (index: [name, w2p, strat, listResults])
        lst lstIndex: List with Index for all cases for the notations in the plots.
    :return:
    '''
    # WriteDf
    writeDf = pd.DataFrame()

    # Hydrogen market
    tmpHMRef = dfHMRef.set_index(['Year', 'Run'])
    tmpHMStrat = dfHMStrat.set_index(['Year', 'Run'])
    tmpHMW2P = dfHMW2P.set_index(['Year', 'Run'])
    tmpSaleRef = dfSaleRef.set_index(['Year', 'Run'])
    tmpSaleStrat = dfSaleStrat.set_index(['Year', 'Run'])
    tmpSaleW2P = dfSaleW2P.set_index(['Year', 'Run'])
    tmpSaleCumRef = pd.Series(data=0, index=tmpHMRef.loc[0].index)
    tmpSaleCumStrat = pd.Series(data=0, index=tmpHMRef.loc[0].index)
    tmpSaleCumW2P = pd.Series(data=0, index=tmpHMRef.loc[0].index)
    tmpSaleCumSens = pd.DataFrame(data=0, index=tmpHMRef.loc[0].index, columns=dictSens.keys())

    dfInvest = pd.DataFrame(data=0, index=range(yearDelta), columns=dictSens.keys())
    dfInvest['Ref'] = 0
    dfInvest['Strat'] = 0
    dfInvest['W2P'] = 0

    # Cumulative investment
    for i in range(yearDelta):
        # Reference case
        if i in tmpSaleRef.index.levels[0]:
            tmpDf = tmpSaleRef.loc[i]['Price'] * tmpSaleRef.loc[i]['Capacity']
            tmpDf = tmpDf.groupby(level=0).sum()/1e9
            tmpSaleCumRef = tmpSaleCumRef.add(tmpDf, fill_value=0)
        dfInvest.loc[i, 'Ref'] = tmpSaleCumRef.median()
        # Strategic case
        if i in tmpSaleStrat.index.levels[0]:
            tmpDf = tmpSaleStrat.loc[i]['Price'] * tmpSaleStrat.loc[i]['Capacity']
            tmpDf = tmpDf.groupby(level=0).sum()/1e9
            tmpSaleCumStrat = tmpSaleCumStrat.add(tmpDf, fill_value=0)
        dfInvest.loc[i, 'Strat'] = tmpSaleCumStrat.median()
        # W2P case
        if i in tmpSaleW2P.index.levels[0]:
            tmpDf = tmpSaleW2P.loc[i]['Price'] * tmpSaleW2P.loc[i]['Capacity']
            tmpDf = tmpDf.groupby(level=0).sum()/1e9
            tmpSaleCumW2P = tmpSaleCumW2P.add(tmpDf, fill_value=0)
        dfInvest.loc[i, 'W2P'] = tmpSaleCumW2P.median()
        # Sensitivity analysis
        for j in dictSens.keys():
            tmpSale = dictSens[j][-1][-1]
            tmpSale = tmpSale.set_index(['Year', 'Run'])
            if i in tmpSale.index.levels[0]:
                tmpDf = tmpSale.loc[i]['Price'] * tmpSale.loc[i]['Capacity']
                tmpDf = tmpDf.groupby(level=0).sum()/1e9
                tmpSaleCumSens[j] = tmpSaleCumSens[j].add(tmpDf, fill_value=0)
            dfInvest.loc[i, j] = tmpSaleCumSens[j].median()

    # Go through years
    for year in yearSense:
        tmpYear = year - year0
        tmpData = []
        # Reference case
        tmpELC, tmpINV = np.nan, np.nan
        if tmpYear in tmpHMRef.index.levels[0]:
            tmpELC = tmpHMRef.loc[tmpYear, 'Installed capacity Electrolyzers'].median()/1e3
        if tmpYear in dfInvest.index:
            tmpINV = dfInvest.loc[tmpYear, 'Ref']
        tmpData.append([tmpELC, tmpINV])
        # Strategic case
        tmpELC, tmpINV = np.nan, np.nan
        if tmpYear in tmpHMStrat.index.levels[0]:
            tmpELC = tmpHMStrat.loc[tmpYear, 'Installed capacity Electrolyzers'].median()/1e3
        if tmpYear in dfInvest.index:
            tmpINV = dfInvest.loc[tmpYear, 'Strat']
        tmpData.append([tmpELC, tmpINV])
        # W2P case
        tmpELC, tmpINV = np.nan, np.nan
        if tmpYear in tmpHMW2P.index.levels[0]:
            tmpELC = tmpHMW2P.loc[tmpYear, 'Installed capacity Electrolyzers'].median()/1e3
        if tmpYear in dfInvest.index:
            tmpINV = dfInvest.loc[tmpYear, 'W2P']
        tmpData.append([tmpELC, tmpINV])
        # Sensitivity analysis
        for i in dictSens.keys():
            tmpELC, tmpINV = np.nan, np.nan
            tmpDf = dictSens[i][-1][4].set_index(['Year', 'Run'])
            if tmpYear in tmpDf.index.levels[0]:
                tmpELC = tmpDf.loc[tmpYear, 'Installed capacity Electrolyzers'].median()/1e3
            if tmpYear in dfInvest.index:
                tmpINV = dfInvest.loc[tmpYear, i]
            tmpData.append([tmpELC, tmpINV])

        # Plot
        dfPlot = pd.DataFrame(data=tmpData, index=lstIndex, columns=['Electrolyzers', 'Cumulative investment'])

        # Figure
        fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                                dpi=plotSettings['dpi'])

        # Scatter plot
        for index in dfPlot.index:
            if index == 'Ref.':
                tmpMarker = 'ref'
                tmpColor = 'ref'
            elif index == 'Non-strat.':
                tmpMarker = 'strat'
                tmpColor = 'strat'
            elif index == 'Grey H2':
                tmpMarker = 'w2p'
                tmpColor = 'w2p'
            else:
                tmpMarker = round(float(index.split(sep=';')[0].split(sep=':')[1]), 3)
                tmpColor = round(float(index.split(sep=';')[1].split(sep=':')[1]), 3)

            ax1.scatter(dfPlot.loc[index, 'Electrolyzers'], dfPlot.loc[index, 'Cumulative investment'],
                        color=SensColor[tmpColor], edgecolor=None, s=20, marker=SensMarker[tmpMarker])

        # Notation
        #ax1.text(dfPlot.loc['Ref.', 'Electrolyzers'], dfPlot.loc['Ref.', 'Cumulative investment'], 'Ref.',
        #         fontsize=plotSettings['fontsize'], ha='right', va='bottom')
        #ax1.text(dfPlot.loc['Non-strat.', 'Electrolyzers'], dfPlot.loc['Non-strat.', 'Cumulative investment'], 'Non-strat.',
        #         fontsize=plotSettings['fontsize'], ha='right', va='bottom')
        #ax1.text(dfPlot.loc['Grey H2', 'Electrolyzers'], dfPlot.loc['Grey H2', 'Cumulative investment'], 'Grey H2',
        #         fontsize=plotSettings['fontsize'], ha='right', va='bottom')

        # Add box with year
        tmpStr = f'Year:{year}'
        ax1.text(0.05, 0.95, tmpStr, transform=ax1.transAxes, fontsize=plotSettings['fontsize'],
                 va='top', ha='left', bbox=dict(facecolor='white', edgecolor='white'))

        # Adjust axis
        ax1.set_xlabel('Installed Electrolyzers capacity [GW]', fontsize=plotSettings['fontsize'])
        ax1.set_ylabel('Cumulative investment in Electrolyzers [Bn.€]', fontsize=plotSettings['fontsize'])
        ax1.minorticks_on()
        ax1.xaxis.set_minor_locator(MultipleLocator(25))
        ax1.yaxis.set_minor_locator(MultipleLocator(5))
        ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
        ax1.tick_params(axis='both', which='minor', color='gray')

        # Legend
        for i in SensMarker.keys():
            if i == 'ref':
                tmpLabel = 'Reference'
                tmpColor = black
            elif i == 'strat':
                tmpLabel = 'Non-strategic'
                tmpColor = green
            elif i == 'w2p':
                tmpLabel = 'Grey hydrogen'
                tmpColor = purple
            else:
                tmpLabel = str(str(i) + ' €/kg')
                tmpColor = darkgrey
            ax1.scatter(-10, -10, color=tmpColor, edgecolor=None, s=20, marker=SensMarker[i], label=tmpLabel)

        plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.65), fontsize=plotSettings['fontsize'], frameon=False,
                   ncol=3)

        # Color map
        cbar = plt.colorbar(ScalarMappable(cmap=SensCMap), ax=ax1)
        cbar.ax.tick_params(labelsize=plotSettings['fontsize'])
        cbar.set_label('Investment threshold [-]', fontsize=plotSettings['fontsize'])

        ax1.set_xlim([0, 50])
        ax1.set_ylim([0, 110])

        # Save plot
        plt.savefig(os.getcwd() + '\\figure28_' + str(year) + '.' + plotType, bbox_inches='tight')

        # Add to writeDf
        dfPlot.columns = [str('Installed capacity Electrolyzers - ' + str(year) + ' [GW]'),
                          str('Cumulative investment in Electrolyzers - ' + str(year) + ' [Bn.€]')]
        writeDf = pd.concat([writeDf, dfPlot], axis=1)

    # Write data
    writeDf.to_csv(os.getcwd() + '\\figure28.csv', sep=';')


def figure_29(dfPMRef, dfPMStrat, dfPMW2P, dfHMRef, dfHMStrat, dfHMW2P, dictSens, lstIndex):
    '''
    Function that will create Fig. 29 - Share of RES at general electricity mix vs produced hydrogen for the sensitivity
    analysis.
    :param:
        pd.DataFrame dfPMRef: Daily data from the power market for the reference case.
        pd.DataFrame dfPMStrat: Daily data from the power market for the strategic investment case.
        pd.DataFrame dfPMW2P: Daily data from the power market for the willingness to pay case.
        pd.DataFrame dfHMRef: Daily data from the hydrogen market for the reference case.
        pd.DataFrame dfHMStrat: Daily data from the hydrogen market for the strategic investment case.
        pd.DataFrame dfHMW2P: Daily data from the hydrogen market for the willingness to pay case.
        dict dictSens: Dictionary with all Results of the sensitivity analysis (index: [name, w2p, strat, listResults])
        lst lstIndex: List with Index for all cases for the notations in the plots.
    :return:
    '''
    # WriteDf
    writeDf = pd.DataFrame()

    # Power market
    tmpPMRef = dfPMRef.set_index(['Year', 'Day', 'Run'])
    tmpPMStrat = dfPMStrat.set_index(['Year', 'Day', 'Run'])
    tmpPMW2P = dfPMW2P.set_index(['Year', 'Day', 'Run'])
    # Hydrogen market
    tmpHMRef = dfHMRef.set_index(['Year', 'Day', 'Run'])
    tmpHMStrat = dfHMStrat.set_index(['Year', 'Day', 'Run'])
    tmpHMW2P = dfHMW2P.set_index(['Year', 'Day', 'Run'])

    # Go through years
    for year in yearSense:
        tmpYear = year - year0
        tmpData = []
        # Reference case
        tmpRES, tmpH2 = np.nan, np.nan
        if tmpYear in tmpPMRef.index.levels[0]:
            tmpGT = (tmpPMRef.loc[tmpYear]['Electricity demand others'] -
                     tmpPMRef.loc[tmpYear]['Actual production renewables'])
            tmpGT = tmpGT.mask(tmpGT < 0, 0)
            tmpGT = tmpGT.groupby(level=1).sum().median()
            tmpDemand = tmpPMRef.loc[tmpYear]['Electricity demand others'].groupby(level=1).sum().median()
            tmpDf = tmpGT / tmpDemand * 100
            tmpRES = 100 - tmpDf
        if tmpYear in tmpHMRef.index.levels[0]:
            tmpDf = tmpHMRef.loc[tmpYear]['Actual production electrolyzers'].groupby(level=1).sum()/1e6
            tmpH2 = tmpDf.median()
        tmpData.append([tmpRES, tmpH2])
        # Strategic case
        tmpRES, tmpH2 = np.nan, np.nan
        if tmpYear in tmpPMStrat.index.levels[0]:
            tmpGT = (tmpPMStrat.loc[tmpYear]['Electricity demand others'] -
                     tmpPMStrat.loc[tmpYear]['Actual production renewables'])
            tmpGT = tmpGT.mask(tmpGT < 0, 0)
            tmpGT = tmpGT.groupby(level=1).sum().median()
            tmpDemand = tmpPMStrat.loc[tmpYear]['Electricity demand others'].groupby(level=1).sum().median()
            tmpDf = tmpGT / tmpDemand * 100
            tmpRES = 100 - tmpDf
        if tmpYear in tmpHMStrat.index.levels[0]:
            tmpDf = tmpHMStrat.loc[tmpYear]['Actual production electrolyzers'].groupby(level=1).sum()/1e6
            tmpH2 = tmpDf.median()
        tmpData.append([tmpRES, tmpH2])
        # W2P case
        tmpRES, tmpH2 = np.nan, np.nan
        if tmpYear in tmpPMW2P.index.levels[0]:
            tmpGT = (tmpPMW2P.loc[tmpYear]['Electricity demand others'] -
                     tmpPMW2P.loc[tmpYear]['Actual production renewables'])
            tmpGT = tmpGT.mask(tmpGT < 0, 0)
            tmpGT = tmpGT.groupby(level=1).sum().median()
            tmpDemand = tmpPMW2P.loc[tmpYear]['Electricity demand others'].groupby(level=1).sum().median()
            tmpDf = tmpGT / tmpDemand * 100
            tmpRES = 100 - tmpDf
        if tmpYear in tmpHMW2P.index.levels[0]:
            tmpDf = tmpHMW2P.loc[tmpYear]['Actual production electrolyzers'].groupby(level=1).sum()/1e6
            tmpH2 = tmpDf.median()
        tmpData.append([tmpRES, tmpH2])
        # Sensitivity analysis
        for i in dictSens.keys():
            tmpRES, tmpH2 = np.nan, np.nan
            tmpPM = dictSens[i][-1][7].set_index(['Year', 'Day', 'Run'])
            if tmpYear in tmpPM.index.levels[0]:
                tmpGT = (tmpPM.loc[tmpYear]['Electricity demand others'] -
                         tmpPM.loc[tmpYear]['Actual production renewables'])
                tmpGT = tmpGT.mask(tmpGT < 0, 0)
                tmpGT = tmpGT.groupby(level=1).sum().median()
                tmpDemand = tmpPM.loc[tmpYear]['Electricity demand others'].groupby(level=1).sum().median()
                tmpDf = tmpGT / tmpDemand * 100
                tmpRES = 100 - tmpDf
            tmpHM = dictSens[i][-1][3].set_index(['Year', 'Day', 'Run'])
            if tmpYear in tmpHM.index.levels[0]:
                tmpDf = tmpHM.loc[tmpYear]['Actual production electrolyzers'].groupby(level=1).sum()/1e6
                tmpH2 = tmpDf.median()
            tmpData.append([tmpRES, tmpH2])

        # Plot
        dfPlot = pd.DataFrame(data=tmpData, index=lstIndex, columns=['Renewables', 'H2'])

        # Figure
        fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                                dpi=plotSettings['dpi'])

        # Scatter plot
        for index in dfPlot.index:
            if index == 'Ref.':
                tmpMarker = 'ref'
                tmpColor = 'ref'
            elif index == 'Non-strat.':
                tmpMarker = 'strat'
                tmpColor = 'strat'
            elif index == 'Grey H2':
                tmpMarker = 'w2p'
                tmpColor = 'w2p'
            else:
                tmpMarker = round(float(index.split(sep=';')[0].split(sep=':')[1]), 3)
                tmpColor = round(float(index.split(sep=';')[1].split(sep=':')[1]), 3)

            ax1.scatter(dfPlot.loc[index, 'Renewables'], dfPlot.loc[index, 'H2'], color=SensColor[tmpColor],
                        edgecolor=None, s=20, marker=SensMarker[tmpMarker])

        # Notation
        #ax1.text(dfPlot.loc['Ref.', 'Renewables'], dfPlot.loc['Ref.', 'H2'], 'Ref.',
        #         fontsize=plotSettings['fontsize'], ha='right', va='bottom')
        #ax1.text(dfPlot.loc['Non-strat.', 'Renewables'], dfPlot.loc['Non-strat.', 'H2'], 'Non-strat.',
        #         fontsize=plotSettings['fontsize'], ha='right', va='bottom')
        #ax1.text(dfPlot.loc['Grey H2', 'Renewables'], dfPlot.loc['Grey H2', 'H2'], 'Grey H2',
        #         fontsize=plotSettings['fontsize'], ha='right', va='bottom')

        # Add box with year
        tmpStr = f'Year:{year}'
        ax1.text(0.05, 0.95, tmpStr, transform=ax1.transAxes, fontsize=plotSettings['fontsize'],
                 va='top', ha='left', bbox=dict(facecolor='white', edgecolor='white'))

        # Adjust axis
        ax1.set_xlabel('Share renewables in electricity mix [%]', fontsize=plotSettings['fontsize'])
        ax1.set_ylabel('Hydrogen production [TWh]', fontsize=plotSettings['fontsize'])
        ax1.minorticks_on()
        ax1.xaxis.set_minor_locator(MultipleLocator(10))
        ax1.yaxis.set_minor_locator(MultipleLocator(10))
        ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
        ax1.tick_params(axis='both', which='minor', color='gray')

        # Legend
        for i in SensMarker.keys():
            if i == 'ref':
                tmpLabel = 'Reference'
            elif i == 'strat':
                tmpLabel = 'Non-strategic'
            elif i == 'w2p':
                tmpLabel = 'Grey hydrogen'
            else:
                tmpLabel = str(str(i) + ' €/kg')
            ax1.scatter(-10, -10, color=black, edgecolor=None, s=20, marker=SensMarker[i], label=tmpLabel)

        plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.65), fontsize=plotSettings['fontsize'], frameon=False,
                   ncol=3)

        # Color map
        cbar = plt.colorbar(ScalarMappable(cmap=SensCMap), ax=ax1)
        cbar.ax.tick_params(labelsize=plotSettings['fontsize'])
        cbar.set_label('Investment threshold [-]', fontsize=plotSettings['fontsize'])

        ax1.set_xlim([0, 100])
        ax1.set_ylim([0, 110])

        # Save plot
        plt.savefig(os.getcwd() + '\\figure29_' + str(year) + '.' + plotType, bbox_inches='tight')

        # Add to writeDf
        dfPlot.columns = [str('Share renewables - ' + str(year) + ' [%]'),
                          str('Hydrogen production - ' + str(year) + ' [TWh]')]
        writeDf = pd.concat([writeDf, dfPlot], axis=1)

    # Write data
    writeDf.to_csv(os.getcwd() + '\\figure29.csv', sep=';')


def figure_30(dfPMRef, dfPMStrat, dfPMW2P, dfHMRef, dfHMStrat, dfHMW2P, dictSens, lstIndex):
    '''
    Function that will create Fig. 30 - Weighted electricity price vs hydrogen price
    :param:
        pd.DataFrame dfPMRef: Yearly data from the power market for the reference case.
        pd.DataFrame dfPMStrat: Yearly data from the power market for the strategic investment case.
        pd.DataFrame dfPMW2P: Yearly data from the power market for the willingness to pay case.
        pd.DataFrame dfHMRef: Yearly data from the hydrogen market for the reference case.
        pd.DataFrame dfHMStrat: Yearly data from the hydrogen market for the strategic investment case.
        pd.DataFrame dfHMW2P: Yearly data from the hydrogen market for the willingness to pay case.
        dict dictSens: Dictionary with all Results of the sensitivity analysis (index: [name, w2p, strat, listResults])
        lst lstIndex: List with Index for all cases for the notations in the plots.
    :return:
    '''
    # WriteDf
    writeDf = pd.DataFrame()

    # Power market
    tmpPMRef = dfPMRef.set_index(['Year', 'Run'])
    tmpPMStrat = dfPMStrat.set_index(['Year', 'Run'])
    tmpPMW2P = dfPMW2P.set_index(['Year', 'Run'])
    # Hydrogen market
    tmpHMRef = dfHMRef.set_index(['Year', 'Run'])
    tmpHMStrat = dfHMStrat.set_index(['Year', 'Run'])
    tmpHMW2P = dfHMW2P.set_index(['Year', 'Run'])

    # Go through years
    for year in yearSense:
        tmpYear = year - year0
        tmpData = []
        # Reference case
        tmpELC, tmpH2 = np.nan, np.nan
        if tmpYear in tmpPMRef.index.levels[0]:
            tmpELC = tmpPMRef.loc[tmpYear]['Weighted Price Electricity'].median()
        if tmpYear in tmpHMRef.index.levels[0]:
            tmpH2 = tmpHMRef.loc[tmpYear]['Price Hydrogen'].median()
        tmpData.append([tmpELC, tmpH2, tmpH2*33.3/1e3])
        # Strategic case
        tmpELC, tmpH2 = np.nan, np.nan
        if tmpYear in tmpPMStrat.index.levels[0]:
            tmpELC = tmpPMStrat.loc[tmpYear]['Weighted Price Electricity'].median()
        if tmpYear in tmpHMStrat.index.levels[0]:
            tmpH2 = tmpHMStrat.loc[tmpYear]['Price Hydrogen'].median()
        tmpData.append([tmpELC, tmpH2, tmpH2*33.3/1e3])
        # Reference case
        tmpELC, tmpH2 = np.nan, np.nan
        if tmpYear in tmpPMW2P.index.levels[0]:
            tmpELC = tmpPMW2P.loc[tmpYear]['Weighted Price Electricity'].median()
        if tmpYear in tmpHMW2P.index.levels[0]:
            tmpH2 = tmpHMW2P.loc[tmpYear]['Price Hydrogen'].median()
        tmpData.append([tmpELC, tmpH2, tmpH2*33.3/1e3])
        # Sensitivity analysis
        for i in dictSens.keys():
            tmpELC, tmpH2 = np.nan, np.nan
            tmpDf = dictSens[i][-1][8].set_index(['Year', 'Run'])
            if tmpYear in tmpDf.index.levels[0]:
                tmpELC = tmpDf.loc[tmpYear]['Weighted Price Electricity'].median()
            tmpDf = dictSens[i][-1][4].set_index(['Year', 'Run'])
            if tmpYear in tmpDf.index.levels[0]:
                tmpH2 = tmpDf.loc[tmpYear]['Price Hydrogen'].median()
            tmpData.append([tmpELC, tmpH2, tmpH2*33.3/1e3])

        # Plot
        dfPlot = pd.DataFrame(data=tmpData, index=lstIndex, columns=['ELC', 'H2 - MWh', 'H2 - kg'])

        # Figure
        fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                                dpi=plotSettings['dpi'])

        # Scatter plot
        #ax2 = ax1.twinx()
        for index in dfPlot.index:
            if index == 'Ref.':
                tmpMarker = 'ref'
                tmpColor = 'ref'
            elif index == 'Non-strat.':
                tmpMarker = 'strat'
                tmpColor = 'strat'
            elif index == 'Grey H2':
                tmpMarker = 'w2p'
                tmpColor = 'w2p'
            else:
                tmpMarker = round(float(index.split(sep=';')[0].split(sep=':')[1]), 3)
                tmpColor = round(float(index.split(sep=';')[1].split(sep=':')[1]), 3)

            # €/kg
            ax1.scatter(dfPlot.loc[index, 'ELC'], dfPlot.loc[index, 'H2 - kg'], color=SensColor[tmpColor],
                        edgecolor=None, s=20, marker=SensMarker[tmpMarker])
            # €/MWh
            #ax2.scatter(dfPlot.loc[index, 'ELC'], dfPlot.loc[index, 'H2 - MWh'], color=SensColor[tmpColor],
            #            edgecolor=None, s=20, marker=SensMarker[tmpMarker])

        # Notation
        #ax1.text(dfPlot.loc['Ref.', 'ELC'], dfPlot.loc['Ref.', 'H2 - MWh'], 'Ref.',
        #         fontsize=plotSettings['fontsize'], ha='right', va='bottom')
        #ax1.text(dfPlot.loc['Non-strat.', 'ELC'], dfPlot.loc['Non-strat.', 'H2 - MWh'], 'Non-strat.',
        #         fontsize=plotSettings['fontsize'], ha='right', va='bottom')
        #ax1.text(dfPlot.loc['Grey H2', 'ELC'], dfPlot.loc['Grey H2', 'H2 - MWh'], 'Grey H2',
        #         fontsize=plotSettings['fontsize'], ha='right', va='bottom')

        # Add box with year
        tmpStr = f'Year:{year}'
        ax1.text(0.05, 0.95, tmpStr, transform=ax1.transAxes, fontsize=plotSettings['fontsize'],
                 va='top', ha='left', bbox=dict(facecolor='white', edgecolor='white'))

        # Adjust axis
        ax1.set_xlabel('Weighted electricity price [€/MWh]', fontsize=plotSettings['fontsize'])
        ax1.set_ylabel('Hydrogen price [€/kg]', fontsize=plotSettings['fontsize'])
        ax1.minorticks_on()
        ax1.xaxis.set_minor_locator(MultipleLocator(25))
        ax1.yaxis.set_minor_locator(MultipleLocator(25))
        ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
        ax1.tick_params(axis='both', which='minor', color='gray')
        #ax2.set_ylabel('Hydrogen price [€/MWh]', fontsize=plotSettings['fontsize'])
        #ax2.minorticks_on()
        #ax2.yaxis.set_minor_locator(MultipleLocator(1))
        #ax2.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
        #ax2.tick_params(axis='both', which='minor', color='gray')

        # Legend
        for i in SensMarker.keys():
            if i == 'ref':
                tmpLabel = 'Reference'
                tmpColor = black
            elif i == 'strat':
                tmpLabel = 'Non-strategic'
                tmpColor = green
            elif i == 'w2p':
                tmpLabel = 'Grey hydrogen'
                tmpColor = purple
            else:
                tmpLabel = str(str(i) + ' €/kg')
                tmpColor = darkgrey
            ax1.scatter(-10, -10, color=tmpColor, edgecolor=None, s=20, marker=SensMarker[i], label=tmpLabel)

        plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.65), fontsize=plotSettings['fontsize'], frameon=False,
                   ncol=3)

        # Color map
        cbar = plt.colorbar(ScalarMappable(cmap=SensCMap), ax=ax1)
        cbar.ax.tick_params(labelsize=plotSettings['fontsize'])
        cbar.set_label('Investment threshold [-]', fontsize=plotSettings['fontsize'])

        ax1.set_xlim([0, 70])
        ax1.set_ylim([0, 275*33.3/1e3])
        #ax2.set_ylim([0, 275])

        # Save plot
        plt.savefig(os.getcwd() + '\\figure30_' + str(year) + '.' + plotType, bbox_inches='tight')

        # Add to writeDf
        dfPlot.columns = [str('Weighted electricity price - ' + str(year) + ' [€/MWh]'),
                          str('Hydrogen price - ' + str(year) + ' [€/MWh]'),
                          str('Hydrogen price - ' + str(year) + ' [€/kg]')]
        writeDf = pd.concat([writeDf, dfPlot], axis=1)

    # Write data
    writeDf.to_csv(os.getcwd() + '\\figure30.csv', sep=';')


def figure_31(dfHMRef, dfHMStrat, dfHMW2P, dfEPRef, dfEPStrat, dfEPW2P, dictSens, lstIndex):
    '''
    Function that will create Fig. 31 - Hydrogen price vs minimal electrolyzer production costs for sensitivity
    :param:
        pd.DataFrame dfHMRef: Yearly data from the hydrogen market for the reference case.
        pd.DataFrame dfHMStrat: Yearly data from the hydrogen market for the strategic investment case.
        pd.DataFrame dfHMW2P: Yearly data from the hydrogen market for the willingness to pay case.
        pd.DataFrame dfEPRef: Yearly data from the electrolyzer producers for the reference case.
        pd.DataFrame dfEPStrat: Yearly data from the electrolyzer producers for the strategic case.
        pd.DataFrame dfEPW2P: Yearly data from the electrolyzer producers for the willingness to pay case.
        dict dictSens: Dictionary with all Results of the sensitivity analysis (index: [name, w2p, strat, listResults])
        lst lstIndex: List with Index for all cases for the notations in the plots.
    :return:
    '''
    # WriteDf
    writeDf = pd.DataFrame()

    # Hydrogen market
    tmpHMRef = dfHMRef.set_index(['Year', 'Run'])
    tmpHMStrat = dfHMStrat.set_index(['Year', 'Run'])
    tmpHMW2P = dfHMW2P.set_index(['Year', 'Run'])
    tmpEPRef = dfEPRef.set_index(['Year', 'Run', 'ID'])
    tmpEPStrat = dfEPStrat.set_index(['Year', 'Run', 'ID'])
    tmpEPW2P = dfEPW2P.set_index(['Year', 'Run', 'ID'])

    # Go through years
    for year in yearSense:
        tmpYear = year - year0
        tmpData = []
        # Reference case
        tmpH2, tmpELC = np.nan, np.nan
        if tmpYear in tmpHMRef.index.levels[0]:
            tmpH2 = tmpHMRef.loc[tmpYear]['Price Hydrogen'].median()
        if tmpYear in tmpEPRef.index.levels[0]:
            tmpELC = tmpEPRef.loc[tmpYear]['Minimal costs Electrolyzers'].groupby(level=0).min().median()
        tmpData.append([tmpELC/1e3, tmpH2, tmpH2*33.3/1e3])
        # Strategic case
        tmpH2, tmpELC = np.nan, np.nan
        if tmpYear in tmpHMStrat.index.levels[0]:
            tmpH2 = tmpHMStrat.loc[tmpYear]['Price Hydrogen'].median()
        if tmpYear in tmpEPStrat.index.levels[0]:
            tmpELC = tmpEPStrat.loc[tmpYear]['Minimal costs Electrolyzers'].groupby(level=0).min().median()
        tmpData.append([tmpELC/1e3, tmpH2, tmpH2*33.3/1e3])
        # Willingenss to pay case
        tmpH2, tmpELC = np.nan, np.nan
        if tmpYear in tmpHMW2P.index.levels[0]:
            tmpH2 = tmpHMW2P.loc[tmpYear]['Price Hydrogen'].median()
        if tmpYear in tmpEPW2P.index.levels[0]:
            tmpELC = tmpEPW2P.loc[tmpYear]['Minimal costs Electrolyzers'].groupby(level=0).min().median()
        tmpData.append([tmpELC/1e3, tmpH2, tmpH2*33.3/1e3])
        # Sensitivity analysis
        for i in dictSens.keys():
            tmpH2, tmpELC = np.nan, np.nan
            tmpDf = dictSens[i][-1][4].set_index(['Year', 'Run'])
            if tmpYear in tmpDf.index.levels[0]:
                tmpH2 = tmpDf.loc[tmpYear]['Price Hydrogen'].median()
            tmpDf = dictSens[i][-1][2].set_index(['Year', 'Run', 'ID'])
            if tmpYear in tmpDf.index.levels[0]:
                tmpELC = tmpDf.loc[tmpYear]['Minimal costs Electrolyzers'].groupby(level=0).min().median()
            tmpData.append([tmpELC/1e3, tmpH2, tmpH2 * 33.3/1e3])

        # Plot
        dfPlot = pd.DataFrame(data=tmpData, index=lstIndex, columns=['ELC', 'H2 - MWh', 'H2 - kg'])

        # Figure
        fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                                dpi=plotSettings['dpi'])

        # Scatter plot
        # €/MWh
        ax1.scatter(dfPlot['ELC'], dfPlot['H2 - MWh'], color=darkgreen, edgecolor=None, s=20)
        # €/kg
        ax2 = ax1.twinx()
        ax2.scatter(dfPlot['ELC'], dfPlot['H2 - kg'], color=darkgreen, edgecolor=None, s=20)

        # Notation
        for index in dfPlot.index:
            ax1.text(dfPlot.loc[index, 'ELC'], dfPlot.loc[index, 'H2 - MWh'], index,
                     fontsize=plotSettings['fontsize'], ha='right', va='bottom')

        # Add box with year
        tmpStr = f'Year:{year}'
        ax1.text(0.05, 0.95, tmpStr, transform=ax1.transAxes, fontsize=plotSettings['fontsize'],
                 va='top', ha='left', bbox=dict(facecolor='white', edgecolor='white'))

        # Adjust axis
        ax1.set_xlabel('Electrolyzer production costs [€/kW]', fontsize=plotSettings['fontsize'])
        ax1.set_ylabel('Hydrogen price [€/MWh]', fontsize=plotSettings['fontsize'])
        ax1.set_xlim([0, 5500])
        ax1.set_ylim([0, 275])
        ax1.minorticks_on()
        ax1.xaxis.set_minor_locator(MultipleLocator(500))
        ax1.yaxis.set_minor_locator(MultipleLocator(25))
        ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
        ax1.tick_params(axis='both', which='minor', color='gray')
        ax2.set_ylabel('Hydrogen price [€/kg]', fontsize=plotSettings['fontsize'])
        ax2.set_ylim([0, 275 * 33.3 / 1e3])
        ax2.minorticks_on()
        ax2.yaxis.set_minor_locator(MultipleLocator(1))
        ax2.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
        ax2.tick_params(axis='both', which='minor', color='gray')

        # Save plot
        plt.savefig(os.getcwd() + '\\figure31_' + str(year) + '.' + plotType, bbox_inches='tight')

        # Add to writeDf
        dfPlot.columns = [str('Electrolyzer costs - ' + str(year) + ' [€/kW]'),
                          str('Hydrogen price - ' + str(year) + ' [€/MWh]'),
                          str('Hydrogen price - ' + str(year) + ' [€/kg]')]
        writeDf = pd.concat([writeDf, dfPlot], axis=1)

    # Write data
    writeDf.to_csv(os.getcwd() + '\\figure31.csv', sep=';')


def figure_32(dfHMRef, dfHMStrat, dfHMW2P, dfEMRef, dfEMStrat, dfEMW2P, dictSens, lstIndex):
    '''
    Function that will create Fig. 32 - No. of HP vs No. of EP
    :param:
        pd.DataFrame dfHMRef: Yearly data from the hydrogen market for the reference case.
        pd.DataFrame dfHMStrat: Yearly data from the hydrogen market for the strategic investment case.
        pd.DataFrame dfHMW2P: Yearly data from the hydrogen market for the willingness to pay case.
        pd.DataFrame dfEMRef: Yearly data from the electrolyzer market for the reference case.
        pd.DataFrame dfEMStrat: Yearly data from the electrolyzer market for the strategic case.
        pd.DataFrame dfEMW2P: Yearly data from the electrolyzer market for the willingness to pay case.
        dict dictSens: Dictionary with all Results of the sensitivity analysis (index: [name, w2p, strat, listResults])
        lst lstIndex: List with Index for all cases for the notations in the plots.
    :return:
    '''
    # WriteDf
    writeDf = pd.DataFrame()

    # Hydrogen market
    tmpHMRef = dfHMRef.set_index(['Year', 'Run'])
    tmpHMStrat = dfHMStrat.set_index(['Year', 'Run'])
    tmpHMW2P = dfHMW2P.set_index(['Year', 'Run'])
    tmpEMRef = dfEMRef.set_index(['Year', 'Run'])
    tmpEMStrat = dfEMStrat.set_index(['Year', 'Run'])
    tmpEMW2P = dfEMW2P.set_index(['Year', 'Run'])

    # Go through years
    for year in yearSense:
        tmpYear = year - year0
        tmpData  = []
        # Reference case
        tmpHP, tmpEP = np.nan, np.nan
        if tmpYear in tmpHMRef.index.levels[0]:
            tmpHP = tmpHMRef.loc[tmpYear]['No. of Hydrogenproducers'].median()
        if tmpYear in tmpEMRef.index.levels[0]:
            tmpEP = tmpEMRef.loc[tmpYear]['No. of Electrolyzerproducers'].median()
        tmpData.append([tmpHP, tmpEP])
        # Strategic case
        tmpHP, tmpEP = np.nan, np.nan
        if tmpYear in tmpHMStrat.index.levels[0]:
            tmpHP = tmpHMStrat.loc[tmpYear]['No. of Hydrogenproducers'].median()
        if tmpYear in tmpEMStrat.index.levels[0]:
            tmpEP = tmpEMStrat.loc[tmpYear]['No. of Electrolyzerproducers'].median()
        tmpData.append([tmpHP, tmpEP])
        # Willingness to pay case
        tmpHP, tmpEP = np.nan, np.nan
        if tmpYear in tmpHMW2P.index.levels[0]:
            tmpHP = tmpHMW2P.loc[tmpYear]['No. of Hydrogenproducers'].median()
        if tmpYear in tmpEMW2P.index.levels[0]:
            tmpEP = tmpEMW2P.loc[tmpYear]['No. of Electrolyzerproducers'].median()
        tmpData.append([tmpHP, tmpEP])
        # Sensitivity analysis
        for i in dictSens.keys():
            tmpHP, tmpEP = np.nan, np.nan
            tmpHM = dictSens[i][-1][4].set_index(['Year', 'Run'])
            if tmpYear in tmpHM.index.levels[0]:
                tmpHP = tmpHM.loc[tmpYear]['No. of Hydrogenproducers'].median()
            tmpEM = dictSens[i][-1][1].set_index(['Year', 'Run'])
            if tmpYear in tmpEM.index.levels[0]:
                tmpEP = tmpEM.loc[tmpYear]['No. of Electrolyzerproducers'].median()
            tmpData.append([tmpHP, tmpEP])

        # Plot
        dfPlot = pd.DataFrame(data=tmpData, index=lstIndex, columns=['HP', 'EP'])

        # Figure
        fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                                dpi=plotSettings['dpi'])

        # Scatter plot
        ax1.scatter(dfPlot['HP'], dfPlot['EP'], color=darkgreen, edgecolor=None, s=20)

        # Notation
        for index in dfPlot.index:
            ax1.text(dfPlot.loc[index, 'HP'], dfPlot.loc[index, 'EP'], index,
                     fontsize=plotSettings['fontsize'], ha='right', va='bottom')

        # Add box with year
        tmpStr = f'Year:{year}'
        ax1.text(0.05, 0.95, tmpStr, transform=ax1.transAxes, fontsize=plotSettings['fontsize'],
                 va='top', ha='left', bbox=dict(facecolor='white', edgecolor='white'))

        # Adjust axis
        ax1.set_xlabel('No. of Hydrogen producers', fontsize=plotSettings['fontsize'])
        ax1.set_ylabel('No. of Electrolyzer producers', fontsize=plotSettings['fontsize'])
        ax1.set_xlim([0, 20])
        ax1.set_ylim([0, 5])
        #ax1.minorticks_on()
        #ax1.xaxis.set_minor_locator(MultipleLocator(500))
        #ax1.yaxis.set_minor_locator(MultipleLocator(25))
        ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
        #ax1.tick_params(axis='both', which='minor', color='gray')

        # Save plot
        plt.savefig(os.getcwd() + '\\figure32_' + str(year) + '.' + plotType, bbox_inches='tight')

        # Add to writeDf
        dfPlot.columns = [str('No. of Hydrogen producers - ' + str(year) + ' [-]'),
                          str('No. of Electrolyzer producers - ' + str(year) + ' [-]')]
        writeDf = pd.concat([writeDf, dfPlot], axis=1)

    # Write data
    writeDf.to_csv(os.getcwd() + '\\figure32.csv', sep=';')


def figure_33(dfHPRef, dfHPStrat, dfHPW2P, dfEPRef, dfEPStrat, dfEPW2P, dictSens, lstIndex):
    '''
    Function that will create Fig. 33 - ROI of HP vs ROI of EP
    :param:
        pd.DataFrame dfHPRef: Yearly data from the hydrogen producers for the reference case.
        pd.DataFrame dfHPStrat: Yearly data from the hydrogen producers for the strategic investment case.
        pd.DataFrame dfHPW2P: Yearly data from the hydrogen producers for the willingness to pay case.
        pd.DataFrame dfEPRef: Yearly data from the electrolyzer producers for the reference case.
        pd.DataFrame dfEPStrat: Yearly data from the electrolyzer producers for the strategic case.
        pd.DataFrame dfEPW2P: Yearly data from the electrolyzer producers for the willingness to pay case.
        dict dictSens: Dictionary with all Results of the sensitivity analysis (index: [name, w2p, strat, listResults])
        lst lstIndex: List with Index for all cases for the notations in the plots.
    :return:
    '''
    # WriteDf
    writeDf = pd.DataFrame()

    # Hydrogen market
    tmpHPRef = dfHPRef.set_index(['Year', 'Run', 'ID'])
    tmpHPStrat = dfHPStrat.set_index(['Year', 'Run', 'ID'])
    tmpHPW2P = dfHPW2P.set_index(['Year', 'Run', 'ID'])
    tmpEPRef = dfEPRef.set_index(['Year', 'Run', 'ID'])
    tmpEPStrat = dfEPStrat.set_index(['Year', 'Run', 'ID'])
    tmpEPW2P = dfEPW2P.set_index(['Year', 'Run', 'ID'])

    for year in yearSense:
        tmpYear = year - year0
        tmpData = []
        # Reference case
        tmpHP, tmpEP = np.nan, np.nan
        if tmpYear in tmpHPRef.index.levels[0]:
            tmpHP = tmpHPRef.loc[tmpYear]['Return on Investment'].median()*100
        if tmpYear in tmpEPRef.index.levels[0]:
            tmpEP = tmpEPRef.loc[tmpYear]['Return on Investment'].median()*100
        tmpData.append([tmpHP, tmpEP])
        # Strategic case
        tmpHP, tmpEP = np.nan, np.nan
        if tmpYear in tmpHPStrat.index.levels[0]:
            tmpHP = tmpHPStrat.loc[tmpYear]['Return on Investment'].median()*100
        if tmpYear in tmpEPStrat.index.levels[0]:
            tmpEP = tmpEPStrat.loc[tmpYear]['Return on Investment'].median()*100
        tmpData.append([tmpHP, tmpEP])
        # Willingness to pay case
        tmpHP, tmpEP = np.nan, np.nan
        if tmpYear in tmpHPW2P.index.levels[0]:
            tmpHP = tmpHPW2P.loc[tmpYear]['Return on Investment'].median()*100
        if tmpYear in tmpEPW2P.index.levels[0]:
            tmpEP = tmpEPW2P.loc[tmpYear]['Return on Investment'].median()*100
        tmpData.append([tmpHP, tmpEP])
        # Sensitivity analysis
        for i in dictSens.keys():
            tmpHP = -100
            tmpHM = dictSens[i][-1][5].set_index(['Year', 'Run', 'ID'])
            if tmpYear in tmpHM.index.levels[0]:
                tmpHP = tmpHM.loc[tmpYear]['Return on Investment'].median()*100
            tmpEP = np.nan
            tmpEM = dictSens[i][-1][2].set_index(['Year', 'Run'])
            if tmpYear in tmpEM.index.levels[0]:
                tmpEP = tmpEM.loc[tmpYear]['Return on Investment'].median()*100
            tmpData.append([tmpHP, tmpEP])

        # Plot
        dfPlot = pd.DataFrame(data=tmpData, index=lstIndex, columns=['HP', 'EP'])

        # Figure
        fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                                dpi=plotSettings['dpi'])

        # Scatter plot
        ax1.scatter(dfPlot['HP'], dfPlot['EP'], color=darkgreen, edgecolor=None, s=20)

        # Notation
        for index in dfPlot.index:
            ax1.text(dfPlot.loc[index, 'HP'], dfPlot.loc[index, 'EP'], index,
                     fontsize=plotSettings['fontsize'], ha='right', va='bottom')

        # Add box with year
        tmpStr = f'Year:{year}'
        ax1.text(0.05, 0.95, tmpStr, transform=ax1.transAxes, fontsize=plotSettings['fontsize'],
                 va='top', ha='left', bbox=dict(facecolor='white', edgecolor='white'))

        # Adjust axis
        ax1.set_xlabel('Return on Investment - Hydrogen producers [%]', fontsize=plotSettings['fontsize'])
        ax1.set_ylabel('Return on Investment - Electrolyzers producers [%]', fontsize=plotSettings['fontsize'])
        ax1.set_xlim([0, 25])
        ax1.set_ylim([0, 25])
        ax1.minorticks_on()
        ax1.xaxis.set_minor_locator(MultipleLocator(5))
        ax1.yaxis.set_minor_locator(MultipleLocator(5))
        ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
        ax1.tick_params(axis='both', which='minor', color='gray')

        # Save plot
        plt.savefig(os.getcwd() + '\\figure33_' + str(year) + '.' + plotType, bbox_inches='tight')

        # Add to writeDf
        dfPlot.columns = [str('Return on Investment - Hydrogen producers - ' + str(year) + ' [%]'),
                          str('Return on Investment - Electrolyzers producers - ' + str(year) + ' [%]')]
        writeDf = pd.concat([writeDf, dfPlot], axis=1)

    # Write data
    writeDf.to_csv(os.getcwd() + '\\figure33.csv', sep=';')


def figure_34(dfPMRef, dfPMStrat, dfPMW2P, dfHMRef, dfHMStrat, dfHMW2P, dictSens, lstIndex):
    '''
    Function that will create Fig. 34 - LCOE vs LCOH
    :param:
        pd.DataFrame dfPMRef: Yearly data from the power market for the reference case.
        pd.DataFrame dfPMStrat: Yearly data from the power market for the strategic investment case.
        pd.DataFrame dfPMW2P: Yearly data from the power market for the willingness to pay case.
        pd.DataFrame dfHMRef: Yearly data from the hydrogen market for the reference case.
        pd.DataFrame dfHMStrat: Yearly data from the hydrogen market for the strategic case.
        pd.DataFrame dfHMW2P: Yearly data from the hydrogen market for the willingness to pay case.
        dict dictSens: Dictionary with all Results of the sensitivity analysis (index: [name, w2p, strat, listResults])
        lst lstIndex: List with Index for all cases for the notations in the plots.
    :return:
    '''
    # WriteDf
    writeDf = pd.DataFrame()

    # Power market
    tmpPMRef = dfPMRef.set_index(['Year', 'Run'])
    tmpPMStrat = dfPMStrat.set_index(['Year', 'Run'])
    tmpPMW2P = dfPMW2P.set_index(['Year', 'Run'])

    # Hydrogen market
    tmpHMRef = dfHMRef.set_index(['Year', 'Run'])
    tmpHMStrat = dfHMStrat.set_index(['Year', 'Run'])
    tmpHMW2P = dfHMW2P.set_index(['Year', 'Run'])

    # Go through year
    for year in yearSense:
        tmpYear = year - year0
        tmpData = []
        # Reference case
        tmpLCOE, tmpLCOH = np.nan, np.nan
        if tmpYear in tmpPMRef.index.levels[0]:
            tmpLCOE = tmpPMRef.loc[tmpYear]['LCOE'].median()
        if tmpYear in tmpHMRef.index.levels[0]:
            tmpLCOH = tmpHMRef.loc[tmpYear]['LCOH'].median()
        tmpData.append([tmpLCOE, tmpLCOH])
        # Non strategic case
        tmpLCOE, tmpLCOH = np.nan, np.nan
        if tmpYear in tmpPMStrat.index.levels[0]:
            tmpLCOE = tmpPMStrat.loc[tmpYear]['LCOE'].median()
        if tmpYear in tmpHMStrat.index.levels[0]:
            tmpLCOH = tmpHMStrat.loc[tmpYear]['LCOH'].median()
        tmpData.append([tmpLCOE, tmpLCOH])
        # W2P case
        tmpLCOE, tmpLCOH = np.nan, np.nan
        if tmpYear in tmpPMW2P.index.levels[0]:
            tmpLCOE = tmpPMW2P.loc[tmpYear]['LCOE'].median()
        if tmpYear in tmpHMW2P.index.levels[0]:
            tmpLCOH = tmpHMW2P.loc[tmpYear]['LCOH'].median()
        tmpData.append([tmpLCOE, tmpLCOH])
        # Sensitivity analysis
        for i in dictSens.keys():
            tmpLCOE, tmpLCOH = np.nan, np.nan
            tmpPM = dictSens[i][-1][8].set_index(['Year', 'Run'])
            if tmpYear in tmpPM.index.levels[0]:
                tmpLCOE = tmpPM.loc[tmpYear]['LCOE'].median()
            tmpHM = dictSens[i][-1][4].set_index(['Year', 'Run'])
            if tmpYear in tmpHM.index.levels[0]:
                tmpLCOH = tmpHM.loc[tmpYear]['LCOH'].median()
            tmpData.append([tmpLCOE, tmpLCOH])

        # Plot
        dfPlot = pd.DataFrame(data=tmpData, index=lstIndex, columns=['LCOE', 'LCOH'])

        # Figure
        fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                                dpi=plotSettings['dpi'])

        # Scatter plot
        ax1.scatter(dfPlot['LCOE'], dfPlot['LCOH'], color=darkgreen, edgecolor=None, s=20)

        # Notation
        for index in dfPlot.index:
            ax1.text(dfPlot.loc[index, 'LCOE'], dfPlot.loc[index, 'LCOE'], index,
                     fontsize=plotSettings['fontsize'], ha='right', va='bottom')

        # Add box with year
        tmpStr = f'Year:{year}'
        ax1.text(0.05, 0.95, tmpStr, transform=ax1.transAxes, fontsize=plotSettings['fontsize'],
                 va='top', ha='left', bbox=dict(facecolor='white', edgecolor='white'))

        # Adjust axis
        ax1.set_xlabel('Levelized costs of electricity [€/MWh]', fontsize=plotSettings['fontsize'])
        ax1.set_ylabel('Levelized costs of Hydrogen [€/MWh]', fontsize=plotSettings['fontsize'])
        ax1.set_xlim([0, 200])
        ax1.set_ylim([0, 200])
        ax1.minorticks_on()
        ax1.xaxis.set_minor_locator(MultipleLocator(25))
        ax1.yaxis.set_minor_locator(MultipleLocator(25))
        ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
        ax1.tick_params(axis='both', which='minor', color='gray')

        # Save plot
        plt.savefig(os.getcwd() + '\\figure34_' + str(year) + '.' + plotType, bbox_inches='tight')

        # Add to writeDf
        dfPlot.columns = [str('Levelized costs of Electricity - ' + str(year) + ' [€/MWh]'),
                          str('Levelized costs of Hydrogen - ' + str(year) + ' [€/MWh]')]
        writeDf = pd.concat([writeDf, dfPlot], axis=1)

    # Write data
    writeDf.to_csv(os.getcwd() + '\\figure34.csv', sep=';')


def figure_35(dfPMRef, dfPMStrat, dfPMW2P, dfEPRef, dfEPStrat, dfEPW2P, dictSens, lstIndex):
    '''
    Function that will create Fig. 35 - Average electricity price for HPs vs minimal production costs of EPs
    :param:
        pd.DataFrame dfPMRef: Daily data from the power market for the reference case.
        pd.DataFrame dfPMStrat: Daily data from the power market for the strategic investment case.
        pd.DataFrame dfPMW2P: Daily data from the power market for the willingness to pay case.
        pd.DataFrame dfEPRef: Yearly data from the electrolyzer producers for the reference case.
        pd.DataFrame dfEPStrat: Yearly data from the electrolyzer producers for the strategic case.
        pd.DataFrame dfEPW2P: Yearly data from the electrolyzer producers for the willingness to pay case.
        dict dictSens: Dictionary with all Results of the sensitivity analysis (index: [name, w2p, strat, listResults])
        lst lstIndex: List with Index for all cases for the notations in the plots.
    :return:
    '''
    # WriteDf
    writeDf = pd.DataFrame()

    # Power market
    tmpPMRef = dfPMRef.set_index(['Year', 'Day', 'Run'])
    tmpPMStrat = dfPMStrat.set_index(['Year', 'Day', 'Run'])
    tmpPMW2P = dfPMW2P.set_index(['Year', 'Day', 'Run'])

    # Hydrogen market
    tmpEPRef = dfEPRef.set_index(['Year', 'Run', 'ID'])
    tmpEPStrat = dfEPStrat.set_index(['Year', 'Run', 'ID'])
    tmpEPW2P = dfEPW2P.set_index(['Year', 'Run', 'ID'])

    # Go through years
    for year in yearSense:
        tmpYear = year - year0
        tmpData = []
        # Reference case
        tmpPM, tmpEM = np.nan, np.nan
        if tmpYear in tmpPMRef.index.levels[0]:
            tmpDf = (tmpPMRef.loc[tmpYear]['Electricity demand electrolyzers'] *
                     tmpPMRef.loc[tmpYear]['Price Electricity'])
            tmpDf = (tmpDf.groupby(level=1).sum() /
                     tmpPMRef.loc[tmpYear]['Electricity demand electrolyzers'].groupby(level=1).sum())
            tmpPM = tmpDf.median()
        if tmpYear in tmpEPRef.index.levels[0]:
            tmpEM = tmpEPRef.loc[tmpYear]['Minimal costs Electrolyzers'].groupby(level=0).min().median()
        tmpData.append([tmpPM, tmpEM/1e3])
        # Non strategic case
        tmpPM, tmpEM = np.nan, np.nan
        if tmpYear in tmpPMStrat.index.levels[0]:
            tmpDf = (tmpPMStrat.loc[tmpYear]['Electricity demand electrolyzers'] *
                     tmpPMStrat.loc[tmpYear]['Price Electricity'])
            tmpDf = (tmpDf.groupby(level=1).sum() /
                     tmpPMStrat.loc[tmpYear]['Electricity demand electrolyzers'].groupby(level=1).sum())
            tmpPM = tmpDf.median()
        if tmpYear in tmpEPStrat.index.levels[0]:
            tmpEM = tmpEPStrat.loc[tmpYear]['Minimal costs Electrolyzers'].groupby(level=0).min().median()
        tmpData.append([tmpPM, tmpEM/1e3])
        # W2P case
        tmpPM, tmpEM = np.nan, np.nan
        if tmpYear in tmpPMW2P.index.levels[0]:
            tmpDf = (tmpPMW2P.loc[tmpYear]['Electricity demand electrolyzers'] *
                     tmpPMW2P.loc[tmpYear]['Price Electricity'])
            tmpDf = (tmpDf.groupby(level=1).sum() /
                     tmpPMW2P.loc[tmpYear]['Electricity demand electrolyzers'].groupby(level=1).sum())
            tmpPM = tmpDf.median()
        if tmpYear in tmpEPW2P.index.levels[0]:
            tmpEM = tmpEPW2P.loc[tmpYear]['Minimal costs Electrolyzers'].groupby(level=0).min().median()
        tmpData.append([tmpPM, tmpEM/1e3])
        # Sensitivity analysis
        for i in dictSens.keys():
            tmpPM, tmpEM = np.nan, np.nan
            tmpPMSense = dictSens[i][-1][7].set_index(['Year', 'Day', 'Run'])
            if tmpYear in tmpPMSense.index.levels[0]:
                tmpDf = (tmpPMSense.loc[tmpYear]['Electricity demand electrolyzers'] *
                         tmpPMSense.loc[tmpYear]['Price Electricity'])
                tmpDf = (tmpDf.groupby(level=1).sum() /
                         tmpPMSense.loc[tmpYear]['Electricity demand electrolyzers'].groupby(level=1).sum())
                tmpPM = tmpDf.median()
            tmpEP = dictSens[i][-1][2].set_index(['Year', 'Run', 'ID'])
            if tmpYear in tmpEP.index.levels[0]:
                tmpEM = tmpEP.loc[tmpYear]['Minimal costs Electrolyzers'].groupby(level=0).min().median()
            tmpData.append([tmpPM, tmpEM/1e3])

        # Plot
        dfPlot = pd.DataFrame(data=tmpData, index=lstIndex, columns=['Electricity', 'Electrolyzers'])

        # Figure
        fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                                dpi=plotSettings['dpi'])

        # Scatter plot
        ax1.scatter(dfPlot['Electricity'], dfPlot['Electrolyzers'], color=darkgreen, edgecolor=None, s=20)
        ax1.set_xlim([0, 50])
        ax1.set_ylim([0, 5000])

        # Notation
        for index in dfPlot.index:
            ax1.text(dfPlot.loc[index, 'Electricity'], dfPlot.loc[index, 'Electrolyzers'], index,
                     fontsize=plotSettings['fontsize'], ha='right', va='bottom')

        # Add box with year
        tmpStr = f'Year:{year}'
        ax1.text(0.05, 0.95, tmpStr, transform=ax1.transAxes, fontsize=plotSettings['fontsize'],
                 va='top', ha='left', bbox=dict(facecolor='white', edgecolor='white'))

        # Adjust axis
        ax1.set_xlabel('Average electricity price [€/MWh]', fontsize=plotSettings['fontsize'])
        ax1.set_ylabel('Minimal electrolyzer costs [€/kW]', fontsize=plotSettings['fontsize'])
        ax1.minorticks_on()
        ax1.xaxis.set_minor_locator(MultipleLocator(5))
        ax1.yaxis.set_minor_locator(MultipleLocator(500))
        ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
        ax1.tick_params(axis='both', which='minor', color='gray')

        # Save plot
        plt.savefig(os.getcwd() + '\\figure35_' + str(year) + '.' + plotType, bbox_inches='tight')

        # Add to writeDf
        dfPlot.columns = [str('Average electricity price for HP  - ' + str(year) + ' [€/MWh]'),
                          str('Minimal electrolyzer production costs - ' + str(year) + ' [€/kW]')]
        writeDf = pd.concat([writeDf, dfPlot], axis=1)

        # Write data
    writeDf.to_csv(os.getcwd() + '\\figure35.csv', sep=';')


def figure_36(dfPMRef, dfPMStrat, dfPMW2P, dfSaleRef, dfSaleStrat, dfSaleW2P, dictSens, lstIndex):
    '''
    Function that will create Fig. 36 - Cumulative invested money into Renewables vs cumulative invested money into
    Electrolyzers for the sensitivity analysis.
    :param:
        pd.DataFrame dfPMRef: Yearly data from the power market for the reference case.
        pd.DataFrame dfPMStrat: Yearly data from the power market for the strategic investment case.
        pd.DataFrame dfPMW2P: Yearly data from the power market for the willingness to pay case.
        pd.DataFrame dfSaleRef: Yearly data from the electrolyzer sales for the reference case.
        pd.DataFrame dfSaleStrat: Yearly data from the electrolyzer sales for the strategic case.
        pd.DataFrame dfSaleW2P: Yearly data from the electrolyzer sales for the willingness to pay case.
        dict dictSens: Dictionary with all Results of the sensitivity analysis (index: [name, w2p, strat, listResults])
        lst lstIndex: List with Index for all cases for the notations in the plots.
    :return:
    '''
    # Write DataFrame
    writeDf = pd.DataFrame()

    # Fixed values
    tmpInvestRES = 1250000.

    # Power market
    tmpPMRef = dfPMRef.set_index(['Year', 'Run'])
    tmpPMStrat = dfPMStrat.set_index(['Year', 'Run'])
    tmpPMW2P = dfPMW2P.set_index(['Year', 'Run'])
    tmpPMCumRef = pd.Series(data=0, index=tmpPMRef.loc[0].index)
    tmpPMCumStrat = pd.Series(data=0, index=tmpPMStrat.loc[0].index)
    tmpPMCumW2P = pd.Series(data=0, index=tmpPMW2P.loc[0].index)
    tmpPMCumSens = pd.DataFrame(data=0, index=tmpPMRef.loc[0].index, columns=dictSens.keys())

    # Hydrogen market
    tmpSaleRef = dfSaleRef.set_index(['Year', 'Run'])
    tmpSaleStrat = dfSaleStrat.set_index(['Year', 'Run'])
    tmpSaleW2P = dfSaleW2P.set_index(['Year', 'Run'])
    tmpSaleCumRef = pd.Series(data=0, index=tmpPMRef.loc[0].index)
    tmpSaleCumStrat = pd.Series(data=0, index=tmpPMRef.loc[0].index)
    tmpSaleCumW2P = pd.Series(data=0, index=tmpPMRef.loc[0].index)
    tmpSaleCumSens = pd.DataFrame(data=0, index=tmpPMRef.loc[0].index, columns=dictSens.keys())

    dfInvestPM = pd.DataFrame(data=0, index=range(yearDelta), columns=dictSens.keys())
    dfInvestPM['Ref'] = 0
    dfInvestPM['Strat'] = 0
    dfInvestPM['W2P'] = 0
    dfInvestHM = dfInvestPM.copy(deep=True)

    # Cumulative investment
    for i in range(yearDelta):
        # Reference case
        # Power market
        if i in tmpPMRef.index.levels[0]:
            tmpDf = tmpPMRef.loc[i]['Added capacity Renewables'] * tmpInvestRES / 1e9
            tmpPMCumRef = tmpPMCumRef + tmpDf
        dfInvestPM.loc[i, 'Ref'] = tmpPMCumRef.median()
        # Hydrogen market
        if i in tmpSaleRef.index.levels[0]:
            tmpDf = tmpSaleRef.loc[i]['Price'] * tmpSaleRef.loc[i]['Capacity']
            tmpDf = tmpDf.groupby(level=0).sum()/1e9
            tmpSaleCumRef = tmpSaleCumRef.add(tmpDf, fill_value=0)
        dfInvestHM.loc[i, 'Ref'] = tmpSaleCumRef.median()
        # Non-strategic case
        # Power market
        if i in tmpPMStrat.index.levels[0]:
            tmpDf = tmpPMStrat.loc[i]['Added capacity Renewables'] * tmpInvestRES / 1e9
            tmpPMCumStrat = tmpPMCumStrat + tmpDf
        dfInvestPM.loc[i, 'Strat'] = tmpPMCumStrat.median()
        # Hydrogen market
        if i in tmpSaleStrat.index.levels[0]:
            tmpDf = tmpSaleStrat.loc[i]['Price'] * tmpSaleStrat.loc[i]['Capacity']
            tmpDf = tmpDf.groupby(level=0).sum()/1e9
            tmpSaleCumStrat = tmpSaleCumStrat.add(tmpDf, fill_value=0)
        dfInvestHM.loc[i, 'Strat'] = tmpSaleCumStrat.median()
        # Grey hydrogen case
        # Power market
        if i in tmpPMW2P.index.levels[0]:
            tmpDf = tmpPMW2P.loc[i]['Added capacity Renewables'] * tmpInvestRES / 1e9
            tmpPMCumW2P = tmpPMCumW2P + tmpDf
        dfInvestPM.loc[i, 'W2P'] = tmpPMCumW2P.median()
        # Hydrogen market
        if i in tmpSaleW2P.index.levels[0]:
            tmpDf = tmpSaleW2P.loc[i]['Price'] * tmpSaleW2P.loc[i]['Capacity']
            tmpDf = tmpDf.groupby(level=0).sum()/1e9
            tmpSaleCumW2P = tmpSaleCumW2P.add(tmpDf, fill_value=0)
        dfInvestHM.loc[i, 'W2P'] = tmpSaleCumW2P.median()
        # Sensitivity analysis
        for j in dictSens.keys():
            # Power market
            tmpPM = dictSens[j][-1][8]
            tmpPM = tmpPM.set_index(['Year', 'Run'])
            if i in tmpPM.index.levels[0]:
                tmpDf = tmpPM.loc[i]['Added capacity Renewables'] * tmpInvestRES / 1e9
                tmpPMCumSens[j] = tmpPMCumSens[j] + tmpDf
            dfInvestPM.loc[i, j] = tmpPMCumSens[j].median()
            # Hydrogen market
            tmpSale = dictSens[j][-1][-1]
            tmpSale = tmpSale.set_index(['Year', 'Run'])
            if i in tmpSale.index.levels[0]:
                tmpDf = tmpSale.loc[i]['Price'] * tmpSale.loc[i]['Capacity']
                tmpDf = tmpDf.groupby(level=0).sum()/1e9
                tmpSaleCumSens[j] = tmpSaleCumSens[j].add(tmpDf, fill_value=0)
            dfInvestHM.loc[i, j] = tmpSaleCumSens[j].median()

    # Go through years
    for year in yearSense:
        tmpYear = year - year0
        tmpData = []
        # Reference case
        tmpRES, tmpELC = np.nan, np.nan
        if tmpYear in dfInvestPM.index:
            tmpRES = dfInvestPM.loc[tmpYear, 'Ref']
        if tmpYear in dfInvestHM.index:
            tmpELC = dfInvestHM.loc[tmpYear, 'Ref']
        tmpData.append([tmpRES, tmpELC])
        # Non-strategic case
        tmpRES, tmpELC = np.nan, np.nan
        if tmpYear in dfInvestPM.index:
            tmpRES = dfInvestPM.loc[tmpYear, 'Strat']
        if tmpYear in dfInvestHM.index:
            tmpELC = dfInvestHM.loc[tmpYear, 'Strat']
        tmpData.append([tmpRES, tmpELC])
        # Grey hydrogen case
        tmpRES, tmpELC = np.nan, np.nan
        if tmpYear in dfInvestPM.index:
            tmpRES = dfInvestPM.loc[tmpYear, 'W2P']
        if tmpYear in dfInvestHM.index:
            tmpELC = dfInvestHM.loc[tmpYear, 'W2P']
        tmpData.append([tmpRES, tmpELC])
        # Sensitivity case
        for i in dictSens.keys():
            tmpRES, tmpELC = np.nan, np.nan
            if tmpYear in dfInvestPM.index:
                tmpRES = dfInvestPM.loc[tmpYear, i]
            if tmpYear in dfInvestHM.index:
                tmpELC = dfInvestHM.loc[tmpYear, i]
                tmpData.append([tmpRES, tmpELC])

        # Plot
        dfPlot = pd.DataFrame(data=tmpData, index=lstIndex, columns=['Renewables', 'Electrolyzers'])

        # Figure
        fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                                dpi=plotSettings['dpi'])

        # Scatter plot
        for index in dfPlot.index:
            if index == 'Ref.':
                tmpMarker = 'ref'
                tmpColor = 'ref'
            elif index == 'Non-strat.':
                tmpMarker = 'strat'
                tmpColor = 'strat'
            elif index == 'Grey H2':
                tmpMarker = 'w2p'
                tmpColor = 'w2p'
            else:
                tmpMarker = round(float(index.split(sep=';')[0].split(sep=':')[1]), 3)
                tmpColor = round(float(index.split(sep=';')[1].split(sep=':')[1]), 3)

            ax1.scatter(dfPlot.loc[index, 'Renewables'], dfPlot.loc[index, 'Electrolyzers'], color=SensColor[tmpColor],
                        edgecolor=None, s=20, marker=SensMarker[tmpMarker])

        # Notation
        #ax1.text(dfPlot.loc['Ref.', 'Renewables'], dfPlot.loc['Ref.', 'Electrolyzers'], 'Ref.',
        #         fontsize=plotSettings['fontsize'], ha='right', va='bottom')
        #ax1.text(dfPlot.loc['Non-strat.', 'Renewables'], dfPlot.loc['Non-strat.', 'Electrolyzers'], 'Non-strat.',
        #         fontsize=plotSettings['fontsize'], ha='right', va='bottom')
        #ax1.text(dfPlot.loc['Grey H2', 'Renewables'], dfPlot.loc['Grey H2', 'Electrolyzers'], 'Grey H2',
        #         fontsize=plotSettings['fontsize'], ha='right', va='bottom')

        # Add box with year
        tmpStr = f'Year:{year}'
        ax1.text(0.05, 0.95, tmpStr, transform=ax1.transAxes, fontsize=plotSettings['fontsize'],
                 va='top', ha='left', bbox=dict(facecolor='white', edgecolor='white'))

        # Adjust axis
        ax1.set_xlabel('Cumulative investment in Renewables [Bn.€]', fontsize=plotSettings['fontsize'])
        ax1.set_ylabel('Cumulative investment in Electrolyzers [Bn.€]', fontsize=plotSettings['fontsize'])
        ax1.minorticks_on()
        ax1.xaxis.set_minor_locator(MultipleLocator(25))
        ax1.yaxis.set_minor_locator(MultipleLocator(5))
        ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
        ax1.tick_params(axis='both', which='minor', color='gray')

        # Legend
        for i in SensMarker.keys():
            if i == 'ref':
                tmpLabel = 'Reference'
                tmpColor = black
            elif i == 'strat':
                tmpLabel = 'Non-strategic'
                tmpColor = green
            elif i == 'w2p':
                tmpLabel = 'Grey hydrogen'
                tmpColor = purple
            else:
                tmpLabel = str(str(i) + ' €/kg')
                tmpColor = darkgrey
            ax1.scatter(-10, -10, color=tmpColor, edgecolor=None, s=20, marker=SensMarker[i], label=tmpLabel)

        plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.65), fontsize=plotSettings['fontsize'], frameon=False,
                   ncol=3)

        # Color map
        cbar = plt.colorbar(ScalarMappable(cmap=SensCMap), ax=ax1)
        cbar.ax.tick_params(labelsize=plotSettings['fontsize'])
        cbar.set_label('Investment threshold [-]', fontsize=plotSettings['fontsize'])

        ax1.set_xlim([0, 1100])
        ax1.set_ylim([0, 110])
        # Save plot
        plt.savefig(os.getcwd() + '\\figure36_' + str(year) + '.' + plotType, bbox_inches='tight')

        # Add to writeDf
        dfPlot.columns = [str('Cumulative investment in Renewables - ' + str(year) + ' [Bn.€]'),
                          str('Cumulative investment in Electrolyzers - ' + str(year) + ' [Bn.€]')]
        writeDf = pd.concat([writeDf, dfPlot], axis=1)

        # Write data
    writeDf.to_csv(os.getcwd() + '\\figure36.csv', sep=';')


def figure_37(dictSens):
    '''
    Function that will create Fig. 37 - Colormap of installed electrolyzers.
    :param:
        dict dictSens: Dictionary with all Results of the sensitivity analysis (index: [name, w2p, strat, listResults])
    :return:
    '''

    # Columns - w2p; Index - strat
    tmpColumns = []
    tmpIndex = []
    for i in dictSens:
        tmpColumns.append(round(float(dictSens[i][1]), 1))
        tmpIndex.append(round(float(dictSens[i][2]), 1))
    tmpColumns = list(set(tmpColumns))
    tmpIndex = list(set(tmpIndex))
    tmpColumns.sort()
    tmpIndex.sort()

    # Write DataFrame
    writeDf = pd.DataFrame()

    # Go through years
    for year in yearSense:
        tmpYear = year - year0
        dfPlot = pd.DataFrame(data=np.nan, index=tmpIndex, columns=tmpColumns)
        # Sensitivity analysis
        for i in dictSens:
            tmpELC = np.nan
            tmpCol, tmpInd = round(float(dictSens[i][1]), 1), round(float(dictSens[i][2]), 1)
            tmpDf = dictSens[i][-1][4].set_index(['Year', 'Run'])
            if tmpYear in tmpDf.index.levels[0]:
                tmpELC = tmpDf.loc[tmpYear, 'Installed capacity Electrolyzers'].median() / 1e3
            dfPlot.loc[tmpInd, tmpCol] = tmpELC

        # Plot
        # Figure
        fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                                dpi=plotSettings['dpi'])

        # Heatmap
        hm = sb.heatmap(dfPlot, ax=ax1, cmap=HeatCMap, vmin=0, vmax=50)

        # Adjust axis
        ax1.set_xlabel('Maximum willingness to pay for green hydrogen [€/kg]', fontsize=plotSettings['fontsize'])
        ax1.set_ylabel('Minimum investment threshold [-]', fontsize=plotSettings['fontsize'])
        ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
        #ax1.set_xlim(3, 8)
        #ax1.set_ylim(-0.9, 0)
        #ax1.set_xticklabels(['3', '4', '5', '6', '7', '8'])
        #ax1.set_yticklabels(['-1', '-0.9', '5', '6', '7', '8'])

        # Adjust colorbar
        tmpColorBar = hm.collections[0].colorbar
        tmpColorBar.set_ticks([10, 20, 30, 40])
        tmpColorBar.ax.tick_params(labelsize=plotSettings['fontsize'])
        tmpColorBar.set_label('Installed electrolyzers in 2050 [GW]', fontsize=plotSettings['fontsize'])

        # Save plot
        plt.savefig(os.getcwd() + '\\figure37_' + str(year) + '.' + plotType, bbox_inches='tight')

        # Add to writeDf
        tmpCol = []
        for i in dfPlot.columns:
            tmpCol.append(str(str(i) + ' - ' + str(year)))
        dfPlot.columns = tmpCol
        writeDf = pd.concat([writeDf, dfPlot], axis=1)

    # Write Data
    writeDf.to_csv(os.getcwd() + '\\figure37.csv', sep=';')


def figure_38(dictSens):
    '''
    Function that will create Fig. 38 - Colormap of weighted electricity price.
    :param:
        dict dictSens: Dictionary with all Results of the sensitivity analysis (index: [name, w2p, strat, listResults])
    :return:
    '''
    # Write DataFrame
    writeDf = pd.DataFrame()

    # Columns - w2p; Index - strat
    tmpColumns = []
    tmpIndex = []
    for i in dictSens:
        tmpColumns.append(round(float(dictSens[i][1]), 1))
        tmpIndex.append(round(float(dictSens[i][2]), 1))
    tmpColumns = list(set(tmpColumns))
    tmpIndex = list(set(tmpIndex))
    tmpColumns.sort()
    tmpIndex.sort()

    # Go through years
    for year in yearSense:
        tmpYear = year - year0
        dfPlot = pd.DataFrame(data=np.nan, index=tmpIndex, columns=tmpColumns)
        # Sensitivity analysis
        for i in dictSens:
            tmpELC = np.nan
            tmpCol, tmpInd = round(float(dictSens[i][1]), 1), round(float(dictSens[i][2]), 1)
            tmpDf = dictSens[i][-1][8].set_index(['Year', 'Run'])
            if tmpYear in tmpDf.index.levels[0]:
                tmpELC = tmpDf.loc[tmpYear]['Weighted Price Electricity'].median()
            dfPlot.loc[tmpInd, tmpCol] = tmpELC

        # Plot
        # Figure
        fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                                dpi=plotSettings['dpi'])

        # Heatmap
        hm = sb.heatmap(dfPlot, ax=ax1, cmap=HeatCMapReverse) #, vmin=50, vmax=90)

        # Adjust axis
        ax1.set_xlabel('Willingness to pay for green hydrogen [€/kg]', fontsize=plotSettings['fontsize'])
        ax1.set_ylabel('Investment threshold [-]', fontsize=plotSettings['fontsize'])
        ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
        # ax1.set_xlim(3, 8)
        # ax1.set_ylim(-0.9, 0)

        # Adjust colorbar
        tmpColorBar = hm.collections[0].colorbar
        #tmpColorBar.set_ticks([55, 60, 65, 70, 75, 80, 85])
        tmpColorBar.ax.tick_params(labelsize=plotSettings['fontsize'])
        tmpColorBar.set_label('Weighted electricity price [€/MWh]', fontsize=plotSettings['fontsize'])

        # Save plot
        plt.savefig(os.getcwd() + '\\figure38_' + str(year) + '.' + plotType, bbox_inches='tight')

        # Add to writeDf
        tmpCol = []
        for i in dfPlot.columns:
            tmpCol.append(str(str(i) + ' - ' + str(year)))
        dfPlot.columns = tmpCol
        writeDf = pd.concat([writeDf, dfPlot], axis=1)

    # Write Data
    writeDf.to_csv(os.getcwd() + '\\figure38.csv', sep=';')


def figure_39(dictSens):
    '''
    Function that will create Fig. 39 - Colormap of cumulative investment.
    :param:
        dict dictSens: Dictionary with all Results of the sensitivity analysis (index: [name, w2p, strat, listResults])
    :return:
    '''
    # Investment costs
    tmpInvestRES = 1250000.
    tmpInvestFAC = 500000.

    # Write DataFrame
    writeDf = pd.DataFrame()

    # Columns - w2p; Index - strat
    tmpColumns = []
    tmpIndex = []
    for i in dictSens:
        tmpColumns.append(round(float(dictSens[i][1]), 1))
        tmpIndex.append(round(float(dictSens[i][2]), 1))
    tmpColumns = list(set(tmpColumns))
    tmpIndex = list(set(tmpIndex))
    tmpColumns.sort()
    tmpIndex.sort()

    dfInvest = pd.DataFrame(data=0, index=range(yearDelta), columns=dictSens.keys())
    dfInvestCum = pd.DataFrame(data=0, index=range(yearDelta), columns=dictSens.keys())

    # Cumulative investment
    for i in range(yearDelta):
        # Sensitivity analysis
        for j in dictSens.keys():
            tmpInvest = 0.
            # Renewables
            tmpPM = dictSens[j][-1][8]
            tmpPM = tmpPM.set_index(['Year', 'Run'])
            if i in tmpPM.index.levels[0]:
                tmpDf = tmpPM.loc[i]['Added capacity Renewables'] * tmpInvestRES / 1e9
                tmpInvest = tmpDf.median()
            # Electrolyzers
            tmpSale = dictSens[j][-1][-1]
            tmpSale = tmpSale.set_index(['Year', 'Run'])
            if i in tmpSale.index.levels[0]:
                tmpDf = tmpSale.loc[i]['Price'] * tmpSale.loc[i]['Capacity']
                tmpDf = tmpDf.groupby(level=0).sum() / 1e9
                tmpInvest = tmpInvest + tmpDf.median()
            # Factories
            tmpEM = dictSens[j][-1][1]
            tmpEM = tmpEM.set_index(['Year', 'Run'])
            if i in tmpEM.index.levels[0]:
                tmpDf = tmpEM.loc[i]['Added capacity Manufacturings'] * tmpInvestFAC / 1e9
                tmpInvest = tmpInvest + tmpDf.median()

            # Yearly investment
            dfInvest.loc[i, j] = tmpInvest

            # Cumulative investment
            if i == 0:
                dfInvestCum.loc[i, j] = tmpInvest
            else:
                dfInvestCum.loc[i, j] = dfInvestCum.loc[i-1, j] + tmpInvest

    # Go through years
    for year in yearSense:
        tmpYear = year - year0
        dfPlot = pd.DataFrame(data=np.nan, index=tmpIndex, columns=tmpColumns)

        # Sensitivity analysis
        for i in dictSens:
            tmpInvest = np.nan
            tmpCol, tmpInd = round(float(dictSens[i][1]), 1), round(float(dictSens[i][2]), 1)
            if tmpYear in dfInvestCum.index:
                tmpInvest = dfInvestCum.loc[tmpYear, i]
            dfPlot.loc[tmpInd, tmpCol] = tmpInvest

        # Plot
        # Figure
        fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                                dpi=plotSettings['dpi'])

        # Heatmap
        hm = sb.heatmap(dfPlot, ax=ax1, cmap=HeatCMapReverse)  # , vmin=50, vmax=90)

        # Adjust axis
        ax1.set_xlabel('Willingness to pay for green hydrogen [€/kg]', fontsize=plotSettings['fontsize'])
        ax1.set_ylabel('Investment threshold [-]', fontsize=plotSettings['fontsize'])
        ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
        # ax1.set_xlim(3, 8)
        # ax1.set_ylim(-0.9, 0)

        # Adjust colorbar
        tmpColorBar = hm.collections[0].colorbar
        # tmpColorBar.set_ticks([55, 60, 65, 70, 75, 80, 85])
        tmpColorBar.ax.tick_params(labelsize=plotSettings['fontsize'])
        tmpColorBar.set_label('Cumulative investment [bn. €]', fontsize=plotSettings['fontsize'])

        # Save plot
        plt.savefig(os.getcwd() + '\\figure39_' + str(year) + '.' + plotType, bbox_inches='tight')

        # Add to writeDf
        tmpCol = []
        for i in dfPlot.columns:
            tmpCol.append(str(str(i) + ' - ' + str(year)))
        dfPlot.columns = tmpCol
        writeDf = pd.concat([writeDf, dfPlot], axis=1)

    # Write Data
    writeDf.to_csv(os.getcwd() + '\\figure39.csv', sep=';')


def figure_d1(dfPM, dfHM, dfEM):
    '''
    Function that will create Fig. D1 - Installed capacities sensitivity analysis learning rate.
    :param:
        pd.DataFrame dfPM: Yearly data from the power market.
        pd.DataFrame dfHM: Yearly data from the hydrogen market.
        pd.DataFrame dfEM: Yearly data from the electrolyzer market.
    :return:
    '''
    # Installed renewables
    tmpPM = dfPM.set_index(['Year', 'Sensitivity', 'Run'])

    # Installed electrolyzers
    tmpHM = dfHM.set_index(['Year', 'Sensitivity', 'Run'])

    # Installede manufacturing
    tmpEM = dfEM.set_index(['Year', 'Sensitivity', 'Run'])

    # Plot data
    tmpIndex = pd.MultiIndex.from_product([range(yearDelta), range(1,101)], names=['Year', 'Sensitivity'])
    dfPlot = pd.DataFrame(data=np.nan, index=tmpIndex, columns=['Renewables', 'Electrolyzers', 'Manufacturings'])

    for i in range(yearDelta):
        # Renewables
        if i in tmpPM.index.levels[0]:
            tmpDf = tmpPM.loc[i]['Installed capacity Renewables']
            for j in tmpDf.groupby(level=0).median().index:
                dfPlot['Renewables'][i][j] = tmpDf.groupby(level=0).median().loc[j]
        # Electrolyzers
        if i in tmpHM.index.levels[0]:
            tmpDf = tmpHM.loc[i]['Installed capacity Electrolyzers']
            for j in tmpDf.groupby(level=0).median().index:
                dfPlot['Electrolyzers'][i][j] = tmpDf.groupby(level=0).median().loc[j]
        # Manufacturing
        if i in tmpEM.index.levels[0]:
            tmpDf = tmpEM.loc[i]['Installed capacity Manufacturings']
            for j in tmpDf.groupby(level=0).median().index:
                dfPlot['Manufacturings'][i][j] = tmpDf.groupby(level=0).median().loc[j]

    # Figure
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=plotSettings['figsize_3t'],
                                        gridspec_kw=plotSettings['gridspec_kw'], dpi=plotSettings['dpi'], sharex=True)

    # Results data
    for i in range(1, 10, 2):
        tmpAlpha = 0.25 + 0.75 * (i - 1) / 8
        # Renewables
        ax1.plot(x, dfPlot['Renewables'].xs(i, level='Sensitivity')/1e3, linestyle='-', color=green, alpha=tmpAlpha)
        # Electrolyzers
        ax2.plot(x, dfPlot['Electrolyzers'].xs(i, level='Sensitivity')/1e3, linestyle='-', color=blue, alpha=tmpAlpha)
        # Manufacturings
        ax3.plot(x, dfPlot['Manufacturings'].xs(i, level='Sensitivity')/1e3, linestyle='-', color=purple, alpha=tmpAlpha)


    # Labels
    ax1.set_ylabel('Renewables [GW]', fontsize=plotSettings['fontsize'])
    ax2.set_ylabel('Electrolyzers [GW]', fontsize=plotSettings['fontsize'])
    ax3.set_ylabel('Electrolyzer manufacturing [GW/year]', fontsize=plotSettings['fontsize'])
    ax3.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    fig.text(-0.1, 0.5, 'Installed capacities', va='center', rotation='vertical', fontsize=plotSettings['fontsize'])

    # Limits
    plt.xlim(plotSettings['xlim'])
    ax1.set_ylim(plotSettings['ylim_res_cap'])
    ax2.set_ylim(plotSettings['ylim_elc_cap'])
    ax3.set_ylim(plotSettings['ylim_fac_cap'])

    # Adjust ticks
    ax1.minorticks_on()
    ax2.minorticks_on()
    ax3.minorticks_on()
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(50))
    ax1.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax1.tick_params(which='minor', axis='both', color='gray')
    ax2.yaxis.set_minor_locator(MultipleLocator(10))
    ax2.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax2.tick_params(which='minor', axis='both', color='gray')
    ax3.yaxis.set_minor_locator(MultipleLocator(5))
    ax3.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax3.tick_params(which='minor', axis='both', color='gray')

    # Legend sensitivity
    tmpHandles = []
    tmpLabels = []

    tmpLine1, = ax1.plot([0, 3000], [-1, -1], color=green, label='Renewables')
    tmpLine2, = ax2.plot([0, 3000], [-1, -1], color=blue, label='Electrolyzers')
    tmpLine3, = ax3.plot([0, 3000], [-1, -1], color=purple, label='Electrolyzer manufacturing')
    tmpLabels.append('Renewables')
    tmpLabels.append('Electrolyzers')
    tmpLabels.append('Electrolyzer manufacturing')
    tmpHandles.append(tmpLine1)
    tmpHandles.append(tmpLine2)
    tmpHandles.append(tmpLine3)

    for i in range(1, 10, 2):
        tmpAlpha = 0.25 + 0.75 * (i - 1) / 8
        tmpLabel = str('$\lambda$: ' + str(int((0.08 + 0.01 * (i - 1)) * 100)) + '%')
        tmpLabels.append(tmpLabel)
        tmpLine1, = ax1.plot([0, 3000], [-1, -1], color=green, label=tmpLabel, alpha=tmpAlpha, linestyle='-')
        tmpLine2, = ax2.plot([0, 3000], [-1, -1], color=blue, label=tmpLabel, alpha=tmpAlpha, linestyle='-')
        tmpLine3, = ax3.plot([0, 3000], [-1, -1], color=purple, label=tmpLabel, alpha=tmpAlpha, linestyle='-')
        tmpHandles.append((tmpLine1, tmpLine2, tmpLine3))

    plt.legend(tmpHandles, tmpLabels, loc='lower center', bbox_to_anchor=(0.5, -0.6),
               handler_map={tuple: HandlerTuple(ndivide=None)},
               fontsize=plotSettings['fontsize'], frameon=False, ncol=3)

    # ax1.legend(tmpHandles, tmpLabels, loc='upper left', bbox_to_anchor=(1, 1),
    #            handler_map={tuple: HandlerTuple(ndivide=None)})

    # Save figure
    plt.savefig(os.getcwd() + '\\figureC1.' + plotType, bbox_inches='tight')


def figure_d2(dfHM):
    '''
    Function that will create Fig. D2 - Hydrogen production for the sensitivity analysis of the learning rate.
    :param:
        pd.DataFrame dfHM: Daily data from the hydrogen market.
    :return:
    '''
    # Hydrogen market
    tmpHM = dfHM.set_index(['Year', 'Day', 'Sensitivity', 'Run'])
    tmpIndex = pd.MultiIndex.from_product([range(yearDelta), range(1, 12)], names=['Year', 'Sensitivity'])
    dfPlot = pd.DataFrame(data=np.nan, index=tmpIndex, columns=['Hydrogen production'])

    for i in range(yearDelta):
        # Hydrogen production
        if i in tmpHM.index.levels[0]:
            tmpDf = tmpHM.loc[i]['Actual production electrolyzers'].groupby(['Run', 'Sensitivity']).sum()
            for j in tmpDf.groupby(level=1).median().index:
                dfPlot['Hydrogen production'][i][j] = tmpDf.groupby(level=1).median().loc[j]

    # Figure
    fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                            dpi=plotSettings['dpi'])

    # Mt
    ax1.set_ylabel('Hydrogen production [Mt]', fontsize=plotSettings['fontsize'])
    ax1.set_xlabel('Year', fontsize=plotSettings['fontsize'])

    # Hydrogen production
    for i in range(1, 10, 2):
        tmpAlpha = 0.25 + 0.75 * (i - 1) / 8
        ax1.plot(x, dfPlot['Hydrogen production'].xs(i, level='Sensitivity')/(1e6*33.3), linestyle='-', color=blue,
                 alpha=tmpAlpha)

    # TWh
    ax2 = ax1.twinx()
    ax2.set_ylabel('Hydrogen production [TWh]', fontsize=plotSettings['fontsize'])
    for i in range(1, 10, 2):
        tmpAlpha = 0.25 + 0.75 * (i - 1) / 8
        ax2.plot(x, dfPlot['Hydrogen production'].xs(i, level='Sensitivity')/1e6, linestyle='-', color=blue,
                 alpha=tmpAlpha)

    # Adjust axis
    ax1.minorticks_on()
    ax1.set_xlim(plotSettings['xlim'])
    ax1.set_ylim(0)
    ax1.set_xticks(plotSettings['xticks'])
    ax1.set_xticklabels(['2025', '2035', '2045'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(1))
    ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax1.tick_params(axis='both', which='minor', color='gray')

    ax2.minorticks_on()
    ax2.set_xlim(plotSettings['xlim'])
    ax2.set_ylim(0)
    ax2.set_xticks(plotSettings['xticks'])
    ax2.xaxis.set_minor_locator(MultipleLocator(5))
    ax2.yaxis.set_minor_locator(MultipleLocator(50))
    ax2.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax2.tick_params(axis='both', which='minor', color='gray')

    # Legend sensitivity
    tmpHandles = []
    tmpLabels = []

    tmpLine, = ax1.plot([0, 3000], [-1, -1], color=blue, label='Hydrogen Production')
    tmpLabels.append('Hydrogen Production')
    tmpHandles.append(tmpLine)

    for i in range(1, 10, 2):
        tmpAlpha = 0.25 + 0.75 * (i - 1) / 8
        tmpLabel = str('$\lambda$: ' + str(int((0.08 + 0.01 * (i - 1)) * 100)) + '%')
        tmpLabels.append(tmpLabel)
        tmpLine, = ax1.plot([0, 3000], [-1, -1], color=blue, label=tmpLabel, alpha=tmpAlpha, linestyle='-')
        tmpHandles.append(tmpLine)

    plt.legend(tmpHandles, tmpLabels, loc='lower center', bbox_to_anchor=(0.5, -0.6),
               handler_map={tuple: HandlerTuple(ndivide=None)},
               fontsize=plotSettings['fontsize'], frameon=False, ncol=3)

    # Save plot
    plt.savefig(os.getcwd() + '\\figureC2.' + plotType, bbox_inches='tight')


def figure_d3(dfPM, dfHM):
    '''
    Function that will create Fig. D3 - Weighted electricity and hydrogen price.
    :param:
        pd.DataFrame dfPM: Yearly data from the power market.
        pd.DataFrame dfHM: Yearly data from the hydrogen market.
    :return:
    '''
    # Power market
    tmpPM = dfPM.set_index(['Year', 'Sensitivity', 'Run'])

    # Hydrogen market
    tmpHM = dfHM.set_index(['Year', 'Sensitivity', 'Run'])
    tmpIndex = pd.MultiIndex.from_product([range(yearDelta), range(1, 12)], names=['Year', 'Sensitivity'])
    dfPlot = pd.DataFrame(data=np.nan, index=tmpIndex, columns=['Electricity price', 'Hydrogen price'])

    for i in range(yearDelta):
        # Power market
        if i in tmpPM.index.levels[0]:
            tmpDf = tmpPM.loc[i]['Weighted Price Electricity']
            for j in tmpDf.groupby(level=0).median().index:
                dfPlot['Electricity price'][i][j] = tmpDf.groupby(level=0).median().loc[j]

        # Hydrogen market
        if i in tmpHM.index.levels[0]:
            tmpDf = tmpHM.loc[i]['Price Hydrogen']
            for j in tmpDf.groupby(level=0).median().index:
                dfPlot['Hydrogen price'][i][j] = tmpDf.groupby(level=0).median().loc[j]

    # Figure
    fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                            dpi=plotSettings['dpi'])

    ax1.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    ax1.set_ylabel('Price [€/MWh]', fontsize=plotSettings['fontsize'])
    ax2 = ax1.twinx()
    ax2.set_ylabel('Price [€/kg]', fontsize=plotSettings['fontsize'])

    # Results
    for i in range(1, 10, 2):
        tmpAlpha = 0.25 + 0.75 * (i - 1) / 8
        # Electricity price
        ax1.plot(x, dfPlot['Electricity price'].xs(i, level='Sensitivity'), linestyle='-', color=green, alpha=tmpAlpha)

        # Hydrogen price
        ax1.plot(x, dfPlot['Hydrogen price'].xs(i, level='Sensitivity'), linestyle='-', color=blue, alpha=tmpAlpha)
        ax2.plot(x, dfPlot['Hydrogen price'].xs(i, level='Sensitivity')*33.3/1e3, linestyle='-', color=blue,
                 alpha=tmpAlpha)

    # Adjust axis
    ax1.minorticks_on()
    ax1.set_xlim(plotSettings['xlim'])
    ax1.set_ylim([0, 275])
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(25))
    ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax1.tick_params(axis='both', which='minor', color='gray')

    ax2.minorticks_on()
    ax2.set_xlim(plotSettings['xlim'])
    ax2.set_ylim([0, 275*33.3/1e3])
    ax2.set_xticks(plotSettings['xticks'])
    ax2.xaxis.set_minor_locator(MultipleLocator(5))
    ax2.yaxis.set_minor_locator(MultipleLocator(1))
    ax2.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax2.tick_params(axis='both', which='minor', color='gray')

    # Legend sensitivity
    tmpHandles = []
    tmpLabels = []

    tmpLine1, = ax1.plot([0, 3000], [-1, -1], color=green, label='Electricity')
    tmpLabels.append('Electricity')
    tmpHandles.append(tmpLine1)
    tmpLine2, = ax1.plot([0, 3000], [-1, -1], color=blue, label='Hydrogen')
    tmpLabels.append('Hydrogen')
    tmpHandles.append(tmpLine2)

    for i in range(1, 10, 2):
        tmpAlpha = 0.25 + 0.75 * (i - 1) / 8
        tmpLabel = str('$\lambda$: ' + str(int((0.08 + 0.01 * (i - 1)) * 100)) + '%')
        tmpLabels.append(tmpLabel)
        tmpLine1, = ax1.plot([0, 3000], [-1, -1], color=green, label=tmpLabel, alpha=tmpAlpha, linestyle='-')
        tmpLine2, = ax2.plot([0, 3000], [-1, -1], color=blue, label=tmpLabel, alpha=tmpAlpha, linestyle='-')
        tmpHandles.append((tmpLine1, tmpLine2))

    plt.legend(tmpHandles, tmpLabels, loc='lower center', bbox_to_anchor=(0.5, -0.6),
               handler_map={tuple: HandlerTuple(ndivide=None)},
               fontsize=plotSettings['fontsize'], frameon=False, ncol=3)

    # Save plot
    plt.savefig(os.getcwd() + '\\figureC3.' + plotType, bbox_inches='tight')


def figure_d4(dfEP):
    '''
    Function that will create Fig. D4 - Minimal electrolyzer production costs.
    :param:
        pd.DataFrame dfEP: Yearly data from the electrolyzer producers.
    :return:
    '''
    # Electrolyzer producer
    tmpEP = dfEP.set_index(['Year', 'Run', 'ID', 'Sensitivity'])
    tmpIndex = pd.MultiIndex.from_product([range(yearDelta), range(1, 12)], names=['Year', 'Sensitivity'])
    dfPlot = pd.DataFrame(data=np.nan, index=tmpIndex, columns=['Electrolyzer price'])

    for i in range(yearDelta):
        # Electrolyzer costs
        if i in tmpEP.index.levels[0]:
            tmpDf = tmpEP.loc[i]['Minimal costs Electrolyzers'].groupby(['Run', 'Sensitivity']).min()
            for j in tmpDf.groupby(level=1).median().index:
                dfPlot['Electrolyzer price'][i][j] = tmpDf.groupby(level=1).median().loc[j]

    # Figure
    fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                            dpi=plotSettings['dpi'])

    # Electrolyzer cost
    ax1.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    ax1.set_ylabel('Production costs [€/kW]', fontsize=plotSettings['fontsize'])

    # Results
    for i in range(1, 10, 2):
        tmpAlpha = 0.25 + 0.75 * (i - 1) / 8
        # Electrolyzer price
        ax1.plot(x, dfPlot['Electrolyzer price'].xs(i, level='Sensitivity')/1e3, linestyle='-', color=purple,
                 alpha=tmpAlpha)

    # Adjust axis
    ax1.minorticks_on()
    ax1.set_xlim(plotSettings['xlim'])
    ax1.set_ylim(0)
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(500))
    ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax1.tick_params(axis='both', which='minor', color='gray')

    # Legend sensitivity
    tmpHandles = []
    tmpLabels = []

    tmpLine1, = ax1.plot([0, 3000], [-1, -1], color=purple, label='Electrolyzer')
    tmpLabels.append('Electrolyzer')
    tmpHandles.append(tmpLine1)

    for i in range(1, 10, 2):
        tmpAlpha = 0.25 + 0.75 * (i - 1) / 8
        tmpLabel = str('$\lambda$: ' + str(int((0.08 + 0.01 * (i - 1)) * 100)) + '%')
        tmpLabels.append(tmpLabel)
        tmpLine1, = ax1.plot([0, 3000], [-1, -1], color=purple, label=tmpLabel, alpha=tmpAlpha, linestyle='-')
        tmpHandles.append((tmpLine1))

    plt.legend(tmpHandles, tmpLabels, loc='lower center', bbox_to_anchor=(0.5, -0.6),
               handler_map={tuple: HandlerTuple(ndivide=None)},
               fontsize=plotSettings['fontsize'], frameon=False, ncol=3)

    # Save plot
    plt.savefig(os.getcwd() + '\\figureC4.' + plotType, bbox_inches='tight')


def figure_d5(dfPM, dfHM):
    '''
    Function that will create Fig. D5 - LCOH and the average electricity price for HP and its ratio.
    :param:
        pd.DataFrame dfPM: Daily data from the power market.
        pd.DataFrame dfHM: Yearly data from the hydrogen market.
    :return:
    '''
    # Power market
    tmpPM = dfPM.set_index(['Year', 'Day', 'Run', 'Sensitivity'])

    # Hydrogen market
    tmpHM = dfHM.set_index(['Year', 'Run', 'Sensitivity'])
    tmpIndex = pd.MultiIndex.from_product([range(yearDelta), range(1, 12)], names=['Year', 'Sensitivity'])
    dfPlot = pd.DataFrame(data=np.nan, index=tmpIndex, columns=['elc', 'lcoh'])

    for i in range(yearDelta):
        # Power market
        if i in tmpPM.index.levels[0]:
            tmpDf = tmpPM.loc[i]['Electricity demand electrolyzers'] * tmpPM.loc[i]['Price Electricity']
            tmpDf = (tmpDf.groupby(['Run', 'Sensitivity']).sum() /
                     tmpPM.loc[i]['Electricity demand electrolyzers'].groupby(['Run', 'Sensitivity']).sum())
            for j in tmpDf.groupby(level=1).median().index:
                dfPlot['elc'][i][j] = tmpDf.groupby(level=1).median().loc[j]
        # Hydrogen market
        if i in tmpHM.index.levels[0]:
            tmpDf = tmpHM.loc[i]['LCOH']
            for j in tmpDf.groupby(level=1).median().index:
                dfPlot['lcoh'][i][j] = tmpDf.groupby(level=1).median().loc[j]

    # Figure
    fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                            dpi=plotSettings['dpi'])

    # Electricity price
    ax1.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    ax1.set_ylabel('Average electricity price [€/MWh]', fontsize=plotSettings['fontsize'], color=green)

    # Hydrogen price
    # €/kg
    ax2 = ax1.twinx()
    ax2.set_ylabel('Levelized costs of hydrogen [€/kg]', fontsize=plotSettings['fontsize'], color=blue)

    # Share
    ax3 = ax1.twinx()
    ax3.set_ylabel('Share of electricity costs at LCOH [%]', fontsize=plotSettings['fontsize'], color=darkblue)

    # Results
    for i in range(1, 10, 2):
        tmpAlpha = 0.25 + 0.75 * (i - 1) / 8
        # Electricity price
        ax1.plot(x, dfPlot['elc'].xs(i, level='Sensitivity'), linestyle='-', color=green, alpha=tmpAlpha)
        # LOCH
        ax1.plot(x, dfPlot['lcoh'].xs(i, level='Sensitivity'), linestyle='-', color=blue, alpha=tmpAlpha)
        ax2.plot(x, dfPlot['lcoh'].xs(i, level='Sensitivity')*33.3/1e3, linestyle='-', color=blue, alpha=tmpAlpha)
        # Share
        tmpDf = dfPlot['elc']/0.7/dfPlot['lcoh']*100
        ax3.plot(x, tmpDf.xs(i, level='Sensitivity'), linestyle='--', color=darkblue, alpha=tmpAlpha)

    # Adjust axis
    ax1.minorticks_on()
    ax1.yaxis.set_label_position('left')
    ax1.set_xlim(plotSettings['xlim'])
    ax1.set_ylim([0, 500])
    ax1.set_xticks(plotSettings['xticks'])
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(25))
    ax1.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax1.tick_params(axis='both', which='minor', color='gray')

    ax2.spines['left'].set_position(('axes', -.2))
    ax2.spines['left'].set_visible(True)
    ax2.yaxis.set_label_position('left')
    ax2.yaxis.set_ticks_position('left')
    ax2.minorticks_on()
    ax2.set_xlim(plotSettings['xlim'])
    ax2.set_ylim([0, 500*33.3/1000])
    ax2.set_xticks(plotSettings['xticks'])
    ax2.yaxis.set_minor_locator(MultipleLocator(1.25))
    ax2.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax2.tick_params(axis='both', which='minor', color='gray')

    ax3.minorticks_on()
    ax3.set_xlim(plotSettings['xlim'])
    ax3.set_ylim([0, 55])
    ax3.set_xticks(plotSettings['xticks'])
    ax3.xaxis.set_minor_locator(MultipleLocator(5))
    ax3.yaxis.set_minor_locator(MultipleLocator(5))
    ax3.tick_params(axis='both', which='major', labelsize=plotSettings['fontsize'])
    ax3.tick_params(axis='both', which='minor', color='gray')

    ax1.set_zorder(1)
    ax2.set_zorder(2)
    ax3.set_zorder(3)

    # Adjust legend
    tmpHandles = []
    tmpLabels = []
    tmpLine1, = ax1.plot([0, 3000], [-2, -2], color=green, label='Electricity price')
    tmpLabels.append('Electricity price')
    tmpHandles.append(tmpLine1)
    tmpLine2, = ax2.plot([0, 3000], [-2, -2], color=blue, label='Levelized costs of hydrogen')
    tmpLabels.append('Levelized costs of hydrogen')
    tmpHandles.append(tmpLine2)
    tmpLine3, = ax3.plot([0, 3000], [-2, -2], color=darkblue, label='Share of LCOH', linestyle='--')
    tmpLabels.append('Share of LCOH')
    tmpHandles.append(tmpLine3)

    for i in range(1, 10, 2):
        tmpAlpha = 0.25 + 0.75 * (i - 1) / 8
        tmpLabel = str('$\lambda$: ' + str(int((0.08 + 0.01 * (i - 1)) * 100)) + '%')
        tmpLabels.append(tmpLabel)
        tmpLine1, = ax1.plot([0, 3000], [-2, -2], color=green, label=tmpLabel, alpha=tmpAlpha, linestyle='-')
        tmpLine2, = ax1.plot([0, 3000], [-2, -2], color=blue, label=tmpLabel, alpha=tmpAlpha, linestyle='-')
        tmpLine3, = ax1.plot([0, 3000], [-2, -2], color=darkblue, label=tmpLabel, alpha=tmpAlpha, linestyle='--')
        tmpHandles.append((tmpLine1, tmpLine2, tmpLine3))

    plt.legend(tmpHandles, tmpLabels, loc='lower center', bbox_to_anchor=(0.5, -0.6),
               handler_map={tuple: HandlerTuple(ndivide=None)},
               fontsize=plotSettings['fontsize'], frameon=False, ncol=3)

    # Save plot
    plt.savefig(os.getcwd() + '\\figureC5.' + plotType, bbox_inches='tight')


def figure_e1(dfPM):
    '''
    Function that will create Fig. E1 - Installed capacities validation.
    :param:
        pd.DataFrame dfPM: Yearly data from the power market.
    :return:
    '''
    # years
    tmpDelta = 25
    tmpX = range(2000, 2025)

    # Installed renewables
    tmpPM = dfPM.set_index(['Year', 'Run'])
    dfPlot = pd.DataFrame(data=np.nan, index=range(tmpDelta), columns=['median', '75%', '25%'])

    for i in range(tmpDelta):
        # Renewables
        tmpDf = tmpPM.loc[i]['Installed capacity Renewables']
        dfPlot['median'][i] = tmpDf.median()
        dfPlot['75%'][i] = tmpDf.quantile(q=0.75)
        dfPlot['25%'][i] = tmpDf.quantile(q=0.25)

    # Figure
    fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                            dpi=plotSettings['dpi'])

    # Renewables
    ax1.set_ylabel('Installed capacity Renewables [GW]', fontsize=plotSettings['fontsize'])
    ax1.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    ax1.plot(tmpX, dfHistoricalData['Installed Capacity Renewables [GW]'],
             label='Renewables - Historical data', linestyle='--', color=green, alpha=0.5)
    ax1.plot(tmpX, dfPlot['median']/1e3, label='Renewables - our work', linestyle='-', color=green)
    ax1.fill_between(tmpX, dfPlot['25%']/1e3, dfPlot['75%']/1e3, alpha=0.25, color=green, edgecolor=None)

    plt.xlim((2000, 2024))

    # Adjust ticks
    ax1.minorticks_on()
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(50))
    ax1.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax1.tick_params(which='minor', axis='both', color='gray')

    # Legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    tmpUnique = dict(zip(labels1, handles1))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.4),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save figure
    plt.savefig(os.getcwd() + '\\figureE1.' + plotType, bbox_inches='tight')

    # Write out Data
    writeDf = pd.DataFrame(data=[dfPlot['median']/1e3, dfPlot['25%']/1e3, dfPlot['75%']/1e3,
                                 dfHistoricalData['Installed Capacity Renewables [GW]']],
                           index=['Inst. Renewables [GW] - Median', 'Inst. Renewables [GW] - 25%',
                                  'Inst. Renewables [GW] - 75%', 'Inst. Renewables [GW] - History'])
    writeDf = writeDf.T
    writeDf.index = tmpX
    writeDf.to_csv(os.getcwd() + '\\figureE1.csv', sep=';')

def figure_e2(dfPM):
    '''
    Function that will create Fig. E2 - Share renewables validation.
    :param:
        pd.DataFrame dfPM: Daily data from the power market.
    :return:
    '''
    # years
    tmpDelta = 25
    tmpX = range(2000, 2025)

    # Installed renewables
    tmpPM = dfPM.set_index(['Year', 'Day', 'Run'])
    dfPlot = pd.DataFrame(data=np.nan, index=range(tmpDelta), columns=['median', '75%', '25%'])

    for i in range(tmpDelta):
        # Renewables
        tmpDf = (tmpPM.loc[i]['Actual production renewables'].groupby(level=1).sum() /
                 tmpPM.loc[i]['Electricity demand others'].groupby(level=1).sum())
        dfPlot['median'][i] = tmpDf.median() * 100
        dfPlot['75%'][i] = tmpDf.quantile(q=0.75) * 100
        dfPlot['25%'][i] = tmpDf.quantile(q=0.25) * 100

    # Figure
    fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                            dpi=plotSettings['dpi'])

    # Renewables
    ax1.set_ylabel('Share of Renewables [%]', fontsize=plotSettings['fontsize'])
    ax1.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    ax1.plot(tmpX, dfHistoricalData['Share Renewables [%]'],
             label='Share of Renewables - Historical data', linestyle='--', color=green, alpha=0.5)
    ax1.plot(tmpX, dfPlot['median'], label='Share of Renewables - our work', linestyle='-', color=green)
    ax1.fill_between(tmpX, dfPlot['25%'], dfPlot['75%'], alpha=0.25, color=green, edgecolor=None)

    plt.xlim((2000, 2024))

    # Adjust ticks
    ax1.minorticks_on()
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(50))
    ax1.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax1.tick_params(which='minor', axis='both', color='gray')

    # Legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    tmpUnique = dict(zip(labels1, handles1))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.4),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save figure
    plt.savefig(os.getcwd() + '\\figureE2.' + plotType, bbox_inches='tight')

    # Write out Data
    writeDf = pd.DataFrame(data=[dfPlot['median'], dfPlot['25%'], dfPlot['75%'],
                                 dfHistoricalData['Share Renewables [%]']],
                           index=['Share Renewables [%] - Median', 'Share Renewables [%] - 25%',
                                  'Share Renewables [%] - 75%', 'Share Renewables [%] - History'])
    writeDf = writeDf.T
    writeDf.index = tmpX
    writeDf.to_csv(os.getcwd() + '\\figureE2.csv', sep=';')

def figure_e3(dfPM):
    '''
    Function that will create Fig. E3 - Production renewables validation.
    :param:
        pd.DataFrame dfPM: Daily data from the power market.
    :return:
    '''
    # years
    tmpDelta = 25
    tmpX = range(2000, 2025)

    # Installed renewables
    tmpPM = dfPM.set_index(['Year', 'Day', 'Run'])
    dfPlot = pd.DataFrame(data=np.nan, index=range(tmpDelta), columns=['median', '75%', '25%'])

    for i in range(tmpDelta):
        # Renewables
        tmpDf = tmpPM.loc[i]['Actual production renewables']/1e6
        tmpDf = tmpDf.groupby(level=1).sum()
        dfPlot['median'][i] = tmpDf.median()
        dfPlot['75%'][i] = tmpDf.quantile(q=0.75)
        dfPlot['25%'][i] = tmpDf.quantile(q=0.25)

    # Figure
    fig, ax1 = plt.subplots(figsize=plotSettings['figsize_s'], gridspec_kw=plotSettings['gridspec_kw'],
                            dpi=plotSettings['dpi'])

    # Renewables
    ax1.set_ylabel('Production Renewables [TWh]', fontsize=plotSettings['fontsize'])
    ax1.set_xlabel('Year', fontsize=plotSettings['fontsize'])
    ax1.plot(tmpX, dfHistoricalData['Production Renewables [TWh]'],
             label='Renewables - Historical data', linestyle='--', color=green, alpha=0.5)
    ax1.plot(tmpX, dfPlot['median'], label='Renewables - our work', linestyle='-', color=green)
    ax1.fill_between(tmpX, dfPlot['25%'], dfPlot['75%'], alpha=0.25, color=green, edgecolor=None)

    plt.xlim((2000, 2024))

    # Adjust ticks
    ax1.minorticks_on()
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(50))
    ax1.tick_params(axis='both', labelsize=plotSettings['fontsize'])
    ax1.tick_params(which='minor', axis='both', color='gray')

    # Legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    tmpUnique = dict(zip(labels1, handles1))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower center', bbox_to_anchor=(0.5, -0.4),
               fontsize=plotSettings['fontsize'], frameon=False, ncol=2)

    # Save figure
    plt.savefig(os.getcwd() + '\\figureE3.' + plotType, bbox_inches='tight')

    # Write out Data
    writeDf = pd.DataFrame(data=[dfPlot['median'], dfPlot['25%'], dfPlot['75%'],
                                 dfHistoricalData['Production Renewables [TWh]']],
                           index=['Production Renewables [TWh] - Median', 'Production Renewables [TWh] - 25%',
                                  'Production Renewables [TWh] - 75%', 'Production Renewables [TWh] - History'])
    writeDf = writeDf.T
    writeDf.index = tmpX
    writeDf.to_csv(os.getcwd() + '\\figureE3.csv', sep=';')


def plot_reference(listResult):
    '''
    Creates all plots for the Reference case.
    :param:
        lst listResult: List with all Results of the Reference case
    :return:
    '''
    # Rearrange data for better code visibility
    dfPMYear, dfHMYear, dfEMYear = listResult[8], listResult[4], listResult[1]
    dfPMDay, dfHMDay = listResult[7], listResult[3]
    dfPP, dfHP, dfEP = listResult[9], listResult[5], listResult[2]
    dfRES, dfELC, dfMAN = listResult[10], listResult[0], listResult[6]
    dfSale = listResult[-1]

    # TODO DEBUG
    #figure_3a()
    #exit(123)

    # Creates Fig for the reference case:
    # Fig. 3 - Hydrogen demand curve after BCG
    # Fig. 3a - Electricity price in differet cases
    # Fig. 4 - Installed capacity reference case
    # Fig. 5 - No. of agents reference case
    # Fig. 6 - Electricity production reference case
    # Fig. 7 - Hydrogen production reference case
    # Fig. 8 - Utilization rate Renewables & Electrolyzers reference case
    # Fig. 9 - Type of loads for Electrolyzers reference case
    # Fig. 10 - Median wallet for market reference case
    # Fig. 11 - ROI for Agents reference case
    # Fig. 12 - Expected profitability of new assets reference case
    # Fig. 13 - Invested money reference case
    # Fig. 14 - Weighted electricity price and hydrogen price reference case
    # Fig. 15 - Minimal electrolyzer production costs reference case
    # Fig. 16 - Electricity price and LCOE and Hydrogen price and LCOH reference case
    # Fig. 16a - Average electricity price of HP and LCOH and share of electricity of LCOH reference case
    # Fig. 16b - Investment threshold for all type of agents reference case

    figure_3()
    figure_3a()
    figure_4(dfPMYear, dfHMYear, dfEMYear)
    #figure_5(dfPMYear, dfHMYear, dfEMYear)
    figure_6(dfPMDay)
    figure_7(dfHMDay)
    figure_8(dfRES, dfELC)
    #figure_9(dfPMYear)
    #figure_10(dfPP, dfHP, dfEP)
    figure_11(dfPP, dfHP, dfEP)
    #figure_12(dfPP, dfHP, dfEP)
    figure_13(dfPMYear, dfSale, dfEMYear)
    figure_14(dfPMYear, dfHMYear)
    figure_15(dfEP)
    figure_16(dfPMYear, dfHMYear)
    figure_16a(dfPMDay, dfHMYear)
    #figure_16b(dfPP, dfHP, dfEP)


def plot_obstacles(listRef, listStrat, listW2P, listWorst):
    '''
    Creates all plots for the Obstacle cases.
    :param:
        lst listRef: List with all Results of the Reference case
        lst listStrat: List with all Results of the strategic investment case
        lst listW2p: List with all Results of the willingness to pay case
        lst listWorst: List with all Results of the worst case
    :return:
    '''
    # Rearrange data for better code visibility
    # Reference case
    dfPMYearRef, dfHMYearRef, dfEMYearRef = listRef[8], listRef[4], listRef[1]
    dfPMDayRef, dfHMDayRef = listRef[7], listRef[3]
    dfPPRef, dfHPRef, dfEPRef = listRef[9], listRef[5], listRef[2]
    dfRESRef, dfELCRef, dfMANRef = listRef[10], listRef[0], listRef[6]
    dfSaleRef = listRef[-1]
    # Strategic investment case
    dfPMYearStrat, dfHMYearStrat, dfEMYearStrat = listStrat[8], listStrat[4], listStrat[1]
    dfPMDayStrat, dfHMDayStrat = listStrat[7], listStrat[3]
    dfPPStrat, dfHPStrat, dfEPStrat = listStrat[9], listStrat[5], listStrat[2]
    dfRESStrat, dfELCStrat, dfMANStrat = listStrat[10], listStrat[0], listStrat[6]
    dfSaleStrat = listStrat[-1]
    # Willingness to pay case
    dfPMYearW2P, dfHMYearW2P, dfEMYearW2P = listW2P[8], listW2P[4], listW2P[1]
    dfPMDayW2P, dfHMDayW2P = listW2P[7], listW2P[3]
    dfPPW2P, dfHPW2P, dfEPW2P = listW2P[9], listW2P[5], listW2P[2]
    dfRESW2P, dfELCW2P, dfMANW2P = listW2P[10], listW2P[0], listW2P[6]
    dfSaleW2P = listW2P[-1]
    # Worst case
    dfPMYearWorst, dfHMYearWorst, dfEMYearWorst = listWorst[8], listWorst[4], listWorst[1]
    dfPMDayWorst, dfHMDayWorst = listWorst[7], listWorst[3]
    dfPPWorst, dfHPWorst, dfEPWorst = listWorst[9], listWorst[5], listWorst[2]
    dfRESWorst, dfELCWorst, dfMANWorst = listWorst[10], listWorst[0], listWorst[6]
    dfSaleWorst = listWorst[-1]

    # TODO DEBUG
    #figure_25a(dfPMDayRef, dfPMDayStrat, dfPMDayW2P, dfHMYearRef, dfHMYearStrat, dfHMYearW2P)
    #exit(123)

    # Creates Fig for the obstacle cases:
    # Fig. 17 - Installed capacities for obstacle cases
    # Fig. 17b - Installed capacities for obstacle cases until 2100
    # Fig. 18 - Electricity mix for obstacle cases
    # Fig. 19 - Hydrogen production for obstacle cases
    # Fig. 20 - Utilization rate for obstacle cases
    # Fig. 21 - ROI for obstacle cases
    # Fig. 22 - Electricity and hydrogen price for obstacle cases
    # Fig. 23 - Electrolyzer costs for obstacle cases
    # Fig. 24 - Invested money for obstacle cases
    # Fig. 25 - LCOE and weighted electricity price and LCOH and hydrogen price for obstacle cases
    # Fig. 25a - Average electricity price for HP and LCOH and share of electricity on LCOH for obstacle cases
    # Fig. 25b - Investment thresholds for all type of agents obstacle cases

    figure_17(dfPMYearRef, dfHMYearRef, dfEMYearRef,dfPMYearStrat, dfHMYearStrat, dfEMYearStrat, dfPMYearW2P,
              dfHMYearW2P, dfEMYearW2P, dfPMYearWorst, dfHMYearWorst, dfEMYearWorst)
    figure_17b(dfPMYearRef, dfHMYearRef, dfEMYearRef,dfPMYearStrat, dfHMYearStrat, dfEMYearStrat, dfPMYearW2P,
              dfHMYearW2P, dfEMYearW2P, dfPMYearWorst, dfHMYearWorst, dfEMYearWorst)
    figure_18(dfPMDayRef, dfPMDayStrat, dfPMDayW2P, dfPMDayWorst)
    figure_19(dfHMDayRef, dfHMDayStrat, dfHMDayW2P, dfHMDayWorst)
    figure_20(dfRESRef, dfRESStrat, dfRESW2P, dfRESWorst, dfELCRef, dfELCStrat, dfELCW2P, dfELCWorst)
    figure_21(dfPPRef, dfPPStrat, dfPPW2P, dfPPWorst, dfHPRef, dfHPStrat, dfHPW2P, dfHPWorst, dfEPRef, dfEPStrat,
              dfEPW2P, dfEPWorst)
    figure_22(dfPMYearRef, dfPMYearStrat, dfPMYearW2P, dfPMYearWorst, dfHMYearRef, dfHMYearStrat, dfHMYearW2P,
              dfHMYearWorst)
    figure_23(dfEPRef, dfEPStrat, dfEPW2P, dfEPWorst)
    figure_24(dfPMYearRef, dfPMYearStrat, dfPMYearW2P, dfPMYearWorst, dfSaleRef, dfSaleStrat, dfSaleW2P, dfSaleWorst,
              dfEMYearRef, dfEMYearStrat, dfEMYearW2P, dfEMYearWorst)
    #figure_25(dfPMYearRef, dfPMYearStrat, dfPMYearW2P, dfHMYearRef, dfHMYearStrat, dfHMYearW2P)
    #figure_25a(dfPMDayRef, dfPMDayStrat, dfPMDayW2P, dfHMYearRef, dfHMYearStrat, dfHMYearW2P)
    #figure_25b(dfPPRef, dfPPStrat, dfPPW2P, dfHPRef, dfHPStrat, dfHPW2P, dfEPRef, dfEPStrat, dfEPW2P)


def plot_sensitivity(listRef, listStrat, listW2P, dictSens):
    '''
    Creates all plots for the sensitivity analysis.
    :param
        lst listRef: List with all Results of the Reference case
        lst listStrat: List with all Results of the strategic investment case
        lst listW2p: List with all Results of the willingness to pay case
        dict dictSens: Dictionary with all Results of the sensitivity analysis (index: [name, w2p, strat, listResults])
    :return:
    '''
    # Rearrange data for better code visibility
    # Reference case
    dfPMYearRef, dfHMYearRef, dfEMYearRef = listRef[8], listRef[4], listRef[1]
    dfPMDayRef, dfHMDayRef = listRef[7], listRef[3]
    dfPPRef, dfHPRef, dfEPRef = listRef[9], listRef[5], listRef[2]
    dfRESRef, dfELCRef, dfMANRef = listRef[10], listRef[0], listRef[6]
    dfSaleRef = listRef[-1]
    # Strategic investment case
    dfPMYearStrat, dfHMYearStrat, dfEMYearStrat = listStrat[8], listStrat[4], listStrat[1]
    dfPMDayStrat, dfHMDayStrat = listStrat[7], listStrat[3]
    dfPPStrat, dfHPStrat, dfEPStrat = listStrat[9], listStrat[5], listStrat[2]
    dfRESStrat, dfELCStrat, dfMANStrat = listStrat[10], listStrat[0], listStrat[6]
    dfSaleStrat = listStrat[-1]
    # Willingness to pay case
    dfPMYearW2P, dfHMYearW2P, dfEMYearW2P = listW2P[8], listW2P[4], listW2P[1]
    dfPMDayW2P, dfHMDayW2P = listW2P[7], listW2P[3]
    dfPPW2P, dfHPW2P, dfEPW2P = listW2P[9], listW2P[5], listW2P[2]
    dfRESW2P, dfELCW2P, dfMANW2P = listW2P[10], listW2P[0], listW2P[6]
    dfSaleW2P = listW2P[-1]

    # Index for scatter plots
    tmpIndex = ['Ref.', 'Non-strat.', 'Grey H2']
    for i in dictSens:
        tmpString = str('w2p:' + str(dictSens[i][1]) + '; strat:' + str(dictSens[i][2]))
        tmpIndex.append(tmpString)


    # TODO DEBUG
    #figure_37(dictSens)
    #exit(123)

    # Creates Fig for the obstacle cases:
    # Fig. 26 - Inst. RES vs Inst. ELC
    # Fig. 27 - Inst. ELC vs Inst. FAC
    # Fig. 28 - Inst. ELC vs cumulative Investment by HP
    # Fig. 29 - Share RES vs H2 Production
    # Fig. 30 - Price hydrogen vs weighted price electricity
    # Fig. 31 - Electrolyzer costs vs hydrogen price
    # Fig. 32 - No. of HP vs No. of EP
    # Fig. 33 - ROI of HP vs ROI of EP
    # Fig. 34 - LCOE vs LCOH
    # Fig. 35 - Average electricity price vs electrolyzer costs
    # Fig. 36 - Cumulative investment by PP vs cumulative investment by HP
    # Fig. 37 - Colormap Inst. ELC
    # Fig. 38 - Colormap Weighted price electricity
    # Fig. 39 - Colormap Cumulative investment

    #figure_26(dfPMYearRef, dfPMYearStrat, dfPMYearW2P, dfHMYearRef, dfHMYearStrat, dfHMYearW2P, dictSens, tmpIndex)
    plt.close('all')
    #figure_27(dfHMYearRef, dfHMYearStrat, dfHMYearW2P, dfEMYearRef, dfEMYearStrat, dfEMYearW2P, dictSens, tmpIndex)
    plt.close('all')
    #figure_28(dfHMYearRef, dfHMYearStrat, dfHMYearW2P, dfSaleRef, dfSaleStrat, dfSaleW2P, dictSens, tmpIndex)
    plt.close('all')
    #figure_29(dfPMDayRef, dfPMDayStrat, dfPMDayW2P, dfHMDayRef, dfHMDayStrat, dfHMDayW2P, dictSens, tmpIndex)
    plt.close('all')
    #figure_30(dfPMYearRef, dfPMYearStrat, dfPMYearW2P, dfHMYearRef, dfHMYearStrat, dfHMYearW2P, dictSens, tmpIndex)
    plt.close('all')
    #figure_31(dfHMYearRef, dfHMYearStrat, dfHMYearW2P, dfEPRef, dfEPStrat, dfEPW2P, dictSens, tmpIndex)
    plt.close('all')
    #figure_32(dfHMYearRef, dfHMYearStrat, dfHMYearW2P, dfEMYearRef, dfEMYearStrat, dfEMYearW2P, dictSens, tmpIndex)
    plt.close('all')
    #figure_33(dfHPRef, dfHPStrat, dfHPW2P, dfEPRef, dfEPStrat, dfEPW2P, dictSens, tmpIndex)
    plt.close('all')
    #figure_34(dfPMYearRef, dfPMYearStrat, dfPMYearW2P, dfHMYearRef, dfHMYearStrat, dfHMYearW2P, dictSens, tmpIndex)
    plt.close('all')
    #figure_35(dfPMDayRef, dfPMDayStrat, dfPMDayW2P, dfEPRef, dfEPStrat, dfEPW2P, dictSens, tmpIndex)
    plt.close('all')
    #figure_36(dfPMYearRef, dfPMYearStrat, dfPMYearW2P, dfSaleRef, dfSaleStrat, dfSaleW2P, dictSens, tmpIndex)
    plt.close('all')
    figure_37(dictSens)
    plt.close('all')
    figure_38(dictSens)
    plt.close('all')
    figure_39(dictSens)
    plt.close('all')


def plot_learningrate(listLearning):
    '''
    Creates all plots for the learning rate sensitivity analysis.
    :param
        lst listLearning: List with all Results of the learning rate sensitivity analysis case
    :return:
    '''
    # Rearrange data for better code visibility
    # Sensitivity analysis
    dfPMYear, dfHMYear, dfEMYear = listLearning[8], listLearning[4], listLearning[1]
    dfPMDay, dfHMDay = listLearning[7], listLearning[3]
    dfPP, dfHP, dfEP = listLearning[9], listLearning[5], listLearning[2]
    dfRES, dfELC, dfMAN = listLearning[10], listLearning[0], listLearning[6]
    dfSale = listLearning[-1]

    # TODO DEBUG

    # Creates Fig for the learning rate sensitivity:
    # Fig. D1 - Installed capacity
    # Fig. D2 - Hydrogen production
    # Fig. D3 - Weighted electricity price and hydrogen price
    # Fig. D4 - Minimal electrolyzer production costs
    # Fig. D5 - Average electricity price of HP and LCOH and share of electricity of LCOH

    figure_d1(dfPMYear, dfHMYear, dfEMYear)
    plt.close('all')
    figure_d2(dfHMDay)
    plt.close('all')
    figure_d3(dfPMYear, dfHMYear)
    plt.close('all')
    figure_d4(dfEP)
    plt.close('all')
    figure_d5(dfPMDay, dfHMYear)
    plt.close('all')


def plot_validation(listValidation):
    '''
    Creates all plots for the validataion.
    :param
        lst listLearning: List with all Results of the learning rate sensitivity analysis case
    :return:
    '''
    # Rearrange data for better code visibility
    # Sensitivity analysis
    dfPMYear, dfHMYear, dfEMYear = listValidation[8], listValidation[4], listValidation[1]
    dfPMDay, dfHMDay = listValidation[7], listValidation[3]
    dfPP, dfHP, dfEP = listValidation[9], listValidation[5], listValidation[2]
    dfRES, dfELC, dfMAN = listValidation[10], listValidation[0], listValidation[6]
    dfSale = listValidation[-1]

    # TODO DEBUG

    # Creates Fig for the validation:
    # Fig. E1 - Installed capacity
    # Fig. E2 - Share renewables
    # Fig. E3 - Production renewables

    figure_e1(dfPMYear)
    plt.close('all')
    figure_e2(dfPMDay)
    plt.close('all')
    figure_e3(dfPMDay)
    plt.close('all')


def main():
    '''
    Function that will create all figures for the results
    :return:
    '''
    # Change folder
    try:
        os.chdir(resultDir)
    except FileNotFoundError:
        print('Error in main: Results folder not found.')
        exit(100)

    # DEBUG
    check_data(resultValidation)
    listResultValidation = load_data(resultValidation)
    plot_validation(listResultValidation)
    exit()


    # Reference Case
    # Check and load data for Reference case
    print('Check and load data for the reference case...')
    check_data(resultRefDir)
    print('Check data for the reference case... done')
    listResultRef = load_data(resultRefDir)
    print('Load data for the reference case... done')

    # Plots for Reference case
    print('Creating all figures for the reference case...')
    plot_reference(listResultRef)
    plt.close('all')
    print('Creating all figures for the reference case... done')

    # Obstacle Cases
    # Check and load data for the Strategic Investment case
    print('Check and load data for the strategic investment case...')
    check_data(resultStratDir)
    print('Check data for the strategic investment case... done')
    listResultStrat = load_data(resultStratDir)
    print('Load data for the strategic investment case... done')

    # Check and load data for the W2P case
    print('Check and load data for the willingness to pay case...')
    check_data(resultW2PDir)
    print('Check data for the willingness to pay case... done')
    listResultW2P = load_data(resultW2PDir)
    print('Load data for the willingness to pay case... done')

    # Check and load data for the Worst case
    print('Check and load data for the worst case...')
    check_data(resultWorstDir)
    print('Check data for the worst case... done')
    listResultWorst = load_data(resultWorstDir)
    print('Load data for the worst case... done')

    # Plots for Obstacle cases
    print('Creating all figure for the obstacle cases...')
    plot_obstacles(listResultRef, listResultStrat, listResultW2P, listResultWorst)
    plt.close('all')
    print('Creating all figure for the obstacle cases... done')

    # Check and load data for the sensitivity analysis
    print('Check and load data for the sensitivity analysis...')
    print('This might take a while!')
    check_sensitivity(resultSensCsv)
    print('Check data for the sensitivity analysis...done')
    listResultSens = load_sensitivity(resultSensCsv)
    print('Load data for sensitivity analysis...done')

    # Plots for Sensitivity analysis
    print('Creating all figure for the sensitivity analysis...')
    print('This might take even longer!')
    plot_sensitivity(listResultRef, listResultStrat, listResultW2P, listResultSens)
    plt.close('all')
    print('Creating all figure for the sensitivity analysis...done')

    # Check and load data for the learning rate
    print('Check and load data for the learning rate analysis...')
    print('This might take a while!')
    check_learningrate(resultLearning)
    print('Check data for the learning rate analysis...done')
    listResultLearning = load_learningrate(resultLearning)
    print('Load data for the learning rate analysis...done')

    # Plots for learning rate analysis
    print('Creating all figure for the learning rate analysis...')
    plot_learningrate(listResultLearning)
    plt.close('all')
    print('Creating all figure for the learning rate analysis...done')

    # Check and load data for the validation
    print('Check and load data for validation...')
    check_data(resultValidation)
    print('Check data for validation...done')
    listResultValidation = load_data(resultValidation)
    print('Load data for validation...done')

    # Plots for validation
    print('Creating all figure for the validation...')
    plot_validation(listResultValidation)
    plt.close('all')
    print('Creating all figure for the validation...done')



if __name__ == '__main__':
    main()