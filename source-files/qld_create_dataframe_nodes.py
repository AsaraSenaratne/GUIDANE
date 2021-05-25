import pandas as pd
import statistics

def create_dataframe():
    print("Generating features for QLD nodes dataset...")
    df = pd.read_pickle("../results/qld_groupby_postcode_week_reduced_cols_not_norm.pkl")
    dataframe = pd.DataFrame()
    dataframe['week_number'] = df.week_number
    dataframe['postcode'] = df.postcode

    new_col = []
    for index, row in df.iterrows():
        if row['hospitalisaed_count'] > row['not_hospitalised_count']:
            new_col.append(1)
        else:
            new_col.append(0)
    dataframe['HighHospitalizedCount'] = new_col

    new_col = []
    for index, row in df.iterrows():
        if row['male_count'] > row['female_count']:
            new_col.append(1)
        else:
            new_col.append(0)
    dataframe['HighMalesThanFemales'] = new_col

    new_col = []
    for index, row in df.iterrows():
        if row['locally_acquired_contact_known_count'] > row['locally_acquired_unidentified_count']:
            new_col.append(1)
        else:
            new_col.append(0)
    dataframe['HighLocalAcqKnownCount'] = new_col

    columns = ['localacq_unident_interstate_trvl_count', 'overseas_acquired_count', 'under_investigation_count',
       'indigenous_count', 'deceased_count', 'admitted_to_icu_count', 'ventilated_count', 'patient_count']
    new_cols = ['LocalAcqUnidentInterstateTravelCount', 'OverseasAcqCount', 'UnderInvestigationCount',
               'IndigenousCount', 'DeceasedCount', 'AdmittedICUCount', 'VentilatedCount', 'PatientCount']

    col_medians = {}
    for col in columns:
        col_med = df[col].mean()
        col_medians[col] = col_med

    for pos, col in enumerate(columns):
        new_col = []
        new_col_name = "High" + new_cols[pos]
        for index, row in df.iterrows():
            if row[col] > col_medians[col]:
                new_col.append(1)
            else:
                new_col.append(0)
        dataframe[new_col_name] = new_col

    new_col = []
    for index, row in df.iterrows():
        sum = int(row['1_agegroup_count']) + int(row['2_agegroup_count']) + int(row['3_agegroup_count'])
        new_col.append(sum)
    median_val = statistics.mean(new_col)
    new_col = []
    for index, row in df.iterrows():
        if int(row['1_agegroup_count']) + int(row['2_agegroup_count']) + int(row['3_agegroup_count']) > median_val:
            new_col.append(1)
        else:
            new_col.append(0)
    dataframe["HighYoungAgedCount"] = new_col

    new_col = []
    for index, row in df.iterrows():
        sum = int(row['4_agegroup_count']) + int(row['5_agegroup_count']) + int(row['6_agegroup_count']) + int(row['7_agegroup_count'])
        new_col.append(sum)
    median_val = statistics.mean(new_col)
    new_col = []
    for index, row in df.iterrows():
        if int(row['4_agegroup_count']) + int(row['5_agegroup_count']) + int(row['6_agegroup_count']) + int(row['7_agegroup_count']) > median_val:
            new_col.append(1)
        else:
            new_col.append(0)
    dataframe["HighMidAgedCount"] = new_col

    new_col = []
    for index, row in df.iterrows():
        sum = int(row['8_agegroup_count']) + int(row['9_agegroup_count']) + int(row['10_agegroup_count'])
        new_col.append(sum)
    median_val = statistics.mean(new_col)
    new_col = []
    for index, row in df.iterrows():
        if int(row['8_agegroup_count']) + int(row['9_agegroup_count']) + int(row['10_agegroup_count']) > median_val:
            new_col.append(1)
        else:
            new_col.append(0)
    dataframe["HighOldAgedCount"] = new_col
    feature_reduction(dataframe)

def feature_reduction(df):
    for col in df.columns:
        count_unique = len(df[col].unique())
        if count_unique == 1:
            df.drop(col, inplace=True, axis=1)
    columns = list(df.columns)
    for i in range(0, len(columns) - 1):
        for j in range(i + 1, len(columns)):
            correlation = df[columns[i]].corr(df[columns[j]])
            if correlation == 1:
                print("Correlated features: ", columns[i], columns[j])
    df.to_csv("../results/qld_nodes_dataset.csv")
    df.to_pickle("../results/qld_nodes_dataset.pkl")
    print("Completed generating nodes features...")



