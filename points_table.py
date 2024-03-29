import streamlit as st
from playerAnalysis import Player

def app():

    player = Player()

    season = st.sidebar.selectbox('Select Season:',player.season())
    btn = st.sidebar.button('Show')

    if btn:
        st.title('Points Table')
        st.dataframe(player.seasonPosition(season),width=800)