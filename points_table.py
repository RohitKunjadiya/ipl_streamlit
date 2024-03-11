import streamlit as st
from playerAnalysis import Player

def app():

    player = Player()
    st.title('Points Table:')

    season = st.sidebar.selectbox('Select Season:',player.season())
    btn = st.sidebar.button('Show')

    if btn:
        st.dataframe(player.seasonPosition(season),width=800)