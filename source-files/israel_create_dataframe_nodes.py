import pandas as pd


def create_dataframe():
    df = pd.read_csv("../assets/corona_tested_individuals_ver_006.english.csv")
    dataframe = pd.DataFrame()
    dataframe["test_date"] = df["test_date"]
    dataframe["got_cough"] = df["cough"]
    dataframe["got_fever"] = df["fever"]
    dataframe["got_sore_throat"] = df["sore_throat"]
    dataframe["got_shortness_of_breath"] = df["shortness_of_breath"]
    dataframe["got_head_ache"] = df["head_ache"]

    corona_positive = []
    for item in df["corona_result"]:
        if item == "positive":
            corona_positive.append(1)
        else:
            corona_positive.append(0)
    dataframe["corona_positive"] = corona_positive

    age_above_60 = []
    for item in df["age_60_and_above"]:
        if item == "Yes":
            age_above_60.append(1)
        else:
            age_above_60.append(0)
    dataframe["age_above_60"] = age_above_60


    is_male = []
    for item in df["gender"]:
        if item == "male":
            is_male.append(1)
        else:
            is_male.append(0)
    dataframe["is_male"] = is_male


    is_female = []
    for item in df["gender"]:
        if item == "female":
            is_female.append(1)
        else:
            is_female.append(0)
    dataframe["is_female"] = is_female

    contact_with_confirmed_case = []
    for item in df["test_indication"]:
        if item == "Contact with confirmed":
            contact_with_confirmed_case.append(1)
        else:
            contact_with_confirmed_case.append(0)
    dataframe["contact_with_confirmed_case"] = contact_with_confirmed_case

    acquired_overseas = []
    for item in df["test_indication"]:
        if item == "Abroad":
            acquired_overseas.append(1)
        else:
            acquired_overseas.append(0)
    dataframe["acquired_overseas"] = acquired_overseas

    df1 = pd.read_csv("../assets/corona_tested_individuals_ver_0083.english.csv")
    dataframe1 = pd.DataFrame()
    dataframe1["test_date"] = df1["test_date"]
    dataframe1["got_cough"] = df1["cough"]
    dataframe1["got_fever"] = df1["fever"]
    dataframe1["got_sore_throat"] = df1["sore_throat"]
    dataframe1["got_shortness_of_breath"] = df1["shortness_of_breath"]
    dataframe1["got_head_ache"] = df1["head_ache"]

    corona_positive = []
    for item in df1["corona_result"]:
        if item == "positive":
            corona_positive.append(1)
        else:
            corona_positive.append(0)
    dataframe1["corona_positive"] = corona_positive

    age_above_60 = []
    for item in df1["age_60_and_above"]:
        if item == "Yes":
            age_above_60.append(1)
        else:
            age_above_60.append(0)
    dataframe1["age_above_60"] = age_above_60

    is_male = []
    for item in df1["gender"]:
        if item == "male":
            is_male.append(1)
        else:
            is_male.append(0)
    dataframe1["is_male"] = is_male

    is_female = []
    for item in df1["gender"]:
        if item == "female":
            is_female.append(1)
        else:
            is_female.append(0)
    dataframe1["is_female"] = is_female

    contact_with_confirmed_case = []
    for item in df1["test_indication"]:
        if item == "Contact with confirmed":
            contact_with_confirmed_case.append(1)
        else:
            contact_with_confirmed_case.append(0)
    dataframe1["contact_with_confirmed_case"] = contact_with_confirmed_case

    acquired_overseas = []
    for item in df1["test_indication"]:
        if item == "Abroad":
            acquired_overseas.append(1)
        else:
            acquired_overseas.append(0)
    dataframe1["acquired_overseas"] = acquired_overseas

    dataframe = dataframe.append(dataframe1)
    sum_cols(dataframe)

def sum_cols(df):
    columns = ['GotCoughCount', 'GotFeverCount', 'GotSoreThroatCount',
                   'GotShortBreathCount', 'GotHeadAcheCount',
                   'CoronaPosCount', 'AgeAbove60Count', 'IsMaleCount', 'IsFemaleCount','ContWithConfCaseCount',
                   'AcqOverseasCount']
    dataframe = pd.DataFrame(columns = columns)
    groups = df.groupby("test_date")
    for val in df["test_date"].unique():
        subgroup = groups.get_group(val)
        subgroup_row = []
        for col in subgroup.columns[1:]:
            col_list = list(subgroup[col])
            for i in range(0, len(col_list)):
                try:
                    col_list[i] = int(col_list[i])
                except ValueError:
                    col_list[i] = 0
            sum_col = sum(col_list)
            subgroup_row.append(sum_col)
        dataframe.loc[val] = subgroup_row
    create_binary_df(dataframe)

def create_binary_df(df):
    new_columns = ['GotCoughCount', 'GotFeverCount', 'GotSoreThroatCount',
                   'GotShortBreathCount', 'GotHeadAcheCount',
                   'CoronaPosCount', 'AgeAbove60Count', 'ContWithConfCaseCount',
                   'AcqOverseasCount']
    dataframe = pd.DataFrame(index=df.index)

    col_means = {}
    for col in new_columns:
        col_mean = df[col].mean()
        col_means[col] = col_mean

    for col in new_columns:
        new_col = []
        new_col_name = "High" + col
        for index, row in df.iterrows():
            if row[col] > col_means[col]:
                new_col.append(1)
            else:
                new_col.append(0)
        dataframe[new_col_name] = new_col

    new_col = []
    for index, row in df.iterrows():
        if row['IsMaleCount'] > row['IsFemaleCount']:
            new_col.append(1)
        else:
            new_col.append(0)
    dataframe["HighMalesThanFemales"] = new_col

    feature_reduction(dataframe)

def feature_reduction(df):
    for col in df.columns:
        count_unique = len(df[col].unique())
        if count_unique == 1:
            print(col)
            df.drop(col, inplace=True, axis=1)
    columns = list(df.columns)
    for i in range(0, len(columns) - 1):
        for j in range(i + 1, len(columns)):
            correlation = df[columns[i]].corr(df[columns[j]])
            if correlation == 1:
                print(columns[i], columns[j])
    df.to_csv("../results/israel_nodes_dataset.csv")
    df.to_pickle("../results/israel_nodes_dataset.pkl")

