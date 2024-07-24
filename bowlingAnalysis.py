import pandas as pd

record = pd.read_csv('ipl_2024_ball_by_ball.csv')
ipl = pd.read_csv('IPL_cleaned.csv')

ipl = ipl[~ipl['Team1Players'].isna()]

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

class Bowlers:

    # All batters in ipl till 2024
    def batter(self):
        return data['Batter'].unique()

    # All bowlers in ipl till 2024
    def bowler(self):
        return data['Bowler'].unique()

    # batter vs bowler h2h
    def batterVsbowler(self,batter, bowler):
        data['ball_played'] = data['ExtraType'].apply(lambda x: 0 if x in ['wides'] else 1)
        data['out'] = (data['Batter'] == data['PlayerOut']) & (~data['Kind'].isin(['run out', 'retired hurt', 'retired hurt']))
        batter_df = data[data['Batter'] == batter]
        bowler_df = batter_df[batter_df['Bowler'] == bowler]

        if batter == bowler:
            return 'Not Possible!'
        else:
            x = pd.DataFrame(bowler_df.agg({'BatsmanRun': 'sum', 'ball_played': 'sum', 'out': 'sum'})).T.rename(
                columns={'BatsmanRun': 'Runs', 'ball_played': 'Balls', 'out': 'Out'})
            x['Batter'] = batter
            x['Bowler'] = bowler
            x['Fours'] = bowler_df[bowler_df['BatsmanRun'] == 4].shape[0]
            x['Sixes'] = bowler_df[bowler_df['BatsmanRun'] == 6].shape[0]
            x['Strike Rate'] = round(x['Runs'] / x['Balls'] * 100, 2)
            if x['Strike Rate'].isna().any():
                x['Strike Rate'].fillna(0, inplace=True)
            x['Average'] = round(x['Runs'] / x['Out'], 2)
            x.loc[x['Out'] == 0, 'Average'] = 0
            x = x.iloc[:, [3, 4, 0, 1, 5, 6, 2, 7, 8]]
            x.set_index('Batter', inplace=True)
            return x

    # bowler wickets in ipl till 2024
    def bowler_wickets(self, bowler):
        l = ['caught', 'bowled', 'lbw', 'caught and bowled', 'stumped', 'retired hurt',
             'hit wicket']
        x = data[data['Kind'].isin(l)]
        df = x[x['Bowler'] == bowler]
        if df.empty:
            return 0
        else:
            return df.groupby('Bowler')['IsWicketDelivery'].sum().values[0]

    # best figure of any bowler
    def best_figure(self, bowler):
        wct = data[data['Bowler'] == bowler]
        wct['bowlers_run'] = wct['ExtraType'].apply(lambda x: 0 if x in ['legbyes', 'byes'] else 1) * wct['TotalRun']
        wct['out'] = (wct['Batter'] == wct['PlayerOut']) & (~wct['Kind'].isin(['run out', 'retired hurt', 'retired hurt']))
        wc = wct.groupby(['ID', 'BattingTeam'])[['bowlers_run', 'out']].sum().reset_index().sort_values(['out','bowlers_run'],ascending=[False,True]).head(1)
        return wc[['BattingTeam', 'bowlers_run', 'out']].set_index('BattingTeam').rename(columns={'bowlers_run': 'Runs', 'out': 'Wickets'})

    # bar-chart of bowlers wicket against each team
    def wicket_against_teamChart(self, player):
        l = ['caught', 'bowled', 'lbw', 'caught and bowled', 'stumped', 'retired hurt',
             'hit wicket', 'obstructing the field', 'retired out']

        x = data[data['Kind'].isin(l)]
        wct = x[x['Bowler'] == player]
        wc = wct.groupby('BattingTeam')['IsWicketDelivery'].sum()
        return wc.reset_index().rename(columns={'IsWicketDelivery': 'Wickets'})

    # def wicket_against_team(self, player):
    #     l = ['caught', 'bowled', 'lbw', 'caught and bowled', 'stumped', 'retired hurt',
    #          'hit wicket', 'obstructing the field', 'retired out']
    #     x = data[data['Kind'].isin(l)]
    #     wct = x[x['Bowler'] == player]
    #     wc = wct.groupby('BattingTeam')['IsWicketDelivery'].sum()
    #     return wc.reset_index().rename(columns={'IsWicketDelivery': 'Wickets'}).set_index('BattingTeam')

    # bar-chart of bowlers wicket each season
    def wickets_seasonwiseChart(self, bowler):
        x = data[data['Bowler'] == bowler]
        l = ['caught', 'bowled', 'lbw', 'caught and bowled', 'stumped', 'retired hurt',
             'hit wicket', 'obstructing the field', 'retired out']
        y = x[x['Kind'].isin(l)]
        z = y.groupby(['Season', 'Bowler'])['IsWicketDelivery'].sum().sort_values(
            ascending=False).reset_index().sort_values(by='Season')
        a = z[['Season', 'IsWicketDelivery']]
        return a.rename(columns={'IsWicketDelivery': 'Wickets'})

    # def wickets_seasonwise(self, bowler):
    #     x = data[data['Bowler'] == bowler]
    #     l = ['caught', 'bowled', 'lbw', 'caught and bowled', 'stumped', 'retired hurt',
    #          'hit wicket', 'obstructing the field', 'retired out']
    #     y = x[x['Kind'].isin(l)]
    #     z = y.groupby(['Season', 'Bowler'])['IsWicketDelivery'].sum().sort_values(
    #         ascending=False).reset_index().sort_values(by='Season')
    #     a = z[['Season', 'IsWicketDelivery']]
    #     return a.rename(columns={'IsWicketDelivery': 'Wickets'}).set_index('Season')

    # top-10 wicket-takers in ipl till 2024
    def wickets(self):
        l = ['caught', 'bowled', 'lbw', 'caught and bowled', 'stumped', 'retired hurt',
             'hit wicket', 'obstructing the field', 'retired out']
        x = data[data['Kind'].isin(l)]
        wickets = x.groupby('Bowler')['Kind'].count().sort_values(ascending=False)
        return wickets.head(10)

    # top-10 battles(batter-vs-bowler)
    def h2h_bowler(self):
        data['out'] = (data['Batter'] == data['PlayerOut']) & (~data['Kind'].isin(['run out', 'retired hurt', 'retired hurt']))
        return data.groupby(['Batter', 'Bowler']).agg({
            'BatsmanRun': 'sum',
            'out': 'sum'
        }).sort_values(by=["out", "BatsmanRun"], ascending=[False, True]).reset_index().set_index('Batter').head(10)

    # purple cap holder
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