'''
him - Hydrogen Investment Model
This script will take the results of multiple runs and will create plots. The list of plots can be seen below

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


version: 0.2.24.07.19
date: 2024-07-19
author: Jesse

changelog:
0.1.24.07.15 - start new script
0.1.24.07.16 - add load data
             - add plots for no. of agents
0.2.24.07.19 - feature complete
'''
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
plot_settings['xlim'] = (2023, 2050)
plot_settings['loc'] = 'lower left'
blue = [173 / 255, 189 / 255, 227 / 255]
darkblue = [2 / 255, 61 / 255, 107 / 255]
green = [185 / 255, 210 / 255, 95 / 255]
black = [0, 0, 0]
grey = [235 / 255, 235 / 255, 235 / 255]
orange = [250 / 255, 180 / 255, 90 / 255]
purple = [175 / 255, 130 / 255, 185 / 255]
red = [235 / 255, 95 / 255, 115 / 255]
year0 = 2023
delta_year = 80
x = list(range(year0, year0 + delta_year))


def check_data():
    '''
    Function that checks if all files exists.
    :return:
    '''
    wkdir = os.getcwd()
    global list_runs
    list_runs = []
    for i in os.listdir(wkdir):
        if i.startswith('Run_'):
            for j in list_files:
                if not os.path.isfile(str(i + '\\' + j)):
                    print('Error in check_data: ' + i + '\\' + j + ' not found.')
                    exit(100)
            list_runs.append(i)
    print(str(len(list_runs)) + ' runs found.')


def load_data():
    '''
    Function that loads the data from the csv files.
    :return:
        list tmp_list: List that contains the data from all file as an individual pd.Dataframe.
    '''
    tmp_list = []
    wkdir = os.getcwd()
    for j in list_files:
        list_df = []
        for i in list_runs:
            try:
                file = (str(wkdir) + '\\' + i + '\\' + j)
                tmp_df = pd.read_csv(file, sep=';')
                tmp_df['Run'] = np.ones(len(tmp_df.index)) * int(i.split('_')[1])
                list_df.append(tmp_df)
            except FileNotFoundError:
                print('Error in load_data: ' + i + '\\' + j + ' not found.')
                exit(200)
        tmp_list.append(pd.concat(list_df))

    return (tmp_list)


def plot_no_of_agents(df_pm, df_hm, df_em):
    '''
    Will create the plot of the number of agents for all three markets.
    :param:
        pd.DataFrame df_pm: Yearly data of the power market
        pd.DataFrame df_hm: Yearly data of the hydrogen market
        pd.DataFrame df_em: Yearly data of the electrolyzer market
    :return:
    '''
    # Power Producers
    df_phi_pp = df_pm.set_index(['Year', 'Run'])
    df_plot_pp = pd.DataFrame(data=np.nan, index=range(80), columns=['Max', 'Median', 'Mean', 'Min', '25%', '75%'])

    # Hydrogen Producers
    df_phi_hp = df_hm.set_index(['Year', 'Run'])
    df_plot_hp = pd.DataFrame(data=np.nan, index=range(80), columns=['Max', 'Median', 'Mean', 'Min', '25%', '75%'])

    # Electrolyzer Producers
    df_phi_ep = df_em.set_index(['Year', 'Run'])
    df_plot_ep = pd.DataFrame(data=np.nan, index=range(80), columns=['Max', 'Median', 'Mean', 'Min', '25%', '75%'])

    for i in range(80):
        # Power Producers
        if i in df_phi_pp.index.levels[0]:
            tmp_df = df_phi_pp.loc[i]['No. of Powerproducers']
            df_plot_pp.loc[i, 'Max'] = tmp_df.max()
            df_plot_pp.loc[i, 'Median'] = tmp_df.median()
            df_plot_pp.loc[i, 'Mean'] = tmp_df.mean()
            df_plot_pp.loc[i, 'Min'] = tmp_df.min()
            df_plot_pp.loc[i, '25%'] = tmp_df.quantile(q=0.25)
            df_plot_pp.loc[i, '75%'] = tmp_df.quantile(q=0.75)

        # Hydrogen Producers
        if i in df_phi_hp.index.levels[0]:
            tmp_df = df_phi_hp.loc[i]['No. of Hydrogenproducers']
            df_plot_hp.loc[i, 'Max'] = tmp_df.max()
            df_plot_hp.loc[i, 'Median'] = tmp_df.median()
            df_plot_hp.loc[i, 'Mean'] = tmp_df.mean()
            df_plot_hp.loc[i, 'Min'] = tmp_df.min()
            df_plot_hp.loc[i, '25%'] = tmp_df.quantile(q=0.25)
            df_plot_hp.loc[i, '75%'] = tmp_df.quantile(q=0.75)

        # Electrolyzer Producers
        if i in df_phi_ep.index.levels[0]:
            tmp_df = df_phi_ep.loc[i]['No. of Electrolyzerproducers']
            df_plot_ep.loc[i, 'Max'] = tmp_df.max()
            df_plot_ep.loc[i, 'Median'] = tmp_df.median()
            df_plot_ep.loc[i, 'Mean'] = tmp_df.mean()
            df_plot_ep.loc[i, 'Min'] = tmp_df.min()
            df_plot_ep.loc[i, '25%'] = tmp_df.quantile(q=0.25)
            df_plot_ep.loc[i, '75%'] = tmp_df.quantile(q=0.75)

    fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=plot_settings['figsize'],
                                        gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'],
                                        sharex=True)

    # Power Producers
    # ax1.plot(x, df_plot_pp['97.5%'], linestyle='-', color=black, alpha=0.3)
    # ax1.plot(x, df_plot_pp['2.5%'], linestyle='-', color=black, alpha=0.3)
    # ax1.plot(x, df_plot_pp['Median'], label='Power producers - median', linestyle='--', color=black)
    ax1.plot(x, df_plot_pp['Median'], label='Power producers', linestyle='-', color=green)
    ax1.fill_between(x, df_plot_pp['25%'], df_plot_pp['75%'], color=green, alpha=0.25, edgecolor='none')
    # ax1.legend(loc='upper left')
    ax1.set_ylim(-0.1)

    # Hydrogen Producers
    ax2.set_ylabel('No. of Agents')
    # ax2.plot(x, df_plot_hp['97.5%'], linestyle='-', color=blue, alpha=0.3)
    # ax2.plot(x, df_plot_hp['2.5%'], linestyle='-', color=blue, alpha=0.3)
    # ax2.plot(x, df_plot_hp['Median'], label='Hydrogen producers - median', linestyle='--', color=blue)
    ax2.plot(x, df_plot_hp['Median'], label='Hydrogen producers', linestyle='-', color=blue)
    ax2.fill_between(x, df_plot_hp['25%'], df_plot_hp['75%'], color=blue, alpha=0.25, edgecolor='none')
    # ax2.legend(loc='upper left')
    ax2.set_ylim(-0.1)

    # Electrolyzer Producers
    ax3.set_xlabel('Year')
    # ax3.plot(x, df_plot_ep['97.5%'], linestyle='-', color=green, alpha=0.3)
    # ax3.plot(x, df_plot_ep['2.5%'], linestyle='-', color=green, alpha=0.3)
    # ax3.plot(x, df_plot_ep['Median'], label='Electrolyzer producers - median', linestyle='--', color=green)
    ax3.plot(x, df_plot_ep['Median'], label='Electrolyzer producers', linestyle='-', color=purple)
    ax3.fill_between(x, df_plot_ep['25%'], df_plot_ep['75%'], color=purple, alpha=0.25, edgecolor='none')
    # ax3.legend(loc='upper left')
    ax3.set_ylim(-0.1)

    handle1, label1 = ax1.get_legend_handles_labels()
    handle2, label2 = ax2.get_legend_handles_labels()
    handle3, label3 = ax3.get_legend_handles_labels()
    handles = handle1 + handle2 + handle3
    labels = label1 + label2 + label3

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc=plot_settings['loc'],
               bbox_to_anchor=(-0.05, -0.75), ncol=3, frameon=False)

    plt.xlim(plot_settings['xlim'])
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
    # Power Producers
    df_phi_pp = df_pm.set_index(['Year', 'Run'])
    df_plot_pp = pd.DataFrame(data=np.nan, index=range(80), columns=['Max', 'Median', 'Mean', 'Min', '97.5%', '2.5%'])

    # Hydrogen Producers
    df_phi_hp = df_hm.set_index(['Year', 'Run'])
    df_plot_hp = pd.DataFrame(data=np.nan, index=range(80), columns=['Max', 'Median', 'Mean', 'Min', '97.5%', '2.5%'])

    # Electrolyzer Producers
    df_phi_ep = df_em.set_index(['Year', 'Run'])
    df_plot_ep = pd.DataFrame(data=np.nan, index=range(80), columns=['Max', 'Median', 'Mean', 'Min', '97.5%', '2.5%'])

    for i in range(80):
        # Power Producers
        if i in df_phi_pp.index.levels[0]:
            tmp_df = df_phi_pp.loc[i]['No. of Investments PM']
            df_plot_pp.loc[i, 'Max'] = tmp_df.max()
            df_plot_pp.loc[i, 'Median'] = tmp_df.median()
            df_plot_pp.loc[i, 'Mean'] = tmp_df.mean()
            df_plot_pp.loc[i, 'Min'] = tmp_df.min()
            df_plot_pp.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot_pp.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)

        # Hydrogen Producers
        if i in df_phi_hp.index.levels[0]:
            tmp_df = df_phi_hp.loc[i]['No. of Investments HM']
            df_plot_hp.loc[i, 'Max'] = tmp_df.max()
            df_plot_hp.loc[i, 'Median'] = tmp_df.median()
            df_plot_hp.loc[i, 'Mean'] = tmp_df.mean()
            df_plot_hp.loc[i, 'Min'] = tmp_df.min()
            df_plot_hp.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot_hp.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)

        # Electrolyzer Producers
        if i in df_phi_ep.index.levels[0]:
            tmp_df = df_phi_ep.loc[i]['No. of Investments EM']
            df_plot_ep.loc[i, 'Max'] = tmp_df.max()
            df_plot_ep.loc[i, 'Median'] = tmp_df.median()
            df_plot_ep.loc[i, 'Mean'] = tmp_df.mean()
            df_plot_ep.loc[i, 'Min'] = tmp_df.min()
            df_plot_ep.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot_ep.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)

    fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=plot_settings['figsize'],
                                        gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'],
                                        sharex=True)

    # Power Producers
    # ax1.plot(x, df_plot_pp['97.5%'], linestyle='-', color=black, alpha=0.3)
    # ax1.plot(x, df_plot_pp['2.5%'], linestyle='-', color=black, alpha=0.3)
    ax1.plot(x, df_plot_pp['Median'], label='Power market', linestyle='-', color=green)
    # ax1.plot(x, df_plot_pp['Mean'], label='Power market - mean', linestyle='-', color=black)
    ax1.fill_between(x, df_plot_pp['97.5%'], df_plot_pp['2.5%'], color=green, alpha=0.25, edgecolor='none')
    ax1.set_ylim(0)
    # ax1.legend(loc='upper left')

    # Hydrogen Producers
    ax2.set_ylabel('No. of Investments')
    # ax2.plot(x, df_plot_hp['97.5%'], linestyle='-', color=blue, alpha=0.3)
    # ax2.plot(x, df_plot_hp['2.5%'], linestyle='-', color=blue, alpha=0.3)
    ax2.plot(x, df_plot_hp['Median'], label='Hydrogen market', linestyle='-', color=blue)
    # ax2.plot(x, df_plot_hp['Mean'], label='Hydrogen market - mean', linestyle='-', color=blue)
    ax2.fill_between(x, df_plot_hp['97.5%'], df_plot_hp['2.5%'], color=blue, alpha=0.25, edgecolor='none')
    ax2.set_ylim(0)
    # ax2.legend(loc='upper left')

    # Electrolyzer Producers
    ax3.set_xlabel('Year')
    # ax3.plot(x, df_plot_ep['97.5%'], linestyle='-', color=green, alpha=0.3)
    # ax3.plot(x, df_plot_ep['2.5%'], linestyle='-', color=green, alpha=0.3)
    ax3.plot(x, df_plot_ep['Median'], label='Electrolyzer market', linestyle='-', color=purple)
    # ax3.plot(x, df_plot_ep['Mean'], label='Electrolyzer market - mean', linestyle='-', color=green)
    ax3.fill_between(x, df_plot_ep['97.5%'], df_plot_ep['2.5%'], color=purple, alpha=0.25, edgecolor='none')
    ax3.set_ylim(0)
    # ax3.legend(loc='upper left')

    handle1, label1 = ax1.get_legend_handles_labels()
    handle2, label2 = ax2.get_legend_handles_labels()
    handle3, label3 = ax3.get_legend_handles_labels()
    handles = handle1 + handle2 + handle3
    labels = label1 + label2 + label3

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc=plot_settings['loc'],
               bbox_to_anchor=(-0.05, -0.75), ncol=3, frameon=False)

    plt.xlim(plot_settings['xlim'])
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
    df_phi_pp = df_pm.set_index(['Year', 'Run'])
    df_plot_pp = pd.DataFrame(data=np.nan, index=range(80), columns=['Max', 'Median', 'Mean', 'Min', '97.5%', '2.5%'])

    # Hydrogen Producers
    df_phi_hp = df_hm.set_index(['Year', 'Run'])
    df_plot_hp = pd.DataFrame(data=np.nan, index=range(80), columns=['Max', 'Median', 'Mean', 'Min', '97.5%', '2.5%'])

    # Electrolyzer Producers
    df_phi_ep = df_em.set_index(['Year', 'Run'])
    df_plot_ep = pd.DataFrame(data=np.nan, index=range(80), columns=['Max', 'Median', 'Mean', 'Min', '97.5%', '2.5%'])

    for i in range(80):
        # Power Producers
        if i in df_phi_pp.index.levels[0]:
            tmp_df = (df_phi_pp.loc[i]['No. of Investments PM'] /
                      df_phi_pp.loc[i]['No. of Powerproducers'].replace(0, np.nan))
            df_plot_pp.loc[i, 'Max'] = tmp_df.max()
            df_plot_pp.loc[i, 'Median'] = tmp_df.median()
            df_plot_pp.loc[i, 'Mean'] = tmp_df.mean()
            df_plot_pp.loc[i, 'Min'] = tmp_df.min()
            df_plot_pp.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot_pp.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)

        # Hydrogen Producers
        if i in df_phi_hp.index.levels[0]:
            tmp_df = (df_phi_hp.loc[i]['No. of Investments HM'] /
                      df_phi_hp.loc[i]['No. of Hydrogenproducers'].replace(0, np.nan))
            df_plot_hp.loc[i, 'Max'] = tmp_df.max()
            df_plot_hp.loc[i, 'Median'] = tmp_df.median()
            df_plot_hp.loc[i, 'Mean'] = tmp_df.mean()
            df_plot_hp.loc[i, 'Min'] = tmp_df.min()
            df_plot_hp.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot_hp.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)

        # Electrolyzer Producers
        if i in df_phi_ep.index.levels[0]:
            tmp_df = (df_phi_ep.loc[i]['No. of Investments EM'] /
                      df_phi_ep.loc[i]['No. of Electrolyzerproducers'].replace(0, np.nan))
            df_plot_ep.loc[i, 'Max'] = tmp_df.max()
            df_plot_ep.loc[i, 'Median'] = tmp_df.median()
            df_plot_ep.loc[i, 'Mean'] = tmp_df.mean()
            df_plot_ep.loc[i, 'Min'] = tmp_df.min()
            df_plot_ep.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot_ep.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)

    fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=plot_settings['figsize'],
                                        gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'],
                                        sharex=True)

    # Power Producers
    # ax1.plot(x, df_plot_pp['97.5%'], linestyle='-', color=black, alpha=0.3)
    # ax1.plot(x, df_plot_pp['2.5%'], linestyle='-', color=black, alpha=0.3)
    ax1.plot(x, df_plot_pp['Median'], label='Power market', linestyle='-', color=green)
    # ax1.plot(x, df_plot_pp['Mean'], label='Power market - mean', linestyle='-', color=black)
    ax1.fill_between(x, df_plot_pp['97.5%'], df_plot_pp['2.5%'], color=green, alpha=0.25)
    ax1.set_ylim(0)
    # ax1.legend(loc='upper left')

    # Hydrogen Producers
    ax2.set_ylabel('No. of Investment / No. of Agents')
    # ax2.plot(x, df_plot_hp['97.5%'], linestyle='-', color=blue, alpha=0.3)
    # ax2.plot(x, df_plot_hp['2.5%'], linestyle='-', color=blue, alpha=0.3)
    ax2.plot(x, df_plot_hp['Median'], label='Hydrogen market', linestyle='-', color=blue)
    # ax2.plot(x, df_plot_hp['Mean'], label='Hydrogen market - mean', linestyle='-', color=blue)
    ax2.fill_between(x, df_plot_hp['97.5%'], df_plot_hp['2.5%'], color=blue, alpha=0.25)
    ax2.set_ylim(0)
    # ax2.legend(loc='upper left')

    # Electrolyzer Producers
    ax3.set_xlabel('Year')
    # ax3.plot(x, df_plot_ep['97.5%'], linestyle='-', color=green, alpha=0.3)
    # ax3.plot(x, df_plot_ep['2.5%'], linestyle='-', color=green, alpha=0.3)
    ax3.plot(x, df_plot_ep['Median'], label='Electrolyzer market', linestyle='-', color=purple)
    # ax3.plot(x, df_plot_ep['Mean'], label='Electrolyzer market - mean', linestyle='-', color=green)
    ax3.fill_between(x, df_plot_ep['97.5%'], df_plot_ep['2.5%'], color=purple, alpha=0.25)
    ax3.set_ylim(0)
    # ax3.legend(loc='upper left')

    handle1, label1 = ax1.get_legend_handles_labels()
    handle2, label2 = ax2.get_legend_handles_labels()
    handle3, label3 = ax3.get_legend_handles_labels()
    handles = handle1 + handle2 + handle3
    labels = label1 + label2 + label3

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc=plot_settings['loc'],
               bbox_to_anchor=(-0.05, -0.75), ncol=3, frameon=False)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_ratio_investment_agents.' + plot_type, bbox_inches='tight')


def plot_installed_cap_res(df_pm):
    '''
    Function that will create a plot of the installed capacities of renewables.
    :param:
        pd.DataFrame df_pm: Data from the power market
    :return:
    '''
    # Power Producers
    df_phi_pp = df_pm.set_index(['Year', 'Run'])
    df_plot_pp = pd.DataFrame(data=np.nan, index=range(80), columns=['Max', 'Median', 'Mean', 'Min', '97.5%', '2.5%'])

    for i in range(80):
        # Power Producers
        if i in df_phi_pp.index.levels[0]:
            tmp_df = df_phi_pp.loc[i]['Installed capacity Renewables']
            df_plot_pp.loc[i, 'Max'] = tmp_df.max()
            df_plot_pp.loc[i, 'Median'] = tmp_df.median()
            df_plot_pp.loc[i, 'Mean'] = tmp_df.mean()
            df_plot_pp.loc[i, 'Min'] = tmp_df.min()
            df_plot_pp.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot_pp.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Installed capacity [GW]')
    # ax1.plot(x, df_plot_pp['97.5%']/1e3, linestyle='-', color=black, alpha=0.3)
    # ax1.plot(x, df_plot_pp['2.5%']/1e3, linestyle='-', color=black, alpha=0.3)
    ax1.plot(x, df_plot_pp['Median'] / 1e3, label='Renewables', linestyle='-', color=green)
    # ax1.plot(x, df_plot_pp['Mean']/1e3, label='Renewables - mean', linestyle='-', color=black)
    ax1.fill_between(x, df_plot_pp['97.5%'] / 1e3, df_plot_pp['2.5%'] / 1e3, color=green, alpha=0.25)
    ax1.plot(x, (np.ones(80) * 375), label='Governmental target', linestyle='-.', color=orange)
    ax1.set_ylim(0)

    plt.xlim(plot_settings['xlim'])
    plt.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), ncol=2, frameon=False)
    plt.savefig(os.getcwd() + '\\plot_installed_cap_res.' + plot_type, bbox_inches='tight')


def plot_installed_cap_elc(df_hm):
    '''
    Function that will create a plot of the installed capacities of electrolyzers.
    :param:
        pd.DataFrame df_hm: Data from the hydrogen market
    :return:
    '''
    # Hydrogen Producers
    df_phi_hp = df_hm.set_index(['Year', 'Run'])
    df_plot_hp = pd.DataFrame(data=np.nan, index=range(80), columns=['Max', 'Median', 'Mean', 'Min', '97.5%', '2.5%'])

    for i in range(80):
        # Hydrogen Producers
        if i in df_phi_hp.index.levels[0]:
            tmp_df = df_phi_hp.loc[i]['Installed capacity Electrolyzers']
            df_plot_hp.loc[i, 'Max'] = tmp_df.max()
            df_plot_hp.loc[i, 'Median'] = tmp_df.median()
            df_plot_hp.loc[i, 'Mean'] = tmp_df.mean()
            df_plot_hp.loc[i, 'Min'] = tmp_df.min()
            df_plot_hp.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot_hp.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Installed capacity [GW]')
    ax1.fill_between(x, (np.ones(80) * 50), (np.ones(80) * 80), label='Needed in 2050', color=orange,
                     alpha=0.25, edgecolor='none')
    # ax1.plot(x, df_plot_hp['97.5%']/1e3, linestyle='-', color=blue, alpha=0.3)
    # ax1.plot(x, df_plot_hp['2.5%']/1e3, linestyle='-', color=blue, alpha=0.3)
    ax1.plot(x, df_plot_hp['Median'] / 1e3, label='Electrolyzer', linestyle='-', color=blue)
    # ax1.plot(x, df_plot_hp['Mean']/1e3, label='Electrolyzer - mean', linestyle='-', color=blue)
    ax1.fill_between(x, df_plot_hp['97.5%'] / 1e3, df_plot_hp['2.5%'] / 1e3, color=blue, alpha=0.25)
    ax1.plot(x, (np.ones(80) * 10), label='Governmental target', linestyle='-.', color=orange)
    ax1.set_ylim(-0.1)

    plt.xlim(plot_settings['xlim'])
    plt.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.3), ncol=2, frameon=False)
    plt.savefig(os.getcwd() + '\\plot_installed_cap_elc.' + plot_type, bbox_inches='tight')


def plot_installed_cap_man(df_em):
    '''
    Function that will create a plot of the installed manufacturing capacities for electrolyzers.
    :param:
        pd.DataFrame df_hm: Data from the electrolyzer market
    :return:
    '''
    # Electrolyzer Producers
    df_phi_ep = df_em.set_index(['Year', 'Run'])
    df_plot_ep = pd.DataFrame(data=np.nan, index=range(80), columns=['Max', 'Median', 'Mean', 'Min', '97.5%', '2.5%'])

    for i in range(80):
        # Electrolyzer Producers
        if i in df_phi_ep.index.levels[0]:
            tmp_df = df_phi_ep.loc[i]['Installed capacity Manufacturings']
            df_plot_ep.loc[i, 'Max'] = tmp_df.max()
            df_plot_ep.loc[i, 'Median'] = tmp_df.median()
            df_plot_ep.loc[i, 'Mean'] = tmp_df.mean()
            df_plot_ep.loc[i, 'Min'] = tmp_df.min()
            df_plot_ep.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot_ep.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Installed capacity [GW/Year]')
    # ax1.plot(x, df_plot_ep['97.5%']/1e3, linestyle='-', color=green, alpha=0.3)
    # ax1.plot(x, df_plot_ep['2.5%']/1e3, linestyle='-', color=green, alpha=0.3)
    ax1.plot(x, df_plot_ep['Median'] / 1e3, label='Electrolyzer factory ', linestyle='-', color=purple)
    # ax1.plot(x, df_plot_ep['Mean']/1e3, label='Electrolyzer factory - mean', linestyle='-', color=green)
    ax1.fill_between(x, df_plot_ep['97.5%'] / 1e3, df_plot_ep['2.5%'] / 1e3, color=purple, alpha=0.25)
    ax1.set_ylim(-0.1)

    plt.xlim(plot_settings['xlim'])
    plt.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), ncol=2, frameon=False)
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
    df_phi_pp = df_pm.set_index(['Year', 'Run'])
    df_plot_pp = pd.DataFrame(data=np.nan, index=range(80), columns=['Max', 'Median', 'Mean', 'Min', '97.5%', '2.5%'])

    # Hydrogen Producers
    df_phi_hp = df_hm.set_index(['Year', 'Run'])
    df_plot_hp = pd.DataFrame(data=np.nan, index=range(80), columns=['Max', 'Median', 'Mean', 'Min', '97.5%', '2.5%'])

    # Electrolyzer Producers
    df_phi_ep = df_em.set_index(['Year', 'Run'])
    df_plot_ep = pd.DataFrame(data=np.nan, index=range(80), columns=['Max', 'Median', 'Mean', 'Min', '97.5%', '2.5%'])

    for i in range(80):
        # Power Producers
        if i in df_phi_pp.index.levels[0]:
            tmp_df = df_phi_pp.loc[i]['Installed capacity Renewables']
            df_plot_pp.loc[i, 'Max'] = tmp_df.max()
            df_plot_pp.loc[i, 'Median'] = tmp_df.median()
            df_plot_pp.loc[i, 'Mean'] = tmp_df.mean()
            df_plot_pp.loc[i, 'Min'] = tmp_df.min()
            df_plot_pp.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot_pp.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)

        # Hydrogen Producers
        if i in df_phi_hp.index.levels[0]:
            tmp_df = df_phi_hp.loc[i]['Installed capacity Electrolyzers']
            df_plot_hp.loc[i, 'Max'] = tmp_df.max()
            df_plot_hp.loc[i, 'Median'] = tmp_df.median()
            df_plot_hp.loc[i, 'Mean'] = tmp_df.mean()
            df_plot_hp.loc[i, 'Min'] = tmp_df.min()
            df_plot_hp.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot_hp.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)

        # Electrolyzer Producers
        if i in df_phi_ep.index.levels[0]:
            tmp_df = df_phi_ep.loc[i]['Installed capacity Manufacturings']
            df_plot_ep.loc[i, 'Max'] = tmp_df.max()
            df_plot_ep.loc[i, 'Median'] = tmp_df.median()
            df_plot_ep.loc[i, 'Mean'] = tmp_df.mean()
            df_plot_ep.loc[i, 'Min'] = tmp_df.min()
            df_plot_ep.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot_ep.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)

    fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=plot_settings['figsize'],
                                        gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'], sharex=True)

    ax1.title.set_text('Installed capacity Renewables, Electrolyzers and Electrolyzer Factories')
    ax1.set_ylabel('[GW]')
    # ax1.plot(x, df_plot_pp['97.5%']/1e3, linestyle='-', color=black, alpha=0.3)
    # ax1.plot(x, df_plot_pp['2.5%']/1e3, linestyle='-', color=black, alpha=0.3)
    ax1.plot(x, df_plot_pp['Median'] / 1e3, label='Renewables - median', linestyle='-', color=green)
    # ax1.plot(x, df_plot_pp['Mean']/1e3, label='Renewables - mean', linestyle='-', color=black)
    ax1.fill_between(x, df_plot_pp['97.5%'] / 1e3, df_plot_pp['2.5%'] / 1e3, color=green, alpha=0.25)
    ax1.plot(x, (np.ones(80) * 375), label='Governmental target', linestyle='-.', color=orange)
    ax1.scatter(2030, 375, label='Governmental target', facecolor='None', edgecolor=orange)
    # ax1.scatter(year0, 168, label='Today', color=black)
    ax1.set_ylim([-0.1, 450])
    # ax1.legend(loc='upper left')

    ax2.set_ylabel('[GW]')
    # ax2.plot(x, df_plot_hp['97.5%']/1e3, linestyle='-', color=blue, alpha=0.3)
    # ax2.plot(x, df_plot_hp['2.5%']/1e3, linestyle='-', color=blue, alpha=0.3)
    ax2.fill_between(x, (np.ones(80) * 50), (np.ones(80) * 80), label='Needed in 2050', color=orange,
                     alpha=0.25, edgecolor='none')
    ax2.plot(x, df_plot_hp['Median'] / 1e3, label='Electrolyzer - median', linestyle='-', color=blue)
    # ax2.plot(x, df_plot_hp['Mean']/1e3, label='Electrolyzer - mean', linestyle='-', color=blue)
    ax2.fill_between(x, df_plot_hp['97.5%'] / 1e3, df_plot_hp['2.5%'] / 1e3, color=blue, alpha=0.25)
    ax2.plot(x, (np.ones(80) * 10), label='Governmental target', linestyle='-.', color=orange)
    ax2.scatter(2030, 10, label='Governmental target', facecolor='None', edgecolor=orange)
    # ax2.scatter(year0, 0.05, label='Today', color=blue)
    ax2.set_ylim(-0.1)
    # ax2.legend(loc='upper left')

    ax3.set_xlabel('Year')
    ax3.set_ylabel('[GW/Year]')
    # ax3.plot(x, df_plot_ep['97.5%']/1e3, linestyle='-', color=green, alpha=0.3)
    # ax3.plot(x, df_plot_ep['2.5%']/1e3, linestyle='-', color=green, alpha=0.3)
    ax3.plot(x, df_plot_ep['Median'] / 1e3, label='Electrolyzer factory - median', linestyle='-', color=purple)
    # ax3.plot(x, df_plot_ep['Mean']/1e3, label='Electrolyzer factory - mean', linestyle='-', color=green)
    ax3.fill_between(x, df_plot_ep['97.5%'] / 1e3, df_plot_ep['2.5%'] / 1e3, color=purple, alpha=0.25)
    ax3.set_ylim([-0.1, 25])
    # ax3.legend(loc='upper left')

    # Legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles3, labels3 = ax3.get_legend_handles_labels()

    handles = handles1 + handles2 + handles3
    labels = labels1 + labels2 + labels3

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower left', bbox_to_anchor=(-0.05, -0.85),
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
    # Power market
    df_phi_pm = df_pm.set_index(['Year', 'Day', 'Run'])
    df_plot_pm = pd.DataFrame(data=np.nan, index=range(80),
                              columns=['Production gas turbines', 'General electricity demand',
                                       'Green hydrogen production', 'Curtailment renewables'])

    for i in range(80):
        # Gas turbine production
        tmp_gt = df_phi_pm.loc[i]['Electricity demand others'] - df_phi_pm.loc[i]['Actual production renewables']
        tmp_gt = tmp_gt.mask(tmp_gt < 0, 0)
        tmp_gt = tmp_gt.groupby(level=1).sum().median()

        # Electricity demand
        tmp_demand = df_phi_pm.loc[i]['Electricity demand others'].groupby(level=1).sum().median()

        # Green hydrogen production
        tmp_h2 = tmp_gt + df_phi_pm.loc[i]['Actual production renewables'].groupby(level=1).sum().median()

        # Curtailment
        tmp_curtail = tmp_gt + df_phi_pm.loc[i]['Maximum production renewables'].groupby(level=1).sum().median()

        # Normalize by the electricity demand
        df_plot_pm.loc[i, 'Production gas turbines'] = tmp_gt / tmp_demand
        df_plot_pm.loc[i, 'General electricity demand'] = tmp_demand / tmp_demand
        df_plot_pm.loc[i, 'Green hydrogen production'] = tmp_h2 / tmp_demand
        df_plot_pm.loc[i, 'Curtailment renewables'] = tmp_curtail / tmp_demand

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Electricity mix [-]')

    # ax1.plot(x, df_plot_pm['Production gas turbines'], linestyle='-', color=black)
    ax1.plot(x, df_plot_pm['General electricity demand'], label='General electricity demand', linestyle='-',
             color=black)
    # ax1.plot(x, df_plot_pm['Green hydrogen production'], linestyle='-', color=black)
    # ax1.plot(x, df_plot_pm['Curtailment renewables'], linestyle='-', color=black)

    ax1.fill_between(x, 0, df_plot_pm['Production gas turbines'], label='Production gas turbines', color=grey
                     , alpha=0.25)
    ax1.fill_between(x, df_plot_pm['Production gas turbines'], df_plot_pm['General electricity demand'],
                     label='Production renewables', color=green, alpha=0.25)
    ax1.fill_between(x, df_plot_pm['General electricity demand'], df_plot_pm['Green hydrogen production'],
                     label='Green hydrogen production', color=blue, alpha=0.25)
    ax1.fill_between(x, df_plot_pm['Green hydrogen production'], df_plot_pm['Curtailment renewables'],
                     label='Curtailment renewables', color=purple, alpha=0.25)

    plt.xlim(plot_settings['xlim'])
    plt.ylim(0)
    plt.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.3), ncol=3, frameon=False)
    plt.savefig(os.getcwd() + '\\plot_electricity_production.' + plot_type, bbox_inches='tight')


def plot_hydrogen_production(df_hm_yearly, df_hm_daily):
    '''
    Function that will create a plot of the actual and theoretical maximum hydrogen production.
    :param:
        pd.DataFrame df_hm_yearly: Yearly data from the hydrogen market
        pd.DataFrame df_hm_daily: Daily data from the hydrogen market
    :return:
    '''
    # Effiency electrolyzer
    eta = 0.7

    # Hydrogen market
    df_phi_day = df_hm_daily.set_index(['Year', 'Day', 'Run'])
    df_phi_year = df_hm_yearly.set_index(['Year', 'Run'])
    df_plot_hm = pd.DataFrame(data=np.nan, index=range(80), columns=['Hydrogen production',
                                                                     'Maximum hydrogen production'])
    for i in range(80):
        # Hydrogen production
        if i in df_phi_day.index.levels[0]:
            tmp_h2 = df_phi_day.loc[i]['Actual production electrolyzers'].groupby(level=1).sum().median()
            df_plot_hm.loc[i, 'Hydrogen production'] = tmp_h2

        # Max Production
        if i in df_phi_year.index.levels[0]:
            tmp_max = df_phi_year.loc[i]['Installed capacity Electrolyzers'].median() * 24 * 365 * eta
            df_plot_hm.loc[i, 'Maximum hydrogen production'] = tmp_max

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Hydrogen production [TWh]')
    ax1.fill_between(x, 4, 20, label='Needed Hydrogen in 2030', color=orange, alpha=0.25, hatch='///', edgecolor='None')
    ax1.fill_between(x, 250, 800, label='Needed Hydrogen in 2050', color=orange, alpha=0.25, hatch='...',
                     edgecolor='None')
    ax1.plot(x, df_plot_hm['Hydrogen production'] / 1e6, label='Hydrogen production', linestyle='-', color=blue)
    #ax1.plot(x, df_plot_hm['Maximum hydrogen production'] / 1e6, label='Maximum hydrogen production', linestyle='--',
    #         color=darkblue)

    ax1.fill_between(x, 0, df_plot_hm['Hydrogen production'] / 1e6, color=blue, alpha=0.25, edgecolor='none')
    #ax1.fill_between(x, df_plot_hm['Hydrogen production'] / 1e6, df_plot_hm['Maximum hydrogen production'] / 1e6,
    #                 color=darkblue, alpha=0.25, edgecolor='none')
    ax1.set_ylim([0, 15 * 33])

    ax2 = ax1.twinx()
    ax2.set_ylabel('Hydrogen production [Mio t./year]')
    ax2.plot(x, df_plot_hm['Hydrogen production'] / 33 / 1e6, label='Hydrogen production', linestyle='-', color=blue)
    #ax2.plot(x, df_plot_hm['Maximum hydrogen production'] / 0.33 / 1e6, label='Maximum hydrogen production',
    #         linestyle='--', color=darkblue)

    ax2.fill_between(x, 4 / 33 / 1e6, 20 / 33 / 1e6, color=orange, alpha=0.25, hatch='///', edgecolor='None')
    ax2.fill_between(x, 250 / 33 / 1e6, 800 / 33 / 1e6, color=orange, alpha=0.25, hatch='...',
                     edgecolor='None')

    ax2.set_ylim([0, 15])

    plt.xlim(plot_settings['xlim'])
    plt.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False, ncol=2)
    plt.savefig(os.getcwd() + '\\plot_hydrogen_production.' + plot_type, bbox_inches='tight')


def plot_utilization_elc(df_hm):
    '''
    Function that will create a plot of the utilization per year of the electrolyzers.
    :param:
        pd.DataFrame df_hm: Daily data from the hydrogen market
    :return:
    '''
    # Utilization
    df_phi = df_hm.set_index(['Year', 'Day', 'Run'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Mean', 'Median', '97.5%', '2.5%'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Utilization rate'].groupby(level=1).mean()
            df_plot.loc[i, 'Mean'] = tmp_df.mean()
            df_plot.loc[i, 'Median'] = tmp_df.median()
            df_plot.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Utilization rate [%]')
    # ax1.plot(x, df_plot['Mean']*100, label='Electrolyzers - Mean', linestyle='-', color=blue)
    ax1.plot(x, df_plot['Median'] * 100, label='Electrolyzers - Median', linestyle='-', color=blue)

    ax1.fill_between(x, df_plot['2.5%'] * 100, df_plot['97.5%'] * 100, color=blue, alpha=0.25, edgecolor='none')
    ax1.set_ylim(0, 100)
    ax1.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Full load hours [h]')
    # ax2.plot(x, df_plot['Mean']*8760, linestyle='-', color=blue)
    ax2.plot(x, df_plot['Median'] * 8760, linestyle='-', color=blue)
    ax2.set_ylim(0, 8760)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_utilization_elc.' + plot_type, bbox_inches='tight')


def plot_utilization_all(df_res, df_elc, df_ep):
    '''
    Function that will create a plot of the utilization per year of the renewables, electrolyzers and factories.
    :param:
        pd.DataFrame df_res: Yearly data from the renewables
        pd.DataFrame df_elc: Yearly data from the electrolyzers
        pd.DataFrame df_ep: Yearly data from the electrolyzer producers
    :return:
    '''
    df_phi_res = df_res.set_index(['Year', 'Run', 'ID'])
    df_phi_elc = df_elc.set_index(['Year', 'Run', 'ID'])
    df_phi_ep = df_ep.set_index(['Year', 'Run', 'ID'])

    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['RES - median', 'RES - 25%', 'RES - 75%',
                                                                  'ELC - median', 'ELC - 25%', 'ELC - 75%',
                                                                  'FAC - median', 'FAC - 25%', 'FAC - 75%'])

    for i in range(80):
        if i in df_phi_res.index.levels[0]:
            tmp_df = df_phi_res.loc[i]['Utilization rate'].groupby(level=1).max()
            df_plot.loc[i, 'RES - median'] = tmp_df.median()
            df_plot.loc[i, 'RES - 25%'] = tmp_df.quantile(q=0.25)
            df_plot.loc[i, 'RES - 75%'] = tmp_df.quantile(q=0.75)
        if i in df_phi_elc.index.levels[0]:
            tmp_df = df_phi_elc.loc[i]['Utilization rate'].groupby(level=1).max()
            df_plot.loc[i, 'ELC - median'] = tmp_df.median()
            df_plot.loc[i, 'ELC - 25%'] = tmp_df.quantile(q=0.25)
            df_plot.loc[i, 'ELC - 75%'] = tmp_df.quantile(q=0.75)
        if i in df_phi_ep.index.levels[0]:
            tmp_df = (df_phi_ep.loc[i]['Production'].groupby(level=0).sum() /
                      df_phi_ep.loc[i]['Installed capacity Manufacturings'].groupby(level=0).sum())
            df_plot.loc[i, 'FAC - median'] = tmp_df.median()
            df_plot.loc[i, 'FAC - 25%'] = tmp_df.quantile(q=0.25)
            df_plot.loc[i, 'FAC - 75%'] = tmp_df.quantile(q=0.75)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Utilization rate [%]')

    # Renewables
    ax1.plot(x, df_plot['RES - median'] * 100, label='Renewables', linestyle='-', color=green)
    ax1.fill_between(x, df_plot['RES - 25%'] * 100, df_plot['RES - 75%'] * 100, color=green, alpha=0.25,
                     edgecolor='none')

    # Electrolyzers
    ax1.plot(x, df_plot['ELC - median'] * 100, label='Electrolyzers', linestyle='-', color=blue)
    ax1.fill_between(x, df_plot['ELC - 75%'] * 100, df_plot['ELC - 25%'] * 100, color=blue, alpha=0.25,
                     edgecolor='none')

    # Manufacturings
    ax1.plot(x, df_plot['FAC - median'] * 100, label='Manufacturings', linestyle='-', color=purple)
    ax1.fill_between(x, df_plot['FAC - 25%'] * 100, df_plot['FAC - 75%'] * 100, color=purple, alpha=0.25,
                     edgecolor='none')

    ax1.set_ylim(0, 100)
    ax1.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False, ncol=3)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Full load hours [h]')
    ax2.set_ylim(0, 8760)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_utilization_all.' + plot_type, bbox_inches='tight')


def plot_utilization_elc_res(df_res, df_elc):
    '''
    Function that will create a plot of the utilization per year of the renewables, electrolyzers and factories.
    :param:
        pd.DataFrame df_res: Yearly data from the renewables
        pd.DataFrame df_elc: Yearly data from the electrolyzers
        pd.DataFrame df_ep: Yearly data from the electrolyzer producers
    :return:
    '''
    df_phi_res = df_res.set_index(['Year', 'Run', 'ID'])
    df_phi_elc = df_elc.set_index(['Year', 'Run', 'ID'])

    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['RES - median', 'RES - 25%', 'RES - 75%',
                                                                  'ELC - median', 'ELC - 25%', 'ELC - 75%',
                                                                  'FAC - median', 'FAC - 25%', 'FAC - 75%'])

    for i in range(80):
        if i in df_phi_res.index.levels[0]:
            tmp_df = df_phi_res.loc[i]['Utilization rate'].groupby(level=1).max()
            df_plot.loc[i, 'RES - median'] = tmp_df.median()
            df_plot.loc[i, 'RES - 25%'] = tmp_df.quantile(q=0.25)
            df_plot.loc[i, 'RES - 75%'] = tmp_df.quantile(q=0.75)
        if i in df_phi_elc.index.levels[0]:
            tmp_df = df_phi_elc.loc[i]['Utilization rate'].groupby(level=1).max()
            df_plot.loc[i, 'ELC - median'] = tmp_df.median()
            df_plot.loc[i, 'ELC - 25%'] = tmp_df.quantile(q=0.25)
            df_plot.loc[i, 'ELC - 75%'] = tmp_df.quantile(q=0.75)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Utilization rate [%]')

    # Renewables
    ax1.plot(x, df_plot['RES - median'] * 100, label='Renewables', linestyle='-', color=green)
    ax1.fill_between(x, df_plot['RES - 25%'] * 100, df_plot['RES - 75%'] * 100, color=green, alpha=0.25,
                     edgecolor='none')

    # Electrolyzers
    ax1.plot(x, df_plot['ELC - median'] * 100, label='Electrolyzers', linestyle='-', color=blue)
    ax1.fill_between(x, df_plot['ELC - 75%'] * 100, df_plot['ELC - 25%'] * 100, color=blue, alpha=0.25,
                     edgecolor='none')


    ax1.set_ylim(0, 100)
    ax1.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False, ncol=3)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Full load hours [h]')
    ax2.set_ylim(0, 8760)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_utilization_elc_res.' + plot_type, bbox_inches='tight')


def plot_duration_curves_res(df_pm_yearly, df_pm_daily, no_of_lines=5):
    '''
    Function that will create a plot of the duration curves of the renewables.
    :param:
        pd.DataFrame df_pm_yearly: Yearly data from the power market
        pd.DataFrame df_pm_daily: Daily data from the power market
        int no_of_lines: The number of years to plot (default 10)
    :return:
    '''
    # Yearly data
    df_phi_year = df_pm_yearly.set_index(['Year', 'Run'])

    # Daily data
    df_phi_day = df_pm_daily.set_index(['Year', 'Day', 'Run'])

    fig = plt.figure(figsize=plot_settings['figsize'], dpi=plot_settings['dpi'])
    ax1 = fig.add_subplot(111, projection='3d')

    for i in range(40):
        if i in df_phi_year.index.levels[0] and i in df_phi_day.index.levels[0] and i % round(40 / no_of_lines) == 0:
            day = list(range(0, 365))
            year = np.full_like(day, i + year0)
            tmp_df = (df_phi_day.loc[i]['Actual production renewables'] /
                      (df_phi_year.loc[i]['Installed capacity Renewables'] * 24) * 100)
            tmp_mean = tmp_df.groupby(level=0).median().sort_values(ascending=False).to_list()

            ax1.plot(day, year, tmp_mean, label=str('Year: ' + str(year[0])), color=green)

    ax1.set_xlabel('Day')
    ax1.set_ylabel('Year')
    ax1.set_zlabel('Utilization rate [%]')

    ax1.set_xlim(0, 365)
    ax1.set_ylim(2023, 2065)
    ax1.set_zlim(0, 100)

    plt.savefig(os.getcwd() + '\\plot_duration_curves_res.' + plot_type, bbox_inches='tight')


def plot_duration_curves_elc(df_hm, no_of_lines=5):
    '''
    Function that will create a plot of the duration curves of the electrolyzers.
    :param:
        pd.DataFrame df_hm: Daily data from the hydrogen market
        int no_of_lines: The number of years to plot (default 10)
    :return:
    '''
    # Electrolyzers
    df_phi = df_hm.set_index(['Year', 'Day', 'Run'])

    fig = plt.figure(figsize=plot_settings['figsize'], dpi=plot_settings['dpi'])
    ax1 = fig.add_subplot(111, projection='3d')

    for i in range(40):
        if i in df_phi.index.levels[0] and i % round(40 / no_of_lines) == 0:
            day = list(range(0, 365))
            year = np.full_like(day, i + year0)
            tmp_df = (df_phi.loc[i]['Utilization rate'] * 100)
            tmp_mean = tmp_df.groupby(level=0).median().sort_values(ascending=False).to_list()

            ax1.plot(day, year, tmp_mean, label=str('Year: ' + str(year[0])), color=blue)

    ax1.set_xlabel('Day')
    ax1.set_ylabel('Year')
    ax1.set_zlabel('Utilization rate [%]')

    ax1.set_xlim(0, 365)
    ax1.set_ylim(2023, 2065)
    ax1.set_zlim(0, 100)

    plt.savefig(os.getcwd() + '\\plot_duration_curves_elc.' + plot_type, bbox_inches='tight')


def plot_load_type_elc(df_pm, df_hm):
    '''
    Function that will create a plot of the load type of the electrolyzer.
    :param:
        pd.DataFrame df_pm: Yearly data from the power market
        pd.DataFrame df_hm: Yearly data from the hydrogen market
    :return:
    '''
    # Electrolyzers
    df_phi_pm = df_pm.set_index(['Year', 'Run'])
    df_phi_hm = df_hm.set_index(['Year', 'Run'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['No load', 'Partial load', 'Full load'])

    for i in range(80):
        if i in df_phi_pm.index.levels[0] and i in df_phi_hm.index.levels[0]:
            tmp_df = pd.DataFrame(
                data=[df_phi_pm.loc[i]['Cost share'], df_phi_hm.loc[i]['Installed capacity Electrolyzers']])
            y1 = pd.Series()
            y2 = pd.Series()
            y3 = pd.Series()
            for j in tmp_df.columns:
                if tmp_df[j]['Installed capacity Electrolyzers'] == 0:
                    tmp_df[j]['Cost share'] = '[1 0 0]'
                y1[j] = float(tmp_df[j]['Cost share'][1:-1].split(' ')[0]) * 100
                y2[j] = float(tmp_df[j]['Cost share'][1:-1].split(' ')[1]) * 100
                y3[j] = float(tmp_df[j]['Cost share'][1:-1].split(' ')[2]) * 100

            df_plot.loc[i, 'No load'] = y1.median()
            df_plot.loc[i, 'Partial load'] = y2.median()
            df_plot.loc[i, 'Full load'] = y3.median()

    cases = {
        'No load': df_plot['No load'],
        'Partial load': df_plot['Partial load'],
        'Full load': df_plot['Full load']
    }

    width = 0.5
    bottom = 0

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    for label, case in cases.items():
        if 'No load' in label:
            tmp_color = grey
        elif 'Partial load' in label:
            tmp_color = blue
        else:
            tmp_color = green

        ax1.bar(x, case, width, label=label, bottom=bottom, color=tmp_color)
        bottom += case

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Share [%]')

    plt.ylim(0, 100)
    plt.xlim(2023.5, 2065.5)
    plt.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), ncol=3, frameon=False)
    plt.savefig(os.getcwd() + '\\plot_load_type_elc.' + plot_type, bbox_inches='tight')


def plot_p_elc_vs_lcoe(df_pm):
    '''
    Function that will create a plot of the price for electricity and the lcoe.
    :param:
        pd.DataFrame df_pm: Yearly data from the power market
    :return:
    '''
    df_phi = df_pm.set_index(['Year', 'Run'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Price - Mean', 'Price - Median', 'Price - 95%',
                                                                  'Price - 5%', 'LCOE - Mean', 'LCOE - Median',
                                                                  'LCOE - 95%', 'LCOE - 5%'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_p = df_phi.loc[i]['Weighted Price Electricity']
            tmp_lcoe = df_phi.loc[i]['LCOE']
            df_plot.loc[i, 'Price - Mean'] = tmp_p.mean()
            df_plot.loc[i, 'Price - Median'] = tmp_p.median()
            df_plot.loc[i, 'Price - 95%'] = tmp_p.quantile(q=0.75)
            df_plot.loc[i, 'Price - 5%'] = tmp_p.quantile(q=0.25)
            df_plot.loc[i, 'LCOE - Mean'] = tmp_lcoe.mean()
            df_plot.loc[i, 'LCOE - Median'] = tmp_lcoe.median()
            df_plot.loc[i, 'LCOE - 95%'] = tmp_lcoe.quantile(q=0.75)
            df_plot.loc[i, 'LCOE - 5%'] = tmp_lcoe.quantile(q=0.25)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Costs [€/MWh]')
    # ax1.plot(x, df_plot['Price - Mean'], label='Weighted price electricity', linestyle='-', color=black)
    ax1.plot(x, df_plot['Price - Median'], label='Weighted price electricity', linestyle='-', color=green)
    # ax1.plot(x, df_plot['LCOE - Mean'], label='Levelized costs of renewable electricity', linestyle='--', color=black)
    ax1.plot(x, df_plot['LCOE - Median'], label='Levelized costs of renewable electricity', linestyle='-.', color=green)

    ax1.fill_between(x, df_plot['Price - 5%'], df_plot['Price - 95%'], color=green, alpha=0.25, edgecolor='none')
    ax1.fill_between(x, df_plot['LCOE - 5%'], df_plot['LCOE - 95%'], color=green, hatch='/', alpha=0.25,
                     edgecolor='none')

    plt.xlim(plot_settings['xlim'])
    plt.ylim(0)
    plt.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False, ncol=2)
    plt.savefig(os.getcwd() + '\\plot_p_elc_vs_lcoe.' + plot_type, bbox_inches='tight')


def plot_p_h2_vs_lcoh(df_hm):
    '''
    Function that will create a plot of the price of hydrogen and the lcoh.
    :param:
        pd.DataFrame df_hm: Yearly data from the hydrogen market
    :return:
    '''
    df_phi = df_hm.set_index(['Year', 'Run'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Price - Mean', 'Price - Median', 'Price - 95%',
                                                                  'Price - 5%', 'LCOH - Mean', 'LCOH - Median',
                                                                  'LCOH - 95%', 'LCOH - 5%'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_p = df_phi.loc[i]['Price Hydrogen'].replace(1e10, np.nan)
            tmp_lcoe = df_phi.loc[i]['LCOH'].replace(1e10, np.nan)
            df_plot.loc[i, 'Price - Mean'] = tmp_p.mean()
            df_plot.loc[i, 'Price - Median'] = tmp_p.median()
            df_plot.loc[i, 'Price - 95%'] = tmp_p.quantile(q=0.75)
            df_plot.loc[i, 'Price - 5%'] = tmp_p.quantile(q=0.25)
            df_plot.loc[i, 'LCOH - Mean'] = tmp_lcoe.mean()
            df_plot.loc[i, 'LCOH - Median'] = tmp_lcoe.median()
            df_plot.loc[i, 'LCOH - 95%'] = tmp_lcoe.quantile(q=0.75)
            df_plot.loc[i, 'LCOH - 5%'] = tmp_lcoe.quantile(q=0.25)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Costs [€/MWh]')
    # ax1.set_yscale('log')
    # ax1.plot(x, df_plot['Price - Mean'], label='Price hydrogen', linestyle='-', color=blue)
    ax1.plot(x, df_plot['Price - Median'], label='Price hydrogen', linestyle='-', color=blue)
    # ax1.plot(x, df_plot['LCOH - Mean'], label='Levelized costs of hydrogen', linestyle='--', color=blue)
    ax1.plot(x, df_plot['LCOH - Median'], label='Levelized costs of hydrogen', linestyle='-.', color=blue)

    ax1.fill_between(x, df_plot['Price - 5%'], df_plot['Price - 95%'], color=blue, alpha=0.25, edgecolor='none')
    ax1.fill_between(x, df_plot['LCOH - 5%'], df_plot['LCOH - 95%'], color=blue, hatch='/', alpha=0.25,
                     edgecolor='none')

    ax1.set_ylim(0)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Costs [€/kg]')
    # ax2.set_yscale('log')
    # ax2.plot(x, df_plot['Price - Mean'] * 0.039, label='Price hydrogen', linestyle='-', color=blue)
    ax2.plot(x, df_plot['Price - Median'] * 0.039, label='Price hydrogen', linestyle='-', color=blue)
    # ax2.plot(x, df_plot['LCOH - Mean'] * 0.039, label='Levelized costs of hydrogen', linestyle='--', color=blue)
    ax2.plot(x, df_plot['LCOH - Median'] * 0.039, label='Levelized costs of hydrogen', linestyle='-.', color=blue)

    ax2.fill_between(x, df_plot['Price - 5%'] * 0.039, df_plot['Price - 95%'] * 0.039, color=blue, alpha=0.25,
                     edgecolor='none')
    ax2.fill_between(x, df_plot['LCOH - 5%'] * 0.039, df_plot['LCOH - 95%'] * 0.039, color=blue, hatch='/', alpha=0.25,
                     edgecolor='none')

    ax2.set_ylim(0)

    plt.xlim(plot_settings['xlim'])
    plt.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False, ncol=2)
    plt.savefig(os.getcwd() + '\\plot_p_h2_vs_lcoh.' + plot_type, bbox_inches='tight')


def plot_p_elc_vs_p_h2(df_pm, df_hm):
    '''
    Function that will create a plot of the price of hydrogen and the weighted price for electricity.
    :param:
        pd.DataFrame df_pm: Yearly data from the power market
        pd.DataFrame df_hm: Yearly data from the hydrogen market
    :return:
    '''
    df_phi_pm = df_pm.set_index(['Year', 'Run'])
    df_phi_hm = df_hm.set_index(['Year', 'Run'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Price elc - Median', 'Price elc - 25%',
                                                                  'Price elc - 75%', 'Price h2 - Median',
                                                                  'Price h2 - 25%', 'Price h2 - 75%'])

    for i in range(80):
        if i in df_phi_pm.index.levels[0]:
            tmp_p = df_phi_pm.loc[i]['Weighted Price Electricity']
            df_plot.loc[i, 'Price elc - Median'] = tmp_p.median()
            df_plot.loc[i, 'Price elc - 75%'] = tmp_p.quantile(q=0.75)
            df_plot.loc[i, 'Price elc - 25%'] = tmp_p.quantile(q=0.25)
        if i in df_phi_hm.index.levels[0]:
            tmp_p = df_phi_hm.loc[i]['Price Hydrogen']
            df_plot.loc[i, 'Price h2 - Median'] = tmp_p.median()
            df_plot.loc[i, 'Price h2 - 75%'] = tmp_p.quantile(q=0.75)
            df_plot.loc[i, 'Price h2 - 25%'] = tmp_p.quantile(q=0.25)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Price [€/MWh]')
    ax1.plot(x, df_plot['Price elc - Median'], label='Weighted price electricity', linestyle='-', color=green)
    ax1.plot(x, df_plot['Price h2 - Median'], label='Price hydrogen', linestyle='-', color=blue)

    ax1.fill_between(x, df_plot['Price elc - 25%'], df_plot['Price elc - 75%'], color=green, alpha=0.25,
                     edgecolor='none')
    ax1.fill_between(x, df_plot['Price h2 - 25%'], df_plot['Price h2 - 75%'], color=blue, alpha=0.25, edgecolor='none')

    plt.xlim(plot_settings['xlim'])
    plt.ylim(0)
    plt.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False, ncol=2)
    plt.savefig(os.getcwd() + '\\plot_p_elc_vs_p_h2.' + plot_type, bbox_inches='tight')


def plot_p_elc(df_pm):
    '''
    Function that will create a plot of the price of hydrogen and the weighted price for electricity.
    :param:
        pd.DataFrame df_pm: Yearly data from the power market
        pd.DataFrame df_hm: Yearly data from the hydrogen market
    :return:
    '''
    df_phi_pm = df_pm.set_index(['Year', 'Run'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Price elc - Median', 'Price elc - 25%',
                                                                  'Price elc - 75%'])

    for i in range(80):
        if i in df_phi_pm.index.levels[0]:
            tmp_p = df_phi_pm.loc[i]['Weighted Price Electricity']
            df_plot.loc[i, 'Price elc - Median'] = tmp_p.median()
            df_plot.loc[i, 'Price elc - 75%'] = tmp_p.quantile(q=0.75)
            df_plot.loc[i, 'Price elc - 25%'] = tmp_p.quantile(q=0.25)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Price [€/MWh]')
    ax1.plot(x, df_plot['Price elc - Median'], label='Weighted price electricity', linestyle='-', color=green)

    ax1.fill_between(x, df_plot['Price elc - 25%'], df_plot['Price elc - 75%'], color=green, alpha=0.25,
                     edgecolor='none')

    plt.xlim(plot_settings['xlim'])
    plt.ylim(0)
    plt.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False, ncol=2)
    plt.savefig(os.getcwd() + '\\plot_p_elc.' + plot_type, bbox_inches='tight')


def plot_p_h2(df_hm):
    '''
    Function that will create a plot of the price of hydrogen and the weighted price for electricity.
    :param:
        pd.DataFrame df_pm: Yearly data from the power market
        pd.DataFrame df_hm: Yearly data from the hydrogen market
    :return:
    '''
    df_phi_hm = df_hm.set_index(['Year', 'Run'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Price h2 - Median',
                                                                  'Price h2 - 25%', 'Price h2 - 75%'])

    for i in range(80):
        if i in df_phi_hm.index.levels[0]:
            tmp_p = df_phi_hm.loc[i]['Price Hydrogen']
            df_plot.loc[i, 'Price h2 - Median'] = tmp_p.median()
            df_plot.loc[i, 'Price h2 - 75%'] = tmp_p.quantile(q=0.75)
            df_plot.loc[i, 'Price h2 - 25%'] = tmp_p.quantile(q=0.25)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Price [€/MWh]')
    ax1.plot(x, df_plot['Price h2 - Median'], label='Price hydrogen', linestyle='-', color=blue)

    ax1.fill_between(x, df_plot['Price h2 - 25%'], df_plot['Price h2 - 75%'], color=blue, alpha=0.25, edgecolor='none')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Price [€/kg]')
    ax2.plot(x, df_plot['Price h2 - Median']/33.3, label='Price hydrogen', linestyle='-', color=blue)

    ax2.fill_between(x, df_plot['Price h2 - 25%']/33.3, df_plot['Price h2 - 75%']/33.3, color=blue, alpha=0.25,
                     edgecolor='none')

    plt.xlim(plot_settings['xlim'])

    ax1.set_ylim([0, 275])
    ax2.set_ylim([0, 275/33.3])
    plt.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False, ncol=2)
    plt.savefig(os.getcwd() + '\\plot_p_h2.' + plot_type, bbox_inches='tight')

def plot_p_elc_ave_vs_lcoe_ave(df_ep, df_sale):
    '''
    Function that will create a plot of the price for electorlyzer and the lcoe
    :param:
        pd.DataFrame df_ep: Yearly data from the electrolyzer producers
        pd.DataFrame df_sale: Yearly data from the electrolyzers' sale
    :return:
    '''
    df_plot = pd.DataFrame(data=np.nan, index=range(80),
                           columns=['Price electrolyzers - Mean', 'Price electrolyzers - Median',
                                    'Price electrolyzers - 95%', 'Price electrolyzers - 5%', 'LCOE - Mean',
                                    'LCOE - Median', 'LCOE - 95%', 'LCOE - 5%'])
    df_phi_ep = df_ep.set_index(['Year', 'Run', 'ID'])
    df_phi_sale = df_sale.set_index(['Year', 'Run', 'EP ID'])

    for i in range(80):
        if i in df_phi_sale.index.levels[0]:
            tmp_df = df_phi_sale.loc[i]['Price'].groupby(level=0).mean()
            df_plot.loc[i, 'Price electrolyzers - Mean'] = tmp_df.mean()
            df_plot.loc[i, 'Price electrolyzers - Median'] = tmp_df.median()
            df_plot.loc[i, 'Price electrolyzers - 95%'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, 'Price electrolyzers - 5%'] = tmp_df.quantile(q=0.25)
            tmp_df = df_phi_ep.loc[i]['LCOE'].replace(1e10, np.nan).groupby(level=0).mean()
            df_plot.loc[i, 'LCOE - Mean'] = tmp_df.mean()
            df_plot.loc[i, 'LCOE - Median'] = tmp_df.median()
            df_plot.loc[i, 'LCOE - 95%'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, 'LCOE - 5%'] = tmp_df.quantile(q=0.25)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Costs [Mio. €/MW]')
    # ax1.plot(x, df_plot['Price electrolyzers - Mean']/1e6, label='Price electrolyzer', linestyle='-', color=green)
    ax1.plot(x, df_plot['Price electrolyzers - Mean'] / 1e6, label='Price electrolyzer - Mean', linestyle='-',
             color=purple)
    # ax1.plot(x, df_plot['LCOE - Mean']/1e6, label='LCOE', linestyle='--', color=green)
    ax1.plot(x, df_plot['LCOE - Mean'] / 1e6, label='LCOE', linestyle='-.', color=purple)

    ax1.fill_between(x, df_plot['Price electrolyzers - 5%'] / 1e6, df_plot['Price electrolyzers - 95%'] / 1e6,
                     color=purple,
                     alpha=0.25, edgecolor='none')
    ax1.fill_between(x, df_plot['LCOE - 5%'] / 1e6, df_plot['LCOE - 95%'] / 1e6, color=purple, hatch='/', alpha=0.25,
                     edgecolor='none')

    ax1.set_ylim(0)
    ax1.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False, ncol=2)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Costs [€/kW]')
    ax2.plot(x, df_plot['Price electrolyzers - Mean'] / 1e3, linestyle='-', color=purple)
    ax2.fill_between(x, df_plot['Price electrolyzers - 5%'] / 1e3, df_plot['Price electrolyzers - 95%'] / 1e3,
                     color=purple, alpha=0.25, edgecolor='none')
    # ax1.plot(x, df_plot['LCOE - Mean']/1e6, label='LCOE', linestyle='--', color=green)
    ax2.plot(x, df_plot['LCOE - Median'] / 1e3, label='LCOE', linestyle='-.', color=purple)

    ax2.fill_between(x, df_plot['Price electrolyzers - 5%'] / 1e3, df_plot['Price electrolyzers - 95%'] / 1e3,
                     color=purple,
                     alpha=0.25, edgecolor='none')
    ax2.fill_between(x, df_plot['LCOE - 5%'] / 1e3, df_plot['LCOE - 95%'] / 1e3, color=purple, hatch='/', alpha=0.25,
                     edgecolor='none')
    ax2.set_ylim(0)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_p_elc_ave_vs_lcoe.' + plot_type, bbox_inches='tight')


def plot_p_elc_vs_c_elc(df_sale):
    '''
    Function that will create a plot of the average ratio of price and costs for electrolyzers
    :param:
        pd.DataFrame df_sale: Yearly data from the electrolyzers' sales
    :return:
    '''
    df_phi = df_sale.set_index(['Year', 'Run', 'EP ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Electrolyzers - Mean', 'Electrolyzers - Median',
                                                                  'Electrolyzers - Weighted average',
                                                                  'Electrolyzers - 95%', 'Electrolyzers - 5%'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Price'] / df_phi.loc[i]['Production costs']
            tmp_df = tmp_df.groupby(level=0).mean()
            df_plot.loc[i, 'Electrolyzers - Mean'] = tmp_df.mean()
            df_plot.loc[i, 'Electrolyzers - Median'] = tmp_df.median()
            df_plot.loc[i, 'Electrolyzers - 95%'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, 'Electrolyzers - 5%'] = tmp_df.quantile(q=0.25)
            tmp_df1 = df_phi.loc[i]['Production costs'] * df_phi.loc[i]['Capacity']
            tmp_df2 = df_phi.loc[i]['Price'] * df_phi.loc[i]['Capacity']
            tmp_df = tmp_df2.groupby(level=0).sum() / tmp_df1.groupby(level=0).sum()
            df_plot.loc[i, 'Electrolyzers - Weighted average'] = tmp_df.mean()

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Ratio Price/Costs [-]')
    # ax1.plot(x, df_plot['Electrolyzers - Mean'], label='Electrolyzers', linestyle='-', color=green)
    ax1.plot(x, df_plot['Electrolyzers - Median'], label='Electorlyzers', linestyle='-', color=purple)
    # ax1.plot(x, df_plot['Electrolyzers - Weighted average'], label='Electrolyzers', linestyle='-.', color=green)

    ax1.fill_between(x, df_plot['Electrolyzers - 5%'], df_plot['Electrolyzers - 95%'], color=purple, alpha=0.25,
                     edgecolor='none')
    ax1.set_ylim(1)
    ax1.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False, ncol=2)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_p_elc_vs_c_elc.' + plot_type, bbox_inches='tight')


def plot_investment_threshold_pp(df_pp, df_pm):
    '''
    Function that will create a plot of the average investment threshold of the Power Producers.
    :param:
        pd.DataFrame df_pp: Yearly data of the Power Producers.
        pd.DataFrame df_pm: Yearly data of the Power market
    :return:
    '''
    df_phi = df_pp.set_index(['Year', 'Run', 'ID'])
    df_phi_pm = df_pp.set_index(['Year', 'Run'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Mean', 'Median', '97.5%', '2.5%', 'Global'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Investment threshold'].groupby(level=0).mean()
            df_plot.loc[i, 'Mean'] = tmp_df.mean()
            df_plot.loc[i, 'Median'] = tmp_df.median()
            df_plot.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)
        if i in df_phi_pm.index.levels[0]:
            tmp_df = 0
            df_plot.loc[i, 'Global'] = tmp_df

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_ylabel('Investment threshold [-]')
    ax1.set_xlabel('Year')
    # ax1.plot(x, df_plot['Mean'], label='Power producers', linestyle='-', color=black)
    ax1.plot(x, df_plot['Global'], label='Global minimal investment threshold', linestyle='-', color=black)
    ax1.plot(x, df_plot['Median'], label='Power producers', linestyle='-', color=green)

    ax1.fill_between(x, df_plot['2.5%'], df_plot['97.5%'], color=green, alpha=0.25, edgecolor='none')
    ax1.set_ylim(-1)
    ax1.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False, ncol=2)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_investment_threshold_pp.' + plot_type, bbox_inches='tight')


def plot_investment_threshold_hp(df_hp, df_hm):
    '''
    Function that will create a plot of the average investment threshold of the Hydrogen Producers.
    :param:
        pd.DataFrame df_pp: Yearly data of the Hydrogen Producers.
        pd.DataFrame df_pm: Yearly data of the Hydrogen market.
    :return:
    '''
    df_phi = df_hp.set_index(['Year', 'Run', 'ID'])
    df_phi_hm = df_hm.set_index(['Year', 'Run'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Mean', 'Median', '97.5%', '2.5%', 'Global'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Investment threshold'].groupby(level=0).mean()
            df_plot.loc[i, 'Mean'] = tmp_df.mean()
            df_plot.loc[i, 'Median'] = tmp_df.median()
            df_plot.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)
        if i in df_phi_hm.index.levels[0]:
            tmp_df = df_phi_hm.loc[i]['Global investment threshold']
            df_plot.loc[i, 'Global'] = tmp_df.median()

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_ylabel('Investment threshold [-]')
    ax1.set_xlabel('Year')
    # ax1.plot(x, df_plot['Mean'], label='Hydrogen producers', linestyle='-', color=blue)
    ax1.plot(x, df_plot['Median'], label='Hydrogen producers', linestyle='-', color=blue)
    ax1.plot(x, df_plot['Global'], label='Global minimal investment threshold', linestyle='-', color=black)

    ax1.fill_between(x, df_plot['2.5%'], df_plot['97.5%'], color=blue, alpha=0.25, edgecolor='none')
    ax1.set_ylim(-1)
    ax1.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False, ncol=2)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_investment_threshold_hp.' + plot_type, bbox_inches='tight')


def plot_investment_threshold_ep(df_ep, df_em):
    '''
    Function that will create a plot of the average investment threshold of the Electrolyzer Producers.
    :param:
        pd.DataFrame df_pp: Yearly data of the Electrolyzer Producers.
        pd.DataFrame df_pm: Yearly data of the Electrolyzer market
    :return:
    '''
    df_phi = df_ep.set_index(['Year', 'Run', 'ID'])
    df_phi_em = df_em.set_index(['Year', 'Run'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Mean', 'Median', '97.5%', '2.5%', 'Global'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Investment threshold'].groupby(level=0).mean()
            df_plot.loc[i, 'Mean'] = tmp_df.mean()
            df_plot.loc[i, 'Median'] = tmp_df.median()
            df_plot.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)
        if i in df_phi_em.index.levels[0]:
            tmp_df = df_phi_em.loc[i]['Global investment threshold']
            df_plot.loc[i, 'Global'] = tmp_df.median()

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_ylabel('Investment threshold [-]')
    ax1.set_xlabel('Year')
    # ax1.plot(x, df_plot['Mean'], label='Electrolyzer producers', linestyle='-', color=green)
    ax1.plot(x, df_plot['Median'], label='Electrolyzer producers', linestyle='-', color=purple)
    ax1.plot(x, df_plot['Global'], label='Global mimial investment threshold', linestyle='-', color=black)

    ax1.fill_between(x, df_plot['2.5%'], df_plot['97.5%'], color=purple, alpha=0.25, edgecolor='none')
    ax1.set_ylim(-1)
    ax1.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False, ncol=2)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_investment_threshold_ep.' + plot_type, bbox_inches='tight')


def plot_weighted_investment_threshold_pp(df_pp, df_pm):
    '''
    Function that will create a plot of the capacity weighted investment threshold of the power producers.
    :param:
        pd.DataFrame df_pp: Yearly data of the power producers
        pd.DataFrame df_pm: Yearly data of the power market
    :return:
    '''
    df_phi = df_pp.set_index(['Year', 'Run', 'ID'])
    df_phi_pm = df_pm.set_index(['Year', 'Run'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Mean', 'Median', '97.5%', '2.5%', 'Global'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Investment threshold'] * df_phi.loc[i]['Installed capacity Renewables']
            tmp_df = tmp_df.groupby(level=0).sum() / df_phi.loc[i]['Installed capacity Renewables'].groupby(
                level=0).sum()
            df_plot.loc[i, 'Mean'] = tmp_df.mean()
            df_plot.loc[i, 'Median'] = tmp_df.median()
            df_plot.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)
        if i in df_phi_pm.index.levels[0]:
            tmp_df = 0
            df_plot.loc[i, 'Global'] = tmp_df

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_ylabel('Investment threshold [-]')
    ax1.set_xlabel('Year')
    # ax1.plot(x, df_plot['Mean'], label='Power producers', linestyle='-', color=black)
    ax1.plot(x, df_plot['Global'], label='Global mimial investment threshold', linestyle='-', color=black)
    ax1.plot(x, df_plot['Median'], label='Power producers', linestyle='-', color=green)

    ax1.fill_between(x, df_plot['2.5%'], df_plot['97.5%'], color=green, alpha=0.25, edgecolor='none')
    ax1.set_ylim(-1)
    ax1.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False, ncol=2)
    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_weighted_investment_threshold_pp.' + plot_type, bbox_inches='tight')


def plot_weighted_investment_threshold_hp(df_hp, df_hm):
    '''
    Function that will create a plot of the capacity weighted investment threshold of the hydrogen producers.
    :param:
        pd.DataFrame df_hp: Yearly data of the hydrogen producers
        pd.DataFrame df_pm: Yearly data of the hydrogen market
    :return:
    '''
    df_phi = df_hp.set_index(['Year', 'Run', 'ID'])
    df_phi_hm = df_hm.set_index(['Year', 'Run'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Mean', 'Median', '97.5%', '2.5%', 'Global'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Investment threshold'] * df_phi.loc[i]['Installed capacity Electrolyzers']
            tmp_df = tmp_df.groupby(level=0).sum() / df_phi.loc[i]['Installed capacity Electrolyzers'].groupby(
                level=0).sum()
            df_plot.loc[i, 'Mean'] = tmp_df.mean()
            df_plot.loc[i, 'Median'] = tmp_df.median()
            df_plot.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)
        if i in df_phi_hm.index.levels[0]:
            tmp_df = df_phi_hm.loc[i]['Global investment threshold']
            df_plot.loc[i, 'Global'] = tmp_df.median()

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_ylabel('Investment threshold [-]')
    ax1.set_xlabel('Year')
    # ax1.plot(x, df_plot['Mean'], label='Hydrogen producers', linestyle='-', color=blue)
    ax1.plot(x, df_plot['Median'], label='Hydrogen producers', linestyle='-', color=blue)
    ax1.plot(x, df_plot['Global'], label='Global mimial investment threshold', linestyle='-', color=black)

    ax1.fill_between(x, df_plot['2.5%'], df_plot['97.5%'], color=blue, alpha=0.25, edgecolor='none')
    ax1.set_ylim(-1)
    ax1.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False, ncol=2)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_weighted_investment_threshold_hp.' + plot_type, bbox_inches='tight')


def plot_weighted_investment_threshold_ep(df_ep, df_em):
    '''
    Function that will create a plot of the capacity weighted investment threshold of the electrolyzers producers.
    :param:
        pd.DataFrame df_ep: Yearly data of the electrolyzers producers
        pd.DataFrame df_pm: Yearly data of the electrolyzer market
    :return:
    '''
    df_phi = df_ep.set_index(['Year', 'Run', 'ID'])
    df_phi_em = df_em.set_index(['Year', 'Run'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Mean', 'Median', '97.5%', '2.5%', 'Global'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Investment threshold'] * df_phi.loc[i]['Installed capacity Manufacturings']
            tmp_df = tmp_df.groupby(level=0).sum() / df_phi.loc[i]['Installed capacity Manufacturings'].groupby(
                level=0).sum()
            df_plot.loc[i, 'Mean'] = tmp_df.mean()
            df_plot.loc[i, 'Median'] = tmp_df.median()
            df_plot.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)
        if i in df_phi_em.index.levels[0]:
            tmp_df = df_phi_em.loc[i]['Global investment threshold']
            df_plot.loc[i, 'Global'] = tmp_df.median()

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_ylabel('Investment threshold [-]')
    ax1.set_xlabel('Year')
    # ax1.plot(x, df_plot['Mean'], label='Electrolyzer producers', linestyle='-', color=green)
    ax1.plot(x, df_plot['Median'], label='Electrolyzer producers', linestyle='-', color=purple)
    ax1.plot(x, df_plot['Global'], label='Global mimial investment threshold', linestyle='-', color=black)

    ax1.fill_between(x, df_plot['2.5%'], df_plot['97.5%'], color=purple, alpha=0.25, edgecolor='none')
    ax1.set_ylim(-1)
    ax1.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False, ncol=2)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_weighted_investment_threshold_ep.' + plot_type, bbox_inches='tight')


def plot_age_res(df_res):
    '''
    Function that will create a plot of the average age of the renewables.
    :param:
        pd.DataFrame df_res: Yearly data of the renewables
    :return:
    '''
    df_phi = df_res.set_index(['Year', 'Run', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Mean', 'Median', '97.5%', '2.5%'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Age'].groupby(level=0).mean()
            df_plot.loc[i, 'Mean'] = tmp_df.mean()
            df_plot.loc[i, 'Median'] = tmp_df.median()
            df_plot.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_ylabel('Age [years]')
    ax1.set_xlabel('Year')
    # ax1.plot(x, df_plot['Mean'], label='Renewables', linestyle='-', color=black)
    ax1.plot(x, df_plot['Median'], label='Renewables', linestyle='-', color=green)

    ax1.fill_between(x, df_plot['2.5%'], df_plot['97.5%'], color=green, alpha=0.25, edgecolor='none')
    ax1.set_ylim(0)
    ax1.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_age_res.' + plot_type, bbox_inches='tight')


def plot_age_elc(df_elc):
    '''
    Function that will create a plot of the average age of the electrolyzers.
    :param:
        pd.DataFrame df_elc: Yearly data of the electrolyzers
    :return:
    '''
    df_phi = df_elc.set_index(['Year', 'Run', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Mean', 'Median', '97.5%', '2.5%'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Age'].groupby(level=0).mean()
            df_plot.loc[i, 'Mean'] = tmp_df.mean()
            df_plot.loc[i, 'Median'] = tmp_df.median()
            df_plot.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_ylabel('Age [years]')
    ax1.set_xlabel('Year')
    # ax1.plot(x, df_plot['Mean'], label='Electrolyzers', linestyle='-', color=blue)
    ax1.plot(x, df_plot['Median'], label='Electrolyzers', linestyle='-', color=blue)

    ax1.fill_between(x, df_plot['2.5%'], df_plot['97.5%'], color=blue, alpha=0.25, edgecolor='none')
    ax1.set_ylim(0)
    ax1.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_age_elc.' + plot_type, bbox_inches='tight')


def plot_age_man(df_man):
    '''
    Function that will create a plot of the average age of the factories for electrolyzers.
    :param:
        pd.DataFrame df_elc: Yearly data of the factories for electrolyzers
    :return:
    '''
    df_phi = df_man.set_index(['Year', 'Run', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Mean', 'Median', '97.5%', '2.5%'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Age'].groupby(level=0).mean()
            df_plot.loc[i, 'Mean'] = tmp_df.mean()
            df_plot.loc[i, 'Median'] = tmp_df.median()
            df_plot.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_ylabel('Age [years]')
    ax1.set_xlabel('Year')
    # ax1.plot(x, df_plot['Mean'], label='Factories', linestyle='-', color=green)
    ax1.plot(x, df_plot['Median'], label='Factories', linestyle='-', color=purple)

    ax1.fill_between(x, df_plot['2.5%'], df_plot['97.5%'], color=purple, alpha=0.25, edgecolor='none')
    ax1.set_ylim(0)
    ax1.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_age_man.' + plot_type, bbox_inches='tight')


def plot_weighted_age_res(df_res):
    '''
    Function that will create a plot of the capacity weighted average age of the renewables.
    :param:
        pd.DataFrame df_res: Yearly data of the renewables
    :return:
    '''
    df_phi = df_res.set_index(['Year', 'Run', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Mean', 'Median', '97.5%', '2.5%'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Age'] * df_phi.loc[i]['Capacity']
            tmp_df = tmp_df.groupby(level=0).sum() / df_phi.loc[i]['Capacity'].groupby(level=0).sum()
            df_plot.loc[i, 'Mean'] = tmp_df.mean()
            df_plot.loc[i, 'Median'] = tmp_df.median()
            df_plot.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_ylabel('Age [years]')
    ax1.set_xlabel('Year')
    # ax1.plot(x, df_plot['Mean'], label='Renewables', linestyle='-', color=black)
    ax1.plot(x, df_plot['Median'], label='Renewables', linestyle='-', color=green)

    ax1.fill_between(x, df_plot['2.5%'], df_plot['97.5%'], color=green, alpha=0.25, edgecolor='none')
    ax1.set_ylim(0)
    ax1.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_weighted_age_res.' + plot_type, bbox_inches='tight')


def plot_weighted_age_elc(df_elc):
    '''
    Function that will create a plot of the capacity weighted average age of the electrolyzers.
    :param:
        pd.DataFrame df_elc: Yearly data of the electrolyzers
    :return:
    '''
    df_phi = df_elc.set_index(['Year', 'Run', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Mean', 'Median', '97.5%', '2.5%'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Age'] * df_phi.loc[i]['Capacity']
            tmp_df = tmp_df.groupby(level=0).sum() / df_phi.loc[i]['Capacity'].groupby(level=0).sum()
            df_plot.loc[i, 'Mean'] = tmp_df.mean()
            df_plot.loc[i, 'Median'] = tmp_df.median()
            df_plot.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_ylabel('Age [years]')
    ax1.set_xlabel('Year')
    # ax1.plot(x, df_plot['Mean'], label='Electrolyzers', linestyle='-', color=blue)
    ax1.plot(x, df_plot['Median'], label='Electrolyzers', linestyle='-', color=blue)

    ax1.fill_between(x, df_plot['2.5%'], df_plot['97.5%'], color=blue, alpha=0.25, edgecolor='none')
    ax1.set_ylim(0)
    ax1.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_weighted_age_elc.' + plot_type, bbox_inches='tight')


def plot_weighted_age_man(df_man):
    '''
    Function that will create a plot of the capacity weighted average age of the factories for electorlyzers.
    :param:
        pd.DataFrame df_res: Yearly data of the factories for electrolyzers
    :return:
    '''
    df_phi = df_man.set_index(['Year', 'Run', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['Mean', 'Median', '97.5%', '2.5%'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Age'] * df_phi.loc[i]['Capacity']
            tmp_df = tmp_df.groupby(level=0).sum() / df_phi.loc[i]['Capacity'].groupby(level=0).sum()
            df_plot.loc[i, 'Mean'] = tmp_df.mean()
            df_plot.loc[i, 'Median'] = tmp_df.median()
            df_plot.loc[i, '97.5%'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, '2.5%'] = tmp_df.quantile(q=0.25)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_ylabel('Age [years]')
    ax1.set_xlabel('Year')
    # ax1.plot(x, df_plot['Mean'], label='Factories', linestyle='-', color=green)
    ax1.plot(x, df_plot['Median'], label='Factories', linestyle='-', color=purple)

    ax1.fill_between(x, df_plot['2.5%'], df_plot['97.5%'], color=purple, alpha=0.25, edgecolor='none')
    ax1.set_ylim(0)
    ax1.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False)

    plt.xlim(plot_settings['xlim'])
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
    df_phi_pp = df_pp.set_index(['Year', 'Run', 'ID'])
    df_phi_hp = df_hp.set_index(['Year', 'Run', 'ID'])
    df_phi_ep = df_ep.set_index(['Year', 'Run', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80),
                           columns=['Mean - Power producers', 'Median - Power producers', '97.5% - Power producers',
                                    '2.5% - Power producers', 'Mean - Hydrogen producers',
                                    'Median - Hydrogen producers',
                                    '97.5% - Hydrogen producers', '2.5% - Hydrogen producers',
                                    'Mean - Electrolyzer producers', 'Median - Electrolyzer producers',
                                    '97.5% - Electrolyzer producers', '2.5% - Electrolyzer producers'])

    for i in range(80):
        if i in df_phi_pp.index.levels[0]:
            tmp_df = df_phi_pp.loc[i]['Profitability'].groupby(level=0).mean()
            df_plot.loc[i, 'Mean - Power producers'] = tmp_df.mean()
            df_plot.loc[i, 'Median - Power producers'] = tmp_df.median()
            df_plot.loc[i, '97.5% - Power producers'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, '2.5% - Power producers'] = tmp_df.quantile(q=0.25)
        if i in df_phi_hp.index.levels[0]:
            tmp_df = df_phi_hp.loc[i]['Profitability'].groupby(level=0).mean()
            df_plot.loc[i, 'Mean - Hydrogen producers'] = tmp_df.mean()
            df_plot.loc[i, 'Median - Hydrogen producers'] = tmp_df.median()
            df_plot.loc[i, '97.5% - Hydrogen producers'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, '2.5% - Hydrogen producers'] = tmp_df.quantile(q=0.25)
        if i in df_phi_ep.index.levels[0]:
            tmp_df = df_phi_ep.loc[i]['Profitability'].groupby(level=0).mean()
            df_plot.loc[i, 'Mean - Electrolyzer producers'] = tmp_df.mean()
            df_plot.loc[i, 'Median - Electrolyzer producers'] = tmp_df.median()
            df_plot.loc[i, '97.5% - Electrolyzer producers'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, '2.5% - Electrolyzer producers'] = tmp_df.quantile(q=0.25)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Profitablity [-]')
    # ax1.plot(x, df_plot['Mean - Power producers'], label='Power producers', linestyle='-', color=black)
    ax1.plot(x, df_plot['Median - Power producers'], label='Power producers', linestyle='-', color=green)
    # ax1.plot(x, df_plot['Mean - Hydrogen producers'], label='Hydrogen producers', linestyle='-', color=blue)
    ax1.plot(x, df_plot['Median - Hydrogen producers'], label='Hydrogen producers', linestyle='-', color=blue)
    # ax1.plot(x, df_plot['Mean - Electrolyzer producers'], label='Electrolyzer producers', linestyle='-', color=green)
    ax1.plot(x, df_plot['Median - Electrolyzer producers'], label='Electrolyzer producers', linestyle='-', color=purple)

    ax1.fill_between(x, df_plot['2.5% - Power producers'], df_plot['97.5% - Power producers'], color=green, alpha=0.25,
                     edgecolor='none')
    ax1.fill_between(x, df_plot['2.5% - Hydrogen producers'], df_plot['97.5% - Hydrogen producers'], color=blue,
                     alpha=0.25, edgecolor='none')
    ax1.fill_between(x, df_plot['2.5% - Electrolyzer producers'], df_plot['97.5% - Electrolyzer producers'],
                     color=purple, alpha=0.25, edgecolor='none')

    ax1.plot(x, np.ones(80), label='Profitability threshold', linestyle='-.', color=orange)

    ax1.set_ylim(0)
    ax1.set_xlim(plot_settings['xlim'])
    ax1.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.3), ncol=2, frameon=False)

    plt.savefig(os.getcwd() + '\\plot_profitability.' + plot_type, bbox_inches='tight')


def plot_profitability_min_max(df_pp, df_hp, df_ep):
    '''
    Function that will create a plot of the min and max profitability of power, hydrogen and electrolyzer producers
    :param:
        pd.DataFrame df_pp: Yearly data of the power producers
        pd.DataFrame df_hp: Yearly data of the hydrogen producers
        pd.DataFrame df_ep: Yearly data of the electrolyzer producers
    :return:
    '''
    df_phi_pp = df_pp.set_index(['Year', 'Run', 'ID'])
    df_phi_hp = df_hp.set_index(['Year', 'Run', 'ID'])
    df_phi_ep = df_ep.set_index(['Year', 'Run', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['PP - median', 'PP - min', 'PP - max', 'HP - median',
                                                                  'HP - min', 'HP - max', 'EP - median', 'EP - min',
                                                                  'EP - max'])

    for i in range(80):
        # Power producers
        if i in df_phi_pp.index.levels[0]:
            tmp_df = df_phi_pp.loc[i]['Profitability'].groupby(level=0).median()
            df_plot.loc[i, 'PP - median'] = tmp_df.median()
            tmp_df = df_phi_pp.loc[i]['Profitability'].groupby(level=0).min()
            df_plot.loc[i, 'PP - min'] = tmp_df.median()
            tmp_df = df_phi_pp.loc[i]['Profitability'].groupby(level=0).max()
            df_plot.loc[i, 'PP - max'] = tmp_df.median()
        # Hydrogen producers
        if i in df_phi_hp.index.levels[0]:
            tmp_df = df_phi_hp.loc[i]['Profitability'].groupby(level=0).median()
            df_plot.loc[i, 'HP - median'] = tmp_df.median()
            tmp_df = df_phi_hp.loc[i]['Profitability'].groupby(level=0).min()
            df_plot.loc[i, 'HP - min'] = tmp_df.median()
            tmp_df = df_phi_hp.loc[i]['Profitability'].groupby(level=0).max()
            df_plot.loc[i, 'HP - max'] = tmp_df.median()
        # Electrolyzer producers
        if i in df_phi_ep.index.levels[0]:
            tmp_df = df_phi_ep.loc[i]['Profitability'].groupby(level=0).median()
            df_plot.loc[i, 'EP - median'] = tmp_df.median()
            tmp_df = df_phi_ep.loc[i]['Profitability'].groupby(level=0).min()
            df_plot.loc[i, 'EP - min'] = tmp_df.median()
            tmp_df = df_phi_ep.loc[i]['Profitability'].groupby(level=0).max()
            df_plot.loc[i, 'EP - max'] = tmp_df.median()

    fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=plot_settings['figsize'],
                                        gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'], sharex=True)

    # Power producers
    ax1.plot(x, df_plot['PP - median'], color=green, label='Power producers')
    ax1.plot(x, df_plot['PP - min'], color=green, alpha=0.3)
    ax1.plot(x, df_plot['PP - max'], color=green, alpha=0.6)
    ax1.plot(x, np.ones(80), color=orange, linestyle='--')
    # Hydrogen producers
    ax2.plot(x, df_plot['HP - median'], color=blue, label='Hydrogen producers')
    ax2.plot(x, df_plot['HP - min'], color=blue, alpha=0.3)
    ax2.plot(x, df_plot['HP - max'], color=blue, alpha=0.6)
    ax2.plot(x, np.ones(80), color=orange, linestyle='--')
    ax2.set_ylabel('Profitability [-]')
    # Electrolyzer producers
    ax3.plot(x, df_plot['EP - median'], color=purple, label='Electrolyzer producers')
    ax3.plot(x, df_plot['EP - min'], color=purple, alpha=0.3)
    ax3.plot(x, df_plot['EP - max'], color=purple, alpha=0.6)
    ax3.plot(x, np.ones(80), color=orange, linestyle='--', label='Profitability threshold')
    ax3.set_xlabel('Year [-]')

    # Legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles3, labels3 = ax3.get_legend_handles_labels()
    handles = handles1 + handles2 + handles3
    labels = labels1 + labels2 + labels3
    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower left', bbox_to_anchor=(-0.05, -0.85),
               frameon=False, ncol=3)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_profitability_min_max.' + plot_type, bbox_inches='tight')


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
    df_phi_pp = df_pp.set_index(['Year', 'Run', 'ID'])
    df_phi_hp = df_hp.set_index(['Year', 'Run', 'ID'])
    df_phi_ep = df_ep.set_index(['Year', 'Run', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80),
                           columns=['Mean - Power producers', 'Median - Power producers', '97.5% - Power producers',
                                    '2.5% - Power producers', 'Mean - Hydrogen producers',
                                    'Median - Hydrogen producers',
                                    '97.5% - Hydrogen producers', '2.5% - Hydrogen producers',
                                    'Mean - Electrolyzer producers', 'Median - Electrolyzer producers',
                                    '97.5% - Electrolyzer producers', '2.5% - Electrolyzer producers'])

    for i in range(80):
        if i in df_phi_pp.index.levels[0]:
            tmp_df = df_phi_pp.loc[i]['Profitability'] * df_phi_pp.loc[i]['Installed capacity Renewables']
            tmp_df = (tmp_df.groupby(level=0).sum() /
                      df_phi_pp.loc[i]['Installed capacity Renewables'].groupby(level=0).sum())
            df_plot.loc[i, 'Mean - Power producers'] = tmp_df.mean()
            df_plot.loc[i, 'Median - Power producers'] = tmp_df.median()
            df_plot.loc[i, '97.5% - Power producers'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, '2.5% - Power producers'] = tmp_df.quantile(q=0.25)
        if i in df_phi_hp.index.levels[0]:
            tmp_df = df_phi_hp.loc[i]['Profitability'] * df_phi_hp.loc[i]['Installed capacity Electrolyzers']
            tmp_df = (tmp_df.groupby(level=0).sum() /
                      df_phi_hp.loc[i]['Installed capacity Electrolyzers'].groupby(level=0).sum())
            df_plot.loc[i, 'Mean - Hydrogen producers'] = tmp_df.mean()
            df_plot.loc[i, 'Median - Hydrogen producers'] = tmp_df.median()
            df_plot.loc[i, '97.5% - Hydrogen producers'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, '2.5% - Hydrogen producers'] = tmp_df.quantile(q=0.25)
        if i in df_phi_ep.index.levels[0]:
            tmp_df = df_phi_ep.loc[i]['Profitability'] * df_phi_ep.loc[i]['Installed capacity Manufacturings']
            tmp_df = (tmp_df.groupby(level=0).sum() /
                      df_phi_ep.loc[i]['Installed capacity Manufacturings'].groupby(level=0).sum())
            df_plot.loc[i, 'Mean - Electrolyzer producers'] = tmp_df.mean()
            df_plot.loc[i, 'Median - Electrolyzer producers'] = tmp_df.median()
            df_plot.loc[i, '97.5% - Electrolyzer producers'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, '2.5% - Electrolyzer producers'] = tmp_df.quantile(q=0.25)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Profitablity [-]')
    # ax1.plot(x, df_plot['Mean - Power producers'], label='Power producers', linestyle='-', color=black)
    ax1.plot(x, df_plot['Median - Power producers'], label='Power producers', linestyle='-', color=green)
    # ax1.plot(x, df_plot['Mean - Hydrogen producers'], label='Hydrogen producers', linestyle='-', color=blue)
    ax1.plot(x, df_plot['Median - Hydrogen producers'], label='Hydrogen producers', linestyle='-', color=blue)
    # ax1.plot(x, df_plot['Mean - Electrolyzer producers'], label='Electrolyzer producers', linestyle='-', color=green)
    ax1.plot(x, df_plot['Median - Electrolyzer producers'], label='Electrolyzer producers', linestyle='-', color=purple)

    ax1.fill_between(x, df_plot['2.5% - Power producers'], df_plot['97.5% - Power producers'], color=green, alpha=0.25,
                     edgecolor='none')
    ax1.fill_between(x, df_plot['2.5% - Hydrogen producers'], df_plot['97.5% - Hydrogen producers'], color=blue,
                     alpha=0.25, edgecolor='none')
    ax1.fill_between(x, df_plot['2.5% - Electrolyzer producers'], df_plot['97.5% - Electrolyzer producers'],
                     color=purple, alpha=0.25, edgecolor='none')

    ax1.plot(x, np.ones(80), label='Profitability threshold', linestyle='-.', color=orange)

    ax1.set_ylim(0)
    ax1.set_xlim(plot_settings['xlim'])
    ax1.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.3), ncol=2, frameon=False)

    plt.savefig(os.getcwd() + '\\plot_weighted_profitability.' + plot_type, bbox_inches='tight')


def plot_best_profitability(df_pp, df_hp, df_ep):
    '''
    Function that will create a plot of the profitability of a new asset for the power, hydrogen and electrolyzer
    producers
    :param:
        pd.DataFrame df_pp: Yearly data of the power producers
        pd.DataFrame df_hp: Yearly data of the hydrogen producers
        pd.DataFrame df_ep: Yearly data of the electrolyzer producers
    :return:
    '''

    # Fixed values
    tmp_investment_res = 1000000.
    tmp_investment_man = 1000000.
    tmp_crf_res = 0.05 / (1 - (1 + 0.05) ** -20)
    tmp_crf_elc = 0.05 / (1 - (1 + 0.05) ** -15)
    tmp_crf_man = 0.05 / (1 - (1 + 0.05) ** -20)


    df_phi_pp = df_pp.set_index(['Year', 'Run', 'ID'])
    df_phi_hp = df_hp.set_index(['Year', 'Run', 'ID'])
    df_phi_ep = df_ep.set_index(['Year', 'Run', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80),
                           columns=['Mean - Power producers', 'Median - Power producers', '75% - Power producers',
                                    '25% - Power producers', 'Mean - Hydrogen producers',
                                    'Median - Hydrogen producers', '75% - Hydrogen producers',
                                    '25% - Hydrogen producers', 'Mean - Electrolyzer producers',
                                    'Median - Electrolyzer producers', '75% - Electrolyzer producers',
                                    '25% - Electrolyzer producers'])

    for i in range(80):
        # Power Producers
        if i in df_phi_pp.index.levels[0]:
            tmp_df = ((df_phi_pp.loc[i]['Income'] / df_phi_pp.loc[i]['Installed capacity Renewables']) /
                      (tmp_crf_res * tmp_investment_res))
            tmp_df = tmp_df.groupby(level=0).max()
            df_plot.loc[i, 'Mean - Power producers'] = tmp_df.mean()
            df_plot.loc[i, 'Median - Power producers'] = tmp_df.median()
            df_plot.loc[i, '75% - Power producers'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, '25% - Power producers'] = tmp_df.quantile(q=0.25)

        # Hydrogen Producers
        if i in df_phi_hp.index.levels[0]:
            tmp_df = ((df_phi_hp.loc[i]['Income'] / df_phi_hp.loc[i]['Installed capacity Electrolyzers']) /
                      ((df_phi_hp.loc[i]['Expense'] / df_phi_hp.loc[i]['Installed capacity Electrolyzers']) +
                       (tmp_crf_elc * df_phi_ep.loc[i]['Minimal costs Electrolyzers'].min())))
            tmp_df = tmp_df.groupby(level=0).max()
            df_plot.loc[i, 'Mean - Hydrogen producers'] = tmp_df.mean()
            df_plot.loc[i, 'Median - Hydrogen producers'] = tmp_df.median()
            df_plot.loc[i, '75% - Hydrogen producers'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, '25% - Hydrogen producers'] = tmp_df.quantile(q=0.25)

        # Electrolyzer Producers
        if i in df_phi_ep.index.levels[0]:
            tmp_df = ((df_phi_ep.loc[i]['Income'] / df_phi_ep.loc[i]['Installed capacity Manufacturings']) /
                      ((df_phi_ep.loc[i]['Expense'] / df_phi_ep.loc[i]['Installed capacity Manufacturings']) +
                       (tmp_crf_man * tmp_investment_man)))
            tmp_df = tmp_df.groupby(level=0).max()
            df_plot.loc[i, 'Mean - Electrolyzer producers'] = tmp_df.mean()
            df_plot.loc[i, 'Median - Electrolyzer producers'] = tmp_df.median()
            df_plot.loc[i, '75% - Electrolyzer producers'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, '25% - Electrolyzer producers'] = tmp_df.quantile(q=0.25)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Profitablity [-]')
    # ax1.plot(x, df_plot['Mean - Power producers'], label='Power producers', linestyle='-', color=green)
    ax1.plot(x, df_plot['Median - Power producers'], label='Power producers', linestyle='-', color=green)
    # ax1.plot(x, df_plot['Mean - Hydrogen producers'], label='Hydrogen producers', linestyle='-', color=blue)
    ax1.plot(x, df_plot['Median - Hydrogen producers'], label='Hydrogen producers', linestyle='-', color=blue)
    # ax1.plot(x, df_plot['Mean - Electrolyzer producers'], label='Electrolyzer producers', linestyle='-', color=purple)
    ax1.plot(x, df_plot['Median - Electrolyzer producers'], label='Electrolyzer producers', linestyle='-', color=purple)

    ax1.fill_between(x, df_plot['25% - Power producers'], df_plot['75% - Power producers'], color=green, alpha=0.25,
                     edgecolor='none')
    ax1.fill_between(x, df_plot['25% - Hydrogen producers'], df_plot['75% - Hydrogen producers'], color=blue,
                     alpha=0.25, edgecolor='none')
    ax1.fill_between(x, df_plot['25% - Electrolyzer producers'], df_plot['75% - Electrolyzer producers'],
                     color=purple, alpha=0.25, edgecolor='none')

    ax1.plot(x, np.ones(80), label='Profitability threshold', linestyle='-.', color=orange)

    ax1.set_ylim(0)
    ax1.set_xlim(plot_settings['xlim'])
    ax1.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.3), ncol=2, frameon=False)

    plt.savefig(os.getcwd() + '\\plot_best_profitability.' + plot_type, bbox_inches='tight')


def plot_liquidity_pp(df_pp):
    '''
    Function that will create a plot of the liquidity of power producers
    :param
        pd.DataFrame df_pp: Yearly data for the power producers
    :return:
    '''
    df_phi = df_pp.set_index(['Year', 'Run', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['PP - median', 'PP - 25%', 'PP - 75%'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Liquidity'].groupby(level=0).median()
            df_plot.loc[i, 'PP - median'] = tmp_df.median() / 1e6
            df_plot.loc[i, 'PP - 25%'] = tmp_df.quantile(q=0.25) / 1e6
            df_plot.loc[i, 'PP - 75%'] = tmp_df.quantile(q=0.75) / 1e6

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_ylabel('Liquidity [Mio. €]')
    ax1.set_xlabel('Year')
    ax1.plot(x, df_plot['PP - median'], label='Power producers', linestyle='-', color=green)

    ax1.fill_between(x, df_plot['PP - 25%'], df_plot['PP - 75%'], color=green, alpha=0.25, edgecolor='none')
    ax1.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_liquidity_pp.' + plot_type, bbox_inches='tight')


def plot_liquidity_hp(df_hp):
    '''
    Function that will create a plot of the liquidity of hydrogen producers
    :param
        pd.DataFrame df_hp: Yearly data for the hydrogen producers
    :return:
    '''
    df_phi = df_hp.set_index(['Year', 'Run', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['HP - median', 'HP - 25%', 'HP - 75%'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Liquidity'].groupby(level=0).median()
            df_plot.loc[i, 'HP - median'] = tmp_df.median() / 1e6
            df_plot.loc[i, 'HP - 25%'] = tmp_df.quantile(q=0.25) / 1e6
            df_plot.loc[i, 'HP - 75%'] = tmp_df.quantile(q=0.75) / 1e6

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_ylabel('Liquidity [Mio. €]')
    ax1.set_xlabel('Year')
    ax1.plot(x, df_plot['HP - median'], label='Hydrogen producers', linestyle='-', color=blue)

    ax1.fill_between(x, df_plot['HP - 25%'], df_plot['HP - 75%'], color=blue, alpha=0.25, edgecolor='none')
    ax1.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_liquidity_hp.' + plot_type, bbox_inches='tight')


def plot_liquidity_ep(df_ep):
    '''
    Function that will create a plot of the liquidity of electrolyzer producers
    :param
        pd.DataFrame df_ep: Yearly data for the electrolyzer producers
    :return:
    '''
    df_phi = df_ep.set_index(['Year', 'Run', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['EP - median', 'EP - 25%', 'EP - 75%'])

    for i in range(80):
        if i in df_phi.index.levels[0]:
            tmp_df = df_phi.loc[i]['Liquidity'].groupby(level=0).median()
            df_plot.loc[i, 'EP - median'] = tmp_df.median() / 1e6
            df_plot.loc[i, 'EP - 25%'] = tmp_df.quantile(q=0.25) / 1e6
            df_plot.loc[i, 'EP - 75%'] = tmp_df.quantile(q=0.75) / 1e6

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_ylabel('Liquidity [Mio. €]')
    ax1.set_xlabel('Year')
    ax1.plot(x, df_plot['EP - median'], label='Electrolyzer producers', linestyle='-', color=purple)

    ax1.fill_between(x, df_plot['EP - 25%'], df_plot['EP - 75%'], color=purple, alpha=0.25, edgecolor='none')
    ax1.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_liquidity_ep.' + plot_type, bbox_inches='tight')


def plot_w2p_elc_vs_c_elc(df_hp, df_hm, df_man):
    '''
    Function that will create a plot of the willingness to pay and the weighted costs for electorlyzers.
    :param
        pd.DataFrane df_hp: Yearly data of the hydrogen producers
        pd.DataFrame df_hm: Yearly data of the hydrogen market
        pd.DataFrame df_man: Yearly data of the manufacturings
    :return:
    '''
    df_phi_hp = df_hp.set_index(['Year', 'Run', 'ID'])
    df_phi_hm = df_hm.set_index(['Year', 'Run'])
    df_phi_man = df_man.set_index(['Year', 'Run', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['w2p - median', 'w2p - 25%', 'w2p - 75%',
                                                                  'costs - median', 'costs - 25%', 'costs - 75%',
                                                                  'threshold - median', 'w2p - max'])

    for i in range(80):
        if i in df_phi_hp.index.levels[0]:
            tmp_df = df_phi_hp.loc[i]['Willingness to pay'].groupby(level=0).median()
            df_plot.loc[i, 'w2p - median'] = tmp_df.median() / 1e3
            df_plot.loc[i, 'w2p - 25%'] = tmp_df.quantile(q=0.25) / 1e3
            df_plot.loc[i, 'w2p - 75%'] = tmp_df.quantile(q=0.75) / 1e3
            tmp_df = df_phi_hp.loc[i]['Willingness to pay'].groupby(level=0).max()
            df_plot.loc[i, 'w2p - max'] = tmp_df.median() / 1e3
        if i in df_phi_hm.index.levels[0]:
            tmp_df = df_phi_hm.loc[i]['Global investment threshold']
            df_plot.loc[i, 'threshold - median'] = tmp_df.median()
        if i in df_phi_man.index.levels[0]:
            tmp_df = df_phi_man.loc[i]['Capacity'] * df_phi_man.loc[i]['Costs']
            tmp_df = tmp_df.groupby(level=0).sum() / df_phi_man.loc[i]['Capacity'].groupby(level=0).sum()
            df_plot.loc[i, 'costs - median'] = tmp_df.median() / 1e3
            df_plot.loc[i, 'costs - 25%'] = tmp_df.quantile(q=0.25) / 1e3
            df_plot.loc[i, 'costs - 75%'] = tmp_df.quantile(q=0.75) / 1e3

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_ylabel('Costs [€/kW]')
    ax1.set_xlabel('Year')

    # Willingness to pay
    ax1.plot(x, df_plot['w2p - median'], label='Willingness to pay', linestyle='-', color=blue)
    ax1.fill_between(x, df_plot['w2p - 25%'], df_plot['w2p - 75%'], color=blue, alpha=0.25, edgecolor='none')
    ax1.plot(x, df_plot['w2p - max'], label='W2P max', linestyle='-', color=darkblue)
    # Costs
    ax1.plot(x, df_plot['costs - median'], label='Weighted electrolyzer costs', linestyle='-', color=purple)
    ax1.fill_between(x, df_plot['costs - 25%'], df_plot['costs - 75%'], color=purple, alpha=0.25, edgecolor='none')

    # Threshold
    ax2 = ax1.twinx()
    ax2.set_ylabel('Investment threshold [-]')
    ax2.plot(x, df_plot['threshold - median'], label='Global minimal investment threshold', linestyle='-', color=black)
    ax2.set_ylim(-1)

    handle1, label1 = ax1.get_legend_handles_labels()
    handle2, label2 = ax2.get_legend_handles_labels()
    handles = handle1 + handle2
    labels = label1 + label2
    tmpUnique = dict(zip(labels, handles))

    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc=plot_settings['loc'], bbox_to_anchor=(-0.1, -0.25),
               frameon=False, ncol=3)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_w2p_elc_vs_c_elc.' + plot_type, bbox_inches='tight')


def plot_w2p_elc_spec_cashflow_investment_threshold(df_hp, df_hm):
    '''
    Function that will create a plot of the willingness to pay, the specific cashflow and the investment threshold for
    the hydrogen producers.
    :param
        pd.DataFrame df_hp: Yearly data of the hydrogen producers
        pd.DataFrame df_hm: Yearly data of the hydrogen market
    :return:
    '''
    df_phi_hm = df_hm.set_index(['Year', 'Run'])
    df_phi_hp = df_hp.set_index(['Year', 'Run', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['w2p - median', 'w2p - 25%', 'w2p - 75%',
                                                                  'cashflow - median', 'cashflow - 25%',
                                                                  'cashflow - 75%', 'threshold - median',
                                                                  'threshold - 25%', 'threshold - 75%',
                                                                  'global - median', 'global - 25%', 'global - 75%'])

    for i in range(80):
        if i in df_phi_hp.index.levels[0]:
            tmp_df = df_phi_hp.loc[i]['Willingness to pay'].groupby(level=0).max()
            df_plot.loc[i, 'w2p - median'] = tmp_df.median() / 1e3
            df_plot.loc[i, 'w2p - 25%'] = tmp_df.quantile(q=0.25) / 1e3
            df_plot.loc[i, 'w2p - 75%'] = tmp_df.quantile(q=0.75) / 1e3
            tmp_df = df_phi_hp.loc[i]['specific cashflow'].groupby(level=0).max()
            df_plot.loc[i, 'cashflow - median'] = tmp_df.median() / 1e3
            df_plot.loc[i, 'cashflow - 25%'] = tmp_df.quantile(q=0.25) / 1e3
            df_plot.loc[i, 'cashflow - 75%'] = tmp_df.quantile(q=0.75) / 1e3
            tmp_df = df_phi_hp.loc[i]['Investment threshold'].groupby(level=0).min()
            df_plot.loc[i, 'threshold - median'] = tmp_df.median()
            df_plot.loc[i, 'threshold - 25%'] = tmp_df.quantile(q=0.25)
            df_plot.loc[i, 'threshold - 75%'] = tmp_df.quantile(q=0.75)
        if i in df_phi_hm.index.levels[0]:
            tmp_df = df_phi_hm.loc[i]['Global investment threshold']
            df_plot.loc[i, 'global - median'] = tmp_df.median()
            df_plot.loc[i, 'global - 25%'] = tmp_df.quantile(q=0.25)
            df_plot.loc[i, 'global - 75%'] = tmp_df.quantile(q=0.75)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_ylabel('Willingness to pay / Specific netto cashflow [€/kW]')
    ax1.set_xlabel('Year')

    # Willingness to pay
    ax1.plot(x, df_plot['w2p - median'], label='Willingness to pay - max', linestyle='-', color=blue)
    ax1.fill_between(x, df_plot['w2p - 25%'], df_plot['w2p - 75%'], color=blue, alpha=0.25, edgecolor='none')

    # specific cashflow
    ax1.plot(x, df_plot['cashflow - median'], label='Specific net cashflow - max', linestyle='-', color=darkblue)
    ax1.fill_between(x, df_plot['cashflow - 25%'], df_plot['cashflow - 75%'], color=darkblue, alpha=0.25,
                     edgecolor='none')

    # Investment threshold
    ax2 = ax1.twinx()
    ax2.set_ylabel('Investment threshold [-]')
    ax2.plot(x, df_plot['threshold - median'], label='Investment threshold - min', linestyle='-', color=black)
    ax2.fill_between(x, df_plot['threshold - 25%'], df_plot['threshold - 75%'], color=black, alpha=0.25,
                     edgecolor='none')

    ax2.plot(x, df_plot['global - median'], label='Minimal investment threshold', linestyle='--', color=grey)
    ax2.fill_between(x, df_plot['global - 25%'], df_plot['global - 75%'], color=grey, alpha=0.25, edgecolor='none')

    # Legend
    handle1, label1 = ax1.get_legend_handles_labels()
    handle2, label2 = ax2.get_legend_handles_labels()
    handles = handle1 + handle2
    labels = label1 + label2
    tmpUnique = dict(zip(labels, handles))

    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc=plot_settings['loc'], bbox_to_anchor=(-0.1, -0.25),
               frameon=False, ncol=2)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_w2p_elc_spec_cashflow_investment_threshold.' + plot_type,
                bbox_inches='tight')


def plot_cashflow_system(df_pm, df_hp, df_ep):
    '''
    Function that will create a plot ot the money earned and spend
    :param
        pd.DataFrame df_pm: Daily data of the power market
        pd.DataFrame df_hp: Yearly data of the hydrogen producers
        pd.DataFrame df_ep: Yearly data of the electrolyzer producers
    :return:
    '''
    df_phi_pm = df_pm.set_index(['Year', 'Day', 'Run'])
    df_phi_hp = df_hp.set_index(['Year', 'Run', 'ID'])
    df_phi_ep = df_ep.set_index(['Year', 'Run', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['GT - No', 'GT - Full', 'GT - Part', 'H2 - Full',
                                                                  'H2 - Part', 'H2', 'ELC', 'Sale', 'Production'])

    for i in range(80):
        # Power market
        if i in df_phi_pm.index.levels[0]:
            dfGTN = []
            dfGTF = []
            dfGTP = []
            dfH2F = []
            dfH2P = []
            for j in df_phi_pm.index.levels[2]:
                tmpGTN = 0
                tmpGTF = 0
                tmpGTP = 0
                tmpH2F = 0
                tmpH2P = 0
                for k in df_phi_pm.index.levels[1]:
                    tmpDF = df_phi_pm.loc[i].loc[k].loc[j]
                    if tmpDF['Electricity demand electrolyzers'] <= 0:
                        tmpGTN += tmpDF['Payout Electricity'] * tmpDF['Actual production renewables']
                    else:
                        if tmpDF['Curtailment of renewables'] <= 0:
                            tmpGTP += tmpDF['Payout Electricity'] * tmpDF['Electricity demand others']
                            tmpH2P += tmpDF['Payout Electricity'] * tmpDF['Electricity demand electrolyzers']
                        else:
                            tmpGTF += tmpDF['Payout Electricity'] * tmpDF['Electricity demand others']
                            tmpH2F += tmpDF['Payout Electricity'] * tmpDF['Electricity demand electrolyzers']

                dfGTN.append(tmpGTN)
                dfGTF.append(tmpGTF)
                dfGTP.append(tmpGTP)
                dfH2F.append(tmpH2F)
                dfH2P.append(tmpH2P)
            df_plot.loc[i, 'GT - No'] = np.median(dfGTN) / 1e9
            df_plot.loc[i, 'GT - Full'] = np.median(dfGTF) / 1e9
            df_plot.loc[i, 'GT - Part'] = np.median(dfGTP) / 1e9
            df_plot.loc[i, 'H2 - Full'] = np.median(dfH2F) / 1e9
            df_plot.loc[i, 'H2 - Part'] = np.median(dfH2P) / 1e9

        # Hydrogen market
        if i in df_phi_hp.index.levels[0]:
            tmpH2 = df_phi_hp.loc[i]['Income'].groupby(level=0).sum()
            tmpELC = df_phi_hp.loc[i]['Expense'].groupby(level=0).sum()
            df_plot.loc[i, 'H2'] = tmpH2.median() / 1e9
            df_plot.loc[i, 'ELC'] = -1 * tmpELC.median() / 1e9

        # Electrolyzer market
        if i in df_phi_ep.index.levels[0]:
            tmpSale = df_phi_ep.loc[i]['Income'].groupby(level=0).sum()
            tmpProd = df_phi_ep.loc[i]['Expense'].groupby(level=0).sum()
            df_plot.loc[i, 'Sale'] = tmpSale.median() / 1e9
            df_plot.loc[i, 'Production'] = -1 * tmpProd.median() / 1e9

    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=plot_settings['figsize'],
                                        gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'], sharex=True)

    # Power market
    ax1.fill_between(x, 0, df_plot['GT - No'], color=grey, alpha=0.5, edgecolor='none')
    ax1.fill_between(x, df_plot['GT - No'], df_plot['GT - No'] + df_plot['GT - Part'], color=grey, alpha=0.5,
                     edgecolor='none', hatch='///')
    ax1.fill_between(x, df_plot['GT - No'] + df_plot['GT - Part'],
                     df_plot['GT - No'] + df_plot['GT - Part'] + df_plot['GT - Full'], color=grey, alpha=0.5,
                     edgecolor='none', hatch='ooo')
    ax1.fill_between(x, df_plot['GT - No'] + df_plot['GT - Part'] + df_plot['GT - Full'],
                     df_plot['GT - No'] + df_plot['GT - Part'] + df_plot['GT - Full'] + df_plot['H2 - Part'],
                     color=green, alpha=0.5, edgecolor='none', hatch='///')
    ax1.fill_between(x, df_plot['GT - No'] + df_plot['GT - Part'] + df_plot['GT - Full'] + df_plot['H2 - Part'],
                     df_plot['GT - No'] + df_plot['GT - Part'] + df_plot['GT - Full'] + df_plot['H2 - Part'] + df_plot[
                         'H2 - Full'],
                     color=green, alpha=0.5, edgecolor='none', hatch='ooo')

    ax1.plot(x, df_plot['GT - No'] + df_plot['GT - Part'] + df_plot['GT - Full'] + df_plot['H2 - Part'] + df_plot[
        'H2 - Full'],
             label='Profits', color=orange, linestyle='--')

    ax1.fill_between(x, 0, 0, color=grey, alpha=0.5, edgecolor='none', label='General demand')
    ax1.fill_between(x, 0, 0, color=green, alpha=0.5, edgecolor='none', label='Electrolyzers demand')

    ax1.set_ylim(0)

    # Hydrogen market
    ax2.set_ylabel('[Bn. €]')
    ax2.fill_between(x, 0, df_plot['H2'], color=blue, alpha=0.5, label='Income hydrogen', edgecolor='none')
    ax2.fill_between(x, 0, df_plot['ELC'], color=red, alpha=0.5, label='Expense electricity', edgecolor='none')

    ax2.plot(x, df_plot['H2'] + df_plot['ELC'], label='Profits', color=orange, linestyle='--')

    # Electrolyzer market
    ax3.fill_between(x, 0, df_plot['Sale'], color=purple, alpha=0.5, label='Income electrolyzers', edgecolor='none')
    ax3.fill_between(x, 0, df_plot['Production'], color=darkblue, alpha=0.5, label='Production costs electrolyzers',
                     edgecolor='none')

    ax3.plot(x, df_plot['Sale'] + df_plot['Production'], label='Profits', color=orange, linestyle='--')

    plt.xlim(plot_settings['xlim'])

    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles3, labels3 = ax3.get_legend_handles_labels()

    handles = handles1 + handles2 + handles3
    labels = labels1 + labels2 + labels3
    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower left', bbox_to_anchor=(-0.1, -1.15),
               frameon=False, ncol=3)

    plt.savefig(os.getcwd() + '\\plot_cashflow_system.' + plot_type, bbox_inches='tight')


def plot_weighted_utilization_all(df_res, df_elc, df_man):
    '''
    Function that will create a plot of the capacity weighted utilization per year of the renewables, electrolyzers and
    factories.
    :param:
        pd.DataFrame df_res: Yearly data from the renewables
        pd.DataFrame df_elc: Yearly data from the electrolyzers
        pd.DataFrame df_man: Yearly data from the manufacturings
    :return:
    '''
    df_phi_res = df_res.set_index(['Year', 'Run', 'ID'])
    df_phi_elc = df_elc.set_index(['Year', 'Run', 'ID'])
    df_phi_man = df_man.set_index(['Year', 'Run', 'ID'])

    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['RES - median', 'RES - 25%', 'RES - 75%',
                                                                  'ELC - median', 'ELC - 25%', 'ELC - 75%',
                                                                  'FAC - median', 'FAC - 25%', 'FAC - 75%'])

    for i in range(80):
        # Renewables
        if i in df_phi_res.index.levels[0]:
            tmpRES = []
            for j in df_phi_res.loc[i].index.levels[0]:
                tmpZ = 0
                tmpN = 0
                for k in df_phi_res.loc[i].loc[j].index:
                    tmpDF = df_phi_res.loc[i].loc[j].loc[k]
                    tmpZ += tmpDF['Capacity'] * tmpDF['Utilization rate']
                    tmpN += tmpDF['Capacity']
                if tmpN > 0:
                    tmpRES.append(tmpZ / tmpN)
                else:
                    tmpRES.append(np.nan)
            df_plot.loc[i, 'RES - median'] = np.median(tmpRES)
            df_plot.loc[i, 'RES - 25%'] = np.percentile(tmpRES, 25)
            df_plot.loc[i, 'RES - 75%'] = np.percentile(tmpRES, 75)

        # Electrolyzers
        if i in df_phi_elc.index.levels[0]:
            tmpELC = []
            for j in df_phi_elc.loc[i].index.levels[0]:
                tmpZ = 0
                tmpN = 0
                for k in df_phi_elc.loc[i].loc[j].index:
                    tmpDF = df_phi_elc.loc[i].loc[j].loc[k]
                    tmpZ += tmpDF['Capacity'] * tmpDF['Utilization rate']
                    tmpN += tmpDF['Capacity']
                if tmpN > 0:
                    tmpELC.append(tmpZ / tmpN)
                else:
                    tmpELC.append(np.nan)
            df_plot.loc[i, 'ELC - median'] = np.median(tmpELC)
            df_plot.loc[i, 'ELC - 25%'] = np.percentile(tmpELC, 25)
            df_plot.loc[i, 'ELC - 75%'] = np.percentile(tmpELC, 75)

        # Factories
        if i in df_phi_man.index.levels[0]:
            tmpMAN = []
            for j in df_phi_man.loc[i].index.levels[0]:
                tmpZ = 0
                tmpN = 0
                for k in df_phi_man.loc[i].loc[j].index:
                    tmpDF = df_phi_man.loc[i].loc[j].loc[k]
                    tmpZ += tmpDF['Capacity'] * tmpDF['Utilization rate']
                    tmpN += tmpDF['Capacity']
                if tmpN > 0:
                    tmpMAN.append(tmpZ / tmpN)
                else:
                    tmpMAN.append(np.nan)
            df_plot.loc[i, 'FAC - median'] = np.median(tmpMAN)
            df_plot.loc[i, 'FAC - 25%'] = np.percentile(tmpMAN, 25)
            df_plot.loc[i, 'FAC - 75%'] = np.percentile(tmpMAN, 75)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Utilization rate [%]')

    # Renewables
    ax1.plot(x, df_plot['RES - median'] * 100, label='Renewables', linestyle='-', color=green)
    ax1.fill_between(x, df_plot['RES - 25%'] * 100, df_plot['RES - 75%'] * 100, color=green, alpha=0.25,
                     edgecolor='none')

    # Electrolyzers
    ax1.plot(x, df_plot['ELC - median'] * 100, label='Electrolyzers', linestyle='-', color=blue)
    ax1.fill_between(x, df_plot['ELC - 75%'] * 100, df_plot['ELC - 25%'] * 100, color=blue, alpha=0.25,
                     edgecolor='none')

    # Manufacturings
    ax1.plot(x, df_plot['FAC - median'] * 100, label='Manufacturings', linestyle='-', color=purple)
    ax1.fill_between(x, df_plot['FAC - 25%'] * 100, df_plot['FAC - 75%'] * 100, color=purple, alpha=0.25,
                     edgecolor='none')

    ax1.set_ylim(0, 100)
    ax1.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False, ncol=3)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Full load hours [h]')
    ax2.set_ylim(0, 8760)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_weighted_utilization_all.' + plot_type, bbox_inches='tight')


def plot_w2p_elc_vs_c_elc_vs_p_elc(df_sale):
    '''
    Function that will create a plot of the willingness to pay, costs & price of electrolyzers.
    :param:
        pd.DataFrame df_sale: Yearly data of the sales of electrolyzers.
    :return:
    '''
    df_phi_sale = df_sale.set_index(['Year', 'Run', 'EP ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80),
                           columns=['Price - median', 'Price - 25%', 'Price - 75%', 'Costs - median', 'Costs - 25%',
                                    'Costs - 75%', 'W2P - median', 'W2P - 25%', 'W2P - 75%'])

    for i in range(80):
        if i in df_phi_sale.index.levels[0]:
            tmp_df = df_phi_sale.loc[i]['Payout'].groupby(level=0).mean()
            df_plot.loc[i, 'Price - median'] = tmp_df.median()
            df_plot.loc[i, 'Price - 75%'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, 'Price - 25%'] = tmp_df.quantile(q=0.25)
            tmp_df = df_phi_sale.loc[i]['Willinges to pay'].groupby(level=0).mean()
            df_plot.loc[i, 'W2P - median'] = tmp_df.median()
            df_plot.loc[i, 'W2P - 75%'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, 'W2P - 25%'] = tmp_df.quantile(q=0.25)
            tmp_df = df_phi_sale.loc[i]['Production costs'].groupby(level=0).mean()
            df_plot.loc[i, 'Costs - median'] = tmp_df.median()
            df_plot.loc[i, 'Costs - 75%'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, 'Costs - 25%'] = tmp_df.quantile(q=0.25)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_xlabel('Year')
    ax1.set_ylabel('[Mio. €/MW]')
    ax1.plot(x, df_plot['Price - median'] / 1e6, label='Price electrolyzer', linestyle='-', color=red)
    ax1.fill_between(x, df_plot['Price - 25%'] / 1e6, df_plot['Price - 75%'] / 1e6, color=red, alpha=0.25,
                     edgecolor='none')

    ax1.plot(x, df_plot['Costs - median'] / 1e6, label='Production costs electrolyzer', linestyle='-', color=purple)
    ax1.fill_between(x, df_plot['Costs - 25%'] / 1e6, df_plot['Costs - 75%'] / 1e6, color=purple, alpha=0.25,
                     edgecolor='none')

    ax1.plot(x, df_plot['W2P - median'] / 1e6, label='Willingness to pay for electrolyzer', linestyle='-', color=blue)
    ax1.fill_between(x, df_plot['W2P - 25%'] / 1e6, df_plot['W2P - 75%'] / 1e6, color=blue, alpha=0.25,
                     edgecolor='none')

    ax1.set_ylim(0)
    ax1.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False, ncol=2)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Costs [€/kW]')
    ax2.plot(x, df_plot['Price - median'] / 1e3, label='Price electrolyzer', linestyle='-', color=red)
    ax2.fill_between(x, df_plot['Price - 25%'] / 1e3, df_plot['Price - 75%'] / 1e3, color=red, alpha=0.25,
                     edgecolor='none')

    ax2.plot(x, df_plot['Costs - median'] / 1e3, label='Production costs electrolyzer', linestyle='-', color=purple)
    ax2.fill_between(x, df_plot['Costs - 25%'] / 1e3, df_plot['Costs - 75%'] / 1e3, color=purple, alpha=0.25,
                     edgecolor='none')

    ax2.plot(x, df_plot['W2P - median'] / 1e3, label='Willingness to pay for electrolyzer', linestyle='-', color=blue)
    ax2.fill_between(x, df_plot['W2P - 25%'] / 1e3, df_plot['W2P - 75%'] / 1e3, color=blue, alpha=0.25,
                     edgecolor='none')
    ax2.set_ylim(0)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_w2p_elc_c_elc_p_elc.' + plot_type, bbox_inches='tight')


def plot_final_p_elc(df_sale):
    '''
    Function that will create a plot of the willingness to pay, costs & price of electrolyzers.
    :param:
        pd.DataFrame df_sale: Yearly data of the sales of electrolyzers.
    :return:
    '''
    df_phi_sale = df_sale.set_index(['Year', 'Run', 'EP ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80),
                           columns=['Price - median', 'Price - 25%', 'Price - 75%'])

    for i in range(80):
        if i in df_phi_sale.index.levels[0]:
            tmp_df = df_phi_sale.loc[i]['Payout'].groupby(level=0).mean()
            df_plot.loc[i, 'Price - median'] = tmp_df.median()
            df_plot.loc[i, 'Price - 75%'] = tmp_df.quantile(q=0.75)
            df_plot.loc[i, 'Price - 25%'] = tmp_df.quantile(q=0.25)

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_xlabel('Year')
    ax1.set_ylabel('[€/kW]')
    ax1.plot(x, df_plot['Price - median'] / 1e3, label='Price electrolyzer', linestyle='-', color=purple)
    ax1.fill_between(x, df_plot['Price - 25%'] / 1e3, df_plot['Price - 75%'] / 1e3, color=purple, alpha=0.25,
                     edgecolor='none')

    ax1.set_ylim(0)
    ax1.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.25), frameon=False, ncol=2)

    #ax2 = ax1.twinx()
    #ax2.set_ylabel('Costs [€/kW]')
    #ax2.plot(x, df_plot['Price - median'] / 1e3, label='Price electrolyzer', linestyle='-', color=red)
    #ax2.fill_between(x, df_plot['Price - 25%'] / 1e3, df_plot['Price - 75%'] / 1e3, color=red, alpha=0.25,
    #                 edgecolor='none')

    #ax2.set_ylim(0)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_final_p_elc.' + plot_type, bbox_inches='tight')


def plot_electricity_production_share(df_pm):
    '''
    Function that will create a plot of the electricity production and its parts for different years, which can be
    selected by changing years.
    :param:
        pd.DataFrame df_pm: Daily data of the power market.
    :return:
    '''
    years = [0, 7, 17, 27, 37, 42]
    df_phi_pm = df_pm.set_index(['Year', 'Day', 'Run'])

    for year in years:
        # Data
        tmpRES = []
        tmpH2 = []
        tmpCurt = []
        for day in range(1, 366):
            tmpRunRES = []
            tmpRunH2 = []
            tmpRunCurt = []
            for run in df_phi_pm.index.levels[2]:
                tmpDf = df_phi_pm.loc[year].loc[day].loc[run]
                tmpDemand = tmpDf['Electricity demand others']
                if tmpDf['Maximum production renewables'] < tmpDemand:
                    tmpRunRES.append(tmpDf['Maximum production renewables'] / tmpDemand)
                    tmpRunH2.append(1)
                    tmpRunCurt.append(1)
                else:
                    tmpRunRES.append(1)
                    tmpRunH2.append(tmpDf['Actual production renewables'] / tmpDemand)
                    tmpRunCurt.append(tmpDf['Maximum production renewables'] / tmpDemand)
            tmpRES.append(np.median(tmpRunRES))
            tmpH2.append(np.median(tmpRunH2))
            tmpCurt.append(np.median(tmpRunCurt))

        tmpRES.sort(reverse=True)
        tmpH2.sort(reverse=True)
        tmpCurt.sort(reverse=True)

        # Plot
        fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                                dpi=plot_settings['dpi'])

        ax1.set_xlabel('Day [-]')
        ax1.set_ylabel('Share [-]')

        tmpx = range(1, 366)
        ax1.plot(tmpx, np.ones(365), label='General electricity demand', color=black, linestyle='-')
        ax1.fill_between(tmpx, np.zeros(365), tmpRES, label='Renewables', color=green, alpha=0.25, edgecolor='none')
        ax1.fill_between(tmpx, tmpRES, np.ones(365), label='Gas turbines', color=grey, alpha=0.25, edgecolor='none')
        ax1.fill_between(tmpx, np.ones(365), tmpH2, label='Green hydrogen', color=blue, alpha=0.25, edgecolor='none')
        ax1.fill_between(tmpx, tmpH2, tmpCurt, label='Curtailment', color=purple, alpha=0.25, edgecolor='none')

        ax1.set_xlim([1, 365])
        ax1.set_ylim([0, 3])
        ax1.legend(loc='lower left', bbox_to_anchor=(-0.05, -0.3), frameon=False, ncol=3)

        plt.savefig(os.getcwd() + '\\plot_electricity_production_share_year_' + str(2023 + year) + '.' +
                    plot_type, bbox_inches='tight')


def plot_electricity_production_excess(df_pm):
    '''
    Function that will create a plot of the electricity production and its parts for different years, which can be
    selected by changing years.
    :param:
        pd.DataFrame df_pm: Daily data of the power market.
    :return:
    '''
    years = [0, 1, 3, 5, 7, 9, 11, 13, 15, 17, 27]
    df_phi_pm = df_pm.set_index(['Year', 'Day', 'Run'])

    for year in years:
        # Data
        tmpRES = []
        tmpH2 = []
        tmpGT = []

        # Average electricity demand by others
        tmpDemandMeanAll = df_phi_pm.loc[year]['Electricity demand others'].groupby('Run').mean()
        for day in range(1, 366):
            tmpRunRES = []
            tmpRunH2 = []
            tmpRunGT = []
            for run in df_phi_pm.index.levels[2]:
                tmpDemandMean = tmpDemandMeanAll.loc[run]
                tmpDf = df_phi_pm.loc[year].loc[day].loc[run]
                if tmpDf['Maximum production renewables'] < tmpDf['Electricity demand others']:
                    tmpRunRES.append(0)
                    tmpRunH2.append(0)
                    tmpRunGT.append((tmpDf['Maximum production renewables'] - tmpDf['Electricity demand others']) /
                                    tmpDemandMean)
                else:
                    tmpRunRES.append((tmpDf['Maximum production renewables'] - tmpDf['Electricity demand others']) /
                                     tmpDemandMean)
                    tmpRunH2.append(tmpDf['Electricity demand electrolyzers'] / tmpDemandMean)
                    tmpRunGT.append(0)

            tmpRES.append(np.median(tmpRunRES))
            tmpH2.append(np.median(tmpRunH2))
            tmpGT.append(np.median(tmpRunGT))

        # Order
        tmpRES.sort(reverse=True)
        tmpH2.sort(reverse=True)
        tmpGT.sort(reverse=True)

        # Plot
        fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                                dpi=plot_settings['dpi'])

        ax1.set_xlabel('Day [-]')
        ax1.set_ylabel('Excess electricity normalized [-]')

        tmpx = range(1, 366)
        ax1.fill_between(tmpx, np.zeros(365), tmpH2, label='Green hydrogen production', color=blue, alpha=0.25,
                         edgecolor='none')
        ax1.fill_between(tmpx, tmpH2, tmpRES, label='Curtailment', color=purple, alpha=0.25, edgecolor='none')
        ax1.fill_between(tmpx, tmpGT, np.zeros(365), label='Gas turbines', color=grey, alpha=0.25, edgecolor='none')
        #ax1.fill_between(tmpx, np.ones(365)*-1, tmpGT, label='Renewables', color=green, alpha=0.25,
        #                 edgecolor='none')

        ax1.set_xlim([1, 365])
        ax1.set_ylim([-1, 3])
        ax1.legend(loc='lower left', bbox_to_anchor=(-0.04, -0.3), frameon=False, ncol=2)

        plt.savefig(os.getcwd() + '\\plot_electricity_production_excess_year_' + str(2023 + year) + '.'
                    + plot_type, bbox_inches='tight')


def plot_return_on_investment_all(df_res, df_elc, df_man):
    '''
    Function that will create a plot of the return on investment for renewables, electrolyzers and manufacturings.
    :param:
        pd.DataFrame df_res: Yearly data for the renewables
        pd.DataFrame df_elc: Yearly data for the electrolyzers
        pd.DataFrame df_man: Yearly data for the renewables
    :return:
    '''
    df_phi_res = df_res.set_index(['Year', 'Run', 'ID'])
    df_phi_elc = df_elc.set_index(['Year', 'Run', 'ID'])
    df_phi_man = df_man.set_index(['Year', 'Run', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['RES - median', 'RES - 25%', 'RES - 75%',
                                                                  'ELC - median', 'ELC - 25%', 'ELC - 75%',
                                                                  'MAN - median', 'MAN - 25%', 'MAN - 75%'])

    for i in range(80):
        # Renewables
        if i in df_phi_res.index.levels[0]:
            tmp_df = df_phi_res.loc[i]['Return on Investment'].groupby(level=0).median()
            df_plot.loc[i, 'RES - median'] = tmp_df.median() * 100
            df_plot.loc[i, 'RES - 25%'] = tmp_df.quantile(q=0.25) * 100
            df_plot.loc[i, 'RES - 75%'] = tmp_df.quantile(q=0.75) * 100
        # Electrolyzers
        if i in df_phi_elc.index.levels[0]:
            tmp_df = df_phi_elc.loc[i]['Return on Investment'].groupby(level=0).median()
            df_plot.loc[i, 'ELC - median'] = tmp_df.median() * 100
            df_plot.loc[i, 'ELC - 25%'] = tmp_df.quantile(q=0.25) * 100
            df_plot.loc[i, 'ELC - 75%'] = tmp_df.quantile(q=0.75) * 100
        # Manufacturings
        if i in df_phi_man.index.levels[0]:
            tmp_df = df_phi_man.loc[i]['Return on Investment'].groupby(level=0).median()
            df_plot.loc[i, 'MAN - median'] = tmp_df.median() * 100
            df_plot.loc[i, 'MAN - 25%'] = tmp_df.quantile(q=0.25) * 100
            df_plot.loc[i, 'MAN - 75%'] = tmp_df.quantile(q=0.75) * 100

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_ylabel('Return on Investment [%]')
    ax1.set_xlabel('Year')

    # Renewables
    ax1.plot(x, df_plot['RES - median'], label='Renewables', linestyle='-', color=green)
    ax1.fill_between(x, df_plot['RES - 25%'], df_plot['RES - 75%'], color=green, alpha=0.25, edgecolor='none')
    # Electrolyzers
    ax1.plot(x, df_plot['ELC - median'], label='Electrolyzers', linestyle='-', color=blue)
    ax1.fill_between(x, df_plot['ELC - 25%'], df_plot['ELC - 75%'], color=blue, alpha=0.25, edgecolor='none')
    # Manufacturings
    ax1.plot(x, df_plot['MAN - median'], label='Manufacturings', linestyle='-', color=purple)
    ax1.fill_between(x, df_plot['MAN - 25%'], df_plot['MAN - 75%'], color=purple, alpha=0.25, edgecolor='none')

    ax1.plot(x, np.ones(80), color=grey)

    ax1.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False, ncol=3)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_return_on_investment_all.' + plot_type, bbox_inches='tight')


def plot_weighted_return_on_investment_all(df_res, df_elc, df_man):
    '''
    Function that will create a plot of the capacity weighted return on investment for renewables, electrolyzers and
    manufacturings.
    :param:
        pd.DataFrame df_res: Yearly data for the renewables
        pd.DataFrame df_elc: Yearly data for the electrolyzers
        pd.DataFrame df_man: Yearly data for the renewables
    :return:
    '''
    df_phi_res = df_res.set_index(['Year', 'Run', 'ID'])
    df_phi_elc = df_elc.set_index(['Year', 'Run', 'ID'])
    df_phi_man = df_man.set_index(['Year', 'Run', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['RES - median', 'RES - 25%', 'RES - 75%',
                                                                  'ELC - median', 'ELC - 25%', 'ELC - 75%',
                                                                  'MAN - median', 'MAN - 25%', 'MAN - 75%'])

    for i in range(80):
        # Renewables
        if i in df_phi_res.index.levels[0]:
            tmp_df = df_phi_res.loc[i]['Return on Investment'] * df_phi_res.loc[i]['Capacity']
            tmp_df = tmp_df.groupby(level=0).sum() / df_phi_res.loc[i]['Capacity'].groupby(level=0).sum()
            df_plot.loc[i, 'RES - median'] = tmp_df.median() * 100
            df_plot.loc[i, 'RES - 25%'] = tmp_df.quantile(q=0.25) * 100
            df_plot.loc[i, 'RES - 75%'] = tmp_df.quantile(q=0.75) * 100
        # Electrolyzers
        if i in df_phi_res.index.levels[0]:
            tmp_df = df_phi_elc.loc[i]['Return on Investment'] * df_phi_res.loc[i]['Capacity']
            tmp_df = tmp_df.groupby(level=0).sum() / df_phi_elc.loc[i]['Capacity'].groupby(level=0).sum()
            df_plot.loc[i, 'ELC - median'] = tmp_df.median() * 100
            df_plot.loc[i, 'ELC - 25%'] = tmp_df.quantile(q=0.25) * 100
            df_plot.loc[i, 'ELC - 75%'] = tmp_df.quantile(q=0.75) * 100
        # Manufacturings
        if i in df_phi_res.index.levels[0]:
            tmp_df = df_phi_man.loc[i]['Return on Investment'] * df_phi_man.loc[i]['Capacity']
            tmp_df = tmp_df.groupby(level=0).sum() / df_phi_man.loc[i]['Capacity'].groupby(level=0).sum()
            df_plot.loc[i, 'MAN - median'] = tmp_df.median() * 100
            df_plot.loc[i, 'MAN - 25%'] = tmp_df.quantile(q=0.25) * 100
            df_plot.loc[i, 'MAN - 75%'] = tmp_df.quantile(q=0.75) * 100


    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_ylabel('Return on Investment [%]')
    ax1.set_xlabel('Year')

    # Renewables
    ax1.plot(x, df_plot['RES - median'], label='Renewables', linestyle='-', color=green)
    ax1.fill_between(x, df_plot['RES - 25%'], df_plot['RES - 75%'], color=green, alpha=0.25, edgecolor='none')
    # Electrolyzers
    ax1.plot(x, df_plot['ELC - median'], label='Electrolyzers', linestyle='-', color=blue)
    ax1.fill_between(x, df_plot['ELC - 25%'], df_plot['ELC - 75%'], color=blue, alpha=0.25, edgecolor='none')
    # Manufacturings
    ax1.plot(x, df_plot['MAN - median'], label='Manufacturings', linestyle='-', color=purple)
    ax1.fill_between(x, df_plot['MAN - 25%'], df_plot['MAN - 75%'], color=purple, alpha=0.25, edgecolor='none')

    ax1.plot(x, np.ones(80)*7, color=orange, linestyle='-.')

    ax1.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False, ncol=3)

    plt.xlim(plot_settings['xlim'])
    plt.ylim([-1, 200])
    plt.savefig(os.getcwd() + '\\plot_weighted_return_on_investment_all.' + plot_type, bbox_inches='tight')


def plot_return_on_investment_max_min(df_res, df_elc, df_man):
    '''
    Function that will create a plot of the return on investment for renewables, electrolyzers and manufacturings but
    shows the max, min and mean.
    :param:
        pd.DataFrame df_res: Yearly data for the renewables
        pd.DataFrame df_elc: Yearly data for the electrolyzers
        pd.DataFrame df_man: Yearly data for the renewables
    :return:
    '''
    df_phi_res = df_res.set_index(['Year', 'Run', 'ID'])
    df_phi_elc = df_elc.set_index(['Year', 'Run', 'ID'])
    df_phi_man = df_man.set_index(['Year', 'Run', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['RES - mean', 'RES - max', 'RES - min',
                                                                  'ELC - mean', 'ELC - max', 'ELC - min',
                                                                  'MAN - mean', 'MAN - max', 'MAN - min'])

    for i in range(80):
        # Renewables
        if i in df_phi_res.index.levels[0]:
            tmp_df = df_phi_res.loc[i]['Return on Investment'].groupby(level=0).mean()
            df_plot.loc[i, 'RES - mean'] = tmp_df.median() * 100
            tmp_df = df_phi_res.loc[i]['Return on Investment'].groupby(level=0).max()
            df_plot.loc[i, 'RES - max'] = tmp_df.median() * 100
            tmp_df = df_phi_res.loc[i]['Return on Investment'].groupby(level=0).min()
            df_plot.loc[i, 'RES - min'] = tmp_df.median() * 100
        # Electrolyzers
        if i in df_phi_elc.index.levels[0]:
            tmp_df = df_phi_elc.loc[i]['Return on Investment'].groupby(level=0).mean()
            df_plot.loc[i, 'ELC - mean'] = tmp_df.median() * 100
            tmp_df = df_phi_elc.loc[i]['Return on Investment'].groupby(level=0).max()
            df_plot.loc[i, 'ELC - max'] = tmp_df.median() * 100
            tmp_df = df_phi_elc.loc[i]['Return on Investment'].groupby(level=0).min()
            df_plot.loc[i, 'ELC - min'] = tmp_df.median() * 100
        # Manufacturings
        if i in df_phi_man.index.levels[0]:
            tmp_df = df_phi_man.loc[i]['Return on Investment'].groupby(level=0).mean()
            df_plot.loc[i, 'MAN - mean'] = tmp_df.median() * 100
            tmp_df = df_phi_man.loc[i]['Return on Investment'].groupby(level=0).max()
            df_plot.loc[i, 'MAN - max'] = tmp_df.median() * 100
            tmp_df = df_phi_man.loc[i]['Return on Investment'].groupby(level=0).min()
            df_plot.loc[i, 'MAN - min'] = tmp_df.median() * 100

    fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=plot_settings['figsize'],
                                        gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'], sharex=True)

    # Renewables
    ax1.plot(x, df_plot['RES - mean'], label='Renewables', linestyle='-', color=green)
    ax1.plot(x, df_plot['RES - max'], color=green, alpha=0.66)
    ax1.plot(x, df_plot['RES - min'], color=green, alpha=0.33)

    # Electrolyzers
    ax2.set_ylabel('Return on Investment [%]')
    ax2.plot(x, df_plot['ELC - mean'], label='Electrolyzers', linestyle='-', color=blue)
    ax2.plot(x, df_plot['ELC - max'], color=blue, alpha=0.66)
    ax2.plot(x, df_plot['ELC - min'], color=blue, alpha=0.33)

    # Manufacturings
    ax3.set_xlabel('Year [-]')
    ax3.plot(x, df_plot['MAN - mean'], label='Manufacturings', linestyle='-', color=purple)
    ax3.plot(x, df_plot['MAN - max'], color=purple, alpha=0.66)
    ax3.plot(x, df_plot['MAN - min'], color=purple, alpha=0.33)
    ax3.set_xlim(plot_settings['xlim'])

    # Legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles3, labels3 = ax3.get_legend_handles_labels()

    handles = handles1 + handles2 + handles3
    labels = labels1 + labels2 + labels3

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower left', bbox_to_anchor=(-0.05, -0.85),
               frameon=False, ncol=3)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_return_on_investment_max_min.' + plot_type, bbox_inches='tight')


def plot_return_on_investment_old(df_res, df_elc, df_man):
    '''
    Function that will create a plot of the return on investment for renewables, electrolyzers and manufacturings but
    shows the oldest asset.
    :param:
        pd.DataFrame df_res: Yearly data for the renewables
        pd.DataFrame df_elc: Yearly data for the electrolyzers
        pd.DataFrame df_man: Yearly data for the renewables
    :return:
    '''
    df_phi_res = df_res.set_index(['Year', 'Run', 'ID', 'Age'])
    df_phi_elc = df_elc.set_index(['Year', 'Run', 'ID', 'Age'])
    df_phi_man = df_man.set_index(['Year', 'Run', 'ID', 'Age'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['RES - median', 'RES - 25%', 'RES - 75%',
                                                                  'ELC - median', 'ELC - 25%', 'ELC - 75%',
                                                                  'MAN - median', 'MAN - 25%', 'MAN - 75%'])

    for i in range(80):
        # Renewables
        if i in df_phi_res.index.levels[0]:
            tmpRES = []
            for run in df_phi_res.loc[i].index.levels[0]:
                tmpAge = df_phi_res.loc[i].loc[run].index.get_level_values('Age').max()
                tmpDf = df_phi_res.loc[i].loc[run]['Return on Investment']
                tmpRES.append(tmpDf[tmpDf.index.get_level_values('Age') == tmpAge].median())
            df_plot.loc[i, 'RES - median'] = np.median(tmpRES) * 100
            df_plot.loc[i, 'RES - 25%'] = np.quantile(tmpRES, 0.25) * 100
            df_plot.loc[i, 'RES - 75%'] = np.quantile(tmpRES, 0.75) * 100
        # ELectrolyzers
        if i in df_phi_elc.index.levels[0]:
            tmpELC = []
            for run in df_phi_elc.loc[i].index.levels[0]:
                tmpAge = df_phi_elc.loc[i].loc[run].index.get_level_values('Age').max()
                tmpDf = df_phi_elc.loc[i].loc[run]['Return on Investment']
                tmpELC.append(tmpDf[tmpDf.index.get_level_values('Age') == tmpAge].median())
            df_plot.loc[i, 'ELC - median'] = np.median(tmpELC) * 100
            df_plot.loc[i, 'ELC - 25%'] = np.quantile(tmpELC, 0.25) * 100
            df_plot.loc[i, 'ELC - 75%'] = np.quantile(tmpELC, 0.75) * 100
        # Manufacturings
        if i in df_phi_man.index.levels[0]:
            tmpMAN = []
            for run in df_phi_man.loc[i].index.levels[0]:
                tmpAge = df_phi_man.loc[i].loc[run].index.get_level_values('Age').max()
                tmpDf = df_phi_man.loc[i].loc[run]['Return on Investment']
                tmpMAN.append(tmpDf[tmpDf.index.get_level_values('Age') == tmpAge].median())
            df_plot.loc[i, 'MAN - median'] = np.median(tmpMAN) * 100
            df_plot.loc[i, 'MAN - 25%'] = np.quantile(tmpMAN, 0.25) * 100
            df_plot.loc[i, 'MAN - 75%'] = np.quantile(tmpMAN, 0.75) * 100


    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_ylabel('Return on Investment [%]')
    ax1.set_xlabel('Year')

    # Renewables
    ax1.plot(x, df_plot['RES - median'], label='Renewables', linestyle='-', color=green)
    ax1.fill_between(x, df_plot['RES - 25%'], df_plot['RES - 75%'], color=green, alpha=0.25, edgecolor='none')
    # Electrolyzers
    ax1.plot(x, df_plot['ELC - median'], label='Electrolyzers', linestyle='-', color=blue)
    ax1.fill_between(x, df_plot['ELC - 25%'], df_plot['ELC - 75%'], color=blue, alpha=0.25, edgecolor='none')
    # Manufacturings
    ax1.plot(x, df_plot['MAN - median'], label='Manufacturings', linestyle='-', color=purple)
    ax1.fill_between(x, df_plot['MAN - 25%'], df_plot['MAN - 75%'], color=purple, alpha=0.25, edgecolor='none')

    ax1.plot(x, np.ones(80), color=grey)

    ax1.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False, ncol=3)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_return_on_investment_old.' + plot_type, bbox_inches='tight')


def plot_return_on_investment_agents(df_pp, df_hp, df_ep):
    '''
    Function that will create a plot of the return on investment for power producers, hydrogen producers and
    electrolyzer producers.
    :param:
        pd.DataFrame df_pp: Yearly data for the power producers
        pd.DataFrame df_hp: Yearly data for the hydrogen producers
        pd.DataFrame df_ep: Yearly data for the electrolyzer producers
    :return:
    '''
    df_phi_pp = df_pp.set_index(['Year', 'Run', 'ID'])
    df_phi_hp = df_hp.set_index(['Year', 'Run', 'ID'])
    df_phi_ep = df_ep.set_index(['Year', 'Run', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['PP - median', 'PP - 25%', 'PP - 75%',
                                                                  'HP - median', 'HP - 25%', 'HP - 75%',
                                                                  'EP - median', 'EP - 25%', 'EP - 75%'])

    for i in range(80):
        # Power Producers
        if i in df_phi_pp.index.levels[0]:
            tmp_df = df_phi_pp.loc[i]['Return on Investment'].groupby(level=0).median()
            df_plot.loc[i, 'PP - median'] = tmp_df.median() * 100
            df_plot.loc[i, 'PP - 25%'] = tmp_df.quantile(q=0.25) * 100
            df_plot.loc[i, 'PP - 75%'] = tmp_df.quantile(q=0.75) * 100
        # Hydrogen Producers
        if i in df_phi_hp.index.levels[0]:
            tmp_df = df_phi_hp.loc[i]['Return on Investment'].groupby(level=0).median()
            df_plot.loc[i, 'HP - median'] = tmp_df.median() * 100
            df_plot.loc[i, 'HP - 25%'] = tmp_df.quantile(q=0.25) * 100
            df_plot.loc[i, 'HP - 75%'] = tmp_df.quantile(q=0.75) * 100
        # Electrolyzers Producers
        if i in df_phi_ep.index.levels[0]:
            tmp_df = df_phi_ep.loc[i]['Return on Investment'].groupby(level=0).median()
            df_plot.loc[i, 'EP - median'] = tmp_df.median() * 100
            df_plot.loc[i, 'EP - 25%'] = tmp_df.quantile(q=0.25) * 100
            df_plot.loc[i, 'EP - 75%'] = tmp_df.quantile(q=0.75) * 100

    fig, ax1 = plt.subplots(figsize=plot_settings['figsize'], gridspec_kw=plot_settings['gridspec_kw'],
                            dpi=plot_settings['dpi'])

    ax1.set_ylabel('Return on Investment [%]')
    ax1.set_xlabel('Year')

    # Power Producers
    ax1.plot(x, df_plot['PP - median'], label='Power Producers', linestyle='-', color=green)
    ax1.fill_between(x, df_plot['PP - 25%'], df_plot['PP - 75%'], color=green, alpha=0.25, edgecolor='none')
    # Hydrogen Producers
    ax1.plot(x, df_plot['HP - median'], label='Hydrogen Producers', linestyle='-', color=blue)
    ax1.fill_between(x, df_plot['HP - 25%'], df_plot['HP - 75%'], color=blue, alpha=0.25, edgecolor='none')
    # Electrolyzer Producers
    ax1.plot(x, df_plot['EP - median'], label='Electrolyzers Producers', linestyle='-', color=purple)
    ax1.fill_between(x, df_plot['EP - 25%'], df_plot['EP - 75%'], color=purple, alpha=0.25, edgecolor='none')

    ax1.plot(x, np.ones(80)*7, color=orange, linestyle='-.')

    ax1.legend(loc=plot_settings['loc'], bbox_to_anchor=(-0.05, -0.25), frameon=False, ncol=3)

    plt.xlim(plot_settings['xlim'])
    plt.ylim([-1, 50])
    plt.savefig(os.getcwd() + '\\plot_return_on_investment_agents.' + plot_type, bbox_inches='tight')


def plot_capacity_extension(df_pm, df_hm, df_em):
    '''
    Function that will create a plot of the capacity expension for renewables, electrolyzers and manufacturings.
    :param:
        pd.DataFrame df_pm: Yearly data for the Power market
        pd.DataFrame df_hm: Yearly data for the Hydrogen market
        pd.DataFrame df_em: Yearly data for the Electrolyzer market
    :return:
    '''
    df_phi_pm = df_pm.set_index(['Year', 'Run'])
    df_phi_hm = df_hm.set_index(['Year', 'Run'])
    df_phi_em = df_em.set_index(['Year', 'Run'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['RES - median', 'RES - 25%', 'RES - 75%',
                                                                  'ELC - median', 'ELC - 25%', 'ELC - 75%',
                                                                  'MAN - median', 'MAN - 25%', 'MAN - 75%'])

    for i in range(80):
        # Power market
        if i in df_phi_pm.index.levels[0]:
            tmp_df = df_phi_pm.loc[i]['Added capacity Renewables']
            df_plot.loc[i, 'RES - median'] = tmp_df.median()
            df_plot.loc[i, 'RES - 25%'] = tmp_df.quantile(q=0.25)
            df_plot.loc[i, 'RES - 75%'] = tmp_df.quantile(q=0.75)
        # Hydrogen market
        if i in df_phi_hm.index.levels[0]:
            tmp_df = df_phi_hm.loc[i]['Added capacity Electrolyzers']
            df_plot.loc[i, 'ELC - median'] = tmp_df.median()
            df_plot.loc[i, 'ELC - 25%'] = tmp_df.quantile(q=0.25)
            df_plot.loc[i, 'ELC - 75%'] = tmp_df.quantile(q=0.75)
        # Electrolyzer market
        if i in df_phi_em.index.levels[0]:
            tmp_df = df_phi_em.loc[i]['Added capacity Manufacturings']
            df_plot.loc[i, 'MAN - median'] = tmp_df.median()
            df_plot.loc[i, 'MAN - 25%'] = tmp_df.quantile(q=0.25)
            df_plot.loc[i, 'MAN - 75%'] = tmp_df.quantile(q=0.75)

    fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=plot_settings['figsize'],
                                        gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'], sharex=True)

    # Renewables
    ax1.plot(x, df_plot['RES - median']/1e3, label='Renewables', linestyle='-', color=green)
    ax1.fill_between(x, df_plot['RES - 25%']/1e3, df_plot['RES - 75%']/1e3, color=green, alpha=0.25, edgecolor='none')
    ax1.set_ylabel('[GW]')

    # Electrolyzers
    ax2.plot(x, df_plot['ELC - median']/1e3, label='Electrolyzers', linestyle='-', color=blue)
    ax2.fill_between(x, df_plot['ELC - 25%']/1e3, df_plot['ELC - 75%']/1e3, color=blue, alpha=0.25, edgecolor='none')
    ax2.set_ylabel('[GW]')

    # Manufacturings
    ax3.plot(x, df_plot['MAN - median']/1e3, label='Manufacturings', linestyle='-', color=purple)
    ax3.fill_between(x, df_plot['MAN - 25%']/1e3, df_plot['MAN - 75%']/1e3, color=purple, alpha=0.25, edgecolor='none')
    ax3.set_ylabel('[GW/year]')
    ax3.set_xlabel('Year [-]')
    ax3.set_xlim(plot_settings['xlim'])

    # Legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles3, labels3 = ax3.get_legend_handles_labels()

    handles = handles1 + handles2 + handles3
    labels = labels1 + labels2 + labels3

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower left', bbox_to_anchor=(-0.05, -0.85),
               frameon=False, ncol=3)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_capacity_extension.' + plot_type, bbox_inches='tight')


def plot_capacity_extension_max(df_pp, df_hp, df_ep):
    '''
    Function that will create a plot of the maximum capacity expension for renewables, electrolyzers and manufacturings
    by one agent.
    :param:
        pd.DataFrame df_pp: Yearly data for the power producers.
        pd.DataFrame df_hp: Yearly data for the hydrogen producers
        pd.DataFrame df_ep: Yearly data for the electrolyzr producers
    :return:
    '''
    df_phi_pp = df_pp.set_index(['Year', 'Run', 'ID'])
    df_phi_hp = df_hp.set_index(['Year', 'Run', 'ID'])
    df_phi_ep = df_ep.set_index(['Year', 'Run', 'ID'])
    df_plot = pd.DataFrame(data=np.nan, index=range(80), columns=['RES - median', 'RES - 25%', 'RES - 75%',
                                                                  'ELC - median', 'ELC - 25%', 'ELC - 75%',
                                                                  'MAN - median', 'MAN - 25%', 'MAN - 75%'])

    for i in range(80):
        # Renewables
        if i in df_phi_pp.index.levels[0]:
            tmp_df = df_phi_pp.loc[i]['Added capacity Renewables'].groupby(level=0).max()
            df_plot.loc[i, 'RES - median'] = tmp_df.median()
            df_plot.loc[i, 'RES - 25%'] = tmp_df.quantile(q=0.25)
            df_plot.loc[i, 'RES - 75%'] = tmp_df.quantile(q=0.75)
        # Electrolyzerse
        if i in df_phi_hp.index.levels[0]:
            tmp_df = df_phi_hp.loc[i]['Added capacity Electrolyzers'].groupby(level=0).max()
            df_plot.loc[i, 'ELC - median'] = tmp_df.median()
            df_plot.loc[i, 'ELC - 25%'] = tmp_df.quantile(q=0.25)
            df_plot.loc[i, 'ELC - 75%'] = tmp_df.quantile(q=0.75)
        # Renewables
        if i in df_phi_ep.index.levels[0]:
            tmp_df = df_phi_ep.loc[i]['Added capacity Manufacturings'].groupby(level=0).max()
            df_plot.loc[i, 'MAN - median'] = tmp_df.median()
            df_plot.loc[i, 'MAN - 25%'] = tmp_df.quantile(q=0.25)
            df_plot.loc[i, 'MAN - 75%'] = tmp_df.quantile(q=0.75)

    fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=plot_settings['figsize'],
                                        gridspec_kw=plot_settings['gridspec_kw'], dpi=plot_settings['dpi'], sharex=True)

    # Renewables
    ax1.plot(x, df_plot['RES - median'] / 1e3, label='Renewables', linestyle='-', color=green)
    ax1.fill_between(x, df_plot['RES - 25%'] / 1e3, df_plot['RES - 75%'] / 1e3, color=green, alpha=0.25,
                     edgecolor='none')
    ax1.set_ylabel('[GW]')

    # Electrolyzers
    ax2.plot(x, df_plot['ELC - median'] / 1e3, label='Electrolyzers', linestyle='-', color=blue)
    ax2.fill_between(x, df_plot['ELC - 25%'] / 1e3, df_plot['ELC - 75%'] / 1e3, color=blue, alpha=0.25,
                     edgecolor='none')
    ax2.set_ylabel('[GW]')

    # Manufacturings
    ax3.plot(x, df_plot['MAN - median'] / 1e3, label='Manufacturings', linestyle='-', color=purple)
    ax3.fill_between(x, df_plot['MAN - 25%'] / 1e3, df_plot['MAN - 75%'] / 1e3, color=purple, alpha=0.25,
                     edgecolor='none')
    ax3.set_ylabel('[GW/year]')
    ax3.set_xlabel('Year [-]')
    ax3.set_xlim(plot_settings['xlim'])

    # Legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles3, labels3 = ax3.get_legend_handles_labels()

    handles = handles1 + handles2 + handles3
    labels = labels1 + labels2 + labels3

    tmpUnique = dict(zip(labels, handles))
    plt.legend(tmpUnique.values(), tmpUnique.keys(), loc='lower left', bbox_to_anchor=(-0.05, -0.85),
               frameon=False, ncol=3)

    plt.xlim(plot_settings['xlim'])
    plt.savefig(os.getcwd() + '\\plot_capacity_extension_max.' + plot_type, bbox_inches='tight')


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
    print('Check and load data for multiple runs...')
    check_data()
    tmp_list = load_data()
    df_pm, df_hm, df_em = tmp_list[8], tmp_list[4], tmp_list[1]
    df_pm_daily, df_hm_daily = tmp_list[7], tmp_list[3]
    df_pp, df_hp, df_ep = tmp_list[9], tmp_list[5], tmp_list[2]
    df_sale = tmp_list[-1]
    df_res, df_elc, df_man = tmp_list[10], tmp_list[0], tmp_list[6]

    # Debug
    plot_best_profitability(df_pp, df_hp, df_ep)
    plot_weighted_return_on_investment_all(df_res, df_elc, df_man)
    return(123)
    #exit(12438934)

    # Create all plots
    print('Create plots for multiple runs...')
    plot_no_of_agents(df_pm, df_hm, df_em)
    plot_no_of_investment(df_pm, df_hm, df_em)
    plot_ratio_investment_agents(df_pm, df_hm, df_em)
    plot_installed_cap_res(df_pm)
    plot_installed_cap_elc(df_hm)
    plot_installed_cap_man(df_em)
    plot_installed_cap_all(df_pm, df_hm, df_em)
    plot_capacity_extension(df_pm, df_hm, df_em)
    plot_capacity_extension_max(df_pp, df_hp, df_ep)
    plot_electricity_production(df_pm_daily)
    plot_electricity_production_share(df_pm_daily)
    plot_electricity_production_excess(df_pm_daily)
    plot_hydrogen_production(df_hm, df_hm_daily)
    plot_utilization_elc(df_hm_daily)
    plot_utilization_all(df_res, df_elc, df_ep)
    plot_utilization_elc_res(df_res, df_elc)
    #plot_weighted_utilization_all(df_res, df_elc, df_man)
    #plot_duration_curves_res(df_pm, df_pm_daily)
    #plot_duration_curves_elc(df_hm_daily)
    plot_load_type_elc(df_pm, df_hm)
    plot_p_elc_vs_lcoe(df_pm)
    plot_p_h2_vs_lcoh(df_hm)
    plot_p_elc_vs_p_h2(df_pm, df_hm)
    plot_p_elc_ave_vs_lcoe_ave(df_ep, df_sale)
    plot_p_elc_vs_c_elc(df_sale)
    plot_investment_threshold_pp(df_pp, df_pm)
    plot_investment_threshold_hp(df_hp, df_hm)
    plot_investment_threshold_ep(df_ep, df_em)
    plot_weighted_investment_threshold_pp(df_pp, df_pm)
    plot_weighted_investment_threshold_hp(df_hp, df_hm)
    plot_weighted_investment_threshold_ep(df_ep, df_em)
    plot_age_res(df_res)
    plot_age_elc(df_elc)
    plot_age_man(df_man)
    plot_weighted_age_res(df_res)
    plot_weighted_age_elc(df_elc)
    plot_weighted_age_man(df_man)
    plot_profitability(df_pp, df_hp, df_ep)
    plot_profitability_min_max(df_pp, df_hp, df_ep)
    plot_weighted_profitability(df_pp, df_hp, df_ep)
    plot_liquidity_pp(df_pp)
    plot_liquidity_hp(df_hp)
    plot_liquidity_ep(df_ep)
    plot_w2p_elc_vs_c_elc(df_hp, df_hm, df_man)
    plot_w2p_elc_vs_c_elc_vs_p_elc(df_sale)
    plot_w2p_elc_spec_cashflow_investment_threshold(df_hp, df_hm)
    plot_final_p_elc(df_sale)
    plot_p_elc(df_pm)
    plot_p_h2(df_hm)
    #plot_cashflow_system(df_pm_daily, df_hp, df_ep)
    plot_best_profitability(df_pp, df_hp, df_ep)
    plot_return_on_investment_agents(df_pp, df_hp, df_ep)
    plot_return_on_investment_all(df_res, df_elc, df_man)
    plot_weighted_return_on_investment_all(df_res, df_elc, df_man)
    print('Done.')


if __name__ == '__main__':
    # Debuging only
    dir = 'D:\\Jesse\\sciebo\\00_Promotion\\06_Model\\02_ABM\\02_NetLogo\\02_Output\\2025-04-16-19-59\\Sensitivity_1\\'
    main(dir)
