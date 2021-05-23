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
Clone the project using the URL:
https://github.com/AsaraSenaratne/abnormality-detection.git

Install the required packages:
```
$ pip install -r requirements.txt
```

Open a terminal and change directory to the cloned project:
```
$ cd <path_to_directory>/abnormality-detection
```

Run main.py:
```
$ python3 main.py
```

## Reading the results
