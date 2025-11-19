'''
him - Hydrogen Investment Model
This script will take the results of compare multiple runs form a sensitivity analysis and will create plots.
The list of plots can be seen below.

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


version: 0.1.24.07.19
date: 2024-07-19
author: Jesse

changelog:
0.1.24.07.19 - start new script
'''
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.legend_handler import HandlerTuple

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
plot_settings['xlim'] = (2023, 2100)
plot_settings['loc'] = 'lower left'
sensitivity_settings = {}
blue = [173/255, 189/255, 227/255]
darkblue = [2/255,  61/255, 107/255]
green = [185/255, 210/255, 95/255]
black = [0, 0, 0]
grey = [235/255, 235/255, 235/255]
orange = [250/255, 180/255, 90/255]
purple = [175/255, 130/255, 185/255]
red = [235/255, 95/255, 115/255]
year0 = 2023
delta_year = 80
x = list(range(year0, year0+delta_year))
para_dict = {'const.beta': r'$\beta$',
             'const.gamma': r'$\gamma$',
             'const.PM.delta_threshold': r'$\Delta\phi_{PM}$',
             'const.HM.delta_threshold': r'$\Delta\phi_{HM}$',
             'const.EM.delta_threshold': r'$\Delta\phi_{EM}$',
             'init.HM.threshold_0': r'$\phi_{HM, 0}$',
             'init.EM.threshold_0': r'$\phi_{EM, 0}$',
             'const.EM.inexperience_penalty_max': r'$\tau$',
             'const.EM.global_share': r'$s_{global}$',
             'const.MAN.learning_rate': r'$\lambda$',
             'GOV.h2_subsidy': r'$sub_{h_{2}}$',
             'GOV.h2_guarant': r'$price_{h_{2},guaranteed}$',
             'GOV.res_subsidy': r'$sub_{RES}$',
             'GOV.power_subsidy': r'$sub_{electricity}$',
             'GOV.power_guarant': r'$price_{electricity, guaranteed}$',
             'GOV.elc_subsidy': r'$sub_{ELC}$',
             'GOV.elc_guarant': r'$sub_{ELC, guaranteed}$',
             'GOV.man_subsidy': r'$sub_{Factory}$'
             }


def check_sensitivity_config():
    '''
    Function that checks and loads the sensitivity config file.
    :return:
    '''
    wkdir = os.getcwd()
    try:
        with open(os.path.join(wkdir, 'sensitivity.config'), 'r') as file:
            tmp_list = []
            for line in file:
                if not line.startswith('#'):
                    if line.split(':')[0] == 'type':
                        sensitivity_settings['Type'] = line.split(':')[1][1:-1]
                        if line.split(':')[1] == 'none':
                            print('No sensitivity analysis was made. Check the sensitivity.config file first.')
                            exit(101)
                    if line.split(':')[0] == 'parameters':
                        sensitivity_settings['Parameters'] = line.split(':')[1][2:-2].replace(' ', '').split(',')
                    if line.split(':')[0] == 'sensitivity_runs':
                        sensitivity_settings['No. of Runs'] = eval(line.split(':')[1][1:-1])
                    if line.split(':')[0].startswith('sensitivity_') and not line.split(':')[0].endswith('_runs'):
                        tmp_list.append(eval(line.split(':')[1][1:-1]))
            sensitivity_settings['Values'] = tmp_list
    except FileNotFoundError:
        print('Error in check_sensitivity_config: sensitivity.config file not found.')
        exit(100)


def check_data():
    '''
    Function that checks if all files exists.
    :return:
    '''
    wkdir = os.getcwd()
    global list_sens, list_runs
    list_sens = []
    list_runs = []
    for i in os.listdir(wkdir):
        if i.startswith('Sensitivity_'):
            for j in os.listdir(os.path.join(wkdir, i)):
                if j.startswith('Run_'):
                    for k in list_files:
                        if not os.path.isfile(os.path.join(wkdir, i, j, k)):
                            print('Error in check_data: ' + i + '\\' + j + '\\' + k + ' not found.')
                            exit(200)
                    if j not in list_runs:
                        list_runs.append(j)
            list_sens.append(i)
    print(str(len(list_sens)) + ' sensitivty runs and ' + str(len(list_runs)) + ' runs found.')


def load_data():
    '''
    Function that loads the data from the csv files.
    :return:
        list tmp_list: List that contains the data from all file as an individual pd.Dataframe.
    '''
    tmp_list = []
    wkdir = os.getcwd()
    for k in list_files:
        list_df = []
        for j in list_runs:
            for i in list_sens:
                try:
                    file = (str(wkdir) + '\\' + i + '\\' + j + '\\' + k)
                    tmp_df = pd.read_csv(file, sep=';')
                    tmp_df['Run'] = np.ones(len(tmp_df.index)) * int(j.split('_')[1])
                    tmp_df['Sensitivity'] = np.ones(len(tmp_df.index)) * int(i.split('_')[1])
                    list_df.append(tmp_df)
                except FileNotFoundError:
                    print('Error in load_data: ' + i + '\\' + j + '\\' + k + ' not found.')
                    exit(300)
        tmp_list.append(pd.concat(list_df))

    return(tmp_list)


def plot_no_of_agents(df_pm, df_hm, df_em):
    '''
    Will create the plot of the number of agents for all three markets.
    :param:
        pd.DataFrame df_pm: Yearly data of the power market
        pd.DataFrame df_hm: Yearly data of the hydrogen market
        pd.DataFrame df_em: Yearly data of the electrolyzer market
    :return:
    '''
    # Data
    df_phi_pp = df_pm.set_index(['Year', 'Sensitivity', 'Run'])
    df_phi_hp = df_hm.set_index(['Year', 'Sensitivity', 'Run'])
    df_phi_ep = df_em.set_index(['Year', 'Sensitivity', 'Run'])

    # Plot data
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index,
                           columns=['Power Producers - Mean', 'Power Producers - Median', 'Hydrogen Producers - Mean',
                                    'Hydrogen Producers - Median', 'Electrolyzer Producers - Mean',
                                    'Electrolyzer Producers - Median'])

    for i in range(80):
        # Power producers
        if i in df_phi_pp.index.levels[0]:
            tmp_df = df_phi_pp.loc[i]['No. of Powerproducers']
            for j in tmp_df.groupby(level=0).mean().index:
                df_plot['Power Producers - Mean'][i][j] = tmp_df.groupby(level=0).mean().loc[j]
                df_plot['Power Producers - Median'][i][j] = tmp_df.groupby(level=0).median().loc[j]
        # Hydrogen producers
        if i in df_phi_hp.index.levels[0]:
            tmp_df = df_phi_hp.loc[i]['No. of Hydrogenproducers']
            for j in tmp_df.groupby(level=0).mean().index:
                df_plot['Hydrogen Producers - Mean'][i][j] = tmp_df.groupby(level=0).mean().loc[j]
                df_plot['Hydrogen Producers - Median'][i][j] = tmp_df.groupby(level=0).median().loc[j]
        # Electrolyzer producers
        if i in df_phi_ep.index.levels[0]:
            tmp_df = df_phi_ep.loc[i]['No. of Electrolyzerproducers']
            for j in tmp_df.groupby(level=0).mean().index:
                df_plot['Electrolyzer Producers - Mean'][i][j] = tmp_df.groupby(level=0).mean().loc[j]
                df_plot['Electrolyzer Producers - Median'][i][j] = tmp_df.groupby(level=0).median().loc[j]

    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    for i in range(1, sensitivity_settings['No. of Runs']+1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Power producers
        #ax1.plot(x, df_plot['Power Producers - Mean'].xs(i, level='Sensitivity run'),linestyle='-', color=black,
        #         alpha=tmp_alpha)
        ax1.plot(x, df_plot['Power Producers - Median'].xs(i, level='Sensitivity run'),
                 label=str('Power producers: ' + str(i)), linestyle='-', color=green, alpha=tmp_alpha)

        # Hydrogen producers
        #ax1.plot(x, df_plot['Hydrogen Producers - Mean'].xs(i, level='Sensitivity run'), linestyle='-', color=blue,
        #         alpha=tmp_alpha)
        ax1.plot(x, df_plot['Hydrogen Producers - Median'].xs(i, level='Sensitivity run'),
                 label=str('Hydrogen producers: ' + str(i)), linestyle='-', color=blue, alpha=tmp_alpha)

        # Electrolyzer producers
        #ax1.plot(x, df_plot['Electrolyzer Producers - Mean'].xs(i, level='Sensitivity run'), linestyle='-', color=green,
        #         alpha=tmp_alpha)
        ax1.plot(x, df_plot['Electrolyzer Producers - Median'].xs(i, level='Sensitivity run'),
                 label=str('Electrolyzer producers: ' + str(i)), linestyle='-', color=purple, alpha=tmp_alpha)

    # Legend
    line1, = ax1.plot(x, np.ones(80)*-1, color=green, label='Power Producers')
    line2, = ax1.plot(x, np.ones(80)*-1, color=blue, label='Hydrogen Producers')
    line3, = ax1.plot(x, np.ones(80)*-1, color=purple, label='Electrolyzer Producers')
    legend1 = ax1.legend(handles=[line1, line2, line3], loc='lower left', bbox_to_anchor=(-0.05, -0.75))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80)*-1, color=green, alpha=tmp_alpha, label=tmp_label)
        tmp_line2, = ax1.plot(x, np.ones(80)*-1, color=blue, alpha=tmp_alpha, label=tmp_label)
        tmp_line3, = ax1.plot(x, np.ones(80)*-1, color=purple, alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1, tmp_line2, tmp_line3))

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    ax1.set_xlabel('Year')
    ax1.set_ylabel('No. of Agents')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(0)

    plt.savefig(os.getcwd() + '\\plot_no_of_agents.' + plot_type, bbox_inches='tight')


def plot_no_of_investment(df_pm, df_hm, df_em):
    '''
    Will create the plot of the number of investments for all three markets.
    :param:
        pd.DataFrame df_pm: Yearly data of the power market
        pd.DataFrame df_hm: Yearly data of the hydrogen market
        pd.DataFrame df_em: Yearly data of the electrolyzer market
    :return:
    '''
    # Data
    df_phi_pp = df_pm.set_index(['Year', 'Sensitivity', 'Run'])
    df_phi_hp = df_hm.set_index(['Year', 'Sensitivity', 'Run'])
    df_phi_ep = df_em.set_index(['Year', 'Sensitivity', 'Run'])

    # Plot data
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index,
                           columns=['Power Producers - Mean', 'Power Producers - Median', 'Hydrogen Producers - Mean',
                                    'Hydrogen Producers - Median', 'Electrolyzer Producers - Mean',
                                    'Electrolyzer Producers - Median'])

    for i in range(80):
        # Power producers
        if i in df_phi_pp.index.levels[0]:
            tmp_df = df_phi_pp.loc[i]['No. of Investments PM']
            for j in tmp_df.groupby(level=0).mean().index:
                df_plot['Power Producers - Mean'][i][j] = tmp_df.groupby(level=0).mean().loc[j]
                df_plot['Power Producers - Median'][i][j] = tmp_df.groupby(level=0).median().loc[j]
        # Hydrogen producers
        if i in df_phi_hp.index.levels[0]:
            tmp_df = df_phi_hp.loc[i]['No. of Investments HM']
            for j in tmp_df.groupby(level=0).mean().index:
                df_plot['Hydrogen Producers - Mean'][i][j] = tmp_df.groupby(level=0).mean().loc[j]
                df_plot['Hydrogen Producers - Median'][i][j] = tmp_df.groupby(level=0).median().loc[j]
        # Electrolyzer producers
        if i in df_phi_ep.index.levels[0]:
            tmp_df = df_phi_ep.loc[i]['No. of Investments EM']
            for j in tmp_df.groupby(level=0).mean().index:
                df_plot['Electrolyzer Producers - Mean'][i][j] = tmp_df.groupby(level=0).mean().loc[j]
                df_plot['Electrolyzer Producers - Median'][i][j] = tmp_df.groupby(level=0).median().loc[j]

    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    for i in range(1, sensitivity_settings['No. of Runs']+1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Power producers
        #ax1.plot(x, df_plot['Power Producers - Mean'].xs(i, level='Sensitivity run'),linestyle='-', color=black,
        #         alpha=tmp_alpha)
        ax1.plot(x, df_plot['Power Producers - Median'].xs(i, level='Sensitivity run'),
                 label=str('Power producers: ' + str(i)), linestyle='-', color=green, alpha=tmp_alpha)

        # Hydrogen producers
        #ax1.plot(x, df_plot['Hydrogen Producers - Mean'].xs(i, level='Sensitivity run'), linestyle='-', color=blue,
        #         alpha=tmp_alpha)
        ax1.plot(x, df_plot['Hydrogen Producers - Median'].xs(i, level='Sensitivity run'),
                 label=str('Hydrogen producers: ' + str(i)), linestyle='-', color=blue, alpha=tmp_alpha)

        # Electrolyzer producers
        #ax1.plot(x, df_plot['Electrolyzer Producers - Mean'].xs(i, level='Sensitivity run'), linestyle='-', color=green,
        #         alpha=tmp_alpha)
        ax1.plot(x, df_plot['Electrolyzer Producers - Median'].xs(i, level='Sensitivity run'),
                 label=str('Electrolyzer producers: ' + str(i)), linestyle='-', color=purple, alpha=tmp_alpha)

    # Legend
    line1, = ax1.plot(x, np.ones(80) * -1, color=green, label='Power market')
    line2, = ax1.plot(x, np.ones(80) * -1, color=blue, label='Hydrogen market')
    line3, = ax1.plot(x, np.ones(80) * -1, color=purple, label='Electrolyzer market')
    legend1 = ax1.legend(handles=[line1, line2, line3], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -1, color=green, alpha=tmp_alpha, label=tmp_label)
        tmp_line2, = ax1.plot(x, np.ones(80) * -1, color=blue, alpha=tmp_alpha, label=tmp_label)
        tmp_line3, = ax1.plot(x, np.ones(80) * -1, color=purple, alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1, tmp_line2, tmp_line3))

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    ax1.set_xlabel('Year')
    ax1.set_ylabel('No. of Investments')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(0)

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
    # Data
    df_phi_pp = df_pm.set_index(['Year', 'Sensitivity', 'Run'])
    df_phi_hp = df_hm.set_index(['Year', 'Sensitivity', 'Run'])
    df_phi_ep = df_em.set_index(['Year', 'Sensitivity', 'Run'])

    # Plot data
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index,
                           columns=['Power Producers - Mean', 'Power Producers - Median', 'Hydrogen Producers - Mean',
                                    'Hydrogen Producers - Median', 'Electrolyzer Producers - Mean',
                                    'Electrolyzer Producers - Median'])

    for i in range(80):
        # Power producers
        if i in df_phi_pp.index.levels[0]:
            tmp_df = (df_phi_pp.loc[i]['No. of Investments PM'] /
                      df_phi_pp.loc[i]['No. of Powerproducers'].replace(0, np.nan))
            for j in tmp_df.groupby(level=0).mean().index:
                df_plot['Power Producers - Mean'][i][j] = tmp_df.groupby(level=0).mean().loc[j]
                df_plot['Power Producers - Median'][i][j] = tmp_df.groupby(level=0).median().loc[j]
        # Hydrogen producers
        if i in df_phi_hp.index.levels[0]:
            tmp_df = (df_phi_hp.loc[i]['No. of Investments HM'] /
                      df_phi_hp.loc[i]['No. of Hydrogenproducers'].replace(0, np.nan))
            for j in tmp_df.groupby(level=0).mean().index:
                df_plot['Hydrogen Producers - Mean'][i][j] = tmp_df.groupby(level=0).mean().loc[j]
                df_plot['Hydrogen Producers - Median'][i][j] = tmp_df.groupby(level=0).median().loc[j]
        # Electrolyzer producers
        if i in df_phi_ep.index.levels[0]:
            tmp_df = (df_phi_ep.loc[i]['No. of Investments EM'] /
                      df_phi_ep.loc[i]['No. of Electrolyzerproducers'].replace(0, np.nan))
            for j in tmp_df.groupby(level=0).mean().index:
                df_plot['Electrolyzer Producers - Mean'][i][j] = tmp_df.groupby(level=0).mean().loc[j]
                df_plot['Electrolyzer Producers - Median'][i][j] = tmp_df.groupby(level=0).median().loc[j]

    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    for i in range(1, sensitivity_settings['No. of Runs']+1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Power producers
        #ax1.plot(x, df_plot['Power Producers - Mean'].xs(i, level='Sensitivity run'), linestyle='-', color=black,
        #         alpha=tmp_alpha)
        ax1.plot(x, df_plot['Power Producers - Median'].xs(i, level='Sensitivity run'), linestyle='-', color=green,
                 alpha=tmp_alpha)

        # Hydrogen producers
        #ax1.plot(x, df_plot['Hydrogen Producers - Mean'].xs(i, level='Sensitivity run'), linestyle='-', color=blue,
        #         alpha=tmp_alpha)
        ax1.plot(x, df_plot['Hydrogen Producers - Median'].xs(i, level='Sensitivity run'), linestyle='-', color=blue,
                 alpha=tmp_alpha)

        # Electrolyzer producers
        #ax1.plot(x, df_plot['Electrolyzer Producers - Mean'].xs(i, level='Sensitivity run'), linestyle='-', color=green,
        #         alpha=tmp_alpha)
        ax1.plot(x, df_plot['Electrolyzer Producers - Median'].xs(i, level='Sensitivity run'), linestyle='--',
                 color=purple, alpha=tmp_alpha)

    # Legend
    line1, = ax1.plot(x, np.ones(80) * -1, color=green, label='Power market')
    line2, = ax1.plot(x, np.ones(80) * -1, color=blue, label='Hydrogen market')
    line3, = ax1.plot(x, np.ones(80) * -1, color=purple, label='Electrolyzer market')
    legend1 = ax1.legend(handles=[line1, line2, line3], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -1, color=green, alpha=tmp_alpha, label=tmp_label)
        tmp_line2, = ax1.plot(x, np.ones(80) * -1, color=blue, alpha=tmp_alpha, label=tmp_label)
        tmp_line3, = ax1.plot(x, np.ones(80) * -1, color=purple, alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1, tmp_line2, tmp_line3))

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    ax1.set_xlabel('Year')
    ax1.set_ylabel('No. of Investments / No. of Agents')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(0)

    plt.savefig(os.getcwd() + '\\plot_ratio_investment_agents.' + plot_type, bbox_inches='tight')


def plot_installed_cap_res(df_pm):
    '''
    Function that will create a plot of the installed capacities of renewables.
    :param:
        pd.DataFrame df_pm: Data from the power market
    :return:
    '''
    # Data
    df_phi_pp = df_pm.set_index(['Year', 'Sensitivity', 'Run'])

    # Plot data
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index,
                           columns=['Renewables - Mean', 'Renewables - Median'])

    for i in range(80):
        # Renewables
        if i in df_phi_pp.index.levels[0]:
            tmp_df = df_phi_pp.loc[i]['Installed capacity Renewables']
            for j in tmp_df.groupby(level=0).mean().index:
                df_plot['Renewables - Mean'][i][j] = tmp_df.groupby(level=0).mean().loc[j]
                df_plot['Renewables - Median'][i][j] = tmp_df.groupby(level=0).median().loc[j]


    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    for i in range(1, sensitivity_settings['No. of Runs']+1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Renewables
        #ax1.plot(x, df_plot['Renewables - Mean'].xs(i, level='Sensitivity run')/1e3, linestyle='-', color=black,
        #         alpha=tmp_alpha)
        ax1.plot(x, df_plot['Renewables - Median'].xs(i, level='Sensitivity run')/1e3, linestyle='-', color=green,
                 alpha=tmp_alpha)


    # Legend
    line1, = ax1.plot(x, np.ones(80) * -1, color=green, label='Renewables')
    legend1 = ax1.legend(handles=[line1], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -1, color=green, alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append(tmp_line1)

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Installed capacity [GW]')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(0)

    plt.savefig(os.getcwd() + '\\plot_installed_cap_res.' + plot_type, bbox_inches='tight')


def plot_installed_cap_elc(df_hm):
    '''
    Function that will create a plot of the installed capacities of electrolyzers.
    :param:
        pd.DataFrame df_hm: Data from the hydrogen market
    :return:
    '''
    # Data
    df_phi = df_hm.set_index(['Year', 'Sensitivity', 'Run'])

    # Plot data
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index, columns=['Electrolyzers - Mean', 'Electrolyzers - Median'])

    for i in range(80):
        # Renewables
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Installed capacity Electrolyzers']
            for j in tmp_df.groupby(level=0).mean().index:
                df_plot['Electrolyzers - Mean'][i][j] = tmp_df.groupby(level=0).mean().loc[j]
                df_plot['Electrolyzers - Median'][i][j] = tmp_df.groupby(level=0).median().loc[j]


    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    for i in range(1, sensitivity_settings['No. of Runs']+1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Renewables
        #ax1.plot(x, df_plot['Electrolyzers - Mean'].xs(i, level='Sensitivity run')/1e3, linestyle='-', color=blue,
        #         alpha=tmp_alpha)
        ax1.plot(x, df_plot['Electrolyzers - Median'].xs(i, level='Sensitivity run')/1e3, linestyle='-', color=blue,
                 alpha=tmp_alpha)


    # Legend
    line1, = ax1.plot(x, np.ones(80) * -1, color=blue, label='Electrolyzers')
    legend1 = ax1.legend(handles=[line1], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -1, color=blue, alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append(tmp_line1)

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Installed capacity [GW]')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(0)

    plt.savefig(os.getcwd() + '\\plot_installed_cap_elc.' + plot_type, bbox_inches='tight')


def plot_installed_cap_man(df_em):
    '''
    Function that will create a plot of the installed manufacturing capacities for electrolyzers.
    :param:
        pd.DataFrame df_hm: Data from the electrolyzer market
    :return:
    '''
    # Data
    df_phi = df_em.set_index(['Year', 'Sensitivity', 'Run'])

    # Plot data
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index, columns=['Manufacturings - Mean', 'Manufacturings - Median'])

    for i in range(80):
        # Renewables
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Installed capacity Manufacturings']
            for j in tmp_df.groupby(level=0).mean().index:
                df_plot['Manufacturings - Mean'][i][j] = tmp_df.groupby(level=0).mean().loc[j]
                df_plot['Manufacturings - Median'][i][j] = tmp_df.groupby(level=0).median().loc[j]


    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    for i in range(1, sensitivity_settings['No. of Runs']+1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Renewables
        #ax1.plot(x, df_plot['Manufacturings - Mean'].xs(i, level='Sensitivity run')/1e3, linestyle='-', color=green,
        #         alpha=tmp_alpha)
        ax1.plot(x, df_plot['Manufacturings - Median'].xs(i, level='Sensitivity run')/1e3, linestyle='-', color=purple,
                 alpha=tmp_alpha)


    # Legend
    line1, = ax1.plot(x, np.ones(80) * -1, color=purple, label='Factories for Electrolyzers')
    legend1 = ax1.legend(handles=[line1], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -1, color=purple, alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append(tmp_line1)

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Installed capacity [GW/Year]')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(0)

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
    # Data
    df_phi_pp = df_pm.set_index(['Year', 'Sensitivity', 'Run'])
    df_phi_hp = df_hm.set_index(['Year', 'Sensitivity', 'Run'])
    df_phi_ep = df_em.set_index(['Year', 'Sensitivity', 'Run'])

    # Plot data
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index,
                           columns=['Renewables - Mean', 'Renewables - Median', 'Electrolyzers - Mean',
                                    'Electrolyzers - Median', 'Manufacturings - Mean',
                                    'Manufacturings - Median'])

    for i in range(80):
        # Renewables
        if i in df_phi_pp.index.levels[0]:
            tmp_df = df_phi_pp.loc[i]['Installed capacity Renewables']
            for j in tmp_df.groupby(level=0).mean().index:
                df_plot['Renewables - Mean'][i][j] = tmp_df.groupby(level=0).mean().loc[j]
                df_plot['Renewables - Median'][i][j] = tmp_df.groupby(level=0).median().loc[j]
        # Electrolyzers
        if i in df_phi_hp.index.levels[0]:
            tmp_df = df_phi_hp.loc[i]['Installed capacity Electrolyzers']
            for j in tmp_df.groupby(level=0).mean().index:
                df_plot['Electrolyzers - Mean'][i][j] = tmp_df.groupby(level=0).mean().loc[j]
                df_plot['Electrolyzers - Median'][i][j] = tmp_df.groupby(level=0).median().loc[j]
        # Manufacturings
        if i in df_phi_ep.index.levels[0]:
            tmp_df = df_phi_ep.loc[i]['Installed capacity Manufacturings']
            for j in tmp_df.groupby(level=0).mean().index:
                df_plot['Manufacturings - Mean'][i][j] = tmp_df.groupby(level=0).mean().loc[j]
                df_plot['Manufacturings - Median'][i][j] = tmp_df.groupby(level=0).median().loc[j]

    # Plot
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=plot_settings['figsize'],
                                        gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'], sharex=True)

    for i in range(1, sensitivity_settings['No. of Runs']+1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Power producers
        #ax1.plot(x, df_plot['Renewables - Mean'].xs(i, level='Sensitivity run')/1e3, linestyle='-', color=black,
        #         alpha=tmp_alpha)
        ax1.plot(x, df_plot['Renewables - Median'].xs(i, level='Sensitivity run')/1e3, linestyle='-', color=green,
                 alpha=tmp_alpha)

        # Hydrogen producers
        #ax2.plot(x, df_plot['Electrolyzers - Mean'].xs(i, level='Sensitivity run')/1e3, linestyle='-', color=blue,
        #         alpha=tmp_alpha)
        ax2.plot(x, df_plot['Electrolyzers - Median'].xs(i, level='Sensitivity run')/1e3, linestyle='-', color=blue,
                 alpha=tmp_alpha)

        # Electrolyzer producers
        #ax3.plot(x, df_plot['Manufacturings - Mean'].xs(i, level='Sensitivity run')/1e3, linestyle='-', color=green,
        #         alpha=tmp_alpha)
        ax3.plot(x, df_plot['Manufacturings - Median'].xs(i, level='Sensitivity run')/1e3, linestyle='-',
                 color=purple, alpha=tmp_alpha)

    # Governmental targets
    gov1, = ax1.plot(x, np.ones(80) * 375, label='Governmental target', color=orange, linestyle='-.')
    gov2 = ax1.scatter(2030, 375, label='Governmental target', facecolor='None', edgecolor=orange)
    gov3, = ax2.plot(x, np.ones(80) * 10, color=orange, linestyle='-.', label='Governmental target')
    gov4 = ax2.scatter(2030, 10, label='Governmental target', facecolor='None', edgecolor=orange)

    # Today
    #today1 = ax1.scatter(year0, 168, label='Today', color=black)
    #today2 = ax2.scatter(year0, 0.05, label='Today', color=blue)
    #today3 = ax3.scatter(year0, 0.05, label='Today', color=green)

    # Legend
    line1, = ax1.plot(x, np.ones(80) * -1, color=green, label='Renewables')
    line2, = ax2.plot(x, np.ones(80) * -1, color=blue, label='Electrolyzers')
    line3, = ax3.plot(x, np.ones(80) * -1, color=purple, label='Factories for Electrolyzers')
    #legend1 = ax1.legend(handles=[line1, gov1, gov2], loc='upper left')
    #ax1.add_artist(legend1)
    #legend2 = ax2.legend(handles=[line2, gov3, gov4], loc='upper left')
    #ax2.add_artist(legend2)
    #legend3 = ax3.legend(handles=[line1, gov1, gov2, line2, gov3, gov4, line3], loc='lower left',
    #                     bbox_to_anchor=(-0.05, -0.25))
    #ax3.add_artist(legend3)

    # Legend 4
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -1, color=green, alpha=tmp_alpha, label=tmp_label)
        tmp_line2, = ax1.plot(x, np.ones(80) * -1, color=blue, alpha=tmp_alpha, label=tmp_label)
        tmp_line3, = ax1.plot(x, np.ones(80) * -1, color=purple, alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1, tmp_line2, tmp_line3))
    ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
               handler_map={tuple: HandlerTuple(ndivide=None)})

    ax1.set_ylabel('[GW]')
    ax2.set_ylabel('[GW]')
    ax3.set_ylabel('[GW/Year]')
    ax1.set_ylim(0)
    ax2.set_ylim(0)
    ax3.set_ylim(0)
    ax3.set_xlim(plot_settings['xlim'])
    ax3.set_xlabel('Year')

    plt.savefig(os.getcwd() + '\\plot_installed_cap_all.' + plot_type, bbox_inches='tight')


def plot_electricity_production(df_pm):
    '''
    Function that will create a plot of the electricity production and its parts.
    :param:
        pd.DataFrame df_pm: Daily data from the power market
    :return:
    '''
    # Data
    df_phi = df_pm.set_index(['Year', 'Day', 'Sensitivity', 'Run'])

    # Plot
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index,
                           columns=['Production gas turbines', 'General electricity demand',
                                    'Green hydrogen production', 'Curtailment renewables'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            # Gas turbine production
            tmp_gt = df_phi.loc[i]['Electricity demand others'] - df_phi.loc[i][('Maximum production renewables')]
            tmp_gt = tmp_gt.clip(lower=0).groupby(['Day', 'Sensitivity']).median().groupby(level=1).sum()

            # Electricity demand
            tmp_demand = df_phi.loc[i]['Electricity demand others'].groupby(['Day', 'Sensitivity']).median()
            tmp_demand = tmp_demand.groupby(level=1).sum()

            # Green hydrogen production
            tmp_h2 = df_phi.loc[i]['Actual production renewables'].groupby(['Day', 'Sensitivity']).median()
            tmp_h2 = tmp_h2.groupby(level=1).sum()
            tmp_h2 = tmp_gt + tmp_h2

            # Curtailment
            tmp_curtail = df_phi.loc[i]['Maximum production renewables'].groupby(['Day', 'Sensitivity']).median()
            tmp_curtail = tmp_curtail.groupby(level=1).sum()
            tmp_curtail = tmp_gt + tmp_curtail

            # Normalize by the electricity demand
            tmp_gt = tmp_gt/tmp_demand
            tmp_h2 = tmp_h2/tmp_demand
            tmp_curtail = tmp_curtail/tmp_demand
            tmp_demand = tmp_demand/tmp_demand

            df_plot['Production gas turbines'][i] = tmp_gt
            df_plot['General electricity demand'][i] = tmp_demand
            df_plot['Green hydrogen production'][i] = tmp_h2
            df_plot['Curtailment renewables'][i] = tmp_curtail

    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'],
                            gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'])

    # Lines
    for i in range(1, sensitivity_settings['No. of Runs'] + 1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Gas turbine
        ax1.plot(x, df_plot['Production gas turbines'].xs(i, level='Sensitivity run'), linestyle='-', color=green,
                 alpha=tmp_alpha)
        # General electricity demand
        ax1.plot(x, df_plot['General electricity demand'].xs(i, level='Sensitivity run'), linestyle='-.', color=black,
                 alpha=tmp_alpha)
        # Green hydrogen production
        ax1.plot(x, df_plot['Green hydrogen production'].xs(i, level='Sensitivity run'), linestyle='-', color=darkblue,
                 alpha=tmp_alpha)
        # Curtailment renewables
        ax1.plot(x, df_plot['Curtailment renewables'].xs(i, level='Sensitivity run'), linestyle='-', color=purple,
                 alpha=tmp_alpha)

    # Areas
    area1 = ax1.fill_between(x, 0, df_plot['Production gas turbines'].groupby(level=0).max(),
                              label='Production gas turbines', color=grey, alpha=0.25, edgecolor='none')
    area2 = ax1.fill_between(x, df_plot['Production gas turbines'].groupby(level=0).max(),
                              df_plot['General electricity demand'].groupby(level=0).max(),
                              label='Production renewables',color=green, alpha=0.25, edgecolor='none')
    area3 = ax1.fill_between(x, df_plot['General electricity demand'].groupby(level=0).max(),
                              df_plot['Green hydrogen production'].groupby(level=0).max(),
                              label='Green hydrogen production', color=blue, alpha=0.25, edgecolor='none')
    area4 = ax1.fill_between(x, df_plot['Green hydrogen production'].groupby(level=0).max(),
                              df_plot['Curtailment renewables'].groupby(level=0).max(),
                              label='Curtailment renewables', color=purple, alpha=0.25, edgecolor='none')

    # Legend 1
    line1, = ax1.plot(x, np.ones(80)*-1, label='General electricity demand', linestyle='-.', color=black)
    legend1 = ax1.legend(handles=[area1, area2, area3, area4, line1], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -1, color=green, alpha=tmp_alpha, label=tmp_label)
        tmp_line2, = ax1.plot(x, np.ones(80) * -1, color=darkblue, alpha=tmp_alpha, label=tmp_label)
        tmp_line3, = ax1.plot(x, np.ones(80) * -1, color=purple, alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1, tmp_line2, tmp_line3))

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    # Plot settings
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Electricity mix [-]')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(0)

    plt.savefig(os.getcwd() + '\\plot_electricity_production.' + plot_type, bbox_inches='tight')


def plot_hydrogen_production(df_hm_yearly, df_hm_daily):
    '''
    Function that will create a plot of the actual and theoratical maximum hydrogen production.
    :param:
        pd.DataFrame df_hm_yearly: Yearly data from the hydrogen market
        pd.DataFrame df_hm_daily: Daily data from the hydrogen market
    :return:
    '''
    # Effiency electrolyzer
    eta = 0.7

    # Data
    df_phi_day = df_hm_daily.set_index(['Year', 'Day', 'Sensitivity', 'Run'])
    df_phi_year = df_hm_yearly.set_index(['Year', 'Sensitivity', 'Run'])

    # Plot
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index, columns=['Hydrogen production', 'Maximum hydrogen production'])

    for i in range(80):
        # Hydrogen production
        if i in df_phi_day.index.levels[0]:
            tmp_h2 = df_phi_day.loc[i]['Actual production electrolyzers'].groupby(['Day', 'Sensitivity']).median()
            df_plot['Hydrogen production'][i] = tmp_h2.groupby(level=1).sum()

        # Maximum hydrogen production
        if i in df_phi_year.index.levels[0]:
            tmp_max = df_phi_year.loc[i]['Installed capacity Electrolyzers'].groupby(['Sensitivity']).median()
            df_plot['Maximum hydrogen production'][i] = tmp_max * 24 * 365 * eta

    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'],
                            gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'])

    # Lines
    for i in range(1, sensitivity_settings['No. of Runs'] + 1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Hydrogen production
        ax1.plot(x, df_plot['Hydrogen production'].xs(i, level='Sensitivity run')/1e6, label='Hydrogen production',
                 linestyle='-', color=blue, alpha=tmp_alpha)
        # Maximum hydrogen production
        ax1.plot(x, df_plot['Maximum hydrogen production'].xs(i, level='Sensitivity run')/1e6,
                 label='Maximum hydrogen production', linestyle='--', color=darkblue, alpha=tmp_alpha)

    # Areas
    area1 = ax1.fill_between(x, 0, df_plot['Hydrogen production'].groupby(level=0).max()/1e6, color=blue, alpha=0.25,
                             edgecolor='none')
    area2 = ax1.fill_between(x, df_plot['Hydrogen production'].groupby(level=0).max()/1e6,
                             df_plot['Maximum hydrogen production'].groupby(level=0).max()/1e6, color=darkblue,
                             alpha=0.25, edgecolor='none')

    # Legend 1
    line1, = ax1.plot(x, np.ones(80)*-1, label='Hydrogen production', linestyle='-', color=blue)
    line2, = ax1.plot(x, np.ones(80)*-1, label='Maximum hydrogen production', linestyle='--', color=darkblue)
    legend1 = ax1.legend(handles=[line1, line2], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -1, color=blue, linestyle='-', alpha=tmp_alpha, label=tmp_label)
        tmp_line2, = ax1.plot(x, np.ones(80) * -1, color=darkblue, linestyle='--', alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1, tmp_line2))

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    # Plot settings
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Hydrogen production [TWh]')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(0)

    plt.savefig(os.getcwd() + '\\plot_hydrogen_production.' + plot_type, bbox_inches='tight')


def plot_utilization_elc(df_hm):
    '''
    Function that will create a plot of the utilization per year of the electrolyzers.
    :param:
        pd.DataFrame df_hm:
    :return:
    '''
    # Utilization
    df_phi = df_hm.set_index(['Year', 'Day', 'Sensitivity', 'Run'])

    # Plot
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index, columns=['Utilization'])

    # Data
    for i in range(80):
        # Utilization
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Utilization rate'].groupby(['Sensitivity']).median() * 100
            df_plot['Utilization'][i] = tmp_df

    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'],
                            gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'])

    ax2 = ax1.twinx()
    # Lines
    for i in range(1, sensitivity_settings['No. of Runs'] + 1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Hydrogen production
        ax1.plot(x, df_plot['Utilization'].xs(i, level='Sensitivity run'), linestyle='-', color=blue, alpha=tmp_alpha)
        ax2.plot(x, df_plot['Utilization'].xs(i, level='Sensitivity run') / 100 * 8760, linestyle='-', color=blue,
                 alpha=tmp_alpha)

    # Legend 1
    line1, = ax1.plot(x, np.ones(80) * -1, label='Electrolyzers', linestyle='-', color=blue)
    legend1 = ax1.legend(handles=[line1], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -1, color=blue, linestyle='-', alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1))

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1.1, 1),
                             handler_map={tuple: HandlerTuple(ndivide=None)})

    # Plot settings
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Utilization rate [%]')
    ax2.set_ylabel('Full load hours [h]')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(0)
    ax2.set_ylim(0)

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
    # TODO
    return(1)


def plot_duration_curves_elc(df_hm, no_of_lines=10):
    '''
    Function that will create a plot of the duration curves of the electrolyzers.
    :param:
        pd.DataFrame df_hm: Daily data from the hydrogen market
        int no_of_lines: The number of years to plot (default 10)
    :return:
    '''
    # TODO
    return(1)


def plot_load_type_elc(df_pm, df_hm):
    '''
    Function that will create a plot of the load type of the electrolyzer.
    :param:
        pd.DataFrame df_pm: Yearly data from the power market
        pd.DataFrame df_hm: Yearly data from the hydrogen market
    :return:
    '''
    # TODO
    return(1)


def plot_p_elc_vs_lcoe(df_pm):
    '''
    Function that will create a plot of the price for electricity and the lcoe.
    :param:
        pd.DataFrame df_pm: Yearly data from the power market
    :return:
    '''
    # Prepare data
    df_phi = df_pm.set_index(['Year', 'Sensitivity', 'Run'])
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index, columns=['Price', 'LCOE'])

    # Data
    for i in range(80):
        if i in df_phi.index.levels[0]:
            # Price
            tmp_df = df_phi.loc[i]['Weighted Price Electricity'].groupby(['Sensitivity']).median()
            df_plot['Price'][i] = tmp_df
            # LCOE
            tmp_df = df_phi.loc[i]['LCOE'].groupby(['Sensitivity']).median()
            df_plot['LCOE'][i] = tmp_df

    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'],
                            gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'])

    # Lines
    for i in range(1, sensitivity_settings['No. of Runs'] + 1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Price
        ax1.plot(x, df_plot['Price'].xs(i, level='Sensitivity run'), linestyle='-', color=green, alpha=tmp_alpha)
        # LCOE
        ax1.plot(x, df_plot['LCOE'].xs(i, level='Sensitivity run'), linestyle='--', color=green, alpha=tmp_alpha)

    # Legend 1
    line1, = ax1.plot(x, np.ones(80) * -1, label='Weighted price electricity', linestyle='-', color=green)
    line2, = ax1.plot(x, np.ones(80) * -1, label='Levelized costs of renewable electricity', linestyle='--',
                      color=green)
    legend1 = ax1.legend(handles=[line1, line2], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -1, color=green, linestyle='-', alpha=tmp_alpha, label=tmp_label)
        tmp_line2, = ax1.plot(x, np.ones(80) * -1, color=green, linestyle='--', alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1, tmp_line2))

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    # Plot settings
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Costs / Price [€/MWh]')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(0)

    # Save plot
    plt.savefig(os.getcwd() + '\\plot_p_elc_vs_lcoe.' + plot_type, bbox_inches='tight')


def plot_p_h2_vs_lcoh(df_hm):
    '''
    Function that will create a plot of the price of hydrogen and the lcoh.
    :param:
        pd.DataFrame df_hm: Yearly data from the hydrogen market
    :return:
    '''
    # Prepare data
    df_phi = df_hm.set_index(['Year', 'Sensitivity', 'Run']).replace(1e10, np.nan)
    tmp_index = pd.MultiIndex.from_product([range(80), range(1, sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index, columns=['Price', 'LCOH'])

    # Data
    for i in range(80):
        if i in df_phi.index.levels[0]:
            # Price
            tmp_df = df_phi.loc[i]['Price Hydrogen'].groupby(['Sensitivity']).median()
            df_plot['Price'][i] = tmp_df
            # LCOE
            tmp_df = df_phi.loc[i]['LCOH'].groupby(['Sensitivity']).median()
            df_plot['LCOH'][i] = tmp_df

    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'],
                            gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'])
    ax2 = ax1.twinx()

    # Lines
    for i in range(1, sensitivity_settings['No. of Runs'] + 1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Price
        ax1.plot(x, df_plot['Price'].xs(i, level='Sensitivity run'), linestyle='-', color=blue, alpha=tmp_alpha)
        ax2.plot(x, df_plot['Price'].xs(i, level='Sensitivity run') * 0.039, linestyle='-', color=blue, alpha=tmp_alpha)
        # LCOE
        ax1.plot(x, df_plot['LCOH'].xs(i, level='Sensitivity run'), linestyle='--', color=blue, alpha=tmp_alpha)
        ax2.plot(x, df_plot['LCOH'].xs(i, level='Sensitivity run') * 0.039, linestyle='--', color=blue, alpha=tmp_alpha)

    # Legend 1
    line1, = ax1.plot(x, np.ones(80) * -1, label='Price hydrogen', linestyle='-', color=blue)
    line2, = ax1.plot(x, np.ones(80) * -1, label='Levelized costs of hydrogen', linestyle='--', color=blue)
    legend1 = ax1.legend(handles=[line1, line2], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -1, color=blue, linestyle='-', alpha=tmp_alpha, label=tmp_label)
        tmp_line2, = ax1.plot(x, np.ones(80) * -1, color=blue, linestyle='--', alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1, tmp_line2))

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1.1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    # Plot settings
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Costs / Price [€/MWh]')
    ax2.set_ylabel('Costs / Price [€/kg]')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(0)
    ax2.set_ylim(0)

    # Save plot
    plt.savefig(os.getcwd() + '\\plot_p_h2_vs_lcoh.' + plot_type, bbox_inches='tight')


def plot_p_elc_ave_vs_lcoe_ave(df_ep, df_sale):
    '''
    Function that will create a plot of the price for electorlyzer and the lcoe
    :param:
        pd.DataFrame df_ep: Yearly data from the electrolyzer producers
        pd.DataFrame df_sale: Yearly data from the electrolyzers' sale
    :return:
    '''
    # Prepare data
    df_phi_ep = df_ep.set_index(['Year', 'Sensitivity', 'Run', 'ID'])
    df_phi_sale = df_sale.set_index(['Year', 'Sensitivity', 'Run', 'EP ID'])
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index, columns=['Price', 'LCOE'])

    # Data
    for i in range(80):
        if i in df_phi_sale.index.levels[0]:
            # Price
            tmp_df = df_phi_sale.loc[i]['Price'].groupby(['Sensitivity']).median()
            for j in df_plot.index.levels[1]:
                if j not in tmp_df.index:
                    tmp_df[j] = np.nan
            df_plot['Price'][i] = tmp_df
        if i in df_phi_ep.index.levels[0]:
            # LCOE
            tmp_df = df_phi_ep.loc[i]['LCOE'].replace(1e10, np.nan).groupby(['Sensitivity']).median()
            for j in df_plot.index.levels[1]:
                if j not in tmp_df.index:
                    tmp_df[j] = np.nan
            df_plot['LCOE'][i] = tmp_df

    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'],
                            gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'])
    ax2 = ax1.twinx()

    # Lines
    for i in range(1, sensitivity_settings['No. of Runs'] + 1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Price
        ax1.plot(x, df_plot['Price'].xs(i, level='Sensitivity run') / 1e6, linestyle='-', color=purple, alpha=tmp_alpha)
        ax2.plot(x, df_plot['Price'].xs(i, level='Sensitivity run') / 1e3, linestyle='-', color=purple, alpha=tmp_alpha)
        # LCOE
        ax1.plot(x, df_plot['LCOE'].xs(i, level='Sensitivity run') / 1e6, linestyle='--', color=purple, alpha=tmp_alpha)
        ax2.plot(x, df_plot['LCOE'].xs(i, level='Sensitivity run') / 1e3, linestyle='--', color=purple, alpha=tmp_alpha)

    # Legend 1
    line1, = ax1.plot(x, np.ones(80) * -1, label='Price electrolyzers', linestyle='-', color=purple)
    line2, = ax1.plot(x, np.ones(80) * -1, label='Levelized costs of electrolyzers', linestyle='--', color=purple)
    legend1 = ax1.legend(handles=[line1, line2], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -1, color=purple, linestyle='-', alpha=tmp_alpha, label=tmp_label)
        tmp_line2, = ax1.plot(x, np.ones(80) * -1, color=purple, linestyle='--', alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1, tmp_line2))

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1.1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    # Plot settings
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Costs / Price [Mio. €/MW]')
    ax2.set_ylabel('Costs / Price [€/kW]')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(0)
    ax2.set_ylim(0)

    # Save plot
    plt.savefig(os.getcwd() + '\\plot_p_elc_ave_vs_lcoe_ave.' + plot_type, bbox_inches='tight')


def plot_p_elc_vs_c_elc(df_sale):
    '''
    Function that will create a plot of the average ratio of price ancosts for electrolyzers
    :param:
        pd.DataFrame df_sale: Yearly data from the electrolyzers' sales
    :return:
    '''
    # Prepare data
    df_phi = df_sale.set_index(['Year', 'Sensitivity', 'Run', 'EP ID'])
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index, columns=['Electrolyzers'])

    # Data
    for i in range(80):
        if i in df_phi.index.levels[0]:
            # Ratio Price/Costs
            tmp_df = df_phi.loc[i]['Price']/df_phi.loc[i]['Production costs']
            tmp_df = tmp_df.groupby(['Sensitivity']).median()
            for j in df_plot.index.levels[1]:
                if j not in tmp_df.index:
                    tmp_df[j] = np.nan
            df_plot['Electrolyzers'][i] = tmp_df

    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'],
                            gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'])

    # Lines
    for i in range(1, sensitivity_settings['No. of Runs'] + 1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Ratio Price/Costs
        ax1.plot(x, df_plot['Electrolyzers'].xs(i, level='Sensitivity run'), linestyle='-', color=purple,
                alpha=tmp_alpha)

    # Legend 1
    line1, = ax1.plot(x, np.ones(80) * -1, label='Electrolyzers', linestyle='-', color=purple)
    line2, = ax1.plot(x, np.ones(80) * 1, label='0% Profits', linestyle='--', color=orange)
    line3, = ax1.plot(x, np.ones(80) * 2, label='100% Profits', linestyle='-.', color=orange)
    legend1 = ax1.legend(handles=[line1, line2, line3], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -1, color=purple, linestyle='-', alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1))

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    # Plot settings
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Ratio Price/Costs [-]')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(0)

    # Save plot
    plt.savefig(os.getcwd() + '\\plot_p_elc_vs_c_elc.' + plot_type, bbox_inches='tight')


def plot_investment_threshold_pp(df_pp):
    '''
    Function that will create a plot of the average investment threshold of the Power Producers.
    :param:
        pd.DataFrame df_pp: Yearly data of the Power Producers.
    :return:
    '''
    # Prepare data
    df_phi = df_pp.set_index(['Year', 'Sensitivity', 'Run', 'ID'])
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index, columns=['Power producers'])

    # Data
    for i in range(80):
        if i in df_phi.index.levels[0]:
            # Power producers
            tmp_df = df_phi.loc[i]['Investment threshold'].groupby(['Sensitivity', 'Run']).median()
            tmp_df = tmp_df.groupby(['Sensitivity']).median()
            for j in df_plot.index.levels[1]:
                if j not in tmp_df.index:
                    tmp_df[j] = np.nan
            df_plot['Power producers'][i] = tmp_df

    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'],
                            gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'])

    # Lines
    for i in range(1, sensitivity_settings['No. of Runs'] + 1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Ratio Price/Costs
        ax1.plot(x, df_plot['Power producers'].xs(i, level='Sensitivity run'), linestyle='-', color=green,
                alpha=tmp_alpha)

    # Legend 1
    line1, = ax1.plot(x, np.ones(80) * -1, label='Power producers', linestyle='-', color=green)
    legend1 = ax1.legend(handles=[line1], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -100, color=green, linestyle='-', alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1))

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    # Plot settings
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Investment threshold [-]')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(-1)

    # Save plot
    plt.savefig(os.getcwd() + '\\plot_investment_threshold_pp.' + plot_type, bbox_inches='tight')


def plot_investment_threshold_hp(df_hp):
    '''
    Function that will create a plot of the average investment threshold of the Hydrogen Producers.
    :param:
        pd.DataFrame df_pp: Yearly data of the Hydrogen Producers.
    :return:
    '''
    # Prepare data
    df_phi = df_hp.set_index(['Year', 'Sensitivity', 'Run', 'ID'])
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index, columns=['Hydrogen producers'])

    # Data
    for i in range(80):
        if i in df_phi.index.levels[0]:
            # Power producers
            tmp_df = df_phi.loc[i]['Investment threshold'].groupby(['Sensitivity', 'Run']).median()
            tmp_df = tmp_df.groupby(['Sensitivity']).median()
            for j in df_plot.index.levels[1]:
                if j not in tmp_df.index:
                    tmp_df[j] = np.nan
            df_plot['Hydrogen producers'][i] = tmp_df

    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'],
                            gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'])

    # Lines
    for i in range(1, sensitivity_settings['No. of Runs'] + 1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Ratio Price/Costs
        ax1.plot(x, df_plot['Hydrogen producers'].xs(i, level='Sensitivity run'), linestyle='-', color=blue,
                alpha=tmp_alpha)

    # Legend 1
    line1, = ax1.plot(x, np.ones(80) * -100, label='Hydrogen producers', linestyle='-', color=blue)
    legend1 = ax1.legend(handles=[line1], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -100, color=blue, linestyle='-', alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1))

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    # Plot settings
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Investment threshold [-]')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(-1)

    # Save plot
    plt.savefig(os.getcwd() + '\\plot_investment_threshold_hp.' + plot_type, bbox_inches='tight')


def plot_investment_threshold_ep(df_ep):
    '''
    Function that will create a plot of the average investment threshold of the Electrolyzer Producers.
    :param:
        pd.DataFrame df_ep: Yearly data of the Electrolyzer Producers.
    :return:
    '''
    # Prepare data
    df_phi = df_ep.set_index(['Year', 'Sensitivity', 'Run', 'ID'])
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index, columns=['Electrolyzer producers'])

    # Data
    for i in range(80):
        if i in df_phi.index.levels[0]:
            # Power producers
            tmp_df = df_phi.loc[i]['Investment threshold'].groupby(['Sensitivity', 'Run']).median()
            tmp_df = tmp_df.groupby(['Sensitivity']).median()
            for j in df_plot.index.levels[1]:
                if j not in tmp_df.index:
                    tmp_df[j] = np.nan
            df_plot['Electrolyzer producers'][i] = tmp_df

    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'],
                            gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'])

    # Lines
    for i in range(1, sensitivity_settings['No. of Runs'] + 1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Ratio Price/Costs
        ax1.plot(x, df_plot['Electrolyzer producers'].xs(i, level='Sensitivity run'), linestyle='-', color=purple,
                alpha=tmp_alpha)

    # Legend 1
    line1, = ax1.plot(x, np.ones(80) * -100, label='Electrolyzer producers', linestyle='-', color=purple)
    legend1 = ax1.legend(handles=[line1], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -100, color=purple, linestyle='-', alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1))

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    # Plot settings
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Investment threshold [-]')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(-1)

    # Save plot
    plt.savefig(os.getcwd() + '\\plot_investment_threshold_ep.' + plot_type, bbox_inches='tight')


def plot_weighted_investment_threshold_pp(df_pp):
    '''
    Function that will create a plot of the capacity weighted investment threshold of the power producers.
    :param:
        pd.DataFrame df_pp: Yearly data of the power producers
    :return:
    '''
    # Prepare data
    df_phi = df_pp.set_index(['Year', 'Sensitivity', 'Run', 'ID'])
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index, columns=['Power producers'])

    # Data
    for i in range(80):
        if i in df_phi.index.levels[0]:
            # Power producers
            tmp_df = df_phi.loc[i]['Investment threshold'] * df_phi.loc[i]['Installed capacity Renewables']
            tmp_df = (tmp_df.groupby(['Sensitivity', 'Run']).sum() /
                      df_phi.loc[i]['Installed capacity Renewables'].groupby(['Sensitivity', 'Run']).sum())
            tmp_df = tmp_df.groupby(['Sensitivity']).median()
            for j in df_plot.index.levels[1]:
                if j not in tmp_df.index:
                    tmp_df[j] = np.nan
            df_plot['Power producers'][i] = tmp_df

    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'],
                            gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'])

    # Lines
    for i in range(1, sensitivity_settings['No. of Runs'] + 1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Ratio Price/Costs
        ax1.plot(x, df_plot['Power producers'].xs(i, level='Sensitivity run'), linestyle='-', color=green,
                     alpha=tmp_alpha)

    # Legend 1
    line1, = ax1.plot(x, np.ones(80) * -100, label='Power producers', linestyle='-', color=green)
    legend1 = ax1.legend(handles=[line1], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -100, color=green, linestyle='-', alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1))

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    # Plot settings
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Investment threshold [-]')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(-1)

    # Save plot
    plt.savefig(os.getcwd() + '\\plot_weighted_investment_threshold_pp.' + plot_type, bbox_inches='tight')


def plot_weighted_investment_threshold_hp(df_hp):
    '''
    Function that will create a plot of the capacity weighted investment threshold of the hydrogen producers.
    :param:
        pd.DataFrame df_hp: Yearly data of the hydrogen producers
    :return:
    '''
    # Prepare data
    df_phi = df_hp.set_index(['Year', 'Sensitivity', 'Run', 'ID'])
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index, columns=['Hydrogen producers'])

    # Data
    for i in range(80):
        if i in df_phi.index.levels[0]:
            # Hydrogen producers
            tmp_df = df_phi.loc[i]['Investment threshold'] * df_phi.loc[i]['Installed capacity Electrolyzers']
            tmp_df = (tmp_df.groupby(['Sensitivity', 'Run']).sum() /
                      df_phi.loc[i]['Installed capacity Electrolyzers'].groupby(['Sensitivity', 'Run']).sum())
            tmp_df = tmp_df.groupby(['Sensitivity']).median()
            for j in df_plot.index.levels[1]:
                if j not in tmp_df.index:
                    tmp_df[j] = np.nan
            df_plot['Hydrogen producers'][i] = tmp_df

    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'],
                            gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'])

    # Lines
    for i in range(1, sensitivity_settings['No. of Runs'] + 1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Hydrogen producer
        ax1.plot(x, df_plot['Hydrogen producers'].xs(i, level='Sensitivity run'), linestyle='-', color=blue,
                     alpha=tmp_alpha)

    # Legend 1
    line1, = ax1.plot(x, np.ones(80) * -100, label='Hydrogen producers', linestyle='-', color=blue)
    legend1 = ax1.legend(handles=[line1], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -100, color=blue, linestyle='-', alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1))

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    # Plot settings
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Investment threshold [-]')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(-1)

    # Save plot
    plt.savefig(os.getcwd() + '\\plot_weighted_investment_threshold_hp.' + plot_type, bbox_inches='tight')


def plot_weighted_investment_threshold_ep(df_ep):
    '''
    Function that will create a plot of the capacity weighted investment threshold of the electrolyzers producers.
    :param:
        pd.DataFrame df_ep: Yearly data of the electrolyzers producers
    :return:
    '''
    # Prepare data
    df_phi = df_ep.set_index(['Year', 'Sensitivity', 'Run', 'ID'])
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index, columns=['Electrolyzer producers'])

    # Data
    for i in range(80):
        if i in df_phi.index.levels[0]:
            # Electrolyzer producers
            tmp_df = df_phi.loc[i]['Investment threshold'] * df_phi.loc[i]['Installed capacity Manufacturings']
            tmp_df = (tmp_df.groupby(['Sensitivity', 'Run']).sum() /
                      df_phi.loc[i]['Installed capacity Manufacturings'].groupby(['Sensitivity', 'Run']).sum())
            tmp_df = tmp_df.groupby(['Sensitivity']).median()
            for j in df_plot.index.levels[1]:
                if j not in tmp_df.index:
                    tmp_df[j] = np.nan
            df_plot['Electrolyzer producers'][i] = tmp_df

    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'],
                            gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'])

    # Lines
    for i in range(1, sensitivity_settings['No. of Runs'] + 1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Electrolyzer producers
        ax1.plot(x, df_plot['Electrolyzer producers'].xs(i, level='Sensitivity run'), linestyle='-', color=purple,
                     alpha=tmp_alpha)

    # Legend 1
    line1, = ax1.plot(x, np.ones(80) * -100, label='Electrolyzer producers', linestyle='-', color=purple)
    legend1 = ax1.legend(handles=[line1], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -100, color=purple, linestyle='-', alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1))

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    # Plot settings
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Investment threshold [-]')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(-1)

    # Save plot
    plt.savefig(os.getcwd() + '\\plot_weighted_investment_threshold_ep.' + plot_type, bbox_inches='tight')


def plot_age_res(df_res):
    '''
    Function that will create a plot of the average age of the renewables.
    :param:
        pd.DataFrame df_res: Yearly data of the renewables
    :return:
    '''
    # Prepare data
    df_phi = df_res.set_index(['Year', 'Sensitivity', 'Run', 'ID'])
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index, columns=['Renewables'])

    # Data
    for i in range(80):
        if i in df_phi.index.levels[0]:
            # Renewables
            tmp_df = df_phi.loc[i]['Age']
            tmp_df = tmp_df.groupby(['Sensitivity', 'Run']).mean()
            tmp_df = tmp_df.groupby(['Sensitivity']).mean()
            for j in df_plot.index.levels[1]:
                if j not in tmp_df.index:
                    tmp_df[j] = np.nan
            df_plot['Renewables'][i] = tmp_df

    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'],
                            gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'])

    # Lines
    for i in range(1, sensitivity_settings['No. of Runs'] + 1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Renewables
        ax1.plot(x, df_plot['Renewables'].xs(i, level='Sensitivity run'), linestyle='-', color=green,
                 alpha=tmp_alpha)

    # Legend 1
    line1, = ax1.plot(x, np.ones(80) * -100, label='Renewables', linestyle='-', color=green)
    legend1 = ax1.legend(handles=[line1], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -100, color=green, linestyle='-', alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1))

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    # Plot settings
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Age [years]')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(0)

    # Save plot
    plt.savefig(os.getcwd() + '\\plot_age_res.' + plot_type, bbox_inches='tight')


def plot_age_elc(df_elc):
    '''
    Function that will create a plot of the average age of the electrolyzers.
    :param:
        pd.DataFrame df_elc: Yearly data of the electrolyzers
    :return:
    '''
    # Prepare data
    df_phi = df_elc.set_index(['Year', 'Sensitivity', 'Run', 'ID'])
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index, columns=['Electrolyzers'])

    # Data
    for i in range(80):
        if i in df_phi.index.levels[0]:
            # Electrolyzers
            tmp_df = df_phi.loc[i]['Age']
            tmp_df = tmp_df.groupby(['Sensitivity', 'Run']).median()
            tmp_df = tmp_df.groupby(['Sensitivity']).median()
            for j in df_plot.index.levels[1]:
                if j not in tmp_df.index:
                    tmp_df[j] = np.nan
            df_plot['Electrolyzers'][i] = tmp_df

    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'],
                            gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'])

    # Lines
    for i in range(1, sensitivity_settings['No. of Runs'] + 1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Electrolyzers
        ax1.plot(x, df_plot['Electrolyzers'].xs(i, level='Sensitivity run'), linestyle='-', color=blue,
                 alpha=tmp_alpha)

    # Legend 1
    line1, = ax1.plot(x, np.ones(80) * -100, label='Electrolyzers', linestyle='-', color=blue)
    legend1 = ax1.legend(handles=[line1], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -100, color=blue, linestyle='-', alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1))

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    # Plot settings
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Age [years]')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(0)

    # Save plot
    plt.savefig(os.getcwd() + '\\plot_age_elc.' + plot_type, bbox_inches='tight')


def plot_age_man(df_man):
    '''
    Function that will create a plot of the average age of the factories for electrolyzers.
    :param:
        pd.DataFrame df_elc: Yearly data of the factories for electrolyzers
    :return:
    '''
    # Prepare data
    df_phi = df_man.set_index(['Year', 'Sensitivity', 'Run', 'ID'])
    tmp_index = pd.MultiIndex.from_product([range(80), range(1, sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index, columns=['Factories'])

    # Data
    for i in range(80):
        if i in df_phi.index.levels[0]:
            # Factories for electrolyzers
            tmp_df = df_phi.loc[i]['Age']
            tmp_df = tmp_df.groupby(['Sensitivity', 'Run']).median()
            tmp_df = tmp_df.groupby(['Sensitivity']).median()
            for j in df_plot.index.levels[1]:
                if j not in tmp_df.index:
                    tmp_df[j] = np.nan
            df_plot['Factories'][i] = tmp_df

    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'],
                            gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'])

    # Lines
    for i in range(1, sensitivity_settings['No. of Runs'] + 1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Factories for electrolyzers
        ax1.plot(x, df_plot['Factories'].xs(i, level='Sensitivity run'), linestyle='-', color=purple,
                 alpha=tmp_alpha)

    # Legend 1
    line1, = ax1.plot(x, np.ones(80) * -100, label='Factories for electrolyzers', linestyle='-', color=purple)
    legend1 = ax1.legend(handles=[line1], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -100, color=purple, linestyle='-', alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1))

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    # Plot settings
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Age [years]')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(0)

    # Save plot
    plt.savefig(os.getcwd() + '\\plot_age_man.' + plot_type, bbox_inches='tight')


def plot_weighted_age_res(df_res):
    '''
    Function that will create a plot of the capacity weighted average age of the renewables.
    :param:
        pd.DataFrame df_res: Yearly data of the renewables
    :return:
    '''
    # Prepare data
    df_phi = df_res.set_index(['Year', 'Sensitivity', 'Run', 'ID'])
    tmp_index = pd.MultiIndex.from_product([range(80), range(1, sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index, columns=['Renewables'])

    # Data
    for i in range(80):
        if i in df_phi.index.levels[0]:
            # Renewables
            tmp_df = df_phi.loc[i]['Age'] * df_phi.loc[i]['Capacity']
            tmp_df = (tmp_df.groupby(['Sensitivity', 'Run']).sum() /
                      df_phi.loc[i]['Capacity'].groupby(['Sensitivity', 'Run']).sum())
            tmp_df = tmp_df.groupby(['Sensitivity']).median()
            for j in df_plot.index.levels[1]:
                if j not in tmp_df.index:
                    tmp_df[j] = np.nan
            df_plot['Renewables'][i] = tmp_df


    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'],
                            gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'])

    # Lines
    for i in range(1, sensitivity_settings['No. of Runs'] + 1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Renewables
        ax1.plot(x, df_plot['Renewables'].xs(i, level='Sensitivity run'), linestyle='-', color=green,
                 alpha=tmp_alpha)

    # Legend 1
    line1, = ax1.plot(x, np.ones(80) * -100, label='Renewables', linestyle='-', color=green)
    legend1 = ax1.legend(handles=[line1], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -100, color=green, linestyle='-', alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1))

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    # Plot settings
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Age [years]')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(0)

    # Save plot
    plt.savefig(os.getcwd() + '\\plot_weighted_age_res.' + plot_type, bbox_inches='tight')


def plot_weighted_age_elc(df_elc):
    '''
    Function that will create a plot of the capacity weighted average age of the electrolyzers.
    :param:
        pd.DataFrame df_elc: Yearly data of the electrolyzers
    :return:
    '''
    # Prepare data
    df_phi = df_elc.set_index(['Year', 'Sensitivity', 'Run', 'ID'])
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index, columns=['Electrolyzers'])

    # Data
    for i in range(80):
        if i in df_phi.index.levels[0]:
            # Electrolyzers
            tmp_df = df_phi.loc[i]['Age'] * df_phi.loc[i]['Capacity']
            tmp_df = (tmp_df.groupby(['Sensitivity', 'Run']).sum() /
                      df_phi.loc[i]['Capacity'].groupby(['Sensitivity', 'Run']).sum())
            tmp_df = tmp_df.groupby(['Sensitivity']).median()
            for j in df_plot.index.levels[1]:
                if j not in tmp_df.index:
                    tmp_df[j] = np.nan
            df_plot['Electrolyzers'][i] = tmp_df


    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'],
                            gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'])

    # Lines
    for i in range(1, sensitivity_settings['No. of Runs'] + 1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Electrolyzers
        ax1.plot(x, df_plot['Electrolyzers'].xs(i, level='Sensitivity run'), linestyle='-', color=blue,
                 alpha=tmp_alpha)

    # Legend 1
    line1, = ax1.plot(x, np.ones(80) * -100, label='Electrolyzers', linestyle='-', color=blue)
    legend1 = ax1.legend(handles=[line1], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -100, color=blue, linestyle='-', alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1))

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    # Plot settings
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Age [years]')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(0)

    # Save plot
    plt.savefig(os.getcwd() + '\\plot_weighted_age_elc.' + plot_type, bbox_inches='tight')


def plot_weighted_age_man(df_man):
    '''
    Function that will create a plot of the capacity weighted average age of the factories for electorlyzers.
    :param:
        pd.DataFrame df_res: Yearly data of the factories for electrolyzers
    :return:
    '''
    # Prepare data
    df_phi = df_man.set_index(['Year', 'Sensitivity', 'Run', 'ID'])
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index, columns=['Factories for electrolyzers'])

    # Data
    for i in range(80):
        if i in df_phi.index.levels[0]:
            # Factories for electrolyzers
            tmp_df = df_phi.loc[i]['Age'] * df_phi.loc[i]['Capacity']
            tmp_df = (tmp_df.groupby(['Sensitivity', 'Run']).sum() /
                      df_phi.loc[i]['Capacity'].groupby(['Sensitivity', 'Run']).sum())
            tmp_df = tmp_df.groupby(['Sensitivity']).median()
            for j in df_plot.index.levels[1]:
                if j not in tmp_df.index:
                    tmp_df[j] = np.nan
            df_plot['Factories for electrolyzers'][i] = tmp_df


    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'],
                            gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'])

    # Lines
    for i in range(1, sensitivity_settings['No. of Runs'] + 1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Electrolyzers
        ax1.plot(x, df_plot['Factories for electrolyzers'].xs(i, level='Sensitivity run'), linestyle='-', color=purple,
                 alpha=tmp_alpha)

    # Legend 1
    line1, = ax1.plot(x, np.ones(80) * -100, label='Factories for electrolyzers', linestyle='-', color=purple)
    legend1 = ax1.legend(handles=[line1], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)

    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -100, color=purple, linestyle='-', alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1))

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    # Plot settings
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Age [years]')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(0)

    # Save plot
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
    # Prepare data
    df_phi_pp = df_pp.set_index(['Year', 'Sensitivity', 'Run', 'ID'])
    df_phi_hp = df_hp.set_index(['Year', 'Sensitivity', 'Run', 'ID'])
    df_phi_ep = df_ep.set_index(['Year', 'Sensitivity', 'Run', 'ID'])
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index, columns=['Power producers', 'Hydrogen producers',
                                                                  'Electrolyzer producers'])

    # Data
    for i in range(80):
        # Power producers
        if i in df_phi_pp.index.levels[0]:
            tmp_df = df_phi_pp.loc[i]['Profitability'].groupby(['Sensitivity', 'Run']).median()
            tmp_df = tmp_df.groupby(['Sensitivity']).median()
            for j in df_plot.index.levels[1]:
                if j not in tmp_df.index:
                    tmp_df[j] = np.nan
            df_plot['Power producers'][i] = tmp_df

        # Hydrogen producers
        if i in df_phi_hp.index.levels[0]:
            tmp_df = df_phi_hp.loc[i]['Profitability'].groupby(['Sensitivity', 'Run']).median()
            tmp_df = tmp_df.groupby(['Sensitivity']).median()
            for j in df_plot.index.levels[1]:
                if j not in tmp_df.index:
                    tmp_df[j] = np.nan
            df_plot['Hydrogen producers'][i] = tmp_df

        # Electrolyzer producers
        if i in df_phi_ep.index.levels[0]:
            tmp_df = df_phi_ep.loc[i]['Profitability'].groupby(['Sensitivity', 'Run']).median()
            tmp_df = tmp_df.groupby(['Sensitivity']).median()
            for j in df_plot.index.levels[1]:
                if j not in tmp_df.index:
                    tmp_df[j] = np.nan
            df_plot['Electrolyzer producers'][i] = tmp_df

    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'],
                            gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'])

    # Lines
    for i in range(1, sensitivity_settings['No. of Runs'] + 1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Power producers
        ax1.plot(x, df_plot['Power producers'].xs(i, level='Sensitivity run'), linestyle='-', color=green,
                 alpha=tmp_alpha)
        # Hydrogen producers
        ax1.plot(x, df_plot['Hydrogen producers'].xs(i, level='Sensitivity run'), linestyle='-', color=blue,
                 alpha=tmp_alpha)
        # Electrolyzer producers
        ax1.plot(x, df_plot['Electrolyzer producers'].xs(i, level='Sensitivity run'), linestyle='-', color=purple,
                 alpha=tmp_alpha)

    # Legend 1
    line1, = ax1.plot(x, np.ones(80) * -100, label='Power producers', linestyle='-', color=green)
    line2, = ax1.plot(x, np.ones(80) * -100, label='Hydrogen producers', linestyle='-', color=blue)
    line3, = ax1.plot(x, np.ones(80) * -100, label='Electrolyzer producers', linestyle='-', color=purple)
    line4, = ax1.plot(x, np.ones(80) * 1, label='Profitability threshold', linestyle='-.', color=orange)
    legend1 = ax1.legend(handles=[line1, line2, line3, line4], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)


    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -100, color=green, linestyle='-', alpha=tmp_alpha, label=tmp_label)
        tmp_line2, = ax1.plot(x, np.ones(80) * -100, color=blue, linestyle='-', alpha=tmp_alpha, label=tmp_label)
        tmp_line3, = ax1.plot(x, np.ones(80) * -100, color=purple, linestyle='-', alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1, tmp_line2, tmp_line3))

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    # Plot settings
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Profitability [-]')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(0)

    # Save plot
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
    # Prepare data
    df_phi_pp = df_pp.set_index(['Year', 'Sensitivity', 'Run', 'ID'])
    df_phi_hp = df_hp.set_index(['Year', 'Sensitivity', 'Run', 'ID'])
    df_phi_ep = df_ep.set_index(['Year', 'Sensitivity', 'Run', 'ID'])
    tmp_index = pd.MultiIndex.from_product([range(80), range(1,sensitivity_settings['No. of Runs']+1)],
                                           names=['Year', 'Sensitivity run'])
    df_plot = pd.DataFrame(data=np.nan, index=tmp_index, columns=['Power producers', 'Hydrogen producers',
                                                                  'Electrolyzer producers'])

    # Data
    for i in range(80):
        # Power producers
        if i in df_phi_pp.index.levels[0]:
            tmp_df = df_phi_pp.loc[i]['Profitability'] * df_phi_pp.loc[i]['Installed capacity Renewables']
            tmp_df = (tmp_df.groupby(['Sensitivity', 'Run']).sum() /
                      df_phi_pp.loc[i]['Installed capacity Renewables'].groupby(['Sensitivity', 'Run']).sum())
            tmp_df = tmp_df.groupby(['Sensitivity']).median()
            for j in df_plot.index.levels[1]:
                if j not in tmp_df.index:
                    tmp_df[j] = np.nan
            df_plot['Power producers'][i] = tmp_df
        # Hydrogen producers
        if i in df_phi_hp.index.levels[0]:
            tmp_df = df_phi_hp.loc[i]['Profitability'] * df_phi_hp.loc[i]['Installed capacity Electrolyzers']
            tmp_df = (tmp_df.groupby(['Sensitivity', 'Run']).sum() /
                      df_phi_hp.loc[i]['Installed capacity Electrolyzers'].groupby(['Sensitivity', 'Run']).sum())
            tmp_df = tmp_df.groupby(['Sensitivity']).median()
            for j in df_plot.index.levels[1]:
                if j not in tmp_df.index:
                    tmp_df[j] = np.nan
            df_plot['Hydrogen producers'][i] = tmp_df
        # Electrolyzer producers
        if i in df_phi_pp.index.levels[0]:
            tmp_df = df_phi_ep.loc[i]['Profitability'] * df_phi_ep.loc[i]['Installed capacity Manufacturings']
            tmp_df = (tmp_df.groupby(['Sensitivity', 'Run']).sum() /
                      df_phi_ep.loc[i]['Installed capacity Manufacturings'].groupby(['Sensitivity', 'Run']).sum())
            tmp_df = tmp_df.groupby(['Sensitivity']).median()
            for j in df_plot.index.levels[1]:
                if j not in tmp_df.index:
                    tmp_df[j] = np.nan
            df_plot['Electrolyzer producers'][i] = tmp_df

    # Plot
    fig, ax1 = plt.subplots(1, 1, figsize=plot_settings['figsize'],
                            gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'])

    # Lines
    for i in range(1, sensitivity_settings['No. of Runs'] + 1):
        tmp_alpha = 0.25 + 0.75 * (i - 1) / (sensitivity_settings['No. of Runs'])
        # Power producers
        ax1.plot(x, df_plot['Power producers'].xs(i, level='Sensitivity run'), linestyle='-', color=green,
                 alpha=tmp_alpha)
        # Hydrogen producers
        ax1.plot(x, df_plot['Hydrogen producers'].xs(i, level='Sensitivity run'), linestyle='-', color=blue,
                 alpha=tmp_alpha)
        # Electrolyzer producers
        ax1.plot(x, df_plot['Electrolyzer producers'].xs(i, level='Sensitivity run'), linestyle='-', color=purple,
                 alpha=tmp_alpha)

    # Legend 1
    line1, = ax1.plot(x, np.ones(80) * -100, label='Power producers', linestyle='-', color=green)
    line2, = ax1.plot(x, np.ones(80) * -100, label='Hydrogen producers', linestyle='-', color=blue)
    line3, = ax1.plot(x, np.ones(80) * -100, label='Electrolyzer producers', linestyle='-', color=purple)
    line4, = ax1.plot(x, np.ones(80) * 1, label='Profitability threshold', linestyle='-.', color=orange)
    legend1 = ax1.legend(handles=[line1, line2, line3, line4], loc='lower left', bbox_to_anchor=(-0.05, -0.25))
    ax1.add_artist(legend1)


    # Legend 2
    tmp_handles = []
    tmp_labels = []
    for i in range(sensitivity_settings['No. of Runs']):
        tmp_alpha = 0.25 + 0.75 * i / (sensitivity_settings['No. of Runs'] - 1)
        tmp_para = str()
        for j in sensitivity_settings['Parameters']:
            tmp = para_dict[j]
            if j in sensitivity_settings['Parameters'][-1]:
                tmp_para += tmp
            else:
                tmp_para += tmp + '; '
        tmp_values = str()
        j = 0
        while j < len(sensitivity_settings['Values'][i]):
            if j == (len(sensitivity_settings['Values'][i]) - 1):
                tmp_values += str(sensitivity_settings['Values'][i][j])
            else:
                tmp_values += str(sensitivity_settings['Values'][i][j]) + '; '
            j += 1
        tmp_label = str(tmp_para + ': ' + tmp_values)
        tmp_labels.append(tmp_label)
        tmp_line1, = ax1.plot(x, np.ones(80) * -100, color=green, linestyle='-', alpha=tmp_alpha, label=tmp_label)
        tmp_line2, = ax1.plot(x, np.ones(80) * -100, color=blue, linestyle='-', alpha=tmp_alpha, label=tmp_label)
        tmp_line3, = ax1.plot(x, np.ones(80) * -100, color=purple, linestyle='-', alpha=tmp_alpha, label=tmp_label)
        tmp_handles.append((tmp_line1, tmp_line2, tmp_line3))

    legend2 = ax1.legend(tmp_handles, tmp_labels, loc='upper left', bbox_to_anchor=(1, 1),
                         handler_map={tuple: HandlerTuple(ndivide=None)})

    # Plot settings
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Profitability [-]')
    ax1.set_xlim(plot_settings['xlim'])
    ax1.set_ylim(0)

    # Save plot
    plt.savefig(os.getcwd() + '\\plot_weighted_profitability.' + plot_type, bbox_inches='tight')


def main(dir):
    '''
    Function that will create all plots based ond the results in dir
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
    print('Check and load data for sensitivity analysis...')
    check_sensitivity_config()
    check_data()
    tmp_list = load_data()
    df_pm, df_hm, df_em = tmp_list[8], tmp_list[4], tmp_list[1]
    df_pm_daily, df_hm_daily = tmp_list[7], tmp_list[3]
    df_pp, df_hp, df_ep = tmp_list[9], tmp_list[5], tmp_list[2]
    df_sale = tmp_list[-1]
    df_res, df_elc, df_man = tmp_list[10], tmp_list[0], tmp_list[6]

    # Create all plots
    print('Create plots for sensitivity analysis...')
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
    #plot_duration_curves_res(df_pm, df_pm_daily)
    #plot_duration_curves_elc(df_hm_daily)
    #plot_load_type_elc(df_pm, df_hm)
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

    # Debuging only
    dir = 'D:\\Jesse\\sciebo\\00_Promotion\\06_Model\\02_ABM\\02_NetLogo\\02_Output\\2024-07-13-20-49\\'
    main(dir)

