from datetime import datetime, timedelta
import pandas as pd


def fill_misssing_onset_date():
    print("Filling missing onset date and aggregating the data...")
    df = pd.read_csv("../assets/qld.csv")
    missing_onset, day_dif_dict = [], {}
    for index, row in df.iterrows():
        day_dif, count,  = [], 0
        if str(row['onset_date']) == 'nan':
            if str(row['collectdate']) in day_dif_dict.keys():
                a_date = datetime.strptime(row['collectdate'], "%Y-%m-%d")
                days = timedelta(day_dif_dict[row['collectdate']])
                new_date = a_date - days
                missing_onset.append(new_date)
            else:
                for indexes, rows in df.iterrows():
                    if str(rows['onset_date']) == 'nan':
                        continue
                    else:
                        if str(row['collectdate']) == str(rows['collectdate']):
                            day_dif.append(days_between(rows['onset_date'], rows['collectdate']))
                            count = count + 1
                avg_days = sum(day_dif)/count
                day_dif_dict[str(row['collectdate'])] = avg_days
                a_date = datetime.strptime(row['collectdate'], "%Y-%m-%d")
                days = timedelta(days = avg_days)
                new_date = a_date - days
                missing_onset.append(new_date)
        else:
            break
    non_empty_dates = [day for day in list(df["onset_date"]) if str(day) != 'nan']
    for item in non_empty_dates:
        missing_onset.append(item)
    df['adjusted_onset_date'] = missing_onset
    adjusted_onset_date = list(df['adjusted_onset_date'])
    new_date_format = []
    for item in adjusted_onset_date:
        if len(str(item)) == 10:
            continue
        else:
            date_only = str(item).split(" ")
            new_date_format.append(date_only[0])
    df['adjusted_onset_date'] = new_date_format

    week_number = []
    for index, row in df.iterrows():
        date_time_obj = datetime.strptime(row['adjusted_onset_date'], '%Y-%m-%d')
        week_num = datetime.date(date_time_obj).isocalendar()[1]
        week_number.append(week_num)
    df["week_number"] = week_number
    df.to_csv("../results/qld_onset_date_imputed.csv")
    week_postcode_grouping()

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def week_postcode_grouping():
    df = pd.read_csv("../results/qld_onset_date_imputed.csv")
    df['counter'] = 1
    columns_binary = ['hospitalisaed', 'not_hospitalised', 'deceased','localacq_unident_interstate_trvl', 'overseas_acquired',
       'locally_acquired_contact_known', 'locally_acquired_unidentified','under_investigation']
    columns_categorical = ['indig_status','hospitalised_ever','died_of_condition', 'icu', 'ventilated']
    master_group = df.groupby(["week_number","postcode"])['counter'].sum()
    list_all_keys = list(master_group.keys())
    dataframe = pd.DataFrame(list_all_keys)
    dataframe = dataframe.set_index([0,1])

    for col in columns_binary:
        dict={}
        group = df[df[col] == 1].groupby(["week_number","postcode"])['counter'].sum()
        for key in list_all_keys:
            if key in group.keys():
                dict[key] = group[key]
            else:
                dict[key] = 0
        column_name = col+"_count"
        row = pd.Series(dict, name=column_name)
        dataframe[column_name] = row

    for col in columns_categorical:
        dict = {}
        df[col] = df[col].str.upper()
        group = df[df[col] == 'YES'].groupby(["week_number","postcode"])['counter'].sum()
        for key in list_all_keys:
            if key in group.keys():
                dict[key] = group[key]
            else:
                dict[key] = 0
        if col == 'indig_status':
            column_name = "indigenous_count"
        elif col == 'hospitalised_ever':
            column_name = "hospitalized_count"
        elif col == 'died_of_condition':
            column_name = "died_count"
        elif col == 'icu':
            column_name = "admitted_to_icu_count"
        elif col == 'ventilated':
            column_name = "ventilated_count"
        row = pd.Series(dict, name=column_name)
        dataframe[column_name] = row

    for col in ['female', 'male']:
        dict = {}
        group = df[df['sex'] == col].groupby(["week_number", "postcode"])['counter'].sum()
        for key in list_all_keys:
            if key in group.keys():
                dict[key] = group[key]
            else:
                dict[key] = 0
        column_name = col + "_count"
        row = pd.Series(dict, name=column_name)
        dataframe[column_name] = row

    for col in range(1,11):
        dict = {}
        group = df[df['agegrp5'] == col].groupby(["week_number", "postcode"])['counter'].sum()
        for key in list_all_keys:
            if key in group.keys():
                dict[key] = group[key]
            else:
                dict[key] = 0
        column_name = str(col) + "_agegroup_count"
        row = pd.Series(dict, name=column_name)
        dataframe[column_name] = row

    group = df.groupby(["week_number", "postcode"])['counter'].sum()
    dict = {}
    for key in group.keys():
        dict[key] = group[key]
    column_name = "patient_count"
    row = pd.Series(dict, name=column_name)
    dataframe[column_name] = row
    dataframe.to_csv("../results/qld_groupby_postcode_week.csv")
    merge_postcode_date()

def merge_postcode_date():
    df = pd.read_csv("../results/qld_groupby_postcode_week.csv")
    key = []
    for index, row in df.iterrows():
        key_val = str(int(row[0])) +"_"+ str(int(row[1]))
        key.append(key_val)
    df["index"] = key
    df = df.set_index(["index"])
    df.rename(columns={'0': 'week_number', '1': 'postcode'}, inplace=True)
    feature_reduction(df)

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
                print(columns[i], columns[j])
    df.drop('died_count', inplace=True, axis=1)
    df.drop('hospitalized_count', inplace=True, axis=1)
    df.to_pickle("../results/qld_groupby_postcode_week_reduced_cols_not_norm.pkl")
    df.to_csv("../results/qld_groupby_postcode_week_reduced_cols_not_norm.csv")
    print("Dataframe created and ready to use for node features creation...")


