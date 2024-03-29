import streamlit as st
from playerAnalysis import Player
import plotly.express as px

def app():

    player = Player()

    ip = st.sidebar.selectbox('Enter Batter Name:',player.batter())
    btn = st.sidebar.button('Show')
    if btn:
        st.subheader("Batter's Performance in IPL till 2023:")
        st.dataframe(player.batter_stats(ip), width=700)

        # st.subheader('Runs Scored Against Each Team:')
        # st.dataframe(player.runs_against_team(ip),width=350,column_config={'BatsmanRun':'Runs'})

        fig = px.bar(player.runs_against_teamChart(ip), x='Bowling Team', y='Runs',title="Visual Representation of Batter's Runs Against Each Teams")
        st.plotly_chart(fig)

        # st.subheader("Batter's Runs in Each Season:")
        st.write(ip,"'s Runs Each Season:")
        fig = px.bar(player.batter_score_seasonwise(ip), x='Season', y='Runs',
                     title="Visual Representation of Batter's Runs Against Each Season")
        fig.update_xaxes(type='category')
        st.plotly_chart(fig)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Total Run of Top Players:')
            st.markdown('''Top-10 Batter in IPL till 2023
                        (in term of Runs scored)''')
            st.dataframe(player.top_10(),width=300,column_config={'BatsmanRun':'Runs'})

        #sr of top 10 players who played in death overs and played more than 200 balls
        with col2:
            st.subheader('Strike Rate Analysis:')
            st.markdown('Strike Rate of top 10 players in Death Overs(Played more than 200 balls)')
            sr=player.sr()
            st.dataframe(sr,column_config={'BatsmanRun':'Strike Rate'},width=300)

        st.subheader('Orange-Cap Holders:')
        st.dataframe(player.orange_cap_holder(),width=500,height=597)
