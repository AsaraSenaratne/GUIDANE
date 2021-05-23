import pandas as pd
import qld_covid_analysis as qldana
import qld_create_dataframe_nodes as qldnodes
import pattern_gen as pg
import svm_training as svm


print("  1 - QLD nodes dataset \n ",
      "2 - QLD temporal edges dataset \n ",
      "3 - QLD spatial edges dataset \n ",
      "4 - QLD temporal and spatial edges dataset \n ",
      "5 - Israel nodes dataset \n ",
      "6 - Israel edges dataset \n ")
dataset_number = input("Enter the number relevant to the dataset you wish to execute from the above list: ")
dataset = int(dataset_number.strip())


def execute_qld_nodes():
    print("-----------------------------------")
    print("Executing QLD nodes dataset...")
    qldana.fill_misssing_onset_date()
    qldnodes.create_dataframe()
    svm.skye_nodes_get_abnormal_count()
    pg.identify_consistent_features()


def execute_qld_edges():
    dataframe_with_abnormal_counts_pkl = "dataframe_with_abnormal_counts.pkl"
    dataframe_with_abnormal_counts_csv = "dataframe_with_abnormal_counts.csv"
    weighted_score_output_pkl = "weighted_score_output.pkl"
    weighted_score_output_csv = "weighted_score_output.csv"
    weighted_importance_of_features_csv = "weighted_importance_of_features.csv"
    weighted_importance_of_features_pkl = "weighted_importance_of_features.pkl"
    svm_output_pkl = "svm_output_qld_edges_grouped_by_postcode.pkl"
    svm_output_csv = "svm_output_qld_edges_grouped_by_postcode.csv"
    clusters_csv = "clusters.csv"
    sorted_clusters = "sorted_clusters.csv"

    dataframemain = pd.read_pickle("qld_edges_grouped_by_postcode.pkl")
    initial_attribute_count = 1


if dataset == 1:
    execute_qld_nodes()
elif dataset == 2:
    execute_qld_edges()
