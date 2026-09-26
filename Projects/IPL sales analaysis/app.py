import streamlit as st
import pandas as pd
import plotly.express as px
from analysis import compute_kpis, compute_team_win_percentage, compute_top_run_scorers, compute_scoring_trend, compute_season_overview
from analysis import compute_team_win_percentage_by_season, compute_team_scoring_profile
from analysis import compute_top_wicket_takers, compute_top_strike_rates, compute_top_economy_bowlers, compute_player_runs_by_season,compute_powerplay_vs_death
from analysis import compute_toss_match_correlation, compute_chase_vs_defend, compute_venue_scoring, compute_venue_toss_advantage, compute_biggest_margins, compute_toss_chase_significance,compute_team_momentum


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

    filter_col1, filter_col2 = st.columns([1, 2])
    with filter_col1:
        season_range = st.slider("Season range", min_value=2008, max_value=2026, value=(2008, 2026))
    with filter_col2:
        all_teams = sorted(df['batting_team_clean'].unique())
        selected_teams = st.multiselect("Teams", all_teams, default=all_teams)

    df_filtered = df[(df['season_clean'] >= season_range[0]) & (df['season_clean'] <= season_range[1])]

    team_stats = compute_team_win_percentage(df_filtered)
    team_stats = team_stats[team_stats['team'].isin(selected_teams)]
    team_stats['losses'] = team_stats['matches_played'] - team_stats['wins']

    st.divider()
    row1_left, row1_right = st.columns(2)
    with row1_left:
        st.subheader("Wins vs. Losses")
        fig1 = px.bar(team_stats, x='team', y=['wins', 'losses'], barmode='group', labels={'value': 'Matches', 'team': ''})
        st.plotly_chart(fig1, use_container_width=True)

    with row1_right:
        st.subheader("Win Percentage")
        fig2 = px.bar(team_stats.sort_values('win_pct'), x='win_pct', y='team', orientation='h', labels={'win_pct': 'Win %', 'team': ''})
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Season-by-Season Performance")
    season_pivot = compute_team_win_percentage_by_season(df_filtered)
    season_pivot = season_pivot.loc[season_pivot.index.isin(selected_teams)]
    fig3 = px.line(season_pivot.T, markers=True, labels={'value': 'Win %', 'season': 'Season', 'variable': 'Team'})
    st.plotly_chart(fig3, use_container_width=True)

    st.divider()
    row2_left, row2_right = st.columns(2)
    with row2_left:
        st.subheader("Scoring & Bowling Profile")
        team_profile = compute_team_scoring_profile(df_filtered)
        team_profile = team_profile[team_profile.index.isin(selected_teams)].reset_index()
        fig4 = px.bar(team_profile, x='batting_team', y=['avg_runs_scored', 'avg_runs_conceded'], barmode='group',
                      labels={'value': 'Runs per Innings', 'batting_team': ''})
        st.plotly_chart(fig4, use_container_width=True)

    with row2_right:
        st.subheader("Team Comparison")
        compare_df = team_stats[['team', 'win_pct', 'matches_played']].merge(
            team_profile[['batting_team', 'avg_runs_scored', 'avg_runs_conceded']],
            left_on='team', right_on='batting_team'
        )[['team', 'matches_played', 'win_pct', 'avg_runs_scored', 'avg_runs_conceded']]
        st.dataframe(compare_df.sort_values('win_pct', ascending=False), use_container_width=True, hide_index=True)
elif page == "Player Analytics":
    st.title("Player Analytics")

    filter_col1, filter_col2, filter_col3 = st.columns([1, 1, 2])
    with filter_col1:
        team_filter = st.selectbox("Team (narrows player list)", ["All"] + sorted(df['batting_team_clean'].unique()))
    with filter_col2:
        season_range = st.slider("Season range", min_value=2008, max_value=2026, value=(2008, 2026), key="player_season")

    if team_filter == "All":
        eligible_players = df['batter'].unique()
    else:
        eligible_players = df[(df['batting_team_clean'] == team_filter) | (df['bowling_team_clean'] == team_filter)]['batter'].unique()

    with filter_col3:
        default_players = sorted(eligible_players)[:5] if len(eligible_players) >= 5 else sorted(eligible_players)
        selected_players = st.multiselect("Players", sorted(eligible_players), default=default_players)

    df_filtered = df[(df['season_clean'] >= season_range[0]) & (df['season_clean'] <= season_range[1])]

    st.divider()
    row1_left, row1_right = st.columns(2)
    with row1_left:
        st.subheader("Runs")
        runs_df = compute_top_run_scorers(df_filtered, top_n=1000).reset_index()
        runs_df = runs_df[runs_df['batter'].isin(selected_players)]
        fig1 = px.bar(runs_df, x='total_runs', y='batter', orientation='h', labels={'total_runs': 'Total Runs', 'batter': ''})
        st.plotly_chart(fig1, use_container_width=True)

    with row1_right:
        st.subheader("Wickets")
        wkts_df = compute_top_wicket_takers(df_filtered, top_n=1000).reset_index()
        wkts_df = wkts_df[wkts_df['bowler'].isin(selected_players)]
        fig2 = px.bar(wkts_df, x='total_wickets', y='bowler', orientation='h', labels={'total_wickets': 'Total Wickets', 'bowler': ''})
        st.plotly_chart(fig2, use_container_width=True)

    row2_left, row2_right = st.columns(2)
    with row2_left:
        st.subheader("Strike Rate")
        sr_df = compute_top_strike_rates(df_filtered, min_balls=1, top_n=1000).reset_index()
        sr_df = sr_df[sr_df['batter'].isin(selected_players)]
        fig3 = px.bar(sr_df, x='strike_rate', y='batter', orientation='h', labels={'strike_rate': 'Strike Rate', 'batter': ''})
        st.plotly_chart(fig3, use_container_width=True)

    with row2_right:
        st.subheader("Economy")
        eco_df = compute_top_economy_bowlers(df_filtered, min_balls=1, top_n=1000).reset_index()
        eco_df = eco_df[eco_df['bowler'].isin(selected_players)]
        fig4 = px.bar(eco_df, x='economy', y='bowler', orientation='h', labels={'economy': 'Economy', 'bowler': ''})
        st.plotly_chart(fig4, use_container_width=True)

    st.divider()
    st.subheader("Performance Over Time")
    if selected_players:
        by_season = compute_player_runs_by_season(df_filtered, selected_players)
        fig5 = px.line(by_season, x='season_clean', y='runs_batter', color='batter', markers=True,
                        labels={'season_clean': 'Season', 'runs_batter': 'Runs', 'batter': 'Player'})
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.info("Select at least one player above to see their trend.")
elif page == "Match Analytics":
    st.title("Match Analytics")

    filter_col1, filter_col2 = st.columns([1, 2])
    with filter_col1:
        season_range = st.slider("Season range", min_value=2008, max_value=2026, value=(2008, 2026), key="match_season")
    with filter_col2:
        all_venues = sorted(df['venue_clean'].unique())
        selected_venues = st.multiselect("Venues (for venue charts below)", all_venues, default=[])

    df_filtered = df[(df['season_clean'] >= season_range[0]) & (df['season_clean'] <= season_range[1])]

    st.divider()
    st.subheader("Toss & Chase Advantage Over Time")
    overall_pct, by_decision, toss_by_season = compute_toss_match_correlation(df_filtered)
    chase_overall, chase_by_season = compute_chase_vs_defend(df_filtered)
    trend_df = pd.DataFrame({'toss_win_match_pct': toss_by_season['toss_win_match_pct'], 'chase_win_pct': chase_by_season}).reset_index()
    fig1 = px.line(trend_df, x='season', y=['toss_win_match_pct', 'chase_win_pct'], markers=True,
                   labels={'value': '%', 'season': 'Season', 'variable': 'Metric'})
    fig1.add_hline(y=50, line_dash="dash", line_color="grey")
    st.plotly_chart(fig1, use_container_width=True)

    st.divider()
    row1_left, row1_right = st.columns(2)
    with row1_left:
        st.subheader("Average Score by Venue")
        venue_scores = compute_venue_scoring(df_filtered, min_matches=10).reset_index()
        if selected_venues:
            venue_scores = venue_scores[venue_scores['venue'].isin(selected_venues)]
        fig2 = px.bar(venue_scores.sort_values('avg_first_innings_score'), x='avg_first_innings_score', y='venue',
                      orientation='h', labels={'avg_first_innings_score': 'Avg First-Innings Score', 'venue': ''})
        st.plotly_chart(fig2, use_container_width=True)

    with row1_right:
        st.subheader("Does Fielding First Help Here?")
        venue_toss = compute_venue_toss_advantage(df_filtered, min_per_decision=5).reset_index()
        if selected_venues:
            venue_toss = venue_toss[venue_toss['venue'].isin(selected_venues)]
        fig3 = px.bar(venue_toss.sort_values('field_advantage'), x='field_advantage', y='venue', orientation='h',
                      labels={'field_advantage': 'Field-First Advantage (pts)', 'venue': ''},
                      color=venue_toss['field_advantage'] > 0, color_discrete_map={True: 'seagreen', False: 'firebrick'})
        fig3.add_vline(x=0, line_color="black")
        fig3.update_layout(showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

    st.divider()
    st.subheader("Match Records")
    biggest_runs, biggest_wickets, closest = compute_biggest_margins(df_filtered, top_n=10)
    rec_col1, rec_col2 = st.columns(2)
    with rec_col1:
        st.write("**Biggest wins by runs**")
        st.dataframe(biggest_runs[['won_by', 'season', 'win_margin']], use_container_width=True, hide_index=True)
    with rec_col2:
        st.write("**Closest finishes**")
        st.dataframe(closest[['won_by', 'season', 'win_margin', 'win_type']], use_container_width=True, hide_index=True)
elif page == "Insights":
    st.title("Insights")
    st.caption("Every number below is calculated live from the dataset each time this page loads - nothing here is hardcoded.")

    team_profile = compute_team_scoring_profile(df).sort_values('run_diff', ascending=False)
    best_team = team_profile.index[0]
    best_diff = team_profile.iloc[0]['run_diff']

    _, _, chase_p = None, None, None
    sig_results = compute_toss_chase_significance(df)

    _, momentum_after_win, momentum_after_loss, _, momentum_p = compute_team_momentum(df)

    pp_death = compute_powerplay_vs_death(df)
    overall_pp_death, by_season_pp_death = pp_death
    early_gap = by_season_pp_death.loc[2015:2019].apply(lambda r: r['death_rr'] - r['powerplay_rr'], axis=1).mean()
    recent_gap = by_season_pp_death.loc[2022:2026].apply(lambda r: r['death_rr'] - r['powerplay_rr'], axis=1).mean()

    venue_toss = compute_venue_toss_advantage(df)
    exception_venues = venue_toss[venue_toss['field_advantage'] < 0]

    insights = [
        {
            "insight": f"{best_team} has the best run differential in the league at +{best_diff}/innings.",
            "why": "Win percentage alone doesn't say *how* a team wins. This is the most balanced team on both sides of the ball - not just the highest-scoring or the lowest-conceding, but the best combination of both."
        },
        {
            "insight": f"Chasing carries a real, statistically significant edge (p = {sig_results['test3_p']}), but winning the toss itself does not (p = {sig_results['test1_p']}).",
            "why": "The toss is luck, provably so. The decision made with it is not. Team strategy should stop treating 'we won the toss' as an advantage in itself, and start treating 'we get to choose' as the actual asset."
        },
        {
            "insight": f"No evidence of momentum: win rate after a win ({momentum_after_win}%) and after a loss ({momentum_after_loss}%) are statistically indistinguishable (p = {momentum_p}).",
            "why": "A widely-believed sports narrative that this dataset does not support. Worth knowing what *isn't* true as much as what is - each match behaves close to independently."
        },
        {
            "insight": f"The powerplay/death-overs scoring gap has nearly closed - {early_gap:.1f} runs/over apart in 2015-2019, down to {recent_gap:.1f} in 2022-2026.",
            "why": "This is where the league-wide scoring increase (Question 14) actually comes from - batters attacking the powerplay far more aggressively, not death-overs hitting becoming even more extreme."
        },
        {
            "insight": f"{len(exception_venues)} venue breaks the league-wide chase advantage: {exception_venues.index[0] if len(exception_venues) else 'none'} actually favors batting first.",
            "why": "A single-venue exception to an otherwise consistent league-wide pattern - worth a specific strategy note for matches played there, rather than applying the general chase-first advice blindly everywhere."
        },
    ]

    for item in insights:
        st.info(f"**Insight:** {item['insight']}")
        st.write(f"*Why it matters:* {item['why']}")
        st.divider()