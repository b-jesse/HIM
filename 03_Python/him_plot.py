'''
him - Hydrogen Investment Model
This script will take the results and create all plots

version: 0.1.24.07.31
date: 2024-07-31
author: Jesse

changelog:
0.1.24.07.31 - start new script
'''

# import
import os, warnings, multiprocessing, sys
import matplotlib.pyplot as plt
import him_plot_single as him_single
import him_plot_multi as him_multi
import him_plot_sens as him_sens

# global
global ListOutdir
global ResultDir
global NoConCurrentRuns

ListOutdir = ['2025-11-24-17-23']
ResultDir = 'D:\\USER\\ABM\\02_Output' # CHANGE THIS
NoConCurrentRuns = 28

def main():
    # Supress all warnings
    warnings.filterwarnings('ignore')

    print('him - Hydrogen Investment Model')
    print('Postprocessing: Creating plots')
    print('This might take a while...')

    # Check if single plots needs to be created
    BoolSingle = True
    if len(sys.argv) > 1:
        print('Setting if single plots needs to be created:')
        BoolSingle = sys.argv[1].lower()
        if BoolSingle in ['true', 't', 'y', 'yes']:
            print('Will create single plots')
            BoolSingle = True
        else:
            print('Will NOT create single plots')
            BoolSingle = False

    # Move to the right folder
    os.chdir(ResultDir)
    # Go thru all Outdirs
    for OutDir in ListOutdir:
        try:
            os.chdir(OutDir)
        except FileNotFoundError:
            print('Error in main: Results folder ' + OutDir + ' does not exist.')
            exit(100)

        # Sensitivity plots (if necessary)
        if os.path.isfile('sensitivity.config'):
            SensDir = os.getcwd()
            him_sens.main(SensDir)

            # Close plots
            plt.close('all')

        # Multi plots
        for SensDir in os.listdir(os.getcwd()):
            if SensDir.startswith('Sensitivity_'):
                print('Creating plots for ' + str(SensDir) + '...')
                os.chdir(SensDir)
                MultiDir = os.getcwd()
                him_multi.main(MultiDir)

                # Close plots
                plt.close('all')

                # Single plots
                ListRunDir = []
                for RunDir in os.listdir(os.getcwd()):
                    if RunDir.startswith('Run_'):
                        ListRunDir.append(RunDir)
                if BoolSingle:
                    with multiprocessing.Pool(processes=NoConCurrentRuns) as pool:
                        pool.map(create_plot_single, ListRunDir)

                # Move a folder back
                os.chdir(os.path.dirname(MultiDir))

        # Move back to the results folder
        os.chdir(ResultDir)


def create_plot_single(RunDir):
    '''
    Calls the function to create plots for a single run
    :param:
        str RunDir: Name of the results folder for the run
    :return:
    '''
    # Supress all warnings
    warnings.filterwarnings('ignore')

    # Create the plots
    print('Creating plots for ' + str(RunDir) + '...')
    os.chdir(RunDir)
    CurrentDir = os.getcwd()
    him_single.main(CurrentDir)

    # Close plots
    plt.close('all')

    # Move a folder back
    os.chdir(os.path.dirname(CurrentDir))


if __name__ == '__main__':
    main()
