import streamlit as st
from points_tableAnalysis import Points_Table

def app():

    pt = Points_Table()
    st.title('Points Table:')

    season = st.sidebar.selectbox('Select Season:',pt.season())
    btn = st.sidebar.button('Show')

    if btn:
        st.dataframe(pt.seasonPosition(season),width=800)