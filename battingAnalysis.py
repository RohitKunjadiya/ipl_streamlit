import numpy as np
import pandas as pd

record = pd.read_csv('IPL_2024_ball_by_ball.csv')
ipl = pd.read_csv('IPL.csv')

ipl = ipl[ipl['WinningTeam'] != 'NR']

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

def st3(t):
    if t == 'Royal Challengers Bangalore':
        return 'Royal Challengers Bengaluru'
    else:
        return t
ipl['Team1'] = ipl['Team1'].apply(st3)
ipl['Team2'] = ipl['Team2'].apply(st3)
ipl['TossWinner'] = ipl['TossWinner'].apply(st3)
ipl['WinningTeam'] = ipl['WinningTeam'].apply(st3)

# print(ipl['Team2'].nunique())

data = record.merge(ipl,on='ID',how='inner').copy()

data['BattingTeam'] = data['BattingTeam'].apply(st)
data['BowlingTeam'] = data['BowlingTeam'].apply(st)

data['BattingTeam'] = data['BattingTeam'].apply(st1)
data['BowlingTeam'] = data['BowlingTeam'].apply(st1)

data['BattingTeam'] = data['BattingTeam'].apply(st2)
data['BowlingTeam'] = data['BowlingTeam'].apply(st2)

data['BattingTeam'] = data['BattingTeam'].apply(st3)
data['BowlingTeam'] = data['BowlingTeam'].apply(st3)

class Batters:

    # All batters in ipl till 2024
    def batter(self):
        return data['Batter'].unique()

    # strike of player
    def strike_rate(self,player):
        df = data[data['Batter'] == player]
        runs = df['BatsmanRun'].sum()
        balls = df['BatsmanRun'].count()
        wides = data[data['ExtraType'] == 'wides']
        wcount = wides[wides['Batter'] == player]['ExtrasRun'].count()
        sr = runs / (balls - wcount) * 100

        return np.round(sr, 2)

    # batter statistics in ipl of batter till 2024
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

        runs = x.groupby(['Batter', 'ID'])['BatsmanRun'].sum()
        fifties = runs[(runs >= 50) & (runs < 100)].shape[0]
        hundreds = runs[runs >= 100].shape[0]
        highest_score = runs.max()

        mask = x[(x['BatsmanRun'] == 4) & (x['ExtrasRun'] == 0)]
        four = mask.groupby('Batter')['BatsmanRun'].count()

        mask = x[(x['BatsmanRun'] == 6) & (x['ExtrasRun'] == 0)]
        six = mask.groupby('Batter')['BatsmanRun'].count()

        sr = self.strike_rate(batter)

        avg = round(total_run/out,2)

        d = {
            'Matches': Matches_played,
            'Innings': inn,
            # 'Out': out,
            'NO': not_out,
            'Runs': total_run,
            'HS':highest_score,
            'Average': avg,
            'SR': sr,
            '100s': hundreds,
            '50s': fifties,
            'Fours': four,
            'Six': six}
        return d

    # batter's run against team
    def runs_against_team(self,player):
        bats = data[data['Batter'] == player]
        tr = bats.groupby('BowlingTeam')['BatsmanRun'].sum()
        run = tr.sort_values(ascending=False)

        return pd.DataFrame(run)

    # def runs_against_teamChart(self,player):
    #     bats = data[data['Batter'] == player]
    #     tr = bats.groupby('BowlingTeam')['BatsmanRun'].sum()
    #     run = tr.sort_values(ascending=False)
    #
    #     runs = pd.DataFrame(run).reset_index()
    #     runs.rename(columns={'BowlingTeam':'Bowling Team','BatsmanRun':'Runs'},inplace=True)
    #
    #     return runs

    # batter's runs in each season
    def batter_score_seasonwise(self, batter):
        try:
            x = data[data['Batter'] == batter]
            y = x.groupby(['Season', 'Batter'])['BatsmanRun'].sum().sort_values(
                ascending=False).reset_index().sort_values(by='Season')
            y.rename(columns={'BatsmanRun': 'Runs'}, inplace=True)

            return y[['Season', 'Runs']]
        except:
            return 'Not Played'

    # top-10 batter's till 2024
    def top_10(self):
        return data.groupby('Batter')['BatsmanRun'].sum().sort_values(ascending=False).head(10)

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

    # orange cap holder
    def orange_cap_holder(self):
        data['ball_played'] = data['ExtraType'].apply(lambda x:0 if x in ['wides'] else 1)
        data['out'] = (data['Batter'] == data['PlayerOut']) & (~data['Kind'].isin(['run out', 'retired hurt', 'retired hurt']))
        x = data.groupby(['Season', 'Batter'])
        x = x.agg({'BatsmanRun': 'sum', 'ball_played': 'sum', 'out': 'sum'}).rename(columns={'BatsmanRun': 'Runs', 'ball_played': 'Balls'}).sort_values(by='Runs',ascending=False).reset_index().drop_duplicates('Season', keep='first').sort_values(by='Season')
        x['Strike Rate'] = round(x['Runs'] / x['Balls'] * 100, 2)
        x['Average'] = round(x['Runs'] / x['out'], 2)
        x.set_index('Season', inplace=True)
        return x