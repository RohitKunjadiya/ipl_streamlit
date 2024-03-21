import streamlit as st
from playerAnalysis import Player
import plotly.express as px

def app():

    st.title("Bowler's Performance")
    player=Player()

    ip = st.selectbox('Enter Bowler Name:',player.bowler())

    col1,col2 = st.columns(2)

    with col1:
        st.subheader('Total Wickets:')
        st.subheader(player.bowler_wickets(ip))

    with col2:
        st.subheader('Best Bowling Figure:')
        st.write(player.best_figure(ip))

    # col1,col2 = st.columns(2)

    # with col1:
    #     st.subheader('Wickets Against Teams:')
    #     st.dataframe(player.wicket_against_team(ip),width=200)

    st.subheader("Bowler's Wickets Against Each Team:")
    fig = px.bar(player.wicket_against_teamChart(ip), x='BattingTeam', y='Wickets',
                 title="Visual Representation of Bowler's Against Each Team")
    fig.update_xaxes(type='category')
    st.plotly_chart(fig)

    # with col2:
    #     st.subheader('Wickets in Each Season:')
    #     st.dataframe(player.wickets_seasonwise(ip), width=290)
    #

    st.subheader("Bowler's Wickets in Each Season:")
    fig = px.bar(player.wickets_seasonwiseChart(ip), x='Season', y='Wickets',
                 title="Visual Representation of Bowler's Wickets Each Season")
    fig.update_xaxes(type='category')
    st.plotly_chart(fig)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Top-10 Highest Wicket-Takers in IPL till 2023: ')
        st.dataframe(player.wickets(),column_config={'Kind':'Wickets'},width=290)

    with col2:
        st.subheader('Top-10 Battles in IPL till 2023: ')
        st.dataframe(player.h2h_bowler(),width=410)

    st.subheader('Purple-Cap Holders:')
    st.dataframe(player.purple_cap(),column_config={'IsWicketDelivery':'Wickets','bowlers_run':'Runs Conceded','islegelball':'Balls'},width=800,height=597)