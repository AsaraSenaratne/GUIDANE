



#QLD nodes - SVM data
dataframemain = pd.read_pickle("qld_nodes_dataset.pkl")
initial_attribute_count = 2
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

#QLD edges - SVM data
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