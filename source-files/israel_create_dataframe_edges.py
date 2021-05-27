from datetime import datetime
import networkx as nx
import pandas as pd


def add_week_number():
    df = pd.read_csv("../assets/corona_tested_individuals_ver_006.english.csv")
    df2 = pd.read_csv("../assets/corona_tested_individuals_ver_0083.english.csv")
    df = df.append(df2)
    week_number = []
    for index, row in df.iterrows():
        date_time_obj = datetime.strptime(row["test_date"], '%Y-%m-%d')
        week_num = datetime.date(date_time_obj).isocalendar()[1]
        week_number.append(week_num)
    df["week_number"] = week_number
    create_inital_df(df)

def create_inital_df(df):
    dataframe = pd.DataFrame()
    dataframe["TestDate"] = df["test_date"]
    dataframe["WeekNumber"] = df["week_number"]
    dataframe["GotCough"] = df["cough"]
    dataframe["GotFever"] = df["fever"]
    dataframe["GotSoreThroat"] = df["sore_throat"]
    dataframe["GotShortnessOfBreath"] = df["shortness_of_breath"]
    dataframe["GotHeadAche"] = df["head_ache"]

    corona_positive = []
    for item in df["corona_result"]:
        if item == "positive":
            corona_positive.append(1)
        else:
            corona_positive.append(0)
    dataframe["CoronaPositive"] = corona_positive

    age_above_60 = []
    for item in df["age_60_and_above"]:
        if item == "Yes":
            age_above_60.append(1)
        else:
            age_above_60.append(0)
    dataframe["AgeAbove60"] = age_above_60

    is_male = []
    for item in df["gender"]:
        if item == "male":
            is_male.append(1)
        else:
            is_male.append(0)
    dataframe["IsMale"] = is_male

    is_female = []
    for item in df["gender"]:
        if item == "female":
            is_female.append(1)
        else:
            is_female.append(0)
    dataframe["IsFemale"] = is_female

    contact_with_confirmed_case = []
    for item in df["test_indication"]:
        if item == "Contact with confirmed":
            contact_with_confirmed_case.append(1)
        else:
            contact_with_confirmed_case.append(0)
    dataframe["ContactWithConfirmedCase"] = contact_with_confirmed_case

    acquired_overseas = []
    for item in df["test_indication"]:
        if item == "Abroad":
            acquired_overseas.append(1)
        else:
            acquired_overseas.append(0)
    dataframe["AcquiredOverseas"] = acquired_overseas
    sum_cols(dataframe)

def sum_cols(df):
    columns = ['GotCoughCount', 'GotFeverCount', 'GotSoreThroatCount', 'GotShortnessOfBreathCount',
               'GotHeadAcheCount', 'CoronaPositiveCount',
               'AgeAbove60Count', 'IsMaleCount', 'IsFemaleCount', 'ContactWithConfirmedCaseCount',
               'AcquiredOverseasCount']
    dataframe = pd.DataFrame(columns=columns)
    groups = df.groupby("WeekNumber")
    for val in df["WeekNumber"].unique():
        subgroup = groups.get_group(val)
        subgroup_row = []
        for col in subgroup.columns[2:]:
            col_list = list(subgroup[col])
            for i in range(0, len(col_list)):
                try:
                    col_list[i] = int(col_list[i])
                except ValueError:
                    col_list[i] = 0
            sum_col = sum(col_list)
            subgroup_row.append(sum_col)
        dataframe.loc[val] = subgroup_row
    create_edges_among_weeks(dataframe)


def create_edges_among_weeks(df):
    df = df.sort_index()
    linkdict = {}
    G = nx.Graph()
    for index, row in df.iterrows():
        G.add_node(index,
                   node_id=index,
                   GotCoughCount=row['GotCoughCount'],
                   GotFeverCount=row['GotFeverCount'],
                   GotSoreThroatCount=row['GotSoreThroatCount'],
                   GotShortnessOfBreathCount=row['GotShortnessOfBreathCount'],
                   GotHeadAcheCount=row['GotHeadAcheCount'],
                   CoronaPositiveCount=row['CoronaPositiveCount'],
                   AgeAbove60Count=row['AgeAbove60Count'],
                   IsMaleCount=row['IsMaleCount'],
                   IsFemaleCount=row['IsFemaleCount'],
                   ContactWithConfirmedCaseCount=row['ContactWithConfirmedCaseCount'],
                   AcquiredOverseasCount=row['AcquiredOverseasCount'])
    for i in range(0, len(df.index) - 1):  # add an edge from one node to another within a bundle
        G.add_edge(df.index[i], df.index[i+1])
        HighGotCoughCount = int(G.nodes[df.index[i]]['GotCoughCount'] >= G.nodes[df.index[i+1]]['GotCoughCount'])
        HighGotFeverCount = int(G.nodes[df.index[i]]['GotFeverCount'] >= G.nodes[df.index[i + 1]]['GotFeverCount'])
        HighGotSoreThroatCount = int(G.nodes[df.index[i]]['GotSoreThroatCount'] >= G.nodes[df.index[i + 1]]['GotSoreThroatCount'])
        HighGotShortnessOfBreathCount = int(G.nodes[df.index[i]]['GotShortnessOfBreathCount'] >= G.nodes[df.index[i + 1]]['GotShortnessOfBreathCount'])
        HighGotHeadAcheCount = int(G.nodes[df.index[i]]['GotHeadAcheCount'] >= G.nodes[df.index[i + 1]]['GotHeadAcheCount'])
        HighCoronaPositiveCount = int(G.nodes[df.index[i]]['CoronaPositiveCount'] >= G.nodes[df.index[i + 1]]['CoronaPositiveCount'])
        HighAgeAbove60Count = int(G.nodes[df.index[i]]['AgeAbove60Count'] >= G.nodes[df.index[i + 1]]['AgeAbove60Count'])
        HighMaleCountThanFemaleCount = int(G.nodes[df.index[i]]['IsMaleCount'] >= G.nodes[df.index[i + 1]]['IsFemaleCount'])
        HighContactWithConfirmedCaseCount = int(G.nodes[df.index[i]]['ContactWithConfirmedCaseCount'] >= G.nodes[df.index[i + 1]]['ContactWithConfirmedCaseCount'])
        HighAcquiredOverseasCount = int(G.nodes[df.index[i]]['AcquiredOverseasCount'] >= G.nodes[df.index[i + 1]]['AcquiredOverseasCount'])

        linkdict[str(df.index[i]) + " - " + str(df.index[i+1])] = [HighGotCoughCount, HighGotFeverCount,
                                                         HighGotSoreThroatCount, HighGotShortnessOfBreathCount,
                                                         HighGotHeadAcheCount, HighCoronaPositiveCount,
                                                         HighAgeAbove60Count, HighMaleCountThanFemaleCount,
                                                         HighContactWithConfirmedCaseCount, HighAcquiredOverseasCount]

    graph_features = pd.DataFrame(linkdict, index=['IncGotCoughCount', 'IncGotFeverCount', 'IncGotSoreThroatCount',
                                                   'IncGotShortBreathCount','IncGotHeadAcheCount',
                                                   'IncCoronaPosCount', 'IncAgeAbove60Count', 'IncMalesThanFemales',
                                                   'IncContWithConfCaseCount', 'IncAcqOverseasCount'])
    graph_features = graph_features.transpose()
    feature_reduction(graph_features)

def feature_reduction(df):
    for col in df.columns:
        count_unique = len(df[col].unique())
        if count_unique == 1:
            print(col)
            df.drop(col, inplace=True, axis=1)
    columns = list(df.columns)
    for i in range(0, len(columns)-1):
        for j in range(i+1, len(columns)):
            correlation = df[columns[i]].corr(df[columns[j]])
            if correlation == 1:
                print(columns[i], columns[j])
    df.to_csv('../results/israel_edges_dataset.csv')
    df.to_pickle('../results/israel_edges_dataset.pkl')
    print("Completed generating the Israel edges dataset...")

