# Unsupervised Identification of Abnormal Nodes and Edges in Graphs

## Introduction
This repository provides the implementation of an approach to unsupervised detection of both abnormal nodes and edges in large graph databases. We first
characterize nodes and edges using a set of features, and then employ a one-class support vector machine classifier to identify nodes and edges that are abnormal.
We extract patterns of features from the nodes and edges classified as abnormal, and apply clustering to identify groups of patterns that have similar
characteristics. We visualize the obtained abnormal patterns to both show the co-occurrences of certain features across these abnormal patterns, as well as the
relationships between the features that mostly influence the abnormality of nodes and edges.

## Technologies
This project is implemented using:
* Python 3.6

Following Python packages are used in the projet. 
* pandas v1.0.1
* plotly v4.8.2
* matplotlib v3.2.0
* seaborn v0.11.0
* networkx v2.4
* statsmodels v0.12.0
* numpy v1.19.1
* scikit_learn v0.24.2

## Execute the project
Clone the project:
```
git clone https://github.com/AsaraSenaratne/abnormality-detection.git
```

Install the required packages:
```
pip install -r requirements.txt
```

Open a terminal and change directory to the cloned project:
```
cd <path_to_directory>/abnormality-detection/source-files
```

Run main.py:
```
python3 -W ignore main.py
```

## Folder structure of the project
Assets folder - this folder contains the datasets used for analysis.  
Results folder - this folder gets created at program execution. All the plots, pickle files and CSV files that are generated as a result of program execution will be stored in this folder.  
Source folder - source code files are within this folder.  
Other files:
* LICENSE - contains information of the license under which this project is available.
* README - provides the users with an introduction to the project and guidance to use.
* requirements.txt - text file with information about the packages used in this project.

## Reading the results folder
The results folder contains all graphs and other intermediary results files generated at different steps of program execution. CSV files are available to view the initial nodes dataset, any intermediary supporting datasets built (such as merged datasets) and SVM output.  
Visualization outputs are available as a tile plot and an association plot in .eps format.  

## Execution time
Below execution times were obtained after running all experiments on a 64-bit MacBook Air with an Intel i5 (1.6 GHz) dual core processor, 8 GBytes of memory, and MacOS Big Sur v11.2.3.

| Dataset | Execution time (sec) |
| QLD nodes dataset | 275.92 (4.60 mins) |
| QLD temporal edges dataset | 16.35 |
| QLD spatial edges dataset | 1402.32 (23.37 mins) |
| QLD temporal and spatial edges dataset | 1922.89 (32.05 mins) |
| Israel nodes dataset | 32.47 |
| Israel edges dataset | 544.64 (9.08 mins) |
