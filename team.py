import numpy as np
import pandas as pd
import streamlit as st
from teamAnalysis import IPL
import plotly.express as px
def app():
    ipl = IPL()

    teams = ipl.teams()

    team1 = st.sidebar.selectbox('Select Team-1',teams)

    team2 = st.sidebar.selectbox('Select Team-2',teams)

    analysis = st.sidebar.button('Show')

    data = ipl.teamVsteam(team1,team2)
    if analysis:
        st.title('IPL Team Analysis')
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
            if team1 == 'Royal Challengers Bangalore':
                st.image('rcb.JPG', width=150)
            if team1 == 'Mumbai Indians':
                st.image('mumbai_indians.JPG', width=200)
            if team1 == 'Chennai Super Kings':
                st.image('csk.JPG', width=163)
            if team1 == 'Kolkata Knight Riders':
                st.image('kkr.JPG', width=109)
            if team1 == 'Delhi Capitals':
                st.image('delhi_capitals.JPG', width=110)
            if team1 == 'Rajasthan Royals':
                st.image('rr.JPG', width=160)
            if team1 == 'Punjab Kings':
                st.image('pk.JPG', width=103)
            if team1 == 'Sunrisers Hyderabad':
                st.image('srh.JPG', width=130)
            if team1 == 'Gujarat Titans':
                st.image('gt.JPG', width=150)
            if team1 == 'Deccan Chargers':
                st.image('dc.JPG', width=140)
            if team1 == 'Kochi Tuskers Kerala':
                st.image('ktk.JPG', width=151)
            if team1 == 'Gujarat Lions':
                st.image('gl.JPG', width=110)
            if team1 == 'Lucknow Super Giants':
                st.image('lsg.JPG', width=200)
            if team1 == 'Rising Pune Supergiants':
                st.image('rps.JPG', width=178)
            if team1 == 'Pune Warriors':
                st.image('pwi.JPG', width=175)

            st.dataframe(team_record,width=350,column_config={'':'Question','value':'Answer'})

            st.subheader('Pie Chart:')
            x = ipl.team_recordPie(team1)
            fig = px.pie(x, names='Question', values='Answer', hover_name='Question',title=team1,
                        labels='Question')
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(showlegend=False, width=400, height=400)
            st.plotly_chart(fig)

        with col2:
            team_record = ipl.team_record(team2)
            if team2 == 'Royal Challengers Bangalore':
                st.image('rcb.JPG', width=150)
            if team2 == 'Mumbai Indians':
                st.image('mumbai_indians.JPG', width=200)
            if team2 == 'Chennai Super Kings':
                st.image('csk.JPG', width=163)
            if team2 == 'Kolkata Knight Riders':
                st.image('kkr.JPG', width=109)
            if team2 == 'Delhi Capitals':
                st.image('delhi_capitals.JPG', width=110)
            if team2 == 'Rajasthan Royals':
                st.image('rr.JPG', width=160)
            if team2 == 'Punjab Kings':
                st.image('pk.JPG', width=103)
            if team2 == 'Sunrisers Hyderabad':
                st.image('srh.JPG', width=130)
            if team2 == 'Gujarat Titans':
                st.image('gt.JPG', width=150)
            if team2 == 'Deccan Chargers':
                st.image('dc.JPG', width=140)
            if team2 == 'Kochi Tuskers Kerala':
                st.image('ktk.JPG', width=151)
            if team2 == 'Gujarat Lions':
                st.image('gl.JPG', width=110)
            if team2 == 'Lucknow Super Giants':
                st.image('lsg.JPG', width=200)
            if team2 == 'Rising Pune Supergiants':
                st.image('rps.JPG', width=178)
            if team2 == 'Pune Warriors':
                st.image('pwi.JPG', width=175)

            st.dataframe(team_record,width=350,column_config={'':'Question','value':'Answer'})

            st.subheader('Pie Chart:')
            x = ipl.team_recordPie(team2)
            fig = px.pie(x, names='Question', values='Answer', hover_name='Question', title=team2,
                        labels='Question')
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(showlegend=False, width=400, height=400)
            st.plotly_chart(fig)