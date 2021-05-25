import networkx as nx
import pandas as pd
import parameters as pm

def def_params(dataset):
    pm.params(dataset)
    global edges_file
    edges_file = pm.params.edges_file
    if dataset == 2:
        create_dataframe_grouped_by_postcode()
    elif dataset == 3:
        create_dataframe_grouped_by_week()
    else:
        create_dataframe_grouped_by_week_n_postcode()


def sum_age_columns():
    df = pd.read_pickle("../results/qld_groupby_postcode_week_reduced_cols_not_norm.pkl")
    young, mid, old = [], [], []
    for index, row in df.iterrows():
        young = int(row['1_agegroup_count']) + int(row['2_agegroup_count'])+ int(row['3_agegroup_count'])
        mid = int(row['4_agegroup_count']) + int(row['5_agegroup_count']) + int(row['6_agegroup_count']) + int(row['7_agegroup_count'])
        old = int(row['8_agegroup_count']) + int(row['9_agegroup_count']) + int(row['10_agegroup_count'])
    df["young_aged_count"] = young
    df["mid_aged_count"] = mid
    df["old_aged_count"] = old
    return df

def create_dataframe_grouped_by_postcode():
    df = sum_age_columns()
    groups = df.groupby("postcode")
    linkdict = {}
    for postcode in df["postcode"].unique():
        subgroup = groups.get_group(postcode)
        G = nx.Graph()
        for i in range(0, len(subgroup.index)):
            G.add_node(subgroup.index[i],
                       node_id=subgroup.index[i],
                       week_number = df.loc[subgroup.index[i],"week_number"],
                       postcode = df.loc[subgroup.index[i],"postcode"],
                       hospitalized_count = df.loc[subgroup.index[i],"hospitalisaed_count"],
                       not_hospitalised_count = df.loc[subgroup.index[i],"not_hospitalised_count"],
                       deceased_count = df.loc[subgroup.index[i],"deceased_count"],
                       localacq_unident_interstate_trvl_count = df.loc[subgroup.index[i],"localacq_unident_interstate_trvl_count"],
                       overseas_acquired_count = df.loc[subgroup.index[i],"overseas_acquired_count"],
                       locally_acquired_contact_known_count = df.loc[subgroup.index[i],"locally_acquired_contact_known_count"],
                       locally_acquired_unidentified_count = df.loc[subgroup.index[i],"locally_acquired_unidentified_count"],
                       under_investigation_count = df.loc[subgroup.index[i],"under_investigation_count"],
                       indigenous_count = df.loc[subgroup.index[i],"indigenous_count"],
                       admitted_to_icu_count = df.loc[subgroup.index[i],"admitted_to_icu_count"],
                       ventilated_count = df.loc[subgroup.index[i],"ventilated_count"],
                       female_count = df.loc[subgroup.index[i],"female_count"],
                       male_count = df.loc[subgroup.index[i],"male_count"],
                       young_aged_count=df.loc[subgroup.index[i], "young_aged_count"],
                       mid_aged_count=df.loc[subgroup.index[i], "mid_aged_count"],
                       old_aged_count=df.loc[subgroup.index[i], "old_aged_count"],
                       patient_count = df.loc[subgroup.index[i],"patient_count"],)
        for i in range(0, len(subgroup.index) - 1):
            for j in range(i + 1, len(subgroup.index)):
                G.add_edge(subgroup.index[i], subgroup.index[j])
                groupid = G.nodes[subgroup.index[i]]['postcode']
                HighHospitalisedCount = G.nodes[subgroup.index[j]]['hospitalized_count'] >= G.nodes[subgroup.index[i]]['not_hospitalised_count']
                HighDeceasedCount = G.nodes[subgroup.index[j]]['deceased_count'] >= G.nodes[subgroup.index[i]]['deceased_count']
                HighLocalAcqUnidentifiedInterstateTravelCount = G.nodes[subgroup.index[j]]['localacq_unident_interstate_trvl_count'] >= G.nodes[subgroup.index[i]]['localacq_unident_interstate_trvl_count']
                HighOverseasAcquiredCount = G.nodes[subgroup.index[j]]['overseas_acquired_count'] >= G.nodes[subgroup.index[i]]['overseas_acquired_count']
                HighLocallyAcquiredContactKnownCount = G.nodes[subgroup.index[j]]['locally_acquired_contact_known_count'] >= G.nodes[subgroup.index[i]]['locally_acquired_unidentified_count']
                HighUnderInvestigationCount = G.nodes[subgroup.index[j]]['under_investigation_count'] >= G.nodes[subgroup.index[i]]['under_investigation_count']
                HighIndigenousCount = G.nodes[subgroup.index[j]]['indigenous_count'] >= G.nodes[subgroup.index[i]]['indigenous_count']
                HighICUCount = G.nodes[subgroup.index[j]]['admitted_to_icu_count'] >= G.nodes[subgroup.index[i]]['admitted_to_icu_count']
                HighVentilatedCount = G.nodes[subgroup.index[j]]['ventilated_count'] >= G.nodes[subgroup.index[i]]['ventilated_count']
                HighMaleCountThanFemaleCount= G.nodes[subgroup.index[j]]['male_count'] >= G.nodes[subgroup.index[i]]['female_count']
                HighYoungAgedCount= G.nodes[subgroup.index[j]]['young_aged_count'] >= G.nodes[subgroup.index[i]]['young_aged_count']
                HighMidAgedCount= G.nodes[subgroup.index[j]]['mid_aged_count'] >= G.nodes[subgroup.index[i]]['mid_aged_count']
                HighOldAgedCount= G.nodes[subgroup.index[j]]['old_aged_count'] >= G.nodes[subgroup.index[i]]['old_aged_count']
                HighPatientCount = G.nodes[subgroup.index[j]]['patient_count'] >= G.nodes[subgroup.index[i]]['patient_count']

                linkdict[subgroup.index[i] + " - " + subgroup.index[j]] = [groupid, int(HighHospitalisedCount), int(HighDeceasedCount), int(HighLocalAcqUnidentifiedInterstateTravelCount), int(HighOverseasAcquiredCount),
                                                                           int(HighLocallyAcquiredContactKnownCount), int(HighUnderInvestigationCount), int(HighIndigenousCount), int(HighICUCount), int(HighVentilatedCount),
                                                                           int(HighMaleCountThanFemaleCount), int(HighYoungAgedCount), int(HighMidAgedCount), int(HighOldAgedCount), int(HighPatientCount)]
                break

    graph_features = pd.DataFrame(linkdict, index=['groupid', "HighHospitalisedCount", "HighDeceasedCount", "HighLocalUnidenInterTravCount", "HighOverseasAcqCount",
                                                    "HighLocalAcqKnownCount", "HighUnderInvestCount", "HighIndigenousCount", 'HighICUCount', 'HighVentilatedCount',
                                                    "HighMalesThanFemales", "HighYoungAgedCount", "HighMidAgedCount", 'HighOldAgedCount', 'HighPatientCount',
                                                   ])
    graph_features = graph_features.transpose()
    graph_features.to_pickle(edges_file)
    feature_reduction(graph_features)

def create_dataframe_grouped_by_week():
    df = sum_age_columns()
    groups = df.groupby("week_number")
    linkdict = {}
    for week in df["week_number"].unique():
        subgroup = groups.get_group(week)
        G = nx.Graph()
        for i in range(0, len(subgroup.index)):
            G.add_node(subgroup.index[i],
                       node_id=subgroup.index[i],
                       week_number=df.loc[subgroup.index[i], "week_number"],
                       postcode=df.loc[subgroup.index[i], "postcode"],
                       hospitalized_count=df.loc[subgroup.index[i], "hospitalisaed_count"],
                       not_hospitalised_count=df.loc[subgroup.index[i], "not_hospitalised_count"],
                       deceased_count=df.loc[subgroup.index[i], "deceased_count"],
                       localacq_unident_interstate_trvl_count=df.loc[subgroup.index[i], "localacq_unident_interstate_trvl_count"],
                       overseas_acquired_count=df.loc[subgroup.index[i], "overseas_acquired_count"],
                       locally_acquired_contact_known_count=df.loc[subgroup.index[i], "locally_acquired_contact_known_count"],
                       locally_acquired_unidentified_count=df.loc[subgroup.index[i], "locally_acquired_unidentified_count"],
                       under_investigation_count=df.loc[subgroup.index[i], "under_investigation_count"],
                       indigenous_count=df.loc[subgroup.index[i], "indigenous_count"],
                       admitted_to_icu_count=df.loc[subgroup.index[i], "admitted_to_icu_count"],
                       ventilated_count=df.loc[subgroup.index[i], "ventilated_count"],
                       female_count=df.loc[subgroup.index[i], "female_count"],
                       male_count=df.loc[subgroup.index[i], "male_count"],
                       young_aged_count=df.loc[subgroup.index[i], "young_aged_count"],
                       mid_aged_count=df.loc[subgroup.index[i], "mid_aged_count"],
                       old_aged_count=df.loc[subgroup.index[i], "old_aged_count"],
                       patient_count=df.loc[subgroup.index[i], "patient_count"], )
        for i in range(0, len(subgroup.index) - 1):
            for j in range(i + 1, len(subgroup.index)):
                G.add_edge(subgroup.index[i], subgroup.index[j])
                groupid = G.nodes[subgroup.index[i]]['week_number']
                HighHospitalisedCount = G.nodes[subgroup.index[j]]['hospitalized_count'] >= G.nodes[subgroup.index[i]]['not_hospitalised_count']
                HighDeceasedCount = G.nodes[subgroup.index[j]]['deceased_count'] >= G.nodes[subgroup.index[i]]['deceased_count']
                HighLocalAcqUnidentifiedInterstateTravelCount = G.nodes[subgroup.index[j]]['localacq_unident_interstate_trvl_count'] >= G.nodes[subgroup.index[i]]['localacq_unident_interstate_trvl_count']
                HighOverseasAcquiredCount = G.nodes[subgroup.index[j]]['overseas_acquired_count'] >= G.nodes[subgroup.index[i]]['overseas_acquired_count']
                HighLocallyAcquiredContactKnownCount = G.nodes[subgroup.index[j]]['locally_acquired_contact_known_count'] >= G.nodes[subgroup.index[i]]['locally_acquired_unidentified_count']
                HighUnderInvestigationCount = G.nodes[subgroup.index[j]]['under_investigation_count'] >= G.nodes[subgroup.index[i]]['under_investigation_count']
                HighIndigenousCount = G.nodes[subgroup.index[j]]['indigenous_count'] >= G.nodes[subgroup.index[i]]['indigenous_count']
                HighICUCount = G.nodes[subgroup.index[j]]['admitted_to_icu_count'] >= G.nodes[subgroup.index[i]]['admitted_to_icu_count']
                HighVentilatedCount = G.nodes[subgroup.index[j]]['ventilated_count'] >= G.nodes[subgroup.index[i]]['ventilated_count']
                HighMaleCountThanFemaleCount = G.nodes[subgroup.index[j]]['male_count'] >= G.nodes[subgroup.index[i]]['female_count']
                HighYoungAgedCount = G.nodes[subgroup.index[j]]['young_aged_count'] >= G.nodes[subgroup.index[i]]['young_aged_count']
                HighMidAgedCount = G.nodes[subgroup.index[j]]['mid_aged_count'] >= G.nodes[subgroup.index[i]]['mid_aged_count']
                HighOldAgedCount = G.nodes[subgroup.index[j]]['old_aged_count'] >= G.nodes[subgroup.index[i]]['old_aged_count']
                HighPatientCount = G.nodes[subgroup.index[j]]['patient_count'] >= G.nodes[subgroup.index[i]]['patient_count']

                linkdict[subgroup.index[i] + " - " + subgroup.index[j]] = [groupid, int(HighHospitalisedCount),
                                                                           int(HighDeceasedCount),
                                                                           int(HighLocalAcqUnidentifiedInterstateTravelCount),
                                                                           int(HighOverseasAcquiredCount),
                                                                           int(HighLocallyAcquiredContactKnownCount),
                                                                           int(HighUnderInvestigationCount),
                                                                           int(HighIndigenousCount), int(HighICUCount),
                                                                           int(HighVentilatedCount),
                                                                           int(HighMaleCountThanFemaleCount),
                                                                           int(HighYoungAgedCount),
                                                                           int(HighMidAgedCount), int(HighOldAgedCount),
                                                                           int(HighPatientCount)]


    graph_features = pd.DataFrame(linkdict, index=['groupid', "HighHospitalisedCount", "HighDeceasedCount", "HighLocalUnidenInterTravCount", "HighOverseasAcqCount",
                                                    "HighLocalAcqKnownCount", "HighUnderInvestCount", "HighIndigenousCount", 'HighICUCount', 'HighVentilatedCount',
                                                    "HighMalesThanFemales", "HighYoungAgedCount", "HighMidAgedCount", 'HighOldAgedCount', 'HighPatientCount',
                                                           ])
    graph_features = graph_features.transpose()
    graph_features.to_pickle(edges_file)
    feature_reduction(graph_features)

def create_dataframe_grouped_by_week_n_postcode():
    df = sum_age_columns()
    groups = df.groupby("week_number")
    linkdict = {}
    sorted_week_numbers = sorted(list(df["week_number"].unique()))
    for week in sorted_week_numbers:
        subgroup = groups.get_group(week)
        if sorted_week_numbers.index(week) == (len(sorted_week_numbers)-1):
            break
        else:
            subgroup_next = groups.get_group(int(week+1))
        G = nx.Graph()
        for i in range(0, len(subgroup.index)):
            G.add_node(subgroup.index[i],
                       node_id=subgroup.index[i],
                       week_number=df.loc[subgroup.index[i], "week_number"],
                       postcode=df.loc[subgroup.index[i], "postcode"],
                       hospitalized_count=df.loc[subgroup.index[i], "hospitalisaed_count"],
                       not_hospitalised_count=df.loc[subgroup.index[i], "not_hospitalised_count"],
                       deceased_count=df.loc[subgroup.index[i], "deceased_count"],
                       localacq_unident_interstate_trvl_count=df.loc[subgroup.index[i], "localacq_unident_interstate_trvl_count"],
                       overseas_acquired_count=df.loc[subgroup.index[i], "overseas_acquired_count"],
                       locally_acquired_contact_known_count=df.loc[subgroup.index[i], "locally_acquired_contact_known_count"],
                       locally_acquired_unidentified_count=df.loc[subgroup.index[i], "locally_acquired_unidentified_count"],
                       under_investigation_count=df.loc[subgroup.index[i], "under_investigation_count"],
                       indigenous_count=df.loc[subgroup.index[i], "indigenous_count"],
                       admitted_to_icu_count=df.loc[subgroup.index[i], "admitted_to_icu_count"],
                       ventilated_count=df.loc[subgroup.index[i], "ventilated_count"],
                       female_count=df.loc[subgroup.index[i], "female_count"],
                       male_count=df.loc[subgroup.index[i], "male_count"],
                       young_aged_count=df.loc[subgroup.index[i], "young_aged_count"],
                       mid_aged_count=df.loc[subgroup.index[i], "mid_aged_count"],
                       old_aged_count=df.loc[subgroup.index[i], "old_aged_count"],
                       patient_count=df.loc[subgroup.index[i], "patient_count"], )
        for i in range(0, len(subgroup_next.index)):
            G.add_node(subgroup_next.index[i],
                       node_id=subgroup_next.index[i],
                       week_number=df.loc[subgroup_next.index[i], "week_number"],
                       postcode=df.loc[subgroup_next.index[i], "postcode"],
                       hospitalized_count=df.loc[subgroup_next.index[i], "hospitalisaed_count"],
                       not_hospitalised_count=df.loc[subgroup_next.index[i], "not_hospitalised_count"],
                       deceased_count=df.loc[subgroup_next.index[i], "deceased_count"],
                       localacq_unident_interstate_trvl_count=df.loc[subgroup_next.index[i], "localacq_unident_interstate_trvl_count"],
                       overseas_acquired_count=df.loc[subgroup_next.index[i], "overseas_acquired_count"],
                       locally_acquired_contact_known_count=df.loc[subgroup_next.index[i], "locally_acquired_contact_known_count"],
                       locally_acquired_unidentified_count=df.loc[subgroup_next.index[i], "locally_acquired_unidentified_count"],
                       under_investigation_count=df.loc[subgroup_next.index[i], "under_investigation_count"],
                       indigenous_count=df.loc[subgroup_next.index[i], "indigenous_count"],
                       admitted_to_icu_count=df.loc[subgroup_next.index[i], "admitted_to_icu_count"],
                       ventilated_count=df.loc[subgroup_next.index[i], "ventilated_count"],
                       female_count=df.loc[subgroup_next.index[i], "female_count"],
                       male_count=df.loc[subgroup_next.index[i], "male_count"],
                       young_aged_count=df.loc[subgroup_next.index[i], "young_aged_count"],
                       mid_aged_count=df.loc[subgroup_next.index[i], "mid_aged_count"],
                       old_aged_count=df.loc[subgroup_next.index[i], "old_aged_count"],
                       patient_count=df.loc[subgroup_next.index[i], "patient_count"], )
        for j in range(0, len(subgroup.index)):  # add an edge from one node to another within a bundle
            for i in range(0, len(subgroup_next.index)):
                G.add_edge(subgroup_next.index[i], subgroup.index[j])
                groupid = G.nodes[subgroup.index[j]]['week_number']
                HighHospitalisedCount = G.nodes[subgroup.index[j]]['hospitalized_count'] >= G.nodes[subgroup_next.index[i]]['not_hospitalised_count']
                HighDeceasedCount = G.nodes[subgroup.index[j]]['deceased_count'] >= G.nodes[subgroup_next.index[i]]['deceased_count']
                HighLocalAcqUnidentifiedInterstateTravelCount = G.nodes[subgroup.index[j]]['localacq_unident_interstate_trvl_count'] >= G.nodes[subgroup_next.index[i]]['localacq_unident_interstate_trvl_count']
                HighOverseasAcquiredCount = G.nodes[subgroup.index[j]]['overseas_acquired_count'] >= G.nodes[subgroup_next.index[i]]['overseas_acquired_count']
                HighLocallyAcquiredContactKnownCount = G.nodes[subgroup.index[j]]['locally_acquired_contact_known_count'] >= G.nodes[subgroup_next.index[i]]['locally_acquired_unidentified_count']
                HighUnderInvestigationCount = G.nodes[subgroup.index[j]]['under_investigation_count'] >= G.nodes[subgroup_next.index[i]]['under_investigation_count']
                HighIndigenousCount = G.nodes[subgroup.index[j]]['indigenous_count'] >= G.nodes[subgroup_next.index[i]]['indigenous_count']
                HighICUCount = G.nodes[subgroup.index[j]]['admitted_to_icu_count'] >= G.nodes[subgroup_next.index[i]]['admitted_to_icu_count']
                HighVentilatedCount = G.nodes[subgroup.index[j]]['ventilated_count'] >= G.nodes[subgroup_next.index[i]]['ventilated_count']
                HighMaleCountThanFemaleCount = G.nodes[subgroup.index[j]]['male_count'] >= G.nodes[subgroup_next.index[i]]['female_count']
                HighYoungAgedCount = G.nodes[subgroup.index[j]]['young_aged_count'] >= G.nodes[subgroup_next.index[i]]['young_aged_count']
                HighMidAgedCount = G.nodes[subgroup.index[j]]['mid_aged_count'] >= G.nodes[subgroup_next.index[i]]['mid_aged_count']
                HighOldAgedCount = G.nodes[subgroup.index[j]]['old_aged_count'] >= G.nodes[subgroup_next.index[i]]['old_aged_count']
                HighPatientCount = G.nodes[subgroup.index[j]]['patient_count'] >= G.nodes[subgroup_next.index[i]]['patient_count']

                linkdict[subgroup.index[j] + " - " + subgroup_next.index[i]] = [groupid, int(HighHospitalisedCount),
                                                                           int(HighDeceasedCount),
                                                                           int(HighLocalAcqUnidentifiedInterstateTravelCount),
                                                                           int(HighOverseasAcquiredCount),
                                                                           int(HighLocallyAcquiredContactKnownCount),
                                                                           int(HighUnderInvestigationCount),
                                                                           int(HighIndigenousCount), int(HighICUCount),
                                                                           int(HighVentilatedCount),
                                                                           int(HighMaleCountThanFemaleCount),
                                                                           int(HighYoungAgedCount),
                                                                           int(HighMidAgedCount), int(HighOldAgedCount),
                                                                           int(HighPatientCount)]

    graph_features = pd.DataFrame(linkdict, index=['groupid', "HighHospitalisedCount", "HighDeceasedCount", "HighLocalUnidenInterTravCount", "HighOverseasAcqCount",
                                                    "HighLocalAcqKnownCount", "HighUnderInvestCount", "HighIndigenousCount", 'HighICUCount', 'HighVentilatedCount',
                                                    "HighMalesThanFemales", "HighYoungAgedCount", "HighMidAgedCount", 'HighOldAgedCount', 'HighPatientCount',
                                                           ])
    graph_features = graph_features.transpose()
    graph_features.to_pickle(edges_file)
    feature_reduction(graph_features)

def feature_reduction(df):
    for col in df.columns:
        count_unique = len(df[col].unique())
        if count_unique == 1:
            df.drop(col, inplace=True, axis=1)
    columns = list(df.columns)
    for i in range(0, len(columns)-1):
        for j in range(i+1, len(columns)):
            correlation = df[columns[i]].corr(df[columns[j]])
            if correlation == 1:
                print("Correlated Features: ", columns[i], columns[j])
    df.to_pickle(edges_file)
    print("Compeleted creating node features...")

