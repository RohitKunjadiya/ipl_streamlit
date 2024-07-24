import numpy as np
import pandas as pd

record = pd.read_csv('ipl_2024_ball_by_ball.csv')
ipl = pd.read_csv('IPL_cleaned.csv')

def st(x):
    if x == 'Kings XI Punjab':
        return 'Punjab Kings'
    else:
        return x

def st1(x):
    if x == 'Delhi Daredevils':
        return 'Delhi Capitals'
    else:
        return x

def st2(x):
    if x == 'Rising Pune Supergiant':
        return 'Rising Pune Supergiants'
    else:
        return x

def st3(t):
    if t == 'Royal Challengers Bangalore':
        return 'Royal Challengers Bengaluru'
    else:
        return t

data = record.merge(ipl,on='ID',how='inner').copy()

data['BattingTeam'] = data['BattingTeam'].apply(st)
data['BowlingTeam'] = data['BowlingTeam'].apply(st)

data['BattingTeam'] = data['BattingTeam'].apply(st1)
data['BowlingTeam'] = data['BowlingTeam'].apply(st1)

data['BattingTeam'] = data['BattingTeam'].apply(st2)
data['BowlingTeam'] = data['BowlingTeam'].apply(st2)

data['BattingTeam'] = data['BattingTeam'].apply(st3)
data['BowlingTeam'] = data['BowlingTeam'].apply(st3)

class Stats:

    # win percentage of teams(home and away)
    def win_percentage(self):
        ipl1 = ipl[~(ipl['WinningTeam'] == 'NR')]
        tm = ipl1['Team1'].value_counts() + ipl1['Team2'].value_counts()

        home_win = round((ipl1[ipl1['Team1'] == ipl1['WinningTeam']]['WinningTeam'].value_counts()) / ipl1[
            'Team1'].value_counts() * 100, 2)
        away_win = round((ipl1[ipl1['Team2'] == ipl1['WinningTeam']]['WinningTeam'].value_counts()) / ipl1[
            'Team2'].value_counts() * 100, 2)

        total_win = round((ipl1[ipl1['Team1'] == ipl1['WinningTeam']]['WinningTeam'].value_counts() +
                           ipl1[ipl1['Team2'] == ipl1['WinningTeam']]['WinningTeam'].value_counts()) / tm * 100, 2)


        df = pd.DataFrame()
        df = df._append([tm.astype('int'), total_win, home_win, away_win], ignore_index=True)

        x = df.reset_index()
        x.loc[0, 'index'] = 'Total Matches'
        x.loc[1, 'index'] = 'Total Win(%)'
        x.loc[2, 'index'] = 'Home Win(%)'
        x.loc[3, 'index'] = 'Away Win(%)'

        return x.set_index('index').T

    # best batting partners in ipl till 2024
    def func(self,x):
        return '-'.join(list(np.sort(x.values)))

    def partnerships(self):
        data["batter-pair"] = data[["Batter", "NonStriker"]].apply(self.func, axis=1)

        temp = data.groupby("batter-pair").agg({'TotalRun': 'sum','BatsmanRun': 'count','IsWicketDelivery': 'sum'}).reset_index()

        temp = temp.rename(columns={'TotalRun': 'Runs', 'BatsmanRun': 'Balls'})
        temp['Strike Rate'] = round((temp['Runs'] / temp['Balls']) * 100,2)
        temp['Average'] = round((temp['Runs'] / temp['IsWicketDelivery']),2)
        temp['Batter-1'] = temp['batter-pair'].str.split('-').str.get(0)
        temp['Batter-2'] = temp['batter-pair'].str.split('-').str.get(1)
        ans = temp[['Batter-1', 'Batter-2', 'Runs', 'Balls', 'Strike Rate', 'Average']].sort_values(by='Runs',ascending=False).head(10)

        x = ans.set_index('Batter-1').reset_index().reset_index()
        x['index'] = x['index'].shift(-1)
        x.loc[9, 'index'] = 10.0
        x['index'] = x['index'].astype('int')
        x.set_index('index', inplace=True)

        return x

    #most boundries
    def fours(self):
        mask = data[data['BatsmanRun'] == 4]
        four = mask.groupby('Batter')['BatsmanRun'].count().sort_values(ascending=False).head(10)

        return four

    # most sixes
    def sixes(self):
        mask = data[data['BatsmanRun'] == 6]
        six = mask.groupby('Batter')['BatsmanRun'].count().sort_values(ascending=False).head(10)

        return six

    # def win_percentagePie(self):
    #     ipl1 = ipl[~ipl['WinningTeam'].isna()]
    #
    #     home_win = round((ipl1[ipl1['Team1'] == ipl1['WinningTeam']]['WinningTeam'].value_counts()) / ipl1[
    #         'Team1'].value_counts() * 100, 2)
    #     away_win = round((ipl1[ipl1['Team2'] == ipl1['WinningTeam']]['WinningTeam'].value_counts()) / ipl1[
    #         'Team2'].value_counts() * 100, 2)
    #
    #     df = pd.DataFrame()
    #     df = df._append([home_win, away_win], ignore_index=True)
    #
    #     x = df.reset_index()
    #     x.loc[0, 'index'] = 'Total Matches'
    #     x.loc[1, 'index'] = 'Total Win(%)'
    #     x.loc[2, 'index'] = 'Home Win(%)'
    #     x.loc[3, 'index'] = 'Away Win(%)'
    #
    #     return x.set_index('index')