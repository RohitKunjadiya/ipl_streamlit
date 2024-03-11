import numpy as np
import pandas as pd
import streamlit as st
from teamAnalysis import IPL
import plotly.express as px
def app():
    ipl = IPL()

    st.title('IPL Team Analysis')

    teams = ipl.teams()

    st.sidebar.title('IPL Analysis')

    team1 = st.sidebar.selectbox('Select Team-1',teams)

    team2 = st.sidebar.selectbox('Select Team-2',teams)

    analysis = st.sidebar.button('Show Analysis')

    data = ipl.teamVsteam(team1,team2)
    if analysis:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Head to Head:')
            st.dataframe(data,column_config={'':'Question','value':'Answer'},width=500)


        st.subheader('Pie Chart:')
        x = ipl.teamVsteamPie(team1,team2)
        fig = px.pie(x,names='Team Name',values='Results',hover_name='Team Name',labels='Team Name')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=False,width=400,height=400)
        st.plotly_chart(fig)

        st.subheader('Team Record:')

        col1,col2=st.columns(2)
        with col1:
            team_record = ipl.team_record(team1)
            st.dataframe(team_record,width=350,column_config={'':'Question','value':'Answer'})

            st.subheader('Pie Chart:')
            x = ipl.team_recordPie(team1)
            fig = px.pie(x, names='Team Name', values='Results', hover_name='Team Name',title=team1, labels='Team Name')
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(showlegend=False, width=400, height=400)
            st.plotly_chart(fig)

        with col2:
            team_record = ipl.team_record(team2)
            st.dataframe(team_record,width=350,column_config={'':'Question','value':'Answer'})

            st.subheader('Pie Chart:')
            x = ipl.team_recordPie(team2)
            fig = px.pie(x, names='Team Name', values='Results', hover_name='Team Name', title=team2,
                         labels='Team Name')
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(showlegend=False, width=400, height=400)
            st.plotly_chart(fig)