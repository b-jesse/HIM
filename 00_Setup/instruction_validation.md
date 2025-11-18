## Prepare data for validation
You will need to reverse all these changes to run the model for all other cases.

### Adjust time series
- in `01_Data` rename `pm_ts_demand_yearly - Validation.csv` to `pm_ts_demand_yearly.csv`

### Adjust initial data in `setup.nls`
- in 'setup.nls' change:
	- under `setup-constants`:
		- `const.RES.new_capacity` to 300
    	- `const.RES.max_capacity_rate` to 10
	- under `setup-init`:
 		- `init.PM.no_pp_0` to 3
     	- `init.PM.no_res_0` to 21 

- Make sure that in `runs.init` under model settings only `write: true`
- Make sure that in `runs.init` under scenario settings only `co2_tax: true`

- run model with `python him_run_model.py`
