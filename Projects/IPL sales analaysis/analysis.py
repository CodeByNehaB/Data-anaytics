import pandas as pd
from collections import defaultdict

df = pd.read_csv("data/processed/IPL_Dataset_Cleaned.csv", low_memory=False)

TEAM_REBRAND_NAME = {
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru",
    "Rising Pune Supergiants": "Rising Pune Supergiant",
}

def compute_team_win_percentage(df):
    df = df.copy()
    df['match_won_by_clean'] = df['match_won_by'].replace(TEAM_REBRAND_NAME)

    match_level = df.groupby('match_id').agg(
        teams=('batting_team_clean', lambda x: sorted(set(x))),
        won_by=('match_won_by_clean', 'first'),
    ).reset_index()

    decided = match_level[match_level['won_by'] != 'Unknown']

    played, wins = defaultdict(int), defaultdict(int)
    for _, row in decided.iterrows():
        for t in row['teams']:
            played[t] += 1
        wins[row['won_by']] += 1

    team_stats = pd.DataFrame({
        'team': list(played.keys()),
        'matches_played': [played[t] for t in played],
        'wins': [wins.get(t, 0) for t in played],
    })
    team_stats['win_pct'] = (team_stats['wins'] / team_stats['matches_played'] * 100).round(1)
    return team_stats.sort_values('win_pct', ascending=False).reset_index(drop=True)



def compute_team_win_percentage_by_season(df):
    """
    Business Question 2: season-by-season win percentage per team.
    Returns a team x season pivot table. A blank (NaN) cell means that
    team did not play that season - not a 0% loss record.
    """

    df = df.copy()
    df['match_won_by_clean'] = df['match_won_by'].replace(TEAM_REBRAND_NAME)

    match_level= df.groupby('match_id').agg(
        season= ('season_clean', 'first'),
        teams=('batting_team_clean', lambda x: sorted(set(x))),
        won_by=('match_won_by_clean', 'first')
    ).reset_index()

    decided = match_level[match_level['won_by'] != 'Unknown']


    played, wins = defaultdict(int), defaultdict(int)
    for _, row in decided.iterrows():
        for t in row['teams']:
            played[(t, row['season'])] += 1
        wins[(row['won_by'], row['season'])] +=1


    rows = [{'team': t, 'season':s, 'win_pct': round(wins.get((t,s),0)/p*100, 1)}
               for (t, s), p in played.items()]

    return pd.DataFrame(rows).pivot(index='team', columns='season', values='win_pct')

def compute_head_to_head(df):
    """
    Business Question 3: head-to-head win percentage between every pair
    of teams that have played each other at least once.
    Returns a team x team pivot: row_team's win % against column_team.
    Diagonal and never-played pairs are NaN.
    """

    df = df.copy()
    df['match_won_by_clean'] =df['match_won_by'].replace(TEAM_REBRAND_NAME)

    match_level= df.groupby('match_id').agg(
        teams = ('batting_team_clean', lambda x:sorted(set(x))),
        won_by=('match_won_by_clean', 'first')
    ).reset_index()

    decided = match_level[(match_level['won_by'] !='Unknown') & (match_level['teams'].apply(len)==2)]


    h2h_wins = defaultdict(int)
    for _, row in decided.iterrows():
        a,b = row['teams']
        loser = b if row['won_by'] == a else a
        h2h_wins[(row['won_by'], loser)] +=1

    teams = sorted(set(df['batting_team_clean'].unique()))
    rows = []
    for a in teams:
        for b in teams:
            if a == b:
                continue
            wins_a, wins_b = h2h_wins.get((a, b), 0), h2h_wins.get((b, a), 0)
            total = wins_a + wins_b
            if total > 0:
                rows.append({'team': a, 'opponent': b, 'win_pct': round(wins_a / total * 100, 1)})

    return pd.DataFrame(rows).pivot(index='team', columns='opponent', values='win_pct')
def compute_top_run_scorers(df, top_n=15):
    """
    Business Question 4: all-time top run-scorers.
    Sums 'runs_batter' (runs on that specific ball) - NOT 'batter_runs',
    which is a cumulative running total within the innings and would
    wildly overcount if summed directly.
    """
    runs = df.groupby('batter')['runs_batter'].sum()
    matches = df.groupby('batter')['match_id'].nunique()
    innings = df.groupby('batter').apply(lambda x: x[['match_id', 'innings']].drop_duplicates().shape[0])

    top_scorers = pd.DataFrame({
        'total_runs': runs,
        'matches': matches,
        'innings': innings,
    }).sort_values('total_runs', ascending=False).head(top_n)
    top_scorers['avg_runs_per_innings'] = (top_scorers['total_runs'] / top_scorers['innings']).round(1)
    return top_scorers
import pandas as pd
def compute_top_wicket_takers(df, top_n=15):
    """
    Business Question 5: all-time top wicket-takers.
    Sums 'bowler_wicket' (per-ball flag) - NOT 'team_wicket', which is
    the batting team's cumulative wicket count and isn't bowler-specific
    at all.
    """
    wickets = df.groupby('bowler')['bowler_wicket'].sum()
    matches=df.groupby('bowler')['match_id'].nunique()
    balls_bowled = df[df['valid_ball']==1].groupby('bowler').size()


    top_bowlers = pd.DataFrame({
        'total_wickets':wickets,
        'matches':matches,
        'balls_bowled':balls_bowled,

    }).sort_values('total_wickets', ascending=False).head(top_n)
    top_bowlers['wickets_per_match'] =(top_bowlers['total_wickets']/top_bowlers['matches']).round(2)
    return top_bowlers





import pandas as pd

def compute_top_strike_rates(df, min_balls=1500, top_n=15):
    """
    Business Question 6: best batting strike rate, minimum 1500 balls faced
    so a small hot streak doesn't outrank a real season of scoring.
    balls_faced correctly excludes wides and includes no-balls - verified
    against valid_ball and cross-checked against batter_balls.
    """
    runs = df.groupby('batter')['runs_batter'].sum()
    balls = df.groupby('batter')['balls_faced'].sum()
    matches = df.groupby('batter')['match_id'].nunique()

    sr_df = pd.DataFrame({'total_runs': runs, 'balls_faced': balls, 'matches': matches})
    sr_df = sr_df[sr_df['balls_faced'] >= min_balls].copy()
    sr_df['strike_rate'] = (sr_df['total_runs'] / sr_df['balls_faced'] * 100).round(1)
    return sr_df.sort_values('strike_rate', ascending=False).head(top_n)

def compute_top_economy_bowlers(df, min_balls=1200, top_n=15):
    """
    Business Question 7: best economy rate, minimum 200 overs (1200 legal
    balls) bowled. runs_bowler correctly excludes byes/leg-byes on legal
    deliveries - verified: runs_bowler == runs_batter on every legal ball
    in the dataset - while still including wide/no-ball penalties.
    """
    legal = df[df['valid_ball'] == 1]
    balls_bowled = legal.groupby('bowler').size()
    runs_conceded = df.groupby('bowler')['runs_bowler'].sum()

    eco_df = pd.DataFrame({'runs_conceded': runs_conceded, 'balls_bowled': balls_bowled}).dropna()
    eco_df = eco_df[eco_df['balls_bowled'] >= min_balls].copy()
    eco_df['overs_bowled'] = (eco_df['balls_bowled'] / 6).round(1)
    eco_df['economy'] = (eco_df['runs_conceded'] / (eco_df['balls_bowled'] / 6)).round(2)
    return eco_df.sort_values('economy').head(top_n)

def compute_batting_consistency(df, min_innings_per_season=5, min_seasons=6, min_career_avg=20, top_n=10):
    """
    Business Question 8: most consistent run-scorers, season to season.
    Consistency = coefficient of variation (std / mean) of each player's
    average runs-per-innings across qualifying seasons. Lower CV = more
    consistent.
    """
    innings_level = df.groupby(['batter', 'season_clean', 'match_id', 'innings'])['runs_batter'].sum().reset_index()
    season_level = innings_level.groupby(['batter', 'season_clean']).agg(
        innings_played=('runs_batter', 'count'),
        avg_runs=('runs_batter', 'mean')
    ).reset_index()

    real_seasons = season_level[season_level['innings_played'] >= min_innings_per_season]
    seasons_per_player = real_seasons.groupby('batter').size()
    qualified_players = seasons_per_player[seasons_per_player >= min_seasons].index

    consistency = real_seasons[real_seasons['batter'].isin(qualified_players)].groupby('batter')['avg_runs'].agg(['mean', 'std', 'count'])
    consistency['cv'] = (consistency['std'] / consistency['mean']).round(3)
    consistency = consistency.rename(columns={'mean': 'career_avg_runs', 'count': 'qualifying_seasons'})

    return consistency[consistency['career_avg_runs'] >= min_career_avg].sort_values('cv').head(top_n)

def compute_toss_match_correlation(df):
    """
    Business Question 9: does winning the toss correlate with winning the
    match, and has toss strategy shifted over the 19 seasons?
    """
    df = df.copy()
    df['toss_winner_clean'] = df['toss_winner'].replace(TEAM_REBRAND_NAME)
    df['match_won_by_clean'] = df['match_won_by'].replace(TEAM_REBRAND_NAME)

    match_level = df.groupby('match_id').agg(
        season=('season_clean', 'first'),
        toss_winner=('toss_winner_clean', 'first'),
        toss_decision=('toss_decision', 'first'),
        won_by=('match_won_by_clean', 'first'),
    ).reset_index()

    decided = match_level[match_level['won_by'] != 'Unknown'].copy()
    decided['toss_winner_won_match'] = decided['toss_winner'] == decided['won_by']

    overall_pct = round(decided['toss_winner_won_match'].mean() * 100, 1)
    by_decision = decided.groupby('toss_decision')['toss_winner_won_match'].mean().mul(100).round(1)

    by_season = decided.groupby('season').agg(
        toss_win_match_pct=('toss_winner_won_match', lambda x: round(x.mean() * 100, 1)),
        field_first_pct=('toss_decision', lambda x: round((x == 'field').mean() * 100, 1)),
    )
    return overall_pct, by_decision, by_season

def compute_chase_vs_defend(df):
    """
    Business Question 10: is chasing more successful than defending,
    overall and by season?
    """
    df = df.copy()
    df['match_won_by_clean'] = df['match_won_by'].replace(TEAM_REBRAND_NAME)

    first_innings_team = df[df['innings'] == 1].groupby('match_id')['batting_team_clean'].first()
    second_innings_team = df[df['innings'] == 2].groupby('match_id')['batting_team_clean'].first()

    match_level = df.groupby('match_id').agg(
        season=('season_clean', 'first'),
        won_by=('match_won_by_clean', 'first'),
    ).reset_index()
    match_level['team_bat_2nd'] = match_level['match_id'].map(second_innings_team)

    decided = match_level.dropna(subset=['team_bat_2nd'])
    decided = decided[decided['won_by'] != 'Unknown'].copy()
    decided['chasing_team_won'] = decided['team_bat_2nd'] == decided['won_by']

    overall_pct = round(decided['chasing_team_won'].mean() * 100, 1)
    by_season = decided.groupby('season')['chasing_team_won'].mean().mul(100).round(1)
    return overall_pct, by_season

def compute_venue_scoring(df, min_matches=20):
    """
    Business Question 11: average first-innings score by venue.
    Uses the final (max) team_runs of innings 1 as that match's
    first-innings total.
    """
    first_innings = df[df['innings'] == 1].groupby('match_id').agg(
        venue=('venue_clean', 'first'),
        final_score=('team_runs', 'max')
    ).reset_index()

    venue_scores = first_innings.groupby('venue')['final_score'].agg(['mean', 'count']).round(1)
    venue_scores = venue_scores[venue_scores['count'] >= min_matches].sort_values('mean', ascending=False)
    return venue_scores.rename(columns={'mean': 'avg_first_innings_score', 'count': 'matches'})

def compute_biggest_margins(df, top_n=10):
    """
    Business Question 12: biggest winning margins, by runs and by wickets
    (wickets uses balls-remaining as a tiebreaker for the 10-wicket ties).
    """
    second_innings_balls = df[df['innings'] == 2].groupby('match_id')['team_balls'].max()

    match_level = df.groupby('match_id').agg(
        season=('season_clean', 'first'), won_by=('match_won_by_clean', 'first'),
        win_margin=('win_margin', 'first'), win_type=('win_type', 'first'),
    ).reset_index()
    match_level['balls_remaining'] = 120 - match_level['match_id'].map(second_innings_balls)

    biggest_runs = match_level[match_level['win_type'] == 'runs'].sort_values('win_margin', ascending=False).head(top_n)
    biggest_wickets = match_level[(match_level['win_type'] == 'wickets') & (match_level['win_margin'] == 10)].sort_values('balls_remaining', ascending=False).head(top_n)
    closest = match_level.dropna(subset=['win_margin']).sort_values('win_margin').head(top_n)

    return biggest_runs, biggest_wickets, closest

def compute_biggest_margins(df, top_n=10):
    """
    Business Question 12: biggest winning margins, by runs and by wickets
    (wickets uses balls-remaining as a tiebreaker for the 10-wicket ties).
    """
    second_innings_balls = df[df['innings'] == 2].groupby('match_id')['team_balls'].max()

    match_level = df.groupby('match_id').agg(
        season=('season_clean', 'first'), won_by=('matches_won_by_clean', 'first'),
        win_margin=('win_margin', 'first'), win_type=('win_type', 'first'),
    ).reset_index()
    match_level['balls_remaining'] = 120 - match_level['match_id'].map(second_innings_balls)

    biggest_runs = match_level[match_level['win_type'] == 'runs'].sort_values('win_margin', ascending=False).head(top_n)
    biggest_wickets = match_level[(match_level['win_type'] == 'wickets') & (match_level['win_margin'] == 10)].sort_values('balls_remaining', ascending=False).head(top_n)
    closest = match_level.dropna(subset=['win_margin']).sort_values('win_margin').head(top_n)

    return biggest_runs, biggest_wickets, closest

def compute_biggest_margins(df, top_n=10):
    """
    Business Question 12: biggest winning margins, by runs and by wickets
    (wickets uses balls-remaining as a tiebreaker for the 10-wicket ties).
    """
    second_innings_balls = df[df['innings'] == 2].groupby('match_id')['team_balls'].max()

    match_level = df.groupby('match_id').agg(
        season=('season_clean', 'first'), won_by=('match_won_by_clean', 'first'),
        win_margin=('win_margin', 'first'), win_type=('win_type', 'first'),
    ).reset_index()
    match_level['balls_remaining'] = 120 - match_level['match_id'].map(second_innings_balls)

    biggest_runs = match_level[match_level['win_type'] == 'runs'].sort_values('win_margin', ascending=False).head(top_n)
    biggest_wickets = match_level[(match_level['win_type'] == 'wickets') & (match_level['win_margin'] == 10)].sort_values('balls_remaining', ascending=False).head(top_n)
    closest = match_level.dropna(subset=['win_margin']).sort_values('win_margin').head(top_n)

    return biggest_runs, biggest_wickets, closest

def compute_biggest_margins(df, top_n=10):
    """
    Business Question 12: biggest winning margins, by runs and by wickets
    (wickets uses balls-remaining as a tiebreaker for the 10-wicket ties).
    """
    df = df.copy()
    df['match_won_by_clean'] = df['match_won_by'].replace(TEAM_REBRAND_NAME)

    second_innings_balls = df[df['innings'] == 2].groupby('match_id')['team_balls'].max()

    match_level = df.groupby('match_id').agg(
        season=('season_clean', 'first'), won_by=('match_won_by_clean', 'first'),
        win_margin=('win_margin', 'first'), win_type=('win_type', 'first'),
    ).reset_index()
    match_level['balls_remaining'] = 120 - match_level['match_id'].map(second_innings_balls)

    biggest_runs = match_level[match_level['win_type'] == 'runs'].sort_values('win_margin', ascending=False).head(top_n)
    biggest_wickets = match_level[(match_level['win_type'] == 'wickets') & (match_level['win_margin'] == 10)].sort_values('balls_remaining', ascending=False).head(top_n)
    closest = match_level.dropna(subset=['win_margin']).sort_values('win_margin').head(top_n)

    return biggest_runs, biggest_wickets, closest
