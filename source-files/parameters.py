import pandas as pd

dataframemain = pd.read_pickle("../results/qld_nodes_dataset.pkl")
initial_attribute_count = 2
svm_output_pkl = "../results/svm_output_qld_nodes.pkl"
svm_output_csv = "../results/svm_output_qld_nodes.csv"
name = "QLD Nodes"
svm_output_file = "../results/svm_output_qld_nodes.pkl"
tile_plot_file_name = "../results/tile_plot_QLD_nodes.eps"
association_plot_file_name = "../results/association_plot_QLD_nodes.eps"