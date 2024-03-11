import streamlit as st
import plotly.express as px
from statAnalysis import Stats

def app():

    stat = Stats()

    st.title('IPL Stats:')
    st.subheader('Good Batting Partners:')
    st.table(stat.parterships())

    col1,col2 = st.columns(2)

    with col1:
        st.subheader("Most 4's:")
        st.dataframe(stat.fours(),column_config={'BatsmanRun':'Fours'},width=350)

    with col2:
        st.subheader("Most 6's:")
        st.dataframe(stat.sixes(),column_config={'BatsmanRun':'Sixes'},width=350)

    st.subheader("Home and Away Win Percentage of IPL Teams:")
    st.dataframe(stat.win_percentage())