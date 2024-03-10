# DEPC-NSGA-II (Python)
An NSGA-II estate retrofit strategy generator and Bayesian optimisation model for tuning NSGA-II hyperparameters.

## Summary
Takes a csv of retrofits for multiple buildings and finds near-optimal strageies for improving the overall target score. For example, "./example.py" finds the cost to points improved that brings all buildings in the dataset to the target EPC rating, D.
### Features
`example.py` A configurable example of the optimisation process.

`bayes_optimiser.py` A Bayesian optimisiation process for tuning NSGA-II hyperparameters.
## Getting started
### Prerequisites
- PyMOO `pip install pymoo`
- Bayseian-Optimisation `pip install bayesian-optimization`
### Example
The example is straightforward. Just run `python example.py` 
- Add `--summary` to see the NSGA-II and Problem configuration.
- Add `-h` to list command line parameters
#### Output
Output from running `python example.py  --code 11k --gen 10000 --population 100 --children 60 --history-path ./test/water.csv --callback --crossover --crossover-eta 16.1 --crossover-prob 0.8460 --mutation-eta 5.22 --summary`

<img src="https://github.com/soliverit/depc_nsga2/assets/3307541/d0273235-bc44-4fd7-ad47-eb77cb3def6d)" alt="drawing" height="250"/>
   
<img src="https://github.com/soliverit/depc_nsga2/assets/3307541/edcf9c16-c146-4992-abb3-1bab41408642)" alt="drawing" height="250"/>



### Command line parameters
`--code` Input file code: The name of a file in `./data/`. E.g, `mid` points to `./data/mid.csv`

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

### Data format
In the example using results created by https://github.com/soliverit/depc_emulator using the Building and Retrofit base classes, each row has three key component:

- CURRENT_ENERGY_EFFICIENCY:  The building's certificate EPC rating
- TOTAL_FLOOR_AREA: The net internal area
- Retrofit informatio columns: Two columns per Retrofit denoting the cost `-Cost` and EPC rating `-Eff`. In the example, these columns are all possible combinations of `roof`, `envelope`, `windows`, and `hotwater`. E.g, `hotwater_windows-Eff` and `hotwater_windows-Cost`.
