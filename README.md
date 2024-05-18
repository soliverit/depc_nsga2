# DEPC strategy optimisation
A toolkit for dveloping machine learning models and optimisation algorithms for large-scale retrofit analysis. Tailored for national domestic retrofit studies.
## Problem statement
You have an estate of 50,000 Each has up to 16 retrofit options representing every possible combination of 4 option: cavity wall insulation. Each building is below the acceptable EPC threshold, 40. Find the lowest cost strategy for increasing the overall EPC rating by the sum of the differences.
### The solution space
Each building has up to 16 retrofit options: the as-built state and all combinations of 4 retrofits: DHW boiler replacement, roof insulation, wall insulation, and window replacement.

DHW boiler replacement, windows replacement, and roof insulation.
### Includes:
- NSGA-II optimisation
- NSGA-II recurrent, threaded subset optimisation
- XGBoost and sklearn estimator wrappers
- Hyperopt hyperparameter tuning for estimators and genetic algorithms
- Bayesian-optimisation for genetic algorithms
### Features
`nsga2.py` The NSGA-II that optimises datasets as a whole

`nsga2_community.py` The script that parallel processes datasets in subsets

`nsga2_bayes_hp_tuner.py` A Bayesian optimisiation process for tuning NSGA-II hyperparameters.

`nsga2_community_bayes_hp_tuner.py` A Bayesian optimisiation process for tuning NSGA-II hyperparameters.

`estimator.py` A script for generating machine learning optimisers. Intended for the project, will work with any data, though.

`estimator_hyperopt_hp_tuner.py` Hyperopt hyperparameter tuning for estimators.

# Getting started
### Prerequisites
Install dependencies: `pip install -r requirements.txt`
### Examples
Everything has a built-in example. Just run `python <script>.py` and it'll do something. Use command line arguments defined below modify the process
The example is straightforward. Just run `python nsga2.py` 
- Add `--summary` to see the NSGA-II and Problem configuration.
- Add `-h` to list command line parameters
#### Output
Output from running `python nsga2.py  --code 11k --gen 10000 --population 100 --children 60 --crossover --crossover-eta 16.1 --crossover-prob 0.8460 --mutation-eta 5.22 --summary`

<img src="https://github.com/soliverit/depc_nsga2/assets/3307541/d0273235-bc44-4fd7-ad47-eb77cb3def6d)" alt="drawing" height="250"/>
   
<img src="https://github.com/soliverit/depc_nsga2/assets/3307541/edcf9c16-c146-4992-abb3-1bab41408642)" alt="drawing" height="250"/>


# Command line arguments and data formats
## RetrofitNSGA1 and NSGA2Community command line arguments
### Command line parameters (./nsga2.py)
`--code` Input file code: The name of a file in `./data/`. E.g, `mid` points to `./data/mid.csv` or `my_project/initial` to `./data/my_project/initial`

`--summary` Print a summary of the NSGA-II and Problem configs

`--verbose` Print the generation outputs from NSGA-II in real-time

`--crossover` Defines whether it's an evolutionary or genetic algorithm. Add the flag for genetic algorithm

`--crossover-eta`  Determines how much genetic data is swapped between parents during crossover

`--crossover-prob` The probability an action will be crossover instead of mutation

`--mutation-eta`  The extent mutation will change the parent. 

`--gen` Number of generations

`--population` Number of parents in the population

`--children` Number of children parents have each generation

`--history-path` Path to objective score history.

`--best-initial-states` Create the initial population from the building-locked best case for at risk buildings (Worse than D rating, currently)

`--target-rating` The target EPC rating that dictates the EPC point improvement requirements. The genetic algorithm constraint and second objective

`--write-state` Write a .stt (just a csv with a distinct file type) to the input data directory

`--inequality` Explicitly define the minimum points improved constraint

`--state-identifier` Tell the script that the data has a column with a Retrofit ID chosen during a previous optimisation. Use the value as in place of `--best-initial-states` building-locked states
### Additional parameters for ./nsga2_community.py
`--partitions` Number of subsets data is split into.

`--threads` Number of concurrent processses

`--recurrent-steps` The number of times results are fed back into the processor.
### NSGA-II dataset format
In the example using results created by https://github.com/soliverit/depc_emulator using the Building and Retrofit base classes, each row has three key component:

- CURRENT_ENERGY_EFFICIENCY:  The building's certificate EPC rating
- TOTAL_FLOOR_AREA: The net internal area
- Retrofit informatio columns: Two columns per Retrofit denoting the cost `-Cost` and EPC rating `-Eff`. In the example, these columns are all possible combinations of `roof`, `envelope`, `windows`, and `hotwater`. E.g, `hotwater_windows-Eff` and `hotwater_windows-Cost`.

## Estimator command line arguments
NOTE: All estimators have unique args. Due to how `argsparse` works, not all will by listed by the `-h` flag for `estimator.py`. See below for specific flags or check out `<Estimator>.AddAdditionalCMDParams()` for unique arguments.
### Global
`--data` Path to data file. Will work with literally any .csv that contains features and a target. Default: `./data/estimator_depc_example.csv`

`--target` Target feature name. Default `CURRENT_ENERGY_EFFICIENCY` (linked to default `--data` dataset)

`--constructor` String name of a class in `./lib/estimators`/ E.g, `XGBoostEstimator`. This selects the machine learning algorithm used by the script.

### XGBoost
Find out more here: https://xgboost.readthedocs.io/en/stable/index.html 

`--booster` The booster type. E,g. `dart`. 

`--max-depth` Maximum decision tree depth

`--learning-rate` Learning rate

`--objective` Basically what type of learner is it. E,g. `reg:meansquarederror` for regression or `binary:logistic` for binary classification

`--sample-type` Sampling method. E.g, `uniform`

`--normalise-type` Normlisation method. E.g, `tree`

`--rate-drop` Drop-out rate. Rate trees are dropped

`--skip-drop` Dictates the probabbility that drop-out won't be applied during an iteration

`--n-rounds` Number of iterations, interchaneable with n_estimators from scikit GBDT / Random forests













