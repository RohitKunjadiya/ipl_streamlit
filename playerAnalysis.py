import numpy as np
import pandas as pd

record = pd.read_csv('IPL_Ball_by_Ball.csv')
ipl = pd.read_csv('IPL_Matches.csv')

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

def edit(x):
    if x == '2007/08':
        return '2008'
    else:
        return x

def edit1(x):
    if x == '2009/10':
        return '2010'
    else:
        return x

def edit2(x):
    if x == '2020/21':
        return '2020'
    else:
        return x

ipl['Season'] = ipl['Season'].apply(edit)
ipl['Season'] = ipl['Season'].apply(edit1)
ipl['Season'] = ipl['Season'].apply(edit2)

data = record.merge(ipl,on='ID',how='inner').copy()
data['BowlingTeam'] = data['Team1'] + data['Team2']
data['BowlingTeam'] = data[['BattingTeam','BowlingTeam']].apply(lambda x: x.values[1].replace(x.values[0], ''), axis=1)

data['BattingTeam'] = data['BattingTeam'].apply(st)
data['BowlingTeam'] = data['BowlingTeam'].apply(st)

data['BattingTeam'] = data['BattingTeam'].apply(st1)
data['BowlingTeam'] = data['BowlingTeam'].apply(st1)

data['BattingTeam'] = data['BattingTeam'].apply(st2)
data['BowlingTeam'] = data['BowlingTeam'].apply(st2)

data['BowlingTeam'] = data['Team1'] + data['Team2']
data['BowlingTeam'] = data[['BattingTeam','BowlingTeam']].apply(lambda x: x.values[1].replace(x.values[0], ''), axis=1)
# print(data['BowlingTeam'].unique())

data['out'] = (data['Batter'] == data['PlayerOut']) & (
            ~data['Kind'].isin(['run out', 'retired hurt', 'retired hurt']))
data['bowlers_run'] = data['ExtraType'].apply(lambda x: 0 if x in ['legbyes', 'byes'] else 1) * data['TotalRun']
data['ball_played'] = data['ExtraType'].apply(lambda x: 0 if x in ['wides'] else 1)

class Player:

    def batter(self):
        return data['Batter'].unique()

    def season(self):
        return data['Season'].unique()

    def batter_score_in_season(self, batter, season):
        try:
            x = data[data['Batter'] == batter]
            y = x[x['Season'] == season]
            return y.groupby('Batter')['BatsmanRun'].sum().sort_values(ascending=False).values[0]
        except:
            return 'Not Played'

    def batter_score_seasonwise(self,batter):
        try:
            x = data[data['Batter'] == batter]
            y = x.groupby(['Season', 'Batter'])['BatsmanRun'].sum().sort_values(
                ascending=False).reset_index().sort_values(by='Season')
            y.rename(columns={'BatsmanRun': 'Runs'}, inplace=True)

            return y[['Season', 'Runs']]
        except:
            return 'Not Played'

    # Highest Strike Rate
    def sr(self):
        df = data[data['Overs'] > 15]
        x = df.groupby('Batter')['BatsmanRun'].count()
        y = x > 200
        batsman_list = x[y].index.tolist()

        final = df[df['Batter'].isin(batsman_list)]
        runs = final.groupby('Batter')['BatsmanRun'].sum()
        balls = final.groupby('Batter')['BatsmanRun'].count()
        sr = (runs / balls) * 100
        srate = np.round(sr, 2).sort_values(ascending=False).head(10)
        sr = pd.DataFrame(srate)
        return sr

    def top_10(self):
        return data.groupby('Batter')['BatsmanRun'].sum().sort_values(ascending=False).head(10)

    def run(self,player):
        df = data[data['Batter'] == player]
        runs = df['BatsmanRun'].sum()

        return runs
    def strike_rate(self,player):
        df = data[data['Batter'] == player]
        runs = df['BatsmanRun'].sum()
        balls = df['BatsmanRun'].count()
        wides = data[data['ExtraType'] == 'wides']
        wcount = wides[wides['Batter'] == player]['ExtrasRun'].count()
        sr = runs / (balls - wcount) * 100

        return np.round(sr, 2)

    def runs_against_team(self,player):
        bats = data[data['Batter'] == player]
        tr = bats.groupby('BowlingTeam')['BatsmanRun'].sum()
        run = tr.sort_values(ascending=False)

        return pd.DataFrame(run)

    def runs_against_teamChart(self,player):
        bats = data[data['Batter'] == player]
        tr = bats.groupby('BowlingTeam')['BatsmanRun'].sum()
        run = tr.sort_values(ascending=False)

        runs = pd.DataFrame(run).reset_index()
        runs.rename(columns={'BowlingTeam':'Bowling Team','BatsmanRun':'Runs'},inplace=True)

        return runs

    def batter_stats(self,batter):
        out = data[data['PlayerOut'] == batter].shape[0]

        Matches_played = (ipl[ipl['Team1Players'].str.contains(batter)].count() + ipl[
            ipl['Team2Players'].str.contains(batter)].count()).loc['MatchNumber']

        inn = data[data['Batter'] == batter]['ID'].nunique()
        # data[data['Batter']=='V Kohli']['ID'].drop_duplicates().count()
        # data[data['Batter']=='V Kohli']['ID'].unique().shape[0]
        not_out = inn - out
        total_run = data[data['Batter'] == batter]['BatsmanRun'].sum()

        x = data[data['Batter'] == batter]
        mask = x[(x['BatsmanRun'] == 4) & (x['ExtrasRun'] == 0)]
        four = mask.groupby('Batter')['BatsmanRun'].count()

        mask = x[(x['BatsmanRun'] == 6) & (x['ExtrasRun'] == 0)]
        six = mask.groupby('Batter')['BatsmanRun'].count()

        sr = self.strike_rate(batter)

        avg = round(total_run/out,2)

        d = {
            'Matches Played': Matches_played,
            'Innings': inn,
            'Out': out,
            'Not Out': not_out,
            'Total Runs': total_run,
            'Fours': four,
            'Six': six,
            'Strike Rate': sr,
            'Average':avg}
        return d

    #bowling analysis
    def wickets(self):
        l = ['caught', 'bowled', 'lbw', 'caught and bowled', 'stumped', 'retired hurt',
             'hit wicket', 'obstructing the field', 'retired out']
        x = data[data['Kind'].isin(l)]
        wickets = x.groupby('Bowler')['Kind'].count().sort_values(ascending=False)
        return wickets.head(10)

    def run_out(self):
        x = data[data['Kind'] == 'run out']
        runout = x.groupby('Bowler')['Kind'].count().sort_values(ascending=False)
        return runout.head(10)

    #points table
    def matches_played(self,data, team):
        return data[(data['Team1'] == team) | (data['Team2'] == team)].shape[0]

    def matches_won(self,data, team):
        return data[(data['WinningTeam'] == team)].shape[0]

    def matches_no_result(self,data, team):
        return data[((data['Team1'] == team) | (data['Team2'] == team)) & (data['WinningTeam'].isnull())].shape[0]

    def points_table(self,season):
        df = ipl[ipl['Season'] == season]
        temp = pd.DataFrame()
        temp['Team Name'] = df['Team1'].unique()
        temp['Matches Played'] = temp['Team Name'].apply(lambda x: self.matches_played(df, x))
        temp['Matches Won'] = temp['Team Name'].apply(lambda x: self.matches_won(df, x))
        temp['No Result'] = temp['Team Name'].apply(lambda x: self.matches_no_result(df, x))
        temp['Points'] = temp['Matches Won'] * 2 + temp['No Result']

        temp.sort_values(['Points','Matches Played'], ascending=False, inplace=True)
        temp.set_index('Team Name', inplace=True)

        return temp

    def seasonPosition(self,season):
        x = self.points_table(season)
        df = ipl[ipl['Season'] == season].copy()
        x['Position'] = x['Points'].rank(ascending=False, method='first').astype('int')
        # x['Position'] = x.Points.rank(ascending=False, method= 'first').astype('object')

        df['LossingTeam'] = df[df['WinningTeam'] == df['Team1']]['Team2']._append(df[df['WinningTeam'] == df['Team2']]['Team1'])
        final = df[df['MatchNumber'] == 'Final']
        winning_team = final['WinningTeam'].values[0]
        runner_up = final['LossingTeam'].values[0]
        x.at[winning_team, 'Position'] = 'Winners'
        x.at[runner_up, 'Position'] = 'Runners Up'
        q = df[df['MatchNumber'] == 'Qualifier 2']
        e = df[df['MatchNumber'] == 'Eliminator']
        third = q['LossingTeam'].values[0]
        fourth = e['LossingTeam'].values[0]
        x.at[third, 'Position'] = 'Third'
        x.at[fourth, 'Position'] = 'Fourth'

        return x

    def season(self):
        return sorted(ipl.Season.unique())

    #wickets of any bowler
    def bowler(self):
        return data['Bowler'].unique()

    def bowler_wickets(self, bowler):
        l = ['caught', 'bowled', 'lbw', 'caught and bowled', 'stumped', 'retired hurt',
             'hit wicket']
        x = data[data['Kind'].isin(l)]
        df = x[x['Bowler'] == bowler]
        return df.groupby('Bowler')['IsWicketDelivery'].sum().values[0]

    def h2h_bowler(self):

        return data.groupby(['Batter', 'Bowler']).agg({
            'out': 'sum',
            'BatsmanRun': 'sum'
        }).sort_values(by=["out", "BatsmanRun"], ascending=[False, True]).reset_index().set_index('Batter').head(10)

    def purple_cap(self):
        data['IsWicketDelivery'] = data['Kind'].apply(
            lambda x: 1 if x in ['caught', 'caught and bowled', 'bowled', 'stumped', 'lbw', 'hit wicket'] else 0)
        data['bowlers_run'] = data['ExtraType'].apply(lambda x: 0 if x in ['legbyes', 'byes'] else 1) * data['TotalRun']
        data['islegelball'] = data['ExtraType'].apply(lambda x: 0 if x in ['wides', 'noballs'] else 1)

        y = data.groupby(['Season', 'Bowler'], as_index=False)[['IsWicketDelivery', 'bowlers_run', 'islegelball']].sum()
        y['economy'] = round(y['bowlers_run'] / y['islegelball'] * 6,2)
        purple_caps = y.sort_values(by=['IsWicketDelivery', 'economy'], ascending=[False, True]).drop_duplicates(
            'Season', keep='first').sort_values('Season')
        purple_caps = purple_caps.reset_index()
        purple_caps.drop('index', axis=1, inplace=True)
        purple_caps.set_index('Season', inplace=True)

        return purple_caps

    #orange-cap holder
    def orange_cap_holder(self):
        x = data.groupby(['Season', 'Batter'])
        x = x.agg({'BatsmanRun': 'sum', 'ball_played': 'sum', 'out': 'sum'}).rename(
            columns={'BatsmanRun': 'Runs', 'ball_played': 'Balls'}).sort_values(by='Runs',ascending=False).reset_index().drop_duplicates(
            'Season', keep='first').sort_values(by='Season')
        x['Strike Rate'] = round(x['Runs'] / x['Balls'] * 100, 2)
        x['Average'] = round(x['Runs'] / x['out'], 2)
        x.set_index('Season', inplace=True)
        return x

    def wicket_against_team(self, player):
        l = ['caught', 'bowled', 'lbw', 'caught and bowled', 'stumped', 'retired hurt',
             'hit wicket', 'obstructing the field', 'retired out']

        x = data[data['Kind'].isin(l)]
        wct = x[x['Bowler'] == player]
        wc = wct.groupby('BattingTeam')['IsWicketDelivery'].sum()
        return wc.reset_index().rename(columns={'IsWicketDelivery': 'Wickets'}).set_index('BattingTeam')

    def wicket_against_teamChart(self, player):
        l = ['caught', 'bowled', 'lbw', 'caught and bowled', 'stumped', 'retired hurt',
             'hit wicket', 'obstructing the field', 'retired out']

        x = data[data['Kind'].isin(l)]
        wct = x[x['Bowler'] == player]
        wc = wct.groupby('BattingTeam')['IsWicketDelivery'].sum()
        return wc.reset_index().rename(columns={'IsWicketDelivery': 'Wickets'})

    def wickets_seasonwise(self,bowler):
        x = data[data['Bowler'] == bowler]
        l = ['caught', 'bowled', 'lbw', 'caught and bowled', 'stumped', 'retired hurt',
             'hit wicket', 'obstructing the field', 'retired out']
        y = x[x['Kind'].isin(l)]
        z = y.groupby(['Season', 'Bowler'])['IsWicketDelivery'].sum().sort_values(
            ascending=False).reset_index().sort_values(by='Season')
        a = z[['Season', 'IsWicketDelivery']]
        return a.rename(columns={'IsWicketDelivery':'Wickets'}).set_index('Season')

    def wickets_seasonwiseChart(self,bowler):
        x = data[data['Bowler'] == bowler]
        l = ['caught', 'bowled', 'lbw', 'caught and bowled', 'stumped', 'retired hurt',
             'hit wicket', 'obstructing the field', 'retired out']
        y = x[x['Kind'].isin(l)]
        z = y.groupby(['Season', 'Bowler'])['IsWicketDelivery'].sum().sort_values(
            ascending=False).reset_index().sort_values(by='Season')
        a = z[['Season', 'IsWicketDelivery']]
        return a.rename(columns={'IsWicketDelivery':'Wickets'})

    def best_figure(self,bowler):
        wct = data[data['Bowler'] == bowler]
        wc = wct.groupby(['ID', 'BattingTeam'])[['bowlers_run', 'out']].sum().reset_index().sort_values('out',
                                                                                                        ascending=False).head(
            1)
        return wc[['BattingTeam', 'bowlers_run', 'out']].set_index('BattingTeam').rename(
            columns={'bowlers_run': 'Runs', 'out': 'Wickets'})