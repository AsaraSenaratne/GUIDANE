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
