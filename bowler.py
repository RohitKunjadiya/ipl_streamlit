import streamlit as st
from playerAnalysis import Player

def app():

    st.title("Bowler's Performance")
    player=Player()

    ip = st.selectbox('Enter Bowler Name:',player.bowler())

    st.subheader('Total Wickets:')
    st.subheader(player.bowler_wickets(ip))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Top-10 Highest Wicket-Takers in IPL till 2023: ')
        st.dataframe(player.wickets(),column_config={'Kind':'Wickets'},width=290)

    with col2:
        st.subheader('Top-10 Battles in IPL till 2023: ')
        st.dataframe(player.h2h_bowler(),width=410)

    st.subheader('Purple-Cap Holder:')
    st.dataframe(player.purple_cap(),column_config={'IsWicketDelivery':'Wickets','bowlers_run':'Runs Conceded','islegelball':'Balls'},width=800,height=597)