<a href="https://www.fz-juelich.de/en/ice/ice-2"><img src="https://github.com/FZJ-IEK3-VSA/README_assets/blob/main/JSA-Header.svg?raw=True" alt="Forschungszentrum Juelich Logo" width="300px"></a>
<a href="https://www.uu.nl/en"><img src="https://www.uu.nl/themes/custom/corp/src/images/uu-logo-en.svg" alt="Utrecht University Logo" width="300px"></a>
# HIM - Hydrogen Investment Model
HIM is an agent-based model for investment decisions in the German electricity and green hydrogen sectors. The included scripts allow the model to run without the GUI of Netlogo and multiple runs in parallel. It allows to generate the results from our paper `Exploring the Scale-up of a Green Hydrogen Industry: An Agent-Based Modeling Approach` in the International Journal for Hydrogen Energy. 
<img src="https://jugit.fz-juelich.de/b.jesse/him/-/raw/main/Figure-1.png" alt="Model overview" width="600px">
The model itself is written for [NetLogo v.6.4.0](https://www.netlogo.org/). Pre- and postprocessing scripts are written in python.
If you want to use HIM in a published work, please use the following citation:
`Jesse et al. 2025, Exploring the Scale-up of a Green Hydrogen Industry: An Agent-Based Modeling Approach. International Journal for Hydrogen Energy 2025 (in progress)`
## Installation
- Install [NetLogo v6.4.0](https://ccl.northwestern.edu/netlogo/oldversions.shtml)
- Install the [conda distribution](https://conda-forge.org/) of your choice (if you do not have it already)
- Install [OpenJDK 22.0.1](https://jdk.java.net/archive/)
- Create a new environment with `conda create -n myenv python=3.11.5`
- Activate your new environment with `conda activate myenv`
- The list of required packages can be found in `00_Setup`
### If you want to recreate the results from our paper:
- Install needed packages with `pip install -r requirements_results.txt`
### If you want to develope the model further:
- Install needed packages with `pip install -r requirements.txt`
## Usage
### Prepare Data
- Follow the steps outlined in [Data](#Data) to replace the dummy files in `01_Data`
### Using the standalone model in NetLogo:
- You can just double click on main.nlogo file and use the model with the GUI of NetLogo.
### Using the python scripte:
Make sure that you adjust the paths to your installation of jvm and NetLogo in `him_run_model.py`
- `jvm_file = 'C:/User/openJDK/jdk-22.0.1/bin/server/jvm.dll'`
- `netlogo_file = 'C:/Program Files/NetLogo 6.4.0'`
For running the model:
- Open the consol of your choice (e.g. minipromt)
- Activate your new environment with `conda activate myenv`
- Move to the HIM folder (i.e. `C:\\User\\O3_Python`)
- (optional) adjust settings in the `runs.init` in `03_Python\him` 
- To run model use code `python him_run_model.py`
For the validation of our model:
- Open the consol of your choice (e.g. minipromt)
- Activate your new environment with `conda activate myenv`
- Move to the HIM folder (i.e. `C:\\User\\O3_Python`)
- Follow the instruction in [instruction_validation.mb](https://jugit.fz-juelich.de/b.jesse/him/-/blob/main/00_Setup/instruction_validation.md) in `00_Setup` to create all necessary results
For recreating our results:
- Open the consol of your choice (e.g. minipromt)
- Activate your new environment with `conda activate myenv`
- Move to the HIM folder (i.e. `C:\\User\\O3_Python`)
- Follow the instruction in [instruction_paper.mb](https://jugit.fz-juelich.de/b.jesse/him/-/blob/main/00_Setup/instruction_paper.md) in `00_Setup` to create all necessary results
For postprocessing:
- Open the consol of your choice (e.g. minipromt)
- Activate your new environment with `conda activate myenv`
- Move to the HIM folder (i.e. `C:\\User\\O3_Python`)
If you want some general figures:
- Adjust the output folder `ResultDir` with the results folder (i.e. `C:\\User\\O2_Output`) in `him_plot.py`
- Adjust the list of folders `ListOutDir` with results in `him_plot.py`
- To create plots use code `python him_plot.py True` if you want plots for every single run or else `python him_plot.py False`
If you want the figures from our paper:
- Adjust the output folder `resultDir` with the results folder (i.e. `C:\\User\\O2_Output`) in `him_paper.py`

- Adjust the folder for the different scenarios (`resultRefDir, resultW2PDir, resultStratDir, resultWorstDir`) with results in `him_paper.py`
- Adjust the list of results for the sensitivity analysis in `sensitivity.csv` (you can find a default version in `00_Setup`, but it needs to be saved in `02_Output`)
- To create plots from our paper use `python him_paper.py`

**!This has only been tested with our version of Python, Netlogo, and Windows.**!

## Data

The data used for our model results are based on:
|Data|Source|
|----|------|
|*Power market*||
|Non-electrolytic electricity demand|[[1](https://www.smard.de/home),[2](https://doi.org/10.1016/j.esr.2018.04.007)]|
|Installed capacity renewables|[[1](https://www.smard.de/home)]|
|Lifetime renewable asset|[[3](https://juser.fz-juelich.de/record/908382/files/Energie_Umwelt_577.pdf)]|
|Natural gas price|[[4](https://thedocs.worldbank.org/en/doc/18675f1d1639c7a34d463f59263ba0a2-0050012025/related/CMO-Pink-Sheet-August-2025.pdf)]|
|Gas turbine efficiency|[[5](https://doi.org/10.1016/j.energy.2025.134680)]|
|Investment costs renewable asset|[[3](https://juser.fz-juelich.de/record/908382/files/Energie_Umwelt_577.pdf)]|
|Capacity factor renewable asset|[[6](https://doi.org/10.1016/j.energy.2016.08.060),[7](https://doi.org/10.1016/j.energy.2016.08.068)]|
|*Hydrogen market*||
|Maximum hydrogen demand|[[8](https://media-publications.bcg.com/Turning-the-European-Green-H2-Dream-into-Reality.pdf)]|
|Installed capacity electrolyzers|[[9](https://www.wasserstoff-kompass.de/elektrolyse-monitor)]|
|Lifetime electrolyzer asset|[[10](https://doi.org/10.1016/j.ijhydene.2013.01.151)]|
|Electrolyzer efficiency|[[11](https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2020/Dec/IRENA_Green_hydrogen_cost_2020.pdf)]|
|Steam reforming efficiency|[12](https://www.amiqweb.es/app/download/9343795/6hydrogenproductionsteammethanereforming.pdf)]|
|*Electrolyzer market*||
|Installed capacity electrolyzer factories|[[13](https://www.iea.org/reports/global-hydrogen-review-2023)]|
|Investment costs electrolyzer factory|[[14](https://www.topsoe.com/press-releases/topsoe-announces-plans-for-new-state-of-the-art-us-electrolyzer-factory-for-clean-hydrogen),[15](https://nelhydrogen.com/articles/in-depth/nel-plans-gigafactory-in-michigan/),[16](https://www.spglobal.com/commodity-insights/en/news-research/latest-news/electric-power/110921-itm-power-to-build-second-uk-electrolyzer-factory-as-it-eyes-rapid-hydrogen-market-expansion)]|
|Production costs|[[13](https://www.iea.org/reports/global-hydrogen-review-2023),[17](https://observatory.clean-hydrogen.europa.eu/hydrogen-landscape/production-trade-and-cost/electrolyser-cost)]|
|Learning rate electrolyzers|[[11](https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2020/Dec/IRENA_Green_hydrogen_cost_2020.pdf),[18](https://doi.org/10.1016/j.ijhydene.2023.05.031)]|
|*Global*||		
|CO2 price|[[8](https://media-publications.bcg.com/Turning-the-European-Green-H2-Dream-into-Reality.pdf)]|


## Contributing
Contributions are highly welcome. Feel free to send me pull requests.

## About us
<a href="https://www.fz-juelich.de/en/ice/ice-2"><img src="https://github.com/FZJ-IEK3-VSA/README_assets/blob/main/iek3-square.png?raw=True" alt="Institute image ICE-2" width="280" align="right" style="margin:0px 10px"/></a>

We are the <a href="https://www.fz-juelich.de/en/ice/ice-2">Institute of Climate and Energy Systems (ICE) - Jülich Systems Analysis</a> belonging to the <a href="https://www.fz-juelich.de/en">Forschungszentrum Jülich</a>. Our interdisciplinary department's research is focusing on energy-related process and systems analyses. Data searches and system simulations are used to determine energy and mass balances, as well as to evaluate performance, emissions and costs of energy systems. The results are used for performing comparative assessment studies between the various systems. Our current priorities include the development of energy strategies, in accordance with the German Federal Government’s greenhouse gas reduction targets, by designing new infrastructures for sustainable and secure energy supply chains and by conducting cost analysis studies for integrating new technologies into future energy market frameworks.

## License
CC BY-NC 4.0

Copyright (C) 2025 FZJ-ICE-2

Active Developers: Bernhard-Johannes Jesse

Alumni: Bernhard-Johannes Jesse

You should have received a copy of the CC BY-NC License along with this program.
If not, see https://creativecommons.org/licenses/by-nc/4.0/legalcode.en

## Acknowledgement
This work was supported by the Helmholtz Association under the program ["Energy System Design"](https://www.helmholtz.de/en/research/research-fields/energy/energy-system-design/).

<p float="left">
<a href="https://www.helmholtz.de/en/"><img src="https://www.helmholtz.de/fileadmin/user_upload/05_aktuelles/Marke_Design/logos/HG_LOGO_S_ENG_RGB.jpg" alt="Helmholtz Logo" width="300px"></a>
</p>

