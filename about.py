import streamlit as st

def app():
    st.title("About Dataset")
    st.subheader("Dataset : https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020?select=deliveries.csv")

    st.write("\n\n\n\n---------------------------------------------------------------------")

    st.title("About Project ")
    st.subheader("""
        The IPL Data Analysis project meticulously examines the Indian Premier League's comprehensive dataset from 2008 to 2024.This project aims to provide an in-depth understanding of various aspects of the tournament through detailed insights and statistical analysis.
        """)
    st.markdown("<h4> 1. Team vs Team Analysis </h4>", unsafe_allow_html=True)
    st.markdown("""
                           \t - Detailed head-to-head records.
                           \t - Win/loss/NR(No Result) Pie Chart of h2h team and individual team 
                           \t - Performance of team till 2024.
            """)
    st.markdown("<h4> 2. Batting Analysis </h4>", unsafe_allow_html=True)

    st.markdown("""
                               \t - Individual player performances.
                               \t - Runs made by batter against each team.
                               \t - Runs made by batter in each season.
                               \t - Statistics on Total Runs and Strike Rates.
                               \t - Orange Cap Holder in each season.
                """)
    st.markdown("<h4> 3. Bowling Analysis </h4>", unsafe_allow_html=True)
    st.markdown("""
                                   \t - Leading wicket-takers.
                                   \t - Wickets of bowler against each team.
                                   \t - Wickets of bowler in each season.
                                   \t - Purple Cap Holder in each season.
                                   \t - Best Bowling figure and total wickets of bowler
                    """)
    st.markdown("<h4> 4. Points Table </h4>", unsafe_allow_html=True)
    st.markdown("""
                                       \t - Yearly standings and points accumulation.
                                       \t - Qualification scenarios and playoff performances.
                                       \t - Team performances across seasons.
                        """)
    st.markdown("<h4> 5. IPL Stats </h4>", unsafe_allow_html=True)
    st.markdown("""
                                           \t - Good Batting Partners: Identifying the most successful batting pairs in IPL history.
                                           \t - Home and Away Win Percentages
                                           \t - Most 4s and 6s
                            """)
