import pandas as pd

ipl = pd.read_csv('IPL_cleaned.csv')

ipl.sort_values(['Date'],inplace=True)

class IPL:

    # total teams in ipl till now(2024)
    def teams(self):
        return list(ipl['Team1'].unique())
        # print(teams())

    # teamVsteam
    def teamVsteam(self,team1, team2):

        teams = ipl['Team1'].unique()
        if team1 in teams and team2 in teams:
            df = ipl[
                (ipl['Team1'] == team1) & (ipl['Team2'] == team2) | (ipl['Team1'] == team2) & (ipl['Team2'] == team1)]
            tm = df.shape[0]

            t1_won = df[df['WinningTeam'] == team1].shape[0]
            t2_won = df[df['WinningTeam'] == team2].shape[0]

            #     t1_loss = df[df['WinningTeam'] != team1].shape[0]
            #     t2_loss = df[df['WinningTeam'] != team2].shape[0]

            nr = tm - (t1_won + t2_won)

            response = {
                'Total Matches': str(tm),
                team1: str(t1_won),
                team2: str(t2_won),
                'No Result': str(nr),
            }

            return response
        else:
            return {'message': 'Invalid Team Name'}

    # team record
    def team_record(self,team):
        teams = list(ipl['Team1'].unique())

        if team in teams:
            mask = ipl[(ipl['Team1'] == team) | (ipl['Team2'] == team)]
            tm = mask.shape[0]
            title = ipl[(ipl['MatchNumber'] == 'Final') & (ipl['WinningTeam'] == team)].shape[0]
            won = mask[mask['WinningTeam'] == team].shape[0]
            loss = mask[mask['WinningTeam'] != team].shape[0] - mask[mask['WinningTeam'] == 'NR'].shape[0]
            nr = mask[mask['WinningTeam'] == 'NR'].shape[0]

            response = {
                'Team': str(team),
                'Total Matches': str(tm),
                'Won': str(won),
                'Loss': str(loss),
                'No Result': str(nr),
                'Title': str(title)
            }
            return response
        else:
            return {'message': 'Invalid team name'}

    # pie chart
    def team_recordPie(self,team):
        teams = list(ipl['Team1'].unique())

        if team in teams:
            mask = ipl[(ipl['Team1'] == team) | (ipl['Team2'] == team)]
            tm = mask.shape[0]
            title = ipl[(ipl['MatchNumber'] == 'Final') & (ipl['WinningTeam'] == team)].shape[0]
            won = mask[mask['WinningTeam'] == team].shape[0]
            loss = mask[mask['WinningTeam'] != team].shape[0] - mask[mask['WinningTeam'] == 'NR'].shape[0]
            nr = mask[mask['WinningTeam'] == 'NR'].shape[0]

            response = {

                'Won': str(won),
                'Loss': str(loss),
                'No Result': str(nr),
            }

            response = pd.DataFrame(pd.DataFrame(response, index=[1]).stack()).reset_index()
            response.drop('level_0', axis=1, inplace=True)
            response.rename(columns={'level_1': 'Team Name', 0: 'Results'}, inplace=True)

            return response
        else:
            return {'message': 'Invalid team name'}

    # pie chart of h2h(2 teams)
    def teamVsteamPie(self,team1, team2):

        teams = list(ipl['Team1'].unique())
        if team1 in teams and team2 in teams:
            df = ipl[(ipl['Team1'] == team1) & (ipl['Team2'] == team2) | (ipl['Team1'] == team2) & (ipl['Team2'] == team1)]
            tm = df.shape[0]

            t1_won = df[df['WinningTeam'] == team1].shape[0]
            t2_won = df[df['WinningTeam'] == team2].shape[0]

            #     t1_loss = df[df['WinningTeam'] != team1].shape[0]
            #     t2_loss = df[df['WinningTeam'] != team2].shape[0]

            nr = tm - (t1_won + t2_won)

            response = {
                team1: str(t1_won),
                team2: str(t2_won),
                'No Result': str(nr),
            }
            response = pd.DataFrame(pd.DataFrame(response, index=[1]).stack()).reset_index()
            response.drop('level_0', axis=1, inplace=True)
            response.rename(columns={'level_1': 'Team Name', 0: 'Results'}, inplace=True)

            return response
        else:
            return {'message': 'Invalid Team Name'}