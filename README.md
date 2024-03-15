DEPC-NSGA-II: Standard and stratified parallel optimisation 
An NSGA-II estate retrofit strategy generator and Bayesian optimisation model for tuning NSGA-II hyperparameters.

## Features
 - **NSGA2**: A nondominated sorting genetic algorithm for residential EPCs.
 - **NSGA2Community**: A stratified NSGA2 optimiser for fast optimisation
## Summary
Takes a csv of retrofits for multiple buildings and finds near-optimal strageies for improving the overall target score. 

### Features
`nsga2.py` The script that processes datasets as a whole

`nsga2_community.py` The script that processes datasets in subsets

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
Output from running `python nsga2.py  --code 11k --gen 10000 --population 100 --children 60 --history-path ./test/gen_results.csv --crossover --crossover-eta 16.1 --crossover-prob 0.8460 --mutation-eta 5.22 --summary`

<img src="https://github.com/soliverit/depc_nsga2/assets/3307541/d0273235-bc44-4fd7-ad47-eb77cb3def6d)" alt="drawing" height="250"/>
   
<img src="https://github.com/soliverit/depc_nsga2/assets/3307541/edcf9c16-c146-4992-abb3-1bab41408642)" alt="drawing" height="250"/>



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
### Additional parameters for ./nsga2community.py
`--partitions` Number of subsets data is split into.

`--threads` Number of concurrent processses

### Data format
In the example using results created by https://github.com/soliverit/depc_emulator using the Building and Retrofit base classes, each row has three key component:

- CURRENT_ENERGY_EFFICIENCY:  The building's certificate EPC rating
- TOTAL_FLOOR_AREA: The net internal area
- Retrofit informatio columns: Two columns per Retrofit denoting the cost `-Cost` and EPC rating `-Eff`. In the example, these columns are all possible combinations of `roof`, `envelope`, `windows`, and `hotwater`. E.g, `hotwater_windows-Eff` and `hotwater_windows-Cost`.
