import os
import qld_covid_analysis as qldana
import qld_create_dataframe_nodes as qldnodes
import qld_create_dataframe_edges as qldedges
import israel_create_dataframe_nodes as isrnodes
import israel_create_dataframe_edges as isredges
import pattern_gen as pg
import svm_training as svm

if not os.path.isdir("../results"):
    os.mkdir("../results")

print("  1 - QLD nodes dataset \n ",
      "2 - QLD temporal edges dataset \n ",
      "3 - QLD spatial edges dataset \n ",
      "4 - QLD temporal and spatial edges dataset \n ",
      "5 - Israel nodes dataset \n ",
      "6 - Israel edges dataset \n ")
dataset_number = input("Enter the number relevant to the dataset you wish to execute from the above list: ")
dataset = int(dataset_number.strip())


def execute_qld_nodes(dataset):
    print("-----------------------------------")
    print("Executing QLD nodes dataset...")
    qldana.fill_misssing_onset_date()
    qldnodes.create_dataframe()
    svm.def_params(dataset)
    pg.def_params(dataset)
    print("Generated plots are available in the results folder...")

def execute_qld_temporal_edges(dataset):
    print("-----------------------------------")
    print("Executing QLD temporal edges dataset...")
    qldedges.def_params(dataset)
    svm.def_params(dataset)
    pg.def_params(dataset)
    print("Generated plots are available in the results folder...")

def execute_qld_spatial_edges(dataset):
    print("-----------------------------------")
    print("Executing QLD spatial edges dataset...")
    qldedges.def_params(dataset)
    svm.def_params(dataset)
    pg.def_params(dataset)
    print("Generated plots are available in the results folder...")

def execute_qld_temp_spa_edges(dataset):
    print("-----------------------------------")
    print("Executing QLD temporal and spatial edges dataset...")
    qldedges.def_params(dataset)
    svm.def_params(dataset)
    pg.def_params(dataset)
    print("Generated plots are available in the results folder...")

def execute_israel_nodes(dataset):
    print("-----------------------------------")
    print("Executing Israel nodes dataset...")
    isrnodes.create_dataframe()
    svm.def_params(dataset)
    pg.def_params(dataset)
    print("Generated plots are available in the results folder...")

def execute_israel_edges(dataset):
    print("-----------------------------------")
    print("Executing Israel edges dataset...")
    isredges.add_week_number()
    svm.def_params(dataset)
    pg.def_params(dataset)
    print("Generated plots are available in the results folder...")

try:
    if dataset == 1:
        execute_qld_nodes(dataset)
    elif dataset == 2:
        if os.path.isfile('../results/qld_groupby_postcode_week_reduced_cols_not_norm.pkl'):
            execute_qld_temporal_edges(dataset)
        else:
            print("-----------------------------------")
            print("First execute QLD nodes dataset before proceeding with any of QLD edge datasets...")
    elif dataset == 3:
        if os.path.isfile('../results/qld_groupby_postcode_week_reduced_cols_not_norm.pkl'):
            execute_qld_spatial_edges(dataset)
        else:
            print("-----------------------------------")
            print("First execute QLD nodes dataset before proceeding with any of QLD edge datasets...")
    elif dataset == 4:
        if os.path.isfile('../results/qld_groupby_postcode_week_reduced_cols_not_norm.pkl'):
            execute_qld_temp_spa_edges(dataset)
        else:
            print("-----------------------------------")
            print("First execute QLD nodes dataset before proceeding with any of QLD edge datasets...")
    elif dataset == 5:
        execute_israel_nodes(dataset)
    elif dataset == 6:
        execute_israel_edges(dataset)
    else:
        print("Invalid number entered")
except:
    print("An error occurred during execution...")