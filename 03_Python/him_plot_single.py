'''
him - Hydrogen Investment Model
This script will take the results of one run and will create plots. The list of plots can be seen below

List of plots:
- no. of agents
- no. of investments
- ratio no. of investments/no. of agents
- installed RES capacity
- installed ELC capacity
- installed MAN capacity
- installed all capacity
- electricity mix
- hydrogen production
- duration curve RES
- duration curves ELC
- load type electrolyzers
- price electricity vs lcoe
- price hydrogen vs lcoh
- average price electrolyzer vs average lcoe
- price elc / cost elc
- investment threshold PP
- investment threshold HP
- investment threshold EP
- weighted investment threshold PP
- weighted investment threshold HP
- weighted investment threshold EP
- age RES
- age ELC
- age MAN
- weighted age
- profitability
- weighted profitability


version: 0.1.24.07.15
date: 2024-07-15
author: Jesse

changelog:
0.1.24.07.03 - start new script
0.1.24.07.15 - feature complete
'''

# import
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# global
global list_files
global plot_type
global plot_settings
global blue, darkblue, green, black, grey, orange, purple
global x, year0, delta_year

list_files = ['elc_year.csv', 'em_year.csv', 'ep_year.csv', 'hm_day.csv', 'hm_year.csv', 'hp_year.csv', 'man_year.csv',
              'pm_day.csv', 'pm_year.csv', 'pp_year.csv', 'res_year.csv', 'sale_year.csv']
plot_type = 'png'
plot_settings = {}
plot_settings['figsize'] = (8, 4.5)
plot_settings['gridspec_kw'] = {'left': 0.1, 'bottom': 0.1, 'right': 0.9, 'top': 0.9}
plot_settings['dpi'] = 500
plot_settings['xlim'] = (2023, 2065)
plot_settings['loc'] = 'lower left'
blue = [173/255, 189/255, 227/255]
darkblue = [2/255,  61/255, 107/255]
green = [185/255, 210/255, 95/255]
black = [0, 0, 0]
grey = [235/255, 235/255, 235/255]
orange = [250/255, 180/255, 90/255]
purple = [175/255, 130/255, 185/255]
year0 = 2023
delta_year = 80
x = list(range(year0, year0+delta_year))


def check_data():
    '''
    Function that checks if all files exists.
    :return:
    '''
    wkdir = os.getcwd()
    for i in list_files:
        if not os.path.isfile(str(wkdir + '\\' + i)):
            print('Error in check_data: ' + i + ' not found.')
            exit(100)


def load_data():
    '''
    Function that loads the data from the csv files.
    :return:
        list tmp_list: List that contains the data from all file as an individual pd.Dataframe.
    '''
    tmp_list = []
    wkdir = os.getcwd()
    for i in list_files:
        try:
            file = str(wkdir + '\\' + i)
            tmp_df = pd.read_csv(file, sep=';')
            tmp_list.append(tmp_df)
        except FileNotFoundError:
            print('Error in load_data: ' + i + ' not found.')
            exit(200)

    return(tmp_list)


def plot_no_of_agents(df_pm, df_hm, df_em):
    '''
    Function that will create a plot of the no. of agents.
    :param:
        pd.DataFrame df_pm: Data from the power market
        pd.DataFrame df_hm: Data from the hydrogen market
        pd.DataFrame df_em: Data from the electrolyzer market
    :return:
    '''

    # Power Producers
    y1_column = 'No. of Powerproducers'
    y1 = df_pm[y1_column]

    # Hydrogen Producers
    y2_column = 'No. of Hydrogenproducers'
    y2 = df_hm[y2_column]

    # Electrolyzer Producers
    y3_column = 'No. of Electrolyzerproducers'
    y3 = df_em[y3_column]

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('No. of Agents')

    ax1.plot(x, y1, label=y1_column, linestyle='-', color=green)
    ax1.plot(x, y2, label=y2_column, linestyle='-', color=blue)
    ax1.plot(x, y3, label=y3_column, linestyle='-', color=purple)

    plt.xlim(plot_settings['xlim'])
    plt.ylim(0)
    plt.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), ncol=3, frameon=False)
    plt.title('Number of Agents')
    plt.savefig(os.getcwd() + '\\plot_no_of_agents.' + plot_type, bbox_inches='tight')


def plot_no_of_investment(df_pm, df_hm, df_em):
    '''
    Function that will create a plot of the no. of investments.
    :param:
        pd.Dataframe df_pm: Data from the power market
        pd.Dataframe df_hm: Data from the hydrogen market
        pd.Dataframe df_em: Data from the hydrogen market
    :return:
    '''
    # Power Producers
    y1_column = 'No. of Investments PM'
    y1 = df_pm[y1_column]

    # Hydrogen Producers
    y2_column = 'No. of Investments HM'
    y2 = df_hm[y2_column]

    # Electrolyzer Producers
    y3_column = 'No. of Investments EM'
    y3 = df_em[y3_column]

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Number of Investments')
    ax1.plot(x, y1, label='Powermarket', linestyle='-', color=green)
    ax1.plot(x, y2, label='Hydrogenmarket', linestyle='-', color=blue)
    ax1.plot(x, y3, label='Electrolyzermarket', linestyle='-', color=purple)

    plt.xlim(plot_settings['xlim'])
    plt.ylim(0)
    plt.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), ncol=3, frameon=False)
    plt.savefig(os.getcwd() + '\\plot_no_of_investments.' + plot_type, bbox_inches='tight')


def plot_ratio_investment_agents(df_pm, df_hm, df_em):
    '''
    Function that will create a plot of the ratio investment to agents.
    :param:
        pd.DataFrame df_pm: Data from the power market
        pd.DataFrame df_hm: Data from the hydrogen market
        pd.DataFrame df_em: Data from the electrolyzer market
    :return:
    '''

    # Power Producers
    y11_column = 'No. of Powerproducers'
    y12_column = 'No. of Investments PM'
    y11 = df_pm[y11_column].replace(0, np.nan)
    y12 = df_pm[y12_column]
    y1 = y12/y11

    # Hydrogen Producers
    y21_column = 'No. of Hydrogenproducers'
    y22_column = 'No. of Investments HM'
    y21 = df_hm[y21_column].replace(0, np.nan)
    y22 = df_hm[y22_column]
    y2 = y22/y21

    # Electrolyzer Producers
    y31_column = 'No. of Electrolyzerproducers'
    y32_column = 'No. of Investments EM'
    y31 = df_em[y31_column].replace(0, np.nan)
    y32 = df_em[y32_column]
    y3 = y32/y31

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Investment / Agents')
    ax1.plot(x, y1, label='Powermarket', linestyle='-', color=green)
    ax1.plot(x, y2, label='Hydrogenmarket', linestyle='-', color=blue)
    ax1.plot(x, y3, label='Electrolyzermarket', linestyle='-', color=purple)

    plt.xlim(plot_settings['xlim'])
    plt.ylim(0)
    plt.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), ncol=3, frameon=False)
    plt.savefig(os.getcwd() + '\\plot_ratio_investment_agents.' + plot_type, bbox_inches='tight')


def plot_installed_cap_res(df_pm):
    '''
    Function that will create a plot of the installed capacities of renewables.
    :param:
        pd.DataFrame df_pm: Data from the power market
    :return:
    '''
    y1_column = 'Installed capacity Renewables'
    y1 = df_pm[y1_column]

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Installed capacity [GW]')
    ax1.plot(x, y1/1000, label='Renewables', linestyle='-', color=green)
    ax1.plot(x, (np.ones(80) * 375), label='Governmental target', linestyle='--', color=orange)
    ax1.scatter(2030, 375, label='Governmental target', facecolor='None', edgecolor=orange)
    #ax1.scatter(year0, 128, label='Today', color='black')

    plt.xlim(plot_settings['xlim'])
    plt.ylim(0)
    plt.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False)
    plt.savefig(os.getcwd() + '\\plot_installed_cap_res.' + plot_type, bbox_inches='tight')


def plot_installed_cap_elc(df_hm):
    '''
    Function that will create a plot of the installed capacities of electrolyzers.
    :param:
        pd.DataFrame df_hm: Data from the hydrogen market
    :return:
    '''
    y1_column = 'Installed capacity Electrolyzers'
    y1 = df_hm[y1_column]

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Installed capacity [GW]')
    ax1.plot(x, y1/1000, label='Electrolyzers', linestyle='-', color=blue)
    ax1.plot(x, np.ones(80) * 10, label='Governmental target', linestyle='--', color=blue)
    ax1.scatter(2030, 10, label='Governmental target', facecolor='None', edgecolor=blue)
    #ax1.scatter(year0, 0.05, label='Today', color=blue)

    plt.xlim(plot_settings['xlim'])
    plt.ylim(0)
    plt.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False)
    plt.savefig(os.getcwd() + '\\plot_installed_cap_elc.' + plot_type, bbox_inches='tight')


def plot_installed_cap_man(df_em):
    '''
    Function that will create a plot of the installed manufacturing capacities for electrolyzers.
    :param:
        pd.DataFrame df_em: Data from the electrolyzer market
    :return:
    '''
    y1_column = 'Installed capacity Manufacturings'
    y1 = df_em[y1_column]

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Installed capacity [GW/Year]')
    ax1.plot(x, y1/1000, label='Electrolyzer factory', linestyle='-', color=purple)
    #ax1.scatter(year0, 0.04, label='Today', color=purple)

    plt.xlim(plot_settings['xlim'])
    plt.ylim(0)
    plt.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False)
    plt.savefig(os.getcwd() + '\\plot_installed_cap_man.' + plot_type, bbox_inches='tight')


def plot_installed_cap_all(df_pm, df_hm, df_em):
    '''
    Function that will create a plot of the installed capacities for all markets (renewables, electrolyzers,
    manufacturing).
    :param:
        pd.DataFrame df_pm: Data from the power market
        pd.DataFrame df_hm: Data from the hydrogen market
        pd.DataFrame df_em: Data from the electrolyzer market
    :return:
    '''
    # Power Producers
    y1_column = 'Installed capacity Renewables'
    y1 = df_pm[y1_column]
    # Hydrogen Producers
    y2_column = 'Installed capacity Electrolyzers'
    y2 = df_hm[y2_column]
    # Electrolyzer Producers
    y3_column = 'Installed capacity Manufacturings'
    y3 = df_em[y3_column]

    fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=plot_settings['figsize'],
                                        gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'],
                                        sharex=True)

    ax1.set_ylabel('[GW]')
    ax1.plot(x, y1/1000, label='Renewables', linestyle='-', color=green)
    ax1.plot(x, (np.ones(80) * 375), label='Governmental target', linestyle='--', color=orange)
    ax1.scatter(2030, 375, label='Governmental target', facecolor='None', edgecolor=orange)
    #ax1.scatter(year0, 168, label='Today', color='black')
    #ax1.legend(loc='upper left')
    ax1.title.set_text('Installed capacity Renewables, Electrolyzers and Electrolyzer Factories')
    ax1.set_ylim(0)

    ax2.set_ylabel('[GW]')
    ax2.plot(x, y2/1000, label='Electrolyzers', linestyle='-', color=blue)
    ax2.plot(x, np.ones(80) * 10, label='Governmental target', linestyle='--', color=orange)
    ax2.scatter(2030, 10, label='Governmental target', facecolor='None', edgecolor=orange)
    #ax2.scatter(year0, 0.05, label='Today', color=blue)
    #ax2.legend(loc='upper left')
    ax2.set_ylim(0)

    ax3.set_ylabel('[GW/Year]')
    ax3.plot(x, y3/1000, label='Electrolyzer factory', linestyle='-', color=purple)
    #ax3.scatter(year0, 0.04, label='Today', color=green)
    #ax3.legend(loc='upper left')
    ax3.set_ylim(0)

    # Legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles3, labels3 = ax3.get_legend_handles_labels()

    handles = handles1 + handles2 + handles3
    labels = labels1 + labels2 + labels3

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower left', bbox_to_anchor=(-0.05, -0.75),
               frameon=False, ncol=3)


    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_installed_cap_all.' + plot_type, bbox_inches='tight')


def plot_electricity_production(df_pm):
    '''
    Function that will create a plot of the electricity production and its parts.
    :param:
        pd.DataFrame df_pm: Daily data from the power market
    :return:
    '''
    # Renewables
    y1_column = 'Actual production renewables'
    y1 = df_pm[y1_column]

    # Renewables + curtailment
    y2_column = 'Maximum production renewables'
    y2 = df_pm[y2_column]

    # Electricity demand others
    y4_column = 'Electricity demand others'
    y4 = df_pm[y4_column]

    # GT
    y5_column = 'Production gas turbines'
    y5 = pd.Series()
    for i in y2.index:
        if (y2[i] < y4[i]):
            y5[i] = (y4[i] - y2[i])
        else:
            y5[i] = 0

    # Production renewables
    y6_column = 'Production renewables'
    y6 = y1 + y5

    # Curtailment renewables
    y7_column = 'Curtailment renewables'
    y7 = y2 + y5

    # From daily to yearly datapoints
    WindowSize = int(365)
    i = 0
    y4_year = pd.Series()
    y5_year = pd.Series()
    y6_year = pd.Series()
    y7_year = pd.Series()
    while i < 80:
        y4_year[i] = (y4[i*WindowSize:(i+1)*WindowSize-1].sum())/1e6
        y5_year[i] = (y5[i*WindowSize:(i+1)*WindowSize-1].sum())/1e6
        y6_year[i] = (y6[i*WindowSize:(i+1)*WindowSize-1].sum())/1e6
        y7_year[i] = (y7[i*WindowSize:(i+1)*WindowSize-1].sum())/1e6
        i += 1

    # Normalize with the demand
    y5_year = y5_year/y4_year
    y6_year = y6_year/y4_year
    y7_year = y7_year/y4_year
    y4_year = y4_year/y4_year

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Electricity mix [-]')

    ax1.plot(x, y4_year, label='General electricity demand', linestyle='-', color='black')
    ax1.plot(x, y5_year, linestyle='-', color='black')
    ax1.plot(x, y6_year, linestyle='-', color='black')
    ax1.plot(x, y7_year, linestyle='-', color='black')

    ax1.fill_between(x, y5_year, 0, label='Production gas turbines', color=grey, alpha=0.25, edgecolor='none')
    ax1.fill_between(x, y5_year, y4_year, label='Production renewables', color=green, alpha=0.25, edgecolor='none')
    ax1.fill_between(x, y4_year, y6_year, label='Green hydrogen production', color=blue, alpha=0.25, edgecolor='none')
    ax1.fill_between(x, y6_year, y7_year, label='Curtailment renewables', color=purple, alpha=0.25, edgecolor='none')

    plt.xlim(plot_settings['xlim'])
    plt.ylim(0)
    plt.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), ncol=3, frameon=False)
    plt.savefig(os.getcwd() + '\\plot_electricity_production.' + plot_type, bbox_inches='tight')


def plot_hydrogen_production(df_hm_yearly, df_hm_daily):
    '''
    This function will create a plot of the actual and theoretical maximum hydrogen production.
    :param:
        pd.DataFrame df_hm_yearly: Yearly data of the hydrogen market
        pd.DataFrame df_hm_daily: Daily data of the hydrogen market
    :return:
    '''
    # Effiency electrolyzer
    eta = 0.7

    # Hydrogen
    y1_column = 'Actual production electrolyzers'
    y1 = df_hm_daily[y1_column]

    # Max Production
    y2_column = 'Installed capacity Electrolyzers'
    y2 = df_hm_yearly[y2_column] * 24 * 365 * eta

    # From daily to yearly datapoints
    WindowSize = int(365)
    i = 0
    y1_year = pd.Series()
    y2_year = y2
    while i < 80:
        y1_year[i] = (y1[i*WindowSize:(i+1)*WindowSize-1].sum())
        i += 1

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Hydrogen production [TWh/year]')
    ax1.plot(x, y1_year/1e6, label='Hydrogen production', linestyle='-', color=blue)
    ax1.plot(x, y2_year/1e6, label='Maximum hydrogen production', linestyle='--', color=darkblue)

    ax1.fill_between(x, y1_year/1e6, 0, color=blue, alpha=0.7, edgecolor='none')
    ax1.fill_between(x, y1_year/1e6, y2_year/1e6, color=darkblue, alpha=0.7, edgecolor='none')
    ax1.set_ylim(0)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Hydrogen production [Mio t./year]')
    ax2.plot(x, y1_year/0.33/1e9, label='Hydrogen production', linestyle='-', color=blue)
    ax2.plot(x, y2_year/0.33/1e9, label='Maximum hydrogen production', linestyle='--', color=darkblue)
    ax2.set_ylim(0)

    plt.xlim(plot_settings['xlim'])
    plt.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), ncol=2, frameon=False)
    plt.savefig(os.getcwd() + '\\plot_hydrogen_production.' + plot_type, bbox_inches='tight')


def plot_utilization_elc(df_hm):
    '''
    Function that will create a plot of the utilization per year of the electrolyzers.
    :param:
        pd.DataFrame df_hm: Daily data from the hydrogen market
    :return:
    '''
    # Utilization rate
    y1_column = 'Utilization rate'
    y1 = df_hm[y1_column]

    # From daily to yearly datapoints
    WindowSize = int(365)
    i = 0
    y1_year = pd.Series()
    while i < 80:
        y1_year[i] = y1[i*WindowSize:(i+1)*WindowSize-1].mean() * 100
        i += 1

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Utilization rate [%]')
    ax1.plot(x, y1_year, label='Electrolyzers', linestyle='-', color=blue)
    ax1.set_ylim(0, 100)
    ax1.legend(loc='upper left')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Full load hours [h]')
    ax2.plot(x, y1_year / 100 * 8760, linestyle='-', color=blue)
    ax2.set_ylim(0, 8760)

    plt.xlim(plot_settings['xlim'])
    plt.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False)
    plt.savefig(os.getcwd() + '\\plot_utilization_elc.' + plot_type, bbox_inches='tight')


def plot_duration_curves_res(df_pm_yearly, df_pm_daily, no_of_lines=10):
    '''
    Function that will create a plot of the duration curves of the renewables.
    :param:
        pd.DataFrame df_pm_yearly: Yearly data from the power market
        pd.DataFrame df_pm_daily: Daily data from the power market
        int no_of_lines: The number of years to plot (default 10)
    :return:
    '''
    # Yearly data
    y1_column = 'Installed capacity Renewables'
    y1 = df_pm_yearly[y1_column]

    # Daily data
    y2_column = 'Actual production renewables'
    y2 = df_pm_daily[y2_column]

    fig = plt.figure(figsize=plot_settings['figsize'], dpi=plot_settings['dpi'])
    ax1 = fig.add_subplot(111, projection='3d')

    for i in range(40):
        if i % round(40/no_of_lines) == 0:
            day = list(range(0, 365))
            year = np.full_like(day, i+year0)
            util = y2[(i * 365):((i + 1) * 365)] / (y1[i] * 24)
            util = util.sort_values(ascending=False).to_list()
            ax1.plot(day, year, util, label=str('Year: ' + str(year[0])), color=green)

    ax1.set_xlabel('Day')
    ax1.set_ylabel('Year')
    ax1.set_zlabel('Utilization rate [-]')

    ax1.set_xlim(0, 365)
    ax1.set_ylim(plot_settings['xlim'])
    ax1.set_zlim(0, 1)

    #plt.legend(loc=plot_settings['loc'] , frameon=False)
    plt.savefig(os.getcwd() + '\\plot_duration_curves_res.' + plot_type, bbox_inches='tight')


def plot_duration_curves_elc(df_hm, no_of_lines=10):
    '''
    Function that will create a plot of the duration curves of the electrolyzers.
    :param:
        pd.DataFrame df_hm: Daily data from the hydrogen market
        int no_of_lines: The number of years to plot (default 10)
    :return:
    '''
    y1_column = 'Utilization rate'
    y1 = df_hm[y1_column]

    fig = plt.figure(figsize=plot_settings['figsize'], dpi=plot_settings['dpi'])
    ax1 = fig.add_subplot(111, projection='3d')

    for i in range(40):
        if i % round(40/no_of_lines) == 0:
            day = list(range(0, 365))
            year = np.full_like(day, i+year0)
            util = y1[(i * 365):((i + 1) * 365)]
            util = util.sort_values(ascending=False).to_list()
            ax1.plot(day, year, util, label=str('Year: ' + str(year[0])), color=blue)

    ax1.set_xlabel('Day')
    ax1.set_ylabel('Year')
    ax1.set_zlabel('Utilization rate [-]')

    ax1.set_xlim(0, 365)
    ax1.set_ylim(plot_settings['xlim'])
    ax1.set_zlim(0, 1)

    #plt.legend(loc=plot_settings['loc'], frameon=False)
    plt.savefig(os.getcwd() + '\\plot_duration_curves_elc.' + plot_type, bbox_inches='tight')


def plot_load_type_elc(df_pm, df_hm):
    '''
    Function that will create a plot of the load type of the electrolyzer.
    :param:
        pd.DataFrame df_pm: Yearly data from the power market
        pd.DataFrame df_hm: Yearly data from the hydrogen market
    :return:
    '''

    y_column = 'Cost share'
    y = df_pm[y_column]

    yh_colum = 'Installed capacity Electrolyzers'
    yh = df_hm[yh_colum]

    y1 = pd.Series()
    y2 = pd.Series()
    y3 = pd.Series()
    for i in y.index:
        if yh[i] > 0:
            y1[i] = float(y[i][1:-1].split(' ')[0]) * 100
            y2[i] = float(y[i][1:-1].split(' ')[1]) * 100
            y3[i] = float(y[i][1:-1].split(' ')[2]) * 100
        else:
            y1[i] = 100
            y2[i] = 0
            y3[i] = 0

    cases = {
        'No load': y1,
        'Partial load': y2,
        'Full load': y3
    }

    width = 0.5
    bottom = 0

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    for label, case in cases.items():
        if 'No load' in label:
            tmpcolor = black
        elif 'Partial load' in label:
            tmpcolor = blue
        else:
            tmpcolor = green

        p = ax1.bar(x, case, width, label=label, bottom=bottom, color=tmpcolor)
        bottom += case

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Share [%]')

    plt.ylim(2023.5, 2065.5)
    plt.xlim(plot_settings['xlim'])
    plt.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False)
    plt.savefig(os.getcwd() + '\\plot_load_type_elc.' + plot_type, bbox_inches='tight')


def plot_p_elc_vs_lcoe(df_pm):
    '''
    Function that will create a plot of the price for electricity and the lcoe.
    :param:
        pd.DataFrame df_pm: Yearly data from the power market
    :return:
    '''
    y1_column = 'Weighted Price Electricity'
    y1 = df_pm[y1_column]

    y2_column = 'LCOE'
    y2 = df_pm[y2_column]

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Costs [€/MWh]')
    ax1.plot(x, y1, label='Weighted price electricity', linestyle='-', color=green)
    ax1.plot(x, y2, label='Levelized costs of renewable electricity', linestyle='--', color=green)

    plt.xlim(plot_settings['xlim'])
    plt.ylim(0)
    plt.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False)
    plt.savefig(os.getcwd() + '\\plot_p_elc_vs_lcoe.' + plot_type, bbox_inches='tight')


def plot_p_h2_vs_lcoh(df_hm):
    '''
    Function that will create a plot of the price for hydrogen and the lcoh.
    :param:
        pd.DataFrame df_hm: Yearly data from the hydrogen market
    :return:
    '''
    y1_column = 'Price Hydrogen'
    y1 = df_hm[y1_column]
    y1 = y1.replace(1e-10, np.nan)

    y2_column = 'LCOH'
    y2 = df_hm[y2_column]

    # Remove values for no electrolyzers
    y2 = y2.replace(1e10, np.nan)

    # Convert to €/kg
    y1_new = y1 * 0.039
    y2_new = y2 * 0.039

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Costs [€/MWh]')
    ax1.set_yscale('log')
    ax1.plot(x, y1, label='Price hydrogen', linestyle='-', color=blue)
    ax1.plot(x, y2, label='Levelized costs of hydrogen', linestyle='--', color=blue)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Costs [€/kg]')
    ax2.set_yscale('log')
    ax2.plot(x, y1_new, label='Price hydrogen', linestyle='-', color=blue)
    ax2.plot(x, y2_new, label='Levelized costs of hydrogen', linestyle='--', color=blue)

    plt.xlim(plot_settings['xlim'])
    plt.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False)
    plt.savefig(os.getcwd() + '\\plot_p_h2_vs_lcoh.' + plot_type, bbox_inches='tight')


def plot_p_elc_ave_vs_lcoe_ave(df_ep, df_sale):
    '''
    Function that will create a plot of the price for electrolyzer and the lcoe.
    :param:
        pd.DataFrame df_ep: Yearly data from the electrolyzer producers
        pd.DataFrame df_sale: Yearly data from the electrolyzers' sales
    :return:
    '''
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Mean - Price electrolyzer', 'Mean - LCOE'])
    df_phi_ep = df_ep.set_index(['Year', 'ID'])
    df_phi_sale = df_sale.set_index(['Year', 'EP ID'])

    for i in range(80):
        if i in df_phi_sale.index.levels[0]:
            tmp_df = df_phi_sale.loc[i]['Price']
            df_plot['Mean - Price electrolyzer'][i] = tmp_df.mean()
        if i in df_phi_ep.index.levels[0]:
            tmp_df = df_phi_ep.loc[i]['LCOE']
            tmp_df = tmp_df.replace(1e10, np.nan)
            df_plot['Mean - LCOE'][i] = tmp_df.mean()

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Cost [Mio. €/MW]')
    ax1.plot(x, df_plot['Mean - Price electrolyzer']/1e6, label='Price electrolyzer', linestyle='-', color=purple)
    ax1.plot(x, df_plot['Mean - LCOE']/1e6, label='LCOE', linestyle='--', color=purple)
    ax1.set_ylim(0)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Cost [€/kW]')
    ax2.plot(x, df_plot['Mean - Price electrolyzer']/1000, label='_hidden', linestyle='-', color=purple)
    ax2.plot(x, df_plot['Mean - LCOE']/1000, label='_hidden', linestyle='--', color=purple)
    ax2.set_ylim(0)

    plt.xlim(plot_settings['xlim'])
    plt.ylim(0)
    plt.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False)
    plt.savefig(os.getcwd() + '\\plot_p_elc_ave_vs_lcoe.' + plot_type, bbox_inches='tight')


def plot_p_elc_vs_c_elc(df_sale):
    '''
    Function that will create a plot of the average ratio of price and costs for electroyzers
    :param:
        pd.DataFrame df_sale: Yearly data from the electrolyzers' sales
    :return:
    '''
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Mean - Electrolyzers', 'Median - Electrolyzers',
                                                                  'Min - Electrolyzers', 'Max - Electrolyzers',
                                                                  'Weighted average - Electrolyzers'])
    df_phi = df_sale.set_index(['Year', 'EP ID'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df1 = df_phi.loc[i]['Production costs']
            tmp_df2 = df_phi.loc[i]['Price']
            tmp_df = tmp_df2/tmp_df1
            df_plot['Mean - Electrolyzers'][i] = tmp_df.mean()
            df_plot['Median - Electrolyzers'][i] = tmp_df.median()
            df_plot['Min - Electrolyzers'][i] = tmp_df.min()
            df_plot['Max - Electrolyzers'][i] = tmp_df.max()
            tmp_df1 = df_phi.loc[i]['Production costs'] * df_phi.loc[i]['Capacity']
            tmp_df2 = df_phi.loc[i]['Price'] * df_phi.loc[i]['Capacity']
            tmp_df = tmp_df2.sum()/tmp_df1.sum()
            df_plot['Weighted average - Electrolyzers'][i] = tmp_df

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Ratio Price/Costs [-]')
    ax1.set_yscale('log')
    #ax1.plot(x, df_plot['Mean - Electrolyzers'], label='Mean - Electrolyzers', linestyle='-', color=green)
    ax1.plot(x, df_plot['Median - Electrolyzers'], label='Median - Electrolyzers', linestyle='-', color=purple)
    #ax1.plot(x, df_plot['Weighted average - Electrolyzers'], label='Weighted average - Electrolyzers', linestyle='-.',
    #         color=purple)
    ax1.scatter(x, df_plot['Min - Electrolyzers'], label='Min - Electrolyzers', marker='o', color=purple)

    ax1.plot(x, np.ones(80), label='0% Profit', linestyle='--', color=orange)
    ax1.plot(x, np.ones(80)*2, label='100% Profit', linestyle='-.', color=orange)

    plt.xlim(plot_settings['xlim'])
    #plt.ylim(0)
    plt.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False)
    plt.savefig(os.getcwd() + '\\plot_p_elc_vs_c_elc.' + plot_type, bbox_inches='tight')


def plot_investment_threshold_pp(df_pp):
    '''
    Function that will create a plot of the average investment threshold of the Power Producers.
    :param:
        pd.DataFrame df_pp: Yearly data of the Power Producers.
    :return:
    '''
    df_phi = df_pp.set_index(['Year', 'ID'])
    df_plot = pd.DataFrame(data=0, index=range(80), columns=['97.5 Percentile', '75 Percentile', 'Median', 'Mean',
                                                             '25 Percentile', '2.5 Percentile'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Investment threshold']
            df_plot['97.5 Percentile'][i] = tmp_df.quantile(q=0.975)
            df_plot['75 Percentile'][i] = tmp_df.quantile(q=0.75)
            df_plot['Median'][i] = tmp_df.median()
            df_plot['Mean'][i] = tmp_df.mean()
            df_plot['25 Percentile'][i] = tmp_df.quantile(q=0.25)
            df_plot['2.5 Percentile'][i] = tmp_df.quantile(q=0.025)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Investment threshold')
    ax1.plot(x, df_plot['Median'], label='Median', linestyle='-', color=green)
    #ax1.plot(x, df_plot['Mean'], label='Mean', linestyle='--', color='black')
    #ax1.plot(x, df_plot['97.5 Percentile'], label='97.5 Percentile', linestyle='-', color='black', alpha=0.3)
    #ax1.plot(x, df_plot['75 Percentile'], label='75 Percentile', linestyle='-', color='black', alpha=0.55)
    #ax1.plot(x, df_plot['25 Percentile'], label='25 Percentile', linestyle='-', color='black', alpha=0.55)
    #ax1.plot(x, df_plot['2.5 Percentile'], label='2.5 Percentile', linestyle='-', color='black', alpha=0.3)

    #ax1.fill_between(x, df_plot['97.5 Percentile'], df_plot['2.5 Percentile'], color='black', alpha=0.25)
    #ax1.fill_between(x, df_plot['97.5 Percentile'], df_plot['75 Percentile'], color='black', alpha=0.25)
    ax1.fill_between(x, df_plot['75 Percentile'], df_plot['25 Percentile'], color=green, alpha=0.25, edgecolor='none')
    #ax1.fill_between(x, df_plot['25 Percentile'], df_plot['2.5 Percentile'], color='black', alpha=0.25)

    plt.xlim(plot_settings['xlim'])
    plt.ylim(-1)
    plt.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False)
    plt.savefig(os.getcwd() + '\\plot_investment_threshold_pp.' + plot_type, bbox_inches='tight')


def plot_investment_threshold_hp(df_hp):
    '''
    Function that will create a plot of the average investment threshold of the Hydrogen Producers.
    :param:
        pd.DataFrame df_hp: Yearly data of the Hydrogen Producers.
    :return:
    '''
    df_phi = df_hp.set_index(['Year', 'ID'])
    df_plot = pd.DataFrame(data=0, index=range(80), columns=['97.5 Percentile', '75 Percentile', 'Median', 'Mean',
                                                             '25 Percentile', '2.5 Percentile'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Investment threshold']
            df_plot['97.5 Percentile'][i] = tmp_df.quantile(q=0.975)
            df_plot['75 Percentile'][i] = tmp_df.quantile(q=0.75)
            df_plot['Median'][i] = tmp_df.median()
            df_plot['Mean'][i] = tmp_df.mean()
            df_plot['25 Percentile'][i] = tmp_df.quantile(q=0.25)
            df_plot['2.5 Percentile'][i] = tmp_df.quantile(q=0.025)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Investment threshold')
    ax1.plot(x, df_plot['Median'], label='Median', linestyle='-', color=blue)
    #ax1.plot(x, df_plot['Mean'], label='Mean', linestyle='--', color=blue)
    #ax1.plot(x, df_plot['97.5 Percentile'], label='97.5 Percentile', linestyle='-', color=blue, alpha=0.3)
    #ax1.plot(x, df_plot['75 Percentile'], label='75 Percentile', linestyle='-', color=blue, alpha=0.55)
    #ax1.plot(x, df_plot['25 Percentile'], label='25 Percentile', linestyle='-', color=blue, alpha=0.55)
    #ax1.plot(x, df_plot['2.5 Percentile'], label='2.5 Percentile', linestyle='-', color=blue, alpha=0.3)

    #ax1.fill_between(x, df_plot['97.5 Percentile'], df_plot['75 Percentile'], color=blue, alpha=0.25)
    ax1.fill_between(x, df_plot['75 Percentile'], df_plot['25 Percentile'], color=blue, alpha=0.25, edgecolor='none')
    #ax1.fill_between(x, df_plot['25 Percentile'], df_plot['2.5 Percentile'], color=blue, alpha=0.25)
    #ax1.fill_between(x, df_plot['97.5 Percentile'], df_plot['2.5 Percentile'], color=blue, alpha=0.25)

    plt.xlim(plot_settings['xlim'])
    plt.ylim(-1)
    plt.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False)
    plt.savefig(os.getcwd() + '\\plot_investment_threshold_hp.' + plot_type, bbox_inches='tight')


def plot_investment_threshold_ep(df_ep):
    '''
    Function that will create a plot of the average investment threshold of the electrolyzer producers.
    :param:
        pd.DataFrame df_ep: Yearly data fo the electrolyzer producers
    :return:
    '''
    df_phi = df_ep.set_index(['Year', 'ID'])
    df_plot = pd.DataFrame(data=0, index=range(80), columns=['97.5 Percentile', '75 Percentile', 'Median', 'Mean',
                                                             '25 Percentile', '2.5 Percentile'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Investment threshold']
            df_plot['97.5 Percentile'][i] = tmp_df.quantile(q=0.975)
            df_plot['75 Percentile'][i] = tmp_df.quantile(q=0.75)
            df_plot['Median'][i] = tmp_df.median()
            df_plot['Mean'][i] = tmp_df.mean()
            df_plot['25 Percentile'][i] = tmp_df.quantile(q=0.25)
            df_plot['2.5 Percentile'][i] = tmp_df.quantile(q=0.025)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Investment threshold')
    ax1.plot(x, df_plot['Median'], label='Median', linestyle='-', color=purple)
    #ax1.plot(x, df_plot['Mean'], label='Mean', linestyle='--', color=green)
    #ax1.plot(x, df_plot['97.5 Percentile'], label='97.5 Percentile', linestyle='-', color=green, alpha=0.3)
    #ax1.plot(x, df_plot['75 Percentile'], label='75 Percentile', linestyle='-', color=green, alpha=0.55)
    #ax1.plot(x, df_plot['25 Percentile'], label='25 Percentile', linestyle='-', color=green, alpha=0.55)
    #ax1.plot(x, df_plot['2.5 Percentile'], label='2.5 Percentile', linestyle='-', color=green, alpha=0.3)

    #ax1.fill_between(x, df_plot['97.5 Percentile'], df_plot['75 Percentile'], color=green, alpha=0.25)
    ax1.fill_between(x, df_plot['75 Percentile'], df_plot['25 Percentile'], color=purple, alpha=0.25, edgecolor='none')
    #ax1.fill_between(x, df_plot['25 Percentile'], df_plot['2.5 Percentile'], color=green, alpha=0.25)
    #ax1.fill_between(x, df_plot['97.5 Percentile'], df_plot['2.5 Percentile'], color=green, alpha=0.25)

    plt.xlim(plot_settings['xlim'])
    plt.ylim(-1)
    plt.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False)
    plt.savefig(os.getcwd() + '\\plot_investment_threshold_ep.' + plot_type, bbox_inches='tight')


def plot_weighted_investment_threshold_pp(df_pp):
    '''
    Function that will create a plot of the capacity weighted investment threshold of the power producers.
    :param:
        pd.DataFrame df_pp: Yearly data of the power producers
    :return:
    '''
    df_phi = df_pp.set_index(['Year', 'ID'])
    df_plot = pd.DataFrame(data=0, index=range(80), columns=['Median', 'Mean', 'Weighted average'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Investment threshold']
            tmp_weight = (df_phi.loc[i]['Investment threshold'] * df_phi.loc[i]['Installed capacity Renewables'])
            df_plot['Median'][i] = tmp_df.median()
            df_plot['Mean'][i] = tmp_df.mean()
            df_plot['Weighted average'][i] = tmp_weight.sum() / df_phi.loc[i]['Installed capacity Renewables'].sum()

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Investment threshold')
    #ax1.plot(x, df_plot['Median'], label='Median', linestyle='-', color=black)
    #ax1.plot(x, df_plot['Mean'], label='Mean', linestyle='--', color=black)
    ax1.plot(x, df_plot['Weighted average'], label='Weighted average', linestyle='-', color=green)

    plt.xlim(plot_settings['xlim'])
    plt.ylim(-1)
    plt.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False)
    plt.savefig(os.getcwd() + '\\plot_weighted_investment_threshold_pp.' + plot_type, bbox_inches='tight')


def plot_weighted_investment_threshold_hp(df_hp):
    '''
    Function that will create a plot of the capacity weighted investment threshold of the hydrogen producers.
    :param:
        pd.DataFrame df_hp: Yearly data of the hydrogen producers
    :return:
    '''
    df_phi = df_hp.set_index(['Year', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Median', 'Mean', 'Weighted average'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Investment threshold']
            tmp_weight = (df_phi.loc[i]['Investment threshold'] * df_phi.loc[i]['Installed capacity Electrolyzers'])
            df_plot['Median'][i] = tmp_df.median()
            df_plot['Mean'][i] = tmp_df.mean()
            df_plot['Weighted average'][i] = tmp_weight.sum() / df_phi.loc[i]['Installed capacity Electrolyzers'].sum()

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Investment threshold')
    #ax1.plot(x, df_plot['Median'], label='Median', linestyle='-', color=blue)
    #ax1.plot(x, df_plot['Mean'], label='Mean', linestyle='--', color=blue)
    ax1.plot(x, df_plot['Weighted average'], label='Weighted average', linestyle='-', color=blue)

    plt.xlim(plot_settings['xlim'])
    plt.ylim(-1)
    plt.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False)
    plt.savefig(os.getcwd() + '\\plot_weighted_investment_threshold_hp.' + plot_type, bbox_inches='tight')


def plot_weighted_investment_threshold_ep(df_ep):
    '''
    Function that will create a plot of the capacity weighted investment threshold of the electrolyzer producers.
    :param:
        pd.DataFrame df_ep: Yearly data of the electrolyzer producers
    :return:
    '''
    df_phi = df_ep.set_index(['Year', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Median', 'Mean', 'Weighted average'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Investment threshold']
            tmp_weight = (df_phi.loc[i]['Investment threshold'] * df_phi.loc[i]['Installed capacity Manufacturings'])
            df_plot['Median'][i] = tmp_df.median()
            df_plot['Mean'][i] = tmp_df.mean()
            df_plot['Weighted average'][i] = tmp_weight.sum() / df_phi.loc[i]['Installed capacity Manufacturings'].sum()

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Investment threshold')
    #ax1.plot(x, df_plot['Median'], label='Median', linestyle='-', color=green)
    #ax1.plot(x, df_plot['Mean'], label='Mean', linestyle='--', color=green)
    ax1.plot(x, df_plot['Weighted average'], label='Weighted average', linestyle='-', color=purple)

    plt.xlim(plot_settings['xlim'])
    plt.ylim(-1)
    plt.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False)
    plt.savefig(os.getcwd() + '\\plot_weighted_investment_threshold_ep.' + plot_type, bbox_inches='tight')


def plot_age_res(df_res):
    '''
    Function that will create a plot of the average age of the renewables.
    :param:
        pd.DataFrame df_res: Yearly data of the renewables
    :return:
    '''
    df_phi = df_res.set_index(['Year', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['97.5 Percentile', '75 Percentile', 'Median', 'Mean',
                                                             '25 Percentile', '2.5 Percentile'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Age']
            df_plot['97.5 Percentile'][i] = tmp_df.quantile(q=0.975)
            df_plot['75 Percentile'][i] = tmp_df.quantile(q=0.75)
            df_plot['Median'][i] = tmp_df.median()
            df_plot['Mean'][i] = tmp_df.mean()
            df_plot['25 Percentile'][i] = tmp_df.quantile(q=0.25)
            df_plot['2.5 Percentile'][i] = tmp_df.quantile(q=0.025)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1. set_xlabel('Year')
    ax1.set_ylabel('Age')
    ax1.plot(x, df_plot['Median'], label='Median', linestyle='-', color=green)
    #ax1.plot(x, df_plot['Mean'], label='Mean', linestyle='--', color=black)
    #ax1.plot(x, df_plot['97.5 Percentile'], label='97.5 Percentile', linestyle='-', color=black, alpha=0.3)
    #ax1.plot(x, df_plot['75 Percentile'], label='75 Percentile', linestyle='-', color=black, alpha=0.55)
    #ax1.plot(x, df_plot['25 Percentile'], label='25 Percentile', linestyle='-', color=black, alpha=0.55)
    #ax1.plot(x, df_plot['2.5 Percentile'], label='2.5 Percentile', linestyle='-', color=black, alpha=0.3)

    #ax1.fill_between(x, df_plot['97.5 Percentile'], df_plot['75 Percentile'], color=black, alpha=0.25)
    ax1.fill_between(x, df_plot['75 Percentile'], df_plot['25 Percentile'], color=green, alpha=0.25, edgecolor='none')
    #ax1.fill_between(x, df_plot['25 Percentile'], df_plot['2.5 Percentile'], color=black, alpha=0.25)
    #ax1.fill_between(x, df_plot['97.5 Percentile'], df_plot['2.5 Percentile'], color=black, alpha=0.25)

    plt.xlim(plot_settings['xlim'])
    plt.ylim(0)
    plt.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False)
    plt.savefig(os.getcwd() + '\\plot_age_res.' + plot_type, bbox_inches='tight')


def plot_age_elc(df_elc):
    '''
    Function that will craete a plot of the average age of renewables
    :param:
        pd.DataFrame df_elc: Yearly data of electrolyzers.
    :return:
    '''
    df_phi = df_elc.set_index(['Year', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['97.5 Percentile', '75 Percentile', 'Median', 'Mean',
                                                                  '25 Percentile', '2.5 Percentile'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Age']
            df_plot['97.5 Percentile'][i] = tmp_df.quantile(q=0.975)
            df_plot['75 Percentile'][i] = tmp_df.quantile(q=0.75)
            df_plot['Median'][i] = tmp_df.median()
            df_plot['Mean'][i] = tmp_df.mean()
            df_plot['25 Percentile'][i] = tmp_df.quantile(q=0.25)
            df_plot['2.5 Percentile'][i] = tmp_df.quantile(q=0.025)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1. set_xlabel('Year')
    ax1.set_ylabel('Age')
    ax1.plot(x, df_plot['Median'], label='Median', linestyle='-', color=blue)
    #ax1.plot(x, df_plot['Mean'], label='Mean', linestyle='--', color=blue)
    #ax1.plot(x, df_plot['97.5 Percentile'], label='97.5 Percentile', linestyle='-', color=blue, alpha=0.3)
    #ax1.plot(x, df_plot['75 Percentile'], label='75 Percentile', linestyle='-', color=blue, alpha=0.55)
    #ax1.plot(x, df_plot['25 Percentile'], label='25 Percentile', linestyle='-', color=blue, alpha=0.55)
    #ax1.plot(x, df_plot['2.5 Percentile'], label='2.5 Percentile', linestyle='-', color=blue, alpha=0.3)

    #ax1.fill_between(x, df_plot['97.5 Percentile'], df_plot['75 Percentile'], color=blue, alpha=0.25)
    ax1.fill_between(x, df_plot['75 Percentile'], df_plot['25 Percentile'], color=blue, alpha=0.25, edgecolor='none')
    #ax1.fill_between(x, df_plot['25 Percentile'], df_plot['2.5 Percentile'], color=blue, alpha=0.25)
    #ax1.fill_between(x, df_plot['97.5 Percentile'], df_plot['2.5 Percentile'], color=blue, alpha=0.25)

    plt.xlim(plot_settings['xlim'])
    plt.ylim(0)
    plt.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False)
    plt.savefig(os.getcwd() + '\\plot_age_elc.' + plot_type, bbox_inches='tight')


def plot_age_man(df_man):
    '''
    Function that will create a plot of the average age of the electrolyzer factories
    :param:
        pd.DataFrame df_man: Yearly data of electrolyzer factories.
    :return:
    '''
    df_phi = df_man.set_index(['Year', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['97.5 Percentile', '75 Percentile', 'Median', 'Mean',
                                                                  '25 Percentile', '2.5 Percentile'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Age']
            df_plot['97.5 Percentile'][i] = tmp_df.quantile(q=0.975)
            df_plot['75 Percentile'][i] = tmp_df.quantile(q=0.75)
            df_plot['Median'][i] = tmp_df.median()
            df_plot['Mean'][i] = tmp_df.mean()
            df_plot['25 Percentile'][i] = tmp_df.quantile(q=0.25)
            df_plot['2.5 Percentile'][i] = tmp_df.quantile(q=0.025)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1. set_xlabel('Year')
    ax1.set_ylabel('Age')
    ax1.plot(x, df_plot['Median'], label='Median', linestyle='-', color=purple)
    #ax1.plot(x, df_plot['Mean'], label='Mean', linestyle='--', color=green)
    #ax1.plot(x, df_plot['97.5 Percentile'], label='97.5 Percentile', linestyle='-', color=green, alpha=0.3)
    #ax1.plot(x, df_plot['75 Percentile'], label='75 Percentile', linestyle='-', color=green, alpha=0.55)
    #ax1.plot(x, df_plot['25 Percentile'], label='25 Percentile', linestyle='-', color=green, alpha=0.55)
    #ax1.plot(x, df_plot['2.5 Percentile'], label='2.5 Percentile', linestyle='-', color=green, alpha=0.3)

    #ax1.fill_between(x, df_plot['97.5 Percentile'], df_plot['75 Percentile'], color=green, alpha=0.25)
    ax1.fill_between(x, df_plot['75 Percentile'], df_plot['25 Percentile'], color=purple, alpha=0.25, edgecolor='none')
    #ax1.fill_between(x, df_plot['25 Percentile'], df_plot['2.5 Percentile'], color=green, alpha=0.25)
    #ax1.fill_between(x, df_plot['97.5 Percentile'], df_plot['2.5 Percentile'], color=green, alpha=0.25)

    plt.xlim(plot_settings['xlim'])
    plt.ylim(0)
    plt.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False)
    plt.savefig(os.getcwd() + '\\plot_age_man.' + plot_type, bbox_inches='tight')


def plot_weighted_age_res(df_res):
    '''
    Function that will create a plot of the capacity weighted average age of the renewables.
    :param:
        pd.DataFrame df_res: Yearly data of the renewables
    :return:
    '''
    df_phi = df_res.set_index(['Year', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Median', 'Mean', 'Weighted average'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Age']
            tmp_weight = (df_phi.loc[i]['Age'] * df_phi.loc[i]['Capacity'])
            df_plot['Median'][i] = tmp_df.median()
            df_plot['Mean'][i] = tmp_df.mean()
            df_plot['Weighted average'][i] = tmp_weight.sum() / df_phi.loc[i]['Capacity'].sum()

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1. set_xlabel('Year')
    ax1.set_ylabel('Age')
    #ax1.plot(x, df_plot['Median'], label='Median', linestyle='-', color=black)
    #ax1.plot(x, df_plot['Mean'], label='Mean', linestyle='--', color=black)
    ax1.plot(x, df_plot['Weighted average'], label='Weighted average', linestyle='-', color=green)

    plt.xlim(plot_settings['xlim'])
    plt.ylim(0)
    plt.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False)
    plt.savefig(os.getcwd() + '\\plot_weighted_age_res.' + plot_type, bbox_inches='tight')


def plot_weighted_age_elc(df_elc):
    '''
    Function that will create a plot of the capacity weighted average age of the electrolyzers.
    :param:
        pd.DataFrame df_elc: Yearly data of the electrolyzers
    :return:
    '''
    df_phi = df_elc.set_index(['Year', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Median', 'Mean', 'Weighted average'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Age']
            tmp_weight = (df_phi.loc[i]['Age'] * df_phi.loc[i]['Capacity'])
            df_plot['Median'][i] = tmp_df.median()
            df_plot['Mean'][i] = tmp_df.mean()
            df_plot['Weighted average'][i] = tmp_weight.sum() / df_phi.loc[i]['Capacity'].sum()

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1. set_xlabel('Year')
    ax1.set_ylabel('Age')
    #ax1.plot(x, df_plot['Median'], label='Median', linestyle='-', color=blue)
    #ax1.plot(x, df_plot['Mean'], label='Mean', linestyle='--', color=blue)
    ax1.plot(x, df_plot['Weighted average'], label='Weighted average', linestyle='-', color=blue)

    plt.xlim(plot_settings['xlim'])
    plt.ylim(0)
    plt.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False)
    plt.savefig(os.getcwd() + '\\plot_weighted_age_elc.' + plot_type, bbox_inches='tight')


def plot_weighted_age_man(df_man):
    '''
    Function that will create a plot of the capacity weighted average age of the factories for electrolyzers.
    :param:
        pd.DataFrame df_elc: Yearly data of the factories for electrolyzers
    :return:
    '''
    df_phi = df_man.set_index(['Year', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Median', 'Mean', 'Weighted average'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Age']
            tmp_weight = (df_phi.loc[i]['Age'] * df_phi.loc[i]['Capacity'])
            df_plot['Median'][i] = tmp_df.median()
            df_plot['Mean'][i] = tmp_df.mean()
            df_plot['Weighted average'][i] = tmp_weight.sum() / df_phi.loc[i]['Capacity'].sum()

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Age')
    #ax1.plot(x, df_plot['Median'], label='Median', linestyle='-', color=green)
    #ax1.plot(x, df_plot['Mean'], label='Mean', linestyle='--', color=green)
    ax1.plot(x, df_plot['Weighted average'], label='Weighted average', linestyle='-', color=purple)

    plt.xlim(plot_settings['xlim'])
    plt.ylim(0)
    plt.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False)
    plt.savefig(os.getcwd() + '\\plot_weighted_age_man.' + plot_type, bbox_inches='tight')


def plot_profitability(df_pp, df_hp, df_ep):
    '''
    Function that will create a plot of the mean profitability of power, hydrogen and electrolyzer producers
    :param:
        pd.DataFrame df_pp: Yearly data of the power producers
        pd.DataFrame df_hp: Yearly data of the hydrogen producers
        pd.DataFrame df_ep: Yearly data of the electrolyzer producers
    :return:
    '''
    df_phi_pp = df_pp.set_index(['Year', 'ID'])
    df_phi_hp = df_hp.set_index(['Year', 'ID'])
    df_phi_ep = df_ep.set_index(['Year', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Mean - Power producers', 'Mean - Hydrogen producers',
                                                                  'Mean - Electrolyzer producers'])

    for i in range(80):
        if i in df_phi_pp.index.levels[0]:
            tmp_df = df_phi_pp.loc[i]['Profitability']
            df_plot['Mean - Power producers'][i] = tmp_df.median()
        if i in df_phi_hp.index.levels[0]:
            tmp_df = df_phi_hp.loc[i]['Profitability']
            df_plot['Mean - Hydrogen producers'][i] = tmp_df.median()
        if i in df_phi_ep.index.levels[0]:
            tmp_df = df_phi_ep.loc[i]['Profitability']
            df_plot['Mean - Electrolyzer producers'][i] = tmp_df.median()

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Profitability')
    ax1.plot(x, df_plot['Mean - Power producers'], label='Power producers', color=green)
    ax1.plot(x, df_plot['Mean - Hydrogen producers'], label='Hydrogen producers', color=blue)
    ax1.plot(x, df_plot['Mean - Electrolyzer producers'], label='Electrolyzer producers', color=purple)
    ax1.plot(x, np.ones(80), label='Profitability threshold', linestyle='-.', color=orange)

    plt.xlim(plot_settings['xlim'])
    plt.ylim(0)
    plt.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), ncol=2, frameon=False)
    plt.savefig(os.getcwd() + '\\plot_profitability.' + plot_type, bbox_inches='tight')


def plot_weighted_profitability(df_pp, df_hp, df_ep):
    '''
    Function that will create a plot of the capacity weighted average profitability of power, hydrogen and electrolyzer
    producers
    :param:
        pd.DataFrame df_pp: Yearly data of the power producers
        pd.DataFrame df_hp: Yearly data of the hydrogen producers
        pd.DataFrame df_ep: Yearly data of the electrolyzer producers
    :return:
    '''
    df_phi_pp = df_pp.set_index(['Year', 'ID'])
    df_phi_hp = df_hp.set_index(['Year', 'ID'])
    df_phi_ep = df_ep.set_index(['Year', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Mean - Power producers', 'Mean - Hydrogen producers',
                                                                  'Mean - Electrolyzer producers',
                                                                  'Weighted average - Power producers',
                                                                  'Weighted average - Hydrogen producers',
                                                                  'Weighted average - Electrolyzer producers',])

    for i in range(80):
        if i in df_phi_pp.index.levels[0]:
            tmp_df = df_phi_pp.loc[i]['Profitability']
            tmp_weight = df_phi_pp.loc[i]['Profitability'] * df_phi_pp.loc[i]['Installed capacity Renewables']
            df_plot['Mean - Power producers'][i] = tmp_df.median()
            df_plot['Weighted average - Power producers'][i] = (tmp_weight.sum() /
                                                                df_phi_pp.loc[i]['Installed capacity Renewables'].sum())
        if i in df_phi_hp.index.levels[0]:
            tmp_df = df_phi_hp.loc[i]['Profitability']
            tmp_weight = df_phi_hp.loc[i]['Profitability'] * df_phi_hp.loc[i]['Installed capacity Electrolyzers']
            df_plot['Mean - Hydrogen producers'][i] = tmp_df.median()
            df_plot['Weighted average - Hydrogen producers'][i] = (tmp_weight.sum() /
                                                                   df_phi_hp.loc[i]['Installed capacity Electrolyzers'].sum())
        if i in df_phi_ep.index.levels[0]:
            tmp_df = df_phi_ep.loc[i]['Profitability']
            tmp_weight = df_phi_ep.loc[i]['Profitability'] * df_phi_ep.loc[i]['Installed capacity Manufacturings']
            df_plot['Mean - Electrolyzer producers'][i] = tmp_df.median()
            df_plot['Weighted average - Electrolyzer producers'][i] = (tmp_weight.sum() /
                                                                       df_phi_ep.loc[i]['Installed capacity Manufacturings'].sum())

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Profitability')
    #ax1.plot(x, df_plot['Mean - Power producers'], label='Mean - Power producers', color=black)
    #ax1.plot(x, df_plot['Mean - Hydrogen producers'], label='Mean - Hydrogen producers', color=blue)
    #ax1.plot(x, df_plot['Mean - Electrolyzer producers'], label='Mean - Electrolyzer producers', color=green)
    ax1.plot(x, df_plot['Weighted average - Power producers'], label='Weighted average - Power producers', color=green,
             linestyle='-')
    ax1.plot(x, df_plot['Weighted average - Hydrogen producers'], label='Weighted average - Hydrogen producers',
             color=blue, linestyle='-')
    ax1.plot(x, df_plot['Weighted average - Electrolyzer producers'], label='Weighted average - Electrolyzer producers',
             color=purple, linestyle='-')
    ax1.plot(x, np.ones(80), label='Profitability threshold', linestyle='-.', color=orange)

    plt.xlim(plot_settings['xlim'])
    plt.ylim(0)
    plt.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), ncol=2, frameon=False)
    plt.savefig(os.getcwd() + '\\plot_weighted_profitability.' + plot_type, bbox_inches='tight')


def main(dir):
    '''
    Function that will create all plots based on the results in dir
    :param:
        str dir: Name of the folder with the results files
    :return:
    '''
    # Change folder
    try:
        os.chdir(dir)
    except FileNotFoundError:
        print('Error in main: Results folder not found.')
        exit(500)

    # Check and load data
    print('Check and load data for single run...')
    check_data()
    tmp_list = load_data()
    df_pm, df_hm, df_em = tmp_list[8], tmp_list[4], tmp_list[1]
    df_pm_daily, df_hm_daily = tmp_list[7], tmp_list[3]
    df_pp, df_hp, df_ep = tmp_list[9], tmp_list[5], tmp_list[2]
    df_sale = tmp_list[-1]
    df_res, df_elc, df_man = tmp_list[10], tmp_list[0], tmp_list[6]

    # Create all plots
    print('Create plots for single run...')
    plot_no_of_agents(df_pm, df_hm, df_em)
    plot_no_of_investment(df_pm, df_hm, df_em)
    plot_ratio_investment_agents(df_pm, df_hm, df_em)
    plot_installed_cap_res(df_pm)
    plot_installed_cap_elc(df_hm)
    plot_installed_cap_man(df_em)
    plot_installed_cap_all(df_pm, df_hm, df_em)
    plot_electricity_production(df_pm_daily)
    plot_hydrogen_production(df_hm, df_hm_daily)
    plot_utilization_elc(df_hm_daily)
    plot_duration_curves_res(df_pm, df_pm_daily)
    plot_duration_curves_elc(df_hm_daily)
    plot_load_type_elc(df_pm, df_hm)
    plot_p_elc_vs_lcoe(df_pm)
    plot_p_h2_vs_lcoh(df_hm)
    plot_p_elc_ave_vs_lcoe_ave(df_ep, df_sale)
    plot_p_elc_vs_c_elc(df_sale)
    plot_investment_threshold_pp(df_pp)
    plot_investment_threshold_hp(df_hp)
    plot_investment_threshold_ep(df_ep)
    plot_weighted_investment_threshold_pp(df_pp)
    plot_weighted_investment_threshold_hp(df_hp)
    plot_weighted_investment_threshold_ep(df_ep)
    plot_age_res(df_res)
    plot_age_elc(df_elc)
    plot_age_man(df_man)
    plot_weighted_age_res(df_res)
    plot_weighted_age_elc(df_elc)
    plot_weighted_age_man(df_man)
    plot_profitability(df_pp, df_hp, df_ep)
    plot_weighted_profitability(df_pp, df_hp, df_ep)
    print('Done.')


if __name__ == '__main__':
    dir = 'D:\\Jesse\\sciebo\\00_Promotion\\06_Model\\02_ABM\\02_NetLogo\\02_Output\\2024-08-05-15-07\\Sensitivity_1\\Run_1\\'
    main(dir)
