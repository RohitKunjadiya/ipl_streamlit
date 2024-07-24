import pandas as pd

ipl = pd.read_csv('IPL_cleaned.csv')

class Points_Table:

#points table
    def matches_played(self,data, team):
        return data[(data['Team1'] == team) | (data['Team2'] == team)].shape[0]

    def matches_won(self,data, team):
        return data[(data['WinningTeam'] == team)].shape[0]

    def matches_no_result(self,data, team):
        return data[((data['Team1'] == team) | (data['Team2'] == team)) & (data['WinningTeam'] == 'NR')].shape[0]

    ipl.loc[55, ipl.columns[4]] = 'Qualifier 1'
    ipl.loc[56, ipl.columns[4]] = 'Qualifier 2'
    ipl.loc[112, ipl.columns[4]] = 'Qualifier 1'
    ipl.loc[113, ipl.columns[4]] = 'Qualifier 2'
    ipl.loc[171, ipl.columns[4]] = 'Qualifier 1'
    ipl.loc[172, ipl.columns[4]] = 'Qualifier 2'
    ipl.loc[173, ipl.columns[4]] = 'Eliminator'
    ipl.loc[245, ipl.columns[4]] = 'Eliminator'
    ipl.loc[319, ipl.columns[4]] = 'Eliminator'
    ipl.loc[574, ipl.columns[4]] = 'Eliminator'
    ipl.loc[692, ipl.columns[4]] = 'Qualifier 1'
    ipl.loc[1101,ipl.columns[4]] = 'Qualifier 2'

    ipl['Season'] = ipl['Season'].astype('int')

    # find ipl season(2008-2024)
    def season(self):
        return sorted(ipl.Season.unique())

    # points table of each season
    def points_table(self,season):
        df = ipl[ipl['Season'] == season]
        temp = pd.DataFrame()
        temp['Team Name'] = (ipl[ipl['Season'] == season]['Team1'].value_counts() + ipl[ipl['Season'] == season]['Team2'].value_counts()).index.tolist()
        temp['Matches Played'] = temp['Team Name'].apply(lambda x: self.matches_played(df, x))
        temp['Matches Won'] = temp['Team Name'].apply(lambda x: self.matches_won(df, x))
        temp['No Result'] = temp['Team Name'].apply(lambda x: self.matches_no_result(df, x))
        temp['Points'] = temp['Matches Won'] * 2 + temp['No Result']

        temp.sort_values(['Points','Matches Played'], ascending=False, inplace=True)
        temp.set_index('Team Name', inplace=True)

        return temp

    # season position of ipl team
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

        if (season == 2008) or (season == 2009):
            a = df[df['MatchNumber'] == 'Qualifier 1']
            b = df[df['MatchNumber'] == 'Qualifier 2']
            third = a['LossingTeam'].values[0]
            fourth = b['LossingTeam'].values[0]
            x.at[third, 'Position'] = 'Third'
            x.at[fourth, 'Position'] = 'Fourth'

        elif (season == 2010):
            c = df[df['MatchNumber'] == 'Qualifier 1']
            d = df[df['MatchNumber'] == 'Qualifier 2']
            third = c['LossingTeam'].values[0]
            fourth = d['LossingTeam'].values[0]
            x.at[third, 'Position'] = 'Third'
            x.at[fourth, 'Position'] = 'Fourth'

        else:
            q = df[df['MatchNumber'] == 'Qualifier 2']
            e = df[df['MatchNumber'] == 'Eliminator']
            third = q['LossingTeam'].values[0]
            fourth = e['LossingTeam'].values[0]
            x.at[third, 'Position'] = 'Third'
            x.at[fourth, 'Position'] = 'Fourth'

        return x