For all scenarios:
- Make sure that in `runs.init` under model settings only `write: true`
- Make sure that in `runs.init` under scenario settings only `co2_tax: true`

To create the best-case scenario:
- Make sure that in `runs.init` under sensitivity variables `sensitivty: none`
- Make sure that in `runs.init` under default values
	- `init.HM.threshold: -0.99`
	- `init.EM.threshold: -0.99`
	- `const.MAN.learning_rate: 0.1`
- Make sure that in func.nls at the bottom of func.hm.set_h2_price all DEBUG Settings are comment out
- run model with `python him_run_model.py`

To create the non-strategic scenario:
- Make sure that in `runs.init` under sensitivity variables `sensitivty: none`
- Make sure that in `runs.init` under default values
	- `init.HM.threshold: -0.0`
	- `init.EM.threshold: -0.0`
	- `const.MAN.learning_rate: 0.1`
- Make sure that in func.nls at the bottom of func.hm.set_h2_price all DEBUG Settings are comment out
- run model with `python him_run_model.py`

To create the grey hydrogen scenario:
- Make sure that in `runs.init` under sensitivity variables `sensitivty: none`
- Make sure that in `runs.init` under default values
	- `init.HM.threshold: -0.99`
	- `init.EM.threshold: -0.99`
	- `const.MAN.learning_rate: 0.1`
- In func.nls at the bottom of func.hm.set_h2_price reactivate the code for the grey hydrogen case (should be 3 lines of code)
- run model with `python him_run_model.py`

To create the worst-case scenario:
- Make sure that in `runs.init` under sensitivity variables `sensitivty: none`
- Make sure that in `runs.init` under default values
	- `init.HM.threshold: -0.0`
	- `init.EM.threshold: -0.0`
	- `const.MAN.learning_rate: 0.1`
- In func.nls at the bottom of func.hm.set_h2_price reactivate the code for the grey hydrogen case (should be 3 lines of code)
- run model with `python him_run_model.py`

To create the sensitivty analysis for different maximum willingness to pay for hydrogen
First part
- Make sure that in `runs.init` under sensitivity variables sensitivty: none
- Make sure that in `runs.init` under default values
	- `init.HM.threshold: -0.99`
	- `init.EM.threshold: -0.99`
	- `const.MAN.learning_rate: 0.1`
- In func.nls at the bottom of func.hm.set_h2_price reactivate the code for the sensitivity analysis (should be 3 lines of code)
	- Set the price in the if and execute line to the needed upper limit
- run model with `python him_run_model.py`
Second part
- Make sure that in `runs.init` under sensitivity variables `sensitivty: single`
- Make sure that in `runs.init` under sensitivity variables `paramters: [init.HM.threshold_0]`
- Make sure that in `runs.init` under default values
	- `init.HM.threshold: -0.99`
	- `init.EM.threshold: -0.99`
	- `const.MAN.learning_rate: 0.1`
- In func.nls at the bottom of `func.hm.set_h2_price` reactivate the code for the sensitivity analysis (should be 3 lines of code)
	- Set the price in the if and execute line to the needed upper limit
- run model with `python him_run_model.py`

- repeat both parts with maximum willingness to pay for hydrogen between 3 and 8 €/kg in 1 €/kg steps