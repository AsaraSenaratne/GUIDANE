import numpy as py
import pandas as pd
from sklearn.svm import OneClassSVM
import statistics
from collections import Counter


dataframe_with_abnormal_counts_pkl = "dataframe_with_abnormal_counts.pkl"
dataframe_with_abnormal_counts_csv = "dataframe_with_abnormal_counts.csv"
weighted_score_output_pkl = "weighted_score_output.pkl"
weighted_score_output_csv = "weighted_score_output.csv"
weighted_importance_of_features_csv = "weighted_importance_of_features.csv"
weighted_importance_of_features_pkl = "weighted_importance_of_features.pkl"
svm_output_pkl = "svm_output_qld_nodes.pkl"
svm_output_csv = "svm_output_qld_nodes.csv"
clusters_csv = "clusters.csv"
sorted_clusters = "sorted_clusters.csv"

dataframemain = pd.read_pickle("qld_nodes_dataset.pkl")
initial_attribute_count = 2

def skye_nodes_get_abnormal_count():
    list_of_date_postcodes = list(dataframemain.index)
    print(list_of_date_postcodes)
    new_dataframe = pd.DataFrame(list_of_date_postcodes)
    birth_X = dataframemain.iloc[:, initial_attribute_count:]
    budget = 1000
    records_count = len(birth_X.index)
    nu = budget / records_count
    for kernel in ['rbf', 'sigmoid', 'linear', 'poly']:
        all_dic, binary_outlier, neg_dic, pos_dic, datanormalized = {}, {}, {}, {}, []
        clf = OneClassSVM(kernel=kernel, nu=nu).fit(birth_X)
        detect_binary_outliers = clf.predict(birth_X)
        detect_score_outliers = clf.decision_function(birth_X)
        new_dataframe[kernel + "_binary_output"] = detect_binary_outliers
        rounded_score = py.round(detect_score_outliers, 5)
        new_dataframe[kernel + "_score_output"] = rounded_score
        for i in range(0, len(rounded_score)):
            all_dic[i] = rounded_score[i]
        for i in range(0, len(detect_binary_outliers)):
            binary_outlier[i] = detect_binary_outliers[i]
        for i in range(0, len(all_dic)):
            if all_dic[i] <= 0 and binary_outlier[i] == -1:
                neg_dic.update({i: all_dic[i]})
            else:
                pos_dic.update({i: all_dic[i]})
        min_val_neg = min(neg_dic.values())
        max_val_neg = max(neg_dic.values())
        min_val_pos = min(pos_dic.values())
        max_val_pos = max(pos_dic.values())
        for key in neg_dic.keys():
            normal_val = (((neg_dic[key] - min_val_neg) / (
                        max_val_neg - min_val_neg)) - 1)  # normalize values between 0 and 1
            neg_dic[key] = round(normal_val, 5)
        for key in pos_dic.keys():
            normal_val = (pos_dic[key] - min_val_pos) / (
                        max_val_pos - min_val_pos)  # normalize values between 0 and 1
            pos_dic[key] = round(normal_val, 5)
        combined_dic = {**neg_dic, **pos_dic}
        sorted_dic = sorted(combined_dic.items())
        for i in range(0, len(sorted_dic)):
            datanormalized.append(sorted_dic[i][1])
        new_dataframe[kernel + "_score_output_normalized"] = datanormalized
    new_dataframe.to_pickle(dataframe_with_abnormal_counts_pkl)
    new_dataframe.to_csv(dataframe_with_abnormal_counts_csv)
    count_abnormal_pickups()

def count_abnormal_pickups():
    dataframemain = pd.read_pickle(dataframe_with_abnormal_counts_pkl)
    count_list = []
    for index, row in dataframemain.iterrows():
        count = 0
        for col in [row['sigmoid_binary_output'], row['rbf_binary_output'], row['linear_binary_output'],
                    row['poly_binary_output']]:
            if col == -1:
                count += 1
            else:
                continue
        count_list.append(count)
    dataframemain['count_of_abnormal_pickups'] = count_list
    dataframemain.to_pickle(dataframe_with_abnormal_counts_pkl)
    sum_abnormal_score()

def sum_abnormal_score():
    dataframemain = pd.read_pickle(dataframe_with_abnormal_counts_pkl)
    count_list = []
    for index, row in dataframemain.iterrows():
        count = 0
        for col in [row['sigmoid_score_output_normalized'], row['rbf_score_output_normalized'],
                    row['linear_score_output_normalized'], row['poly_score_output_normalized']]:
            count += col
        count_list.append(count)
    dataframemain['total_score_abnormal_pickups'] = count_list
    dataframemain.to_pickle(dataframe_with_abnormal_counts_pkl)
    calculate_average_score()

def calculate_average_score():
    dataframemain = pd.read_pickle(dataframe_with_abnormal_counts_pkl)
    count_list = []
    for index, row in dataframemain.iterrows():
        si = row['total_score_abnormal_pickups'] / 4
        count_list.append(round(si, 3))
    dataframemain['average_score'] = count_list
    dataframemain = dataframemain.sort_values(by=["average_score"], ascending=True)
    list_adjusted_svm = []
    for index, row in dataframemain.iterrows():
        if row['average_score'] <= 0:
            list_adjusted_svm.append(-1)
        else:
            list_adjusted_svm.append(1)
    dataframemain['adjusted_svm'] = list_adjusted_svm
    dataframemain.to_csv(weighted_score_output_csv)
    dataframemain.to_pickle(weighted_score_output_pkl)
    reconstruct_dataframe()

def reconstruct_dataframe():
    new_dataframemain = pd.read_pickle(weighted_score_output_pkl)
    print(dict(zip(new_dataframemain[0], new_dataframemain['adjusted_svm'])))
    dict_svm_output = dict(zip(new_dataframemain[0], new_dataframemain['adjusted_svm']))
    dict_weighted_score = dict(zip(new_dataframemain[0], new_dataframemain['average_score']))

    old_dataframemain = dataframemain.iloc[:, initial_attribute_count:]
    print(old_dataframemain)
    last_index = (len(old_dataframemain.columns))
    old_dataframemain = old_dataframemain.iloc[:, 0:last_index]

    row = pd.Series(dict_svm_output, name="svm_binary_output")
    old_dataframemain["svm_binary_output"] = row
    row = pd.Series(dict_weighted_score, name="average_score")
    old_dataframemain["average_score"] = row
    old_dataframemain = old_dataframemain.sort_values(by=["average_score"], ascending=True)
    old_dataframemain.to_pickle(svm_output_pkl)
    old_dataframemain.to_csv(svm_output_csv)

def find_unique_feature_vectors():
    df = dataframemain.iloc[:, initial_attribute_count:]
    print(df)
    pattern_col = []
    for index, row in df.iterrows():
        pattern = ""
        for col in df.columns:
            pattern += str(row[col])
        pattern_col.append(pattern)
    df['pattern_col'] = pattern_col
    list_patterns = list(df['pattern_col'])
    print(Counter(list_patterns))