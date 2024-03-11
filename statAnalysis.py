import numpy as np
import pandas as pd

record = pd.read_csv('IPL_Ball_by_Ball.csv')
ipl = pd.read_csv('IPL.csv')

ipl.loc[502,'MatchNumber']='Eliminator'
ipl.loc[503,'MatchNumber']='Qualifier 2'
ipl.loc[559,'MatchNumber']='Eliminator'
ipl.loc[560,'MatchNumber']='Qualifier 2'
ipl.loc[619,'MatchNumber']='Qualifier 1'
ipl.loc[620,'MatchNumber']='Qualifier 2'
ipl.loc[618,'MatchNumber']='Eliminator'
ipl.loc[692,'MatchNumber']='Eliminator'
ipl.loc[766,'MatchNumber']='Eliminator'
ipl.loc[1021,'MatchNumber']='Eliminator'

def st(x):
    if x == 'Kings XI Punjab':
        return 'Punjab Kings'
    else:
        return x
ipl['Team1'] = ipl['Team1'].apply(st)
ipl['Team2'] = ipl['Team2'].apply(st)
ipl['TossWinner'] = ipl['TossWinner'].apply(st)
ipl['WinningTeam'] = ipl['WinningTeam'].apply(st)


def st1(x):
    if x == 'Delhi Daredevils':
        return 'Delhi Capitals'
    else:
        return x
ipl['Team1'] = ipl['Team1'].apply(st1)
ipl['Team2'] = ipl['Team2'].apply(st1)
ipl['TossWinner'] = ipl['TossWinner'].apply(st1)
ipl['WinningTeam'] = ipl['WinningTeam'].apply(st1)


def st2(x):
    if x == 'Rising Pune Supergiant':
        return 'Rising Pune Supergiants'
    else:
        return x
ipl['Team1'] = ipl['Team1'].apply(st2)
ipl['Team2'] = ipl['Team2'].apply(st2)
ipl['TossWinner'] = ipl['TossWinner'].apply(st2)
ipl['WinningTeam'] = ipl['WinningTeam'].apply(st2)

# print(ipl['Team2'].nunique())

data = record.merge(ipl,on='ID',how='inner').copy()
data['BowlingTeam'] = data.Team1 + data.Team2
data['BowlingTeam'] = data[['BowlingTeam', 'BattingTeam']].apply(lambda x: x.values[0].replace(x.values[1], ''), axis=1)

class Stats:

    def func(self,x):
        return '-'.join(list(np.sort(x.values)))

    def parterships(self):
        data["batter-pair"] = data[["Batter", "NonStriker"]].apply(self.func, axis=1)

        temp = data.groupby("batter-pair").agg({'TotalRun': 'sum','BatsmanRun': 'count','IsWicketDelivery': 'sum'}).reset_index()

        temp = temp.rename(columns={'TotalRun': 'Runs', 'BatsmanRun': 'Balls'})
        temp['StrikeRate'] = (temp['Runs'] / temp['Balls']) * 100
        temp['Average'] = (temp['Runs'] / temp['IsWicketDelivery'])
        temp['Batter-1'] = temp['batter-pair'].str.split('-').str.get(0)
        temp['Batter-2'] = temp['batter-pair'].str.split('-').str.get(1)
        ans = temp[['Batter-1', 'Batter-2', 'Runs', 'Balls', 'StrikeRate', 'Average']].sort_values(by='Runs',ascending=False).head(10)

        x = ans.set_index('Batter-1').reset_index().reset_index()
        x['index'] = x['index'].shift(-1)
        x.loc[9, 'index'] = 10.0
        x['index'] = x['index'].astype('int')
        x.set_index('index', inplace=True)

        return x

    #most boundris

    def fours(self):
        mask = data[data['BatsmanRun'] == 4]
        four = mask.groupby('Batter')['BatsmanRun'].count().sort_values(ascending=False).head(10)

        return four

    def sixes(self):
        mask = data[data['BatsmanRun'] == 6]
        six = mask.groupby('Batter')['BatsmanRun'].count().sort_values(ascending=False).head(10)

        return six

    # my logic
    # my logic
    def win_percentage(self):
        ipl1 = ipl[~ipl['WinningTeam'].isna()]
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

        return x.set_index('index')

    def win_percentagePie(self):
        ipl1 = ipl[~ipl['WinningTeam'].isna()]

        home_win = round((ipl1[ipl1['Team1'] == ipl1['WinningTeam']]['WinningTeam'].value_counts()) / ipl1[
            'Team1'].value_counts() * 100, 2)
        away_win = round((ipl1[ipl1['Team2'] == ipl1['WinningTeam']]['WinningTeam'].value_counts()) / ipl1[
            'Team2'].value_counts() * 100, 2)

        df = pd.DataFrame()
        df = df._append([home_win, away_win], ignore_index=True)

        x = df.reset_index()
        x.loc[0, 'index'] = 'Total Matches'
        x.loc[1, 'index'] = 'Total Win(%)'
        x.loc[2, 'index'] = 'Home Win(%)'
        x.loc[3, 'index'] = 'Away Win(%)'

        return x.set_index('index')