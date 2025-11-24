'''
him - Hydrogen Investment Model
This script will read the runs.init and runs the model with the given settings

version: 0.1.24.08.10
date: 2024-08-10
author: Jesse

changelog:
0.1.24.07.03 - feature complete
0.1.24.08.08 - fixed a bug that prevented to set meta.run and meta.run_no with pynetlogo
0.1.24.08.10 - fixed a bug in creating the sensitivity file, parameters now seperated by comma
'''

# import
import os, pynetlogo, multiprocessing, shutil
import pandas as pd
import numpy as np
from datetime import datetime
from SALib.sample import sobol as sobolsample

# globals
# Default paths - may need adjustment
global jvm_file
global netlogo_file
global scenario_settings
global run_settings
global sensitivity_settings

jvm_file = 'C:/Users/openJDK/jdk-22.0.1/bin/server/jvm.dll' # CHANGE THIS
netlogo_file = 'C:/Program Files/NetLogo 6.4.0' # CHANGE THIS

scenario_settings = ['ref', 'co2_tax', 'h2_subsidy', 'h2_guarant', 'res_subsidy', 'power_subsidy', 'power_guarant',
                     'elc_subsidy', 'elc_guarant', 'man_subsidy', 'time_lag']
run_settings = ['plot', 'write', 'debug', 'track']
sensitivity_settings = ['const.beta', 'const.PM.delta_threshold', 'const.HM.delta_threshold',
                        'const.EM.delta_threshold', 'const.gamma', 'init.HM.threshold_0', 'init.EM.threshold_0',
                        'const.EM.inexperience_penalty_max', 'const.MAN.learning_rate', 'const.EM.global_share',
                        'GOV.h2_subsidy', 'GOV.h2_guarant', 'GOV.res_subsidy', 'GOV.power_subsidy', 'GOV.power_guarant',
                        'GOV.elc_subsidy', 'GOV.elc_guarant', 'GOV.man_subsidy']

def check_model():
    '''
    Function to check if the model is at the right location
    :return:
        str modeldir: location of the model
    '''
    wkdir = os.getcwd()
    modeldir = os.path.dirname(wkdir)
    for i in ['class.nls', 'func.nls', 'main.nlogo', 'plot.nls', 'setup.nls', 'write.nls']:
        try:
            os.path.isfile(str(modeldir + '/' + i))
        except OSError:
            print(str('Error in check_model: Model file ' + i + 'not found.'))
            exit(100)

    try:
        os.path.isfile(jvm_file)
    except OSError:
        print(str('Error in check_model: Java file not found.'))
        exit(101)

    try:
        os.path.isdir(netlogo_file)
    except OSError:
        print(str('Error in check_model: Netlogo file not found.'))
        exit(102)

    return(modeldir)

def load_init():
    '''
    Function to load the init file for the runs of the model
    :return:
        int no_runs : Number of runs
        int concurrent_runs : Number of concurrent runs
        dict scenario : Settings for scenario
        dict settings : Settings for model
        dict sensitivity : Settings for sensitivity analysis
    '''
    # Initialize output
    scenario = {}
    settings = {}
    sensitivity = {}
    sensitivity_variables = []

    # Check if runs.init exists
    try:
        os.path.isfile(str(os.getcwd()+'/runs.init'))
    except OSError:
        print('Error: runs.init file not found.')
        exit(200)

    # Load file
    with open(str(os.getcwd() + '/runs.init')) as init_file:
        for line in init_file.readlines():
            if line.strip() and line[0] != '#':
                line = line.replace(' ', '').replace('\n', '').split(':')

                # Runs setting
                if line[0] == 'runs':
                    try:
                        no_runs = int(line[1])
                    except TypeError:
                        print('Error in load_init: Unknown type while loading init file.')
                        exit(201)
                elif line[0] == 'concurrent_runs':
                    try:
                        no_conruns = int(line[1])
                    except TypeError:
                        print('Error in load_init: Unknown type while loading init file.')
                        exit(202)
                elif line[0] in run_settings:
                    try:
                        settings[line[0]] = eval(line[1].capitalize())
                    except TypeError:
                        print('Error in load_init: Unknown type while loading init file.')
                        exit(203)
                elif line[0] in scenario_settings:
                    try:
                        scenario[line[0]] = eval(line[1].capitalize())
                    except TypeError:
                        print('Error in load_init: Unknown type while loading init file.')
                        exit(204)
                elif line[0] == 'sensitivity':
                    try:
                        sensitivity_type = str(line[1].capitalize())
                    except TypeError:
                        print('Error in load_init: Unknown type while loading init file.')
                        exit(205)
                    if sensitivity_type not in ['None', 'Single', 'Sobol']:
                        print('Error in load_init: Unknown type for sensitivity.')
                        exit(206)
                elif line[0] == 'parameters' and sensitivity_type != 'None':
                    try:
                        if sensitivity_type in ['Single']:
                            sensitivity_variables = [line[1][1:-1].split(',')[0]]
                        else:
                            sensitivity_variables = line[1][1:-1].split(',')
                    except TypeError:
                        print('Error in load_init: Unknown type while loading init file.')
                        exit(207)
                elif line[0] in sensitivity_settings:
                    if line[0] not in sensitivity.keys():
                        try:
                            sensitivity[line[0]] = eval(line[1])
                        except TypeError:
                            print('Error in load_init: Unknown type while loading init file.')
                            exit(208)
                    else:
                        if line[0] in sensitivity_variables:
                            try:
                                sensitivity[line[0]] = eval(line[1])
                            except TypeError:
                                print('Error in load_init: Unknown type while loading init file.')
                                exit(209)

    # Close file when done
    init_file.close()

    # Return
    return(no_runs, no_conruns, settings, scenario, sensitivity_type, sensitivity_variables, sensitivity)

def create_sensitivity_file(out_dir, sens_type, sens_var, no_sens, sensitivity):
    '''
    Function to create the sensitivity file for the post processing.
    :param:
        str out_dir: Name of the output folder
    :return:
    '''
    # Create the file
    config = str('# Sensitivity settings\n')
    config += str('type: ' + str(sens_type) + '\n')
    config += str('parameters: [')
    for i in sens_var:
        if i not in sens_var[-1]:
            config += str(i + ', ')
        else:
            config += str(i + ']\n')
    config += str('sensitivity_runs: ' + str(no_sens) + '\n')
    i = 1
    while i <= no_sens:
        config += str('sensitivity_' + str(i) + ': ' + str(sensitivity.loc[i-1].to_list()) + '\n')
        i += 1
    config += str('# End of file')

    # Write file
    out_file = str(os.path.dirname(os.getcwd()) + '\\02_Output\\' + out_dir + '\\sensitivity.config')
    with open(out_file, 'w') as file:
        file.write(config)


def create_sensitivity(s_names, s_dict, no_sens_runs=11):
    '''
    Function to create the sensitivity analysis parameter, depending on the sensitivity type
    :param:
        list s_names: Type of sensitivity analysis
        dict s_dict: Sensitivity analysis parameters
        int no_sens_runs: Number of sensitivity runs (default = 11)
    :return:
        pd.DataFrame sensitivity: Sobol sensitivity analysis parameters
    '''
    # Create Problem
    problem = {
        'num_vars': len(s_names),
        'name': s_names
    }
    tmp_bounds = []
    for i in s_names:
        try:
            tmp_bounds.append(s_dict[i])
        except TypeError:
            print('Error in create_sensitivity: Parameter not found in sensitivity dict.')
            exit(300)
    problem['bounds'] = tmp_bounds

    # Create parameter values sensitivity analysis
    if len(s_names) == 0:
        param_values = []
    elif len(s_names) < 2:
        param_values = []
        for i in np.linspace(tmp_bounds[0][0], tmp_bounds[0][1], no_sens_runs):
            param_values.append([round(i, 5)])
    else:
        tmp_sens_runs = 2 ** round(np.log2(no_sens_runs))  # Ensure no of runs is a 2^x number
        param_values = sobolsample.sample(problem, tmp_sens_runs, calc_second_order=True)

    # Put everything into a pd.DataFrame
    sensitivity = pd.DataFrame(param_values, columns=s_names)

    return sensitivity


def create_out_folder():
    '''
    Function that will create the output folder, named on the current date and time. It also returns the name of the new
    folder.
    :return:
        str date: Name of the output folder
    '''
    wkdir = os.getcwd()
    date = datetime.now().strftime('%Y-%m-%d-%H-%M')
    outdir = os.path.dirname(wkdir) + '\\02_Output\\' + date + '\\'

    if not os.path.isdir(outdir):
        os.mkdir(outdir)
    else:
        print('Error in create_out_folder: Folder already exists.')
        exit(400)

    return(date)


def create_sens_folder(out_dir, no_sens):
    '''
    Function that will create the sensitivity folder, numerated by the number of sensitivity settings.
    :param:
        str out_dir: name of the output folder
        int no_sens: number of the current sensitivity settings
    :return:
        str sens_dir: name of the sensitivity folder
    '''
    wkdir = os.getcwd()
    sensdir = (os.path.dirname(wkdir) + '\\02_Output\\' + out_dir + '\\Sensitivity_' + str(no_sens)
               + '\\')

    if not os.path.isdir(sensdir):
        os.mkdir(sensdir)
    else:
        print('Error in create_sens_folder: Folder already exists.')
        exit(500)

    return sensdir


def create_model_config(sens_dir, settings, scenario, sens, run_no):
    '''
    Function that will create the model.config file, which is needed to run the model and includes all settings for the
    scenario and the sensitivity analysis.
    :param:
        str sens_dir: Path ouf the individual run folder
        dict settings: Dictionary of setting parameters
        dict scenario: Dictionary of scenario parameters
        dict sens: Dictionary of sensitivity analysis parameters
        int run_no: Number of the current run
    :return:
        str run_name: Name of the run
    '''

    run_name = ''
    if scenario['ref']:
        run_name += 'Reference'
    else:
        run_name += 'Strategic'
    if scenario['time_lag']:
        run_name += 'TimeLag'
    if scenario['co2_tax']:
        run_name += 'Co2'
    if scenario['h2_subsidy']:
        run_name += 'H2Sub'
    if scenario['h2_guarant']:
        run_name += 'H2Guarant'
    if scenario['res_subsidy']:
        run_name += 'RESSub'
    if scenario['power_subsidy']:
        run_name += 'PowerSub'
    if scenario['power_guarant']:
        run_name += 'PowerGuarant'
    if scenario['elc_subsidy']:
        run_name += 'ELCSub'
    if scenario['elc_guarant']:
        run_name += 'ELCGuarant'
    if scenario['man_subsidy']:
        run_name += 'MANSub'

    config = str('### NETLOGO ABM MODEL CONFIG\n')

    config += str('### GENERAL SETTINGS\n')
    config += str('run: ' + run_name + '\n')
    config += str('run_no: ' + str(run_no) + '\n')
    config += str('run_path: ' + sens_dir.replace('\\', '/') + '\n')
    for i in settings.keys():
        config += str('settings.' + i + ': ' + str(settings[i]) + '\n')

    config += str('\n### SCENARIO SETTINGS\n')
    for i in scenario.keys():
        config += str('scenario.' + i + ': ' + str(scenario[i]) + '\n')

    config += str('\n### SENSITIVITY SETTINGS\n')
    for i in sens.keys():
        config += str(i + ': ' + str(sens[i]) + '\n')

    filename = str(sens_dir + 'model.config')
    try:
        with open(filename, 'w') as file:
            file.write(config)
            file.close()
    except FileExistsError:
        print('Error in create_model_config: File already exists.')
        exit(600)

    return(run_name)


def create_run_folder(sens_dir, run_no):
    '''
    Function that will create the run folder, named on the current run and sensitivity settings.
    :param:
        str sens_dir: Path of the current sensitivity folder
        int run_no: Number of the current run
    :return:
        str run_dir: Path of the run folder
    '''
    run_dir = sens_dir + 'Run_' + str(run_no) + '\\'

    if not os.path.isdir(run_dir):
        os.mkdir(run_dir)
    else:
        print('Error in create_run_folder: Folder already exists.')
        exit(700)

    return run_dir


def run_model(run_name, run_no, run_dir):
    '''
    Function that will run the model.
    :param:
        str run_name: Name of the run
        int run_no: Number of the run
        str run_dir: Path to the output folder
    :return:
        bool -: True if everything works out
    '''

    # Output so people know it's still running
    print('Run ' + str(run_no) + ' is running...')

    # Clear model
    netlogo.command('setup-meta')

    # Set meta values in the model
    tmpName = str('set meta.run "' + run_name + '"')
    tmpNO = str('set meta.run_no ' + str(run_no))
    tmpDir = str('set meta.run_path "' + run_dir.replace('\\', '/') + '"')
    netlogo.command(tmpName)
    netlogo.command(tmpNO)
    netlogo.command(tmpDir)

    # Setup the model
    netlogo.command('setup')

    # Run model for 80 year
    ticks = 81
    netlogo.repeat_command('go', ticks)

    return(True)


def initializer(model_file):
    '''
    Function that will initialize the model.
    :param:
        str model_file: Filepath for the model to run
    :return:
    '''

    global netlogo
    netlogo = pynetlogo.NetLogoLink(netlogo_home=netlogo_file, jvm_path=jvm_file, gui=False)
    netlogo.load_model(model_file)


def main():
    # List of experiments
    experiment = pd.DataFrame(columns=['Name', 'No', 'Path'])

    # Check if model ok
    model_dir = check_model()
    model_dir += '\\main.nlogo'

    # Load the run.init file
    init = load_init()
    no_runs, no_conruns, settings, scenario, sens_type, sens_var, sens = (init[0], init[1], init[2], init[3], init[4],
                                                                          init[5], init[6])

    # Create Output folder
    out_dir = create_out_folder()

    # Create different settings - not necessary for single_run
    sensitivity = create_sensitivity(sens_var, sens)

    # Create Settings folder
    no_sens = len(sensitivity)
    # Fix for no sensitivity analysis
    if no_sens < 1:
        no_sens = 1
    i = 1
    while i <= no_sens:
        sens_dir = create_sens_folder(out_dir, i)
        for j in sens_var:
            sens[j] = sensitivity.iloc[i-1][j]

        j = 1
        while j <= no_runs:
            # Create Run folders and model.config
            run_dir = create_run_folder(sens_dir, j)
            run_name = create_model_config(run_dir, settings, scenario, sens, j)

            # Add current run to the list of all experiments
            experiment.loc[len(experiment)] = {'Name': run_name, 'No': j, 'Path': run_dir}

            j += 1
        i += 1

    # Copy run.init file to folder
    init_file = str(os.getcwd() + '\\runs.init')
    out_file = str(os.path.dirname(os.getcwd()) + '\\02_Output\\' + out_dir + '\\runs.init')
    shutil.copy(init_file, out_file)

    # Create sensitivity.config
    if len(sensitivity) > 0:
        create_sensitivity_file(out_dir, sens_type, sens_var, no_sens, sensitivity)

    # Calculation with multiprocessing
    with multiprocessing.Pool(no_conruns, initializer=initializer, initargs=(model_dir,)) as executor:
        results = []
        for entry in executor.starmap(run_model, experiment.values.tolist()):
            results.append(entry)
        results = pd.DataFrame(results)

    print('done')


if __name__ == '__main__':
    main()

