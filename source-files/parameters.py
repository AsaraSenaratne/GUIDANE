import pandas as pd

def params(dataset):
    if dataset == 1:
        # QLD nodes
        params.dataframemain = "../results/qld_nodes_dataset.pkl"
        params.initial_attribute_count = 2
        params.budget = 1000
        params.svm_output_pkl = "../results/svm_output_qld_nodes.pkl"
        params.svm_output_csv = "../results/svm_output_qld_nodes.csv"
        params.svm_output_file = "../results/svm_output_qld_nodes.pkl"
        params.support_file = "../results/support_calc_qld_nodes.csv"
        params.name = "QLD Nodes"
        params.tile_plot_file_name = "../results/tile_plot_QLD_nodes.eps"
        params.association_plot_file_name = "../results/association_plot_QLD_nodes.eps"

    elif dataset == 2:
        # QLD temporal edges
        params.edges_file = "../results/qld_edges_grouped_by_postcode.pkl"
        params.dataframemain = "../results/qld_edges_grouped_by_postcode.pkl"
        params.initial_attribute_count = 1
        params.budget = 1000
        params.svm_output_pkl = "../results/svm_output_qld_edges_grouped_by_postcode.pkl"
        params.svm_output_csv = "../results/svm_output_qld_edges_grouped_by_postcode.csv"
        params.svm_output_file = "../results/svm_output_qld_edges_grouped_by_postcode.pkl"
        params.support_file = "../results/support_calc_qld_temp_edges.csv"
        params.name = "QLD Temporal Edges"
        params.tile_plot_file_name = "../results/tile_plot_QLD_temp_edges.eps"
        params.association_plot_file_name = "../results/association_plot_QLD_temp_edges.eps"

    elif dataset == 3:
        # QLD spatial edges
        params.edges_file = "../results/qld_edges_grouped_by_week.pkl"
        params.dataframemain = "../results/qld_edges_grouped_by_week.pkl"
        params.initial_attribute_count = 1
        params.budget = 1000
        params.svm_output_pkl = "../results/svm_output_qld_edges_grouped_by_week.pkl"
        params.svm_output_csv = "../results/svm_output_qld_edges_grouped_by_week.csv"
        params.svm_output_file = "../results/svm_output_qld_edges_grouped_by_week.pkl"
        params.support_file = "../results/support_calc_qld_spatial_edges.csv"
        params.name = "QLD Spatial Edges"
        params.tile_plot_file_name = "../results/tile_plot_QLD_spatial_edges.eps"
        params.association_plot_file_name = "../results/association_plot_QLD_spatial_edges.eps"

    elif dataset == 4:
        # QLD temporal and spatial edges
        params.edges_file = "../results/qld_edges_grouped_by_week_n_postcode.pkl"
        params.dataframemain = "../results/qld_edges_grouped_by_week_n_postcode.pkl"
        params.initial_attribute_count = 1
        params.budget = 1000
        params.svm_output_pkl = "../results/svm_output_qld_edges_grouped_by_week_n_postcode.pkl"
        params.svm_output_csv = "../results/svm_output_qld_edges_grouped_by_week_n_postcode.csv"
        params.svm_output_file = "../results/svm_output_qld_edges_grouped_by_week_n_postcode.pkl"
        params.support_file = "../results/support_calc_qld_temp_spa_edges.csv"
        params.name = "QLD Temporal and Spatial Edges"
        params.tile_plot_file_name = "../results/tile_plot_QLD_temp_spa_edges.eps"
        params.association_plot_file_name = "../results/association_plot_QLD_temp_spa_edges.eps"

    elif dataset == 5:
        # Israel nodes
        params.dataframemain = "../results/israel_nodes_dataset.pkl"
        params.initial_attribute_count = 0
        params.budget = 100
        params.svm_output_pkl = "../results/svm_output_israel_nodes.pkl"
        params.svm_output_csv = "../results/svm_output_israel_nodes.csv"
        params.svm_output_file = "../results/svm_output_israel_nodes.pkl"
        params.support_file = "../results/support_calc_israel_nodes.csv"
        params.name = "Israel Nodes"
        params.tile_plot_file_name = "../results/tile_plot_israel_nodes.eps"
        params.association_plot_file_name = "../results/association_plot_israel_nodes.eps"

    elif dataset == 6:
        # Israel edges
        params.dataframemain = "../results/israel_edges_dataset.pkl"
        params.initial_attribute_count = 0
        params.budget = 20
        params.svm_output_pkl = "../results/svm_output_israel_edges.pkl"
        params.svm_output_csv = "../results/svm_output_israel_edges.csv"
        params.svm_output_file = "../results/svm_output_israel_edges.pkl"
        params.name = "Israel Edges"
        params.support_file = "../results/support_calc_israel_edges.csv"
        params.tile_plot_file_name = "../results/tile_plot_israel_edges.eps"
        params.association_plot_file_name = "../results/association_plot_israel_edges.eps"

    else:
        print("Invalid dataset requested")