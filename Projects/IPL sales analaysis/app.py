import streamlit as st
import pandas as pd
import plotly.express as px
from analysis import compute_kpis, compute_team_win_percentage, compute_top_run_scorers, compute_scoring_trend, compute_season_overview

st.set_page_config(page_title="IPL Performance Analytics", layout="wide", page_icon="🏏")

@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/IPL_Dataset_Cleaned.csv")
    return df

df = load_data()

st.sidebar.title("IPL Performance Analytics")
page = st.sidebar.radio("Go to", ["Executive Overview", "Team Analytics", "Player Analytics", "Match Analytics", "Insights"])

if page == "Executive Overview":
    st.title("Executive Overview")

    kpis = compute_kpis(df)
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Matches", kpis['total_matches'])
    col2.metric("Seasons", kpis['total_seasons'])
    col3.metric("Teams", kpis['total_teams'])
    col4.metric("Players", kpis['total_players'])
    col5.metric("Runs", f"{kpis['total_runs']:,}")
    col6.metric("Wickets", f"{kpis['total_wickets']:,}")

    st.divider()

    row1_left, row1_right = st.columns(2)
    with row1_left:
        st.subheader("Season Trend — Matches Played")
        overview_df = compute_season_overview(df).reset_index()
        fig1 = px.bar(overview_df, x='season_clean', y='matches', labels={'season_clean': 'Season', 'matches': 'Matches'})
        st.plotly_chart(fig1, use_container_width=True)

    with row1_right:
        st.subheader("Team Performance — Win %")
        team_stats = compute_team_win_percentage(df)
        fig2 = px.bar(team_stats, x='win_pct', y='team', orientation='h', labels={'win_pct': 'Win %', 'team': ''})
        fig2.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig2, use_container_width=True)

    row2_left, row2_right = st.columns(2)
    with row2_left:
        st.subheader("Top Run Scorers")
        top_scorers = compute_top_run_scorers(df, top_n=10).reset_index()
        fig3 = px.bar(top_scorers, x='total_runs', y='batter', orientation='h', labels={'total_runs': 'Total Runs', 'batter': ''})
        fig3.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig3, use_container_width=True)

    with row2_right:
        st.subheader("Scoring Trend by Season")
        by_season, corr, pval = compute_scoring_trend(df)
        fig4 = px.line(x=by_season.index, y=by_season.values, markers=True, labels={'x': 'Season', 'y': 'Avg First-Innings Score'})
        st.plotly_chart(fig4, use_container_width=True)

elif page == "Team Analytics":
    st.title("Team Analytics")
    st.write("Coming in Step 3.")
elif page == "Player Analytics":
    st.title("Player Analytics")
    st.write("Coming in Step 4.")
elif page == "Match Analytics":
    st.title("Match Analytics")
    st.write("Coming in Step 5.")
elif page == "Insights":
    st.title("Insights")
    st.write("Coming in Step 6.")